import json
import os
import re
from typing import Dict, Set, Tuple

VOCAB_DIR = "data/vocabulary"


def get_dependencies_usage(pattern: Dict) -> Tuple[Set[str], Set[str], Dict[str, str]]:
    """Return (declared_keys, used_keys, key_to_category)."""
    deps = pattern.get("dependencies", {})
    declared_keys = set()
    key_to_cat = {}

    if isinstance(deps, dict):
        for cat in ["accepts", "yields", "composes_with", "references"]:
            if cat in deps and isinstance(deps[cat], dict):
                for k in deps[cat].keys():
                    declared_keys.add(k)
                    key_to_cat[k] = cat

    text_fields = ["mechanism", "gloss"]
    list_fields = ["failure_modes", "invariants", "preconditions", "postconditions"]

    used_keys = set()
    # Correct regex for {{key}} using hex codes to avoid escape hell
    # \x7b = {, \x7d = }
    # Pattern: {{ \s* (group) \s* }}
    ref_pattern = re.compile(r"\x7b\x7b\s*([a-zA-Z0-9_]+)\s*\x7d\x7d")

    def scan_text(text):
        if not isinstance(text, str):
            return
        matches = ref_pattern.findall(text)
        for m in matches:
            used_keys.add(m)

    for field in text_fields:
        if field in pattern:
            scan_text(pattern[field])

    for field in list_fields:
        if field in pattern and isinstance(pattern[field], list):
            for item in pattern[field]:
                scan_text(item)

    return declared_keys, used_keys, key_to_cat


def replace_in_text(pattern: Dict, old_key: str, new_key: str):
    """Replace {{old_key}} with {{new_key}} in all text fields."""
    text_fields = ["mechanism", "gloss"]
    list_fields = ["failure_modes", "invariants", "preconditions", "postconditions"]

    # Regex: {{ \s* old_key \s* }}
    regex = re.compile(r"\x7b\x7b\s*" + re.escape(old_key) + r"\s*\x7d\x7d")
    # Replacement must be {{new_key}}
    # f-string curly brace escaping: {{ = {
    replacement = f"{{{{{new_key}}}}}"

    changed = False

    for field in text_fields:
        if field in pattern and isinstance(pattern[field], str):
            new_text = regex.sub(replacement, pattern[field])
            if new_text != pattern[field]:
                pattern[field] = new_text
                changed = True

    for field in list_fields:
        if field in pattern and isinstance(pattern[field], list):
            new_list = []
            list_changed = False
            for item in pattern[field]:
                if isinstance(item, str):
                    new_item = regex.sub(replacement, item)
                    if new_item != item:
                        list_changed = True
                    new_list.append(new_item)
                else:
                    new_list.append(item)
            if list_changed:
                pattern[field] = new_list
                changed = True

    return changed


def main():
    print(f"Scanning {VOCAB_DIR}...")
    files = sorted([f for f in os.listdir(VOCAB_DIR) if f.endswith(".json")])

    fixed_count = 0

    for filename in files:
        filepath = os.path.join(VOCAB_DIR, filename)
        with open(filepath) as f:
            try:
                data = json.load(f)
            except Exception:
                print(f"Skipping broken json: {filename}")
                continue

        declared, used, key_to_cat = get_dependencies_usage(data)

        missing_declarations = used - declared
        unused_declarations = declared - used

        if filename == "Aggregate.json":
            print(f"DEBUG: {filename} -> Declared: {declared}, Used: {used}")
            print(f"DEBUG: Missing: {missing_declarations}, Unused: {unused_declarations}")

        changes_made = False

        # General cleanup of empty dependency categories
        deps = data.get("dependencies", {})
        if isinstance(deps, dict):
            for cat in list(deps.keys()):
                if isinstance(deps[cat], dict) and not deps[cat]:
                    del deps[cat]
                    changes_made = True

        if not missing_declarations and not unused_declarations and not changes_made:
            continue

        # Group unused by category logic was unused

        for missing in list(missing_declarations):
            candidate = None

            # 1. Exact substring match
            for unused in unused_declarations:
                if unused in missing or missing in unused:
                    candidate = unused
                    break

            # 2. Only 1 unused total
            if not candidate and len(unused_declarations) == 1:
                candidate = list(unused_declarations)[0]

            # 3. Decision -> Value
            if not candidate and missing == "decision" and "value" in unused_declarations:
                candidate = "value"

            # 4. Proposal -> Message
            if not candidate and missing == "proposal" and "message" in unused_declarations:
                candidate = "message"

            if candidate:
                if replace_in_text(data, missing, candidate):
                    changes_made = True
                    unused_declarations.remove(candidate)
                    missing_declarations.remove(missing)

        # Remove remaining unused dependencies
        if unused_declarations:
            # We need to find where they are in the nested dict structure
            deps = data.get("dependencies", {})
            for unused in unused_declarations:
                # Find category
                cat = key_to_cat.get(unused)
                if cat and cat in deps and unused in deps[cat]:
                    del deps[cat][unused]
                    changes_made = True
                    # print(f"  -> Removed unused dependency: {unused}")

                    # If category is now empty, remove it
                    if not deps[cat]:
                        del deps[cat]

        # General cleanup of empty dependency categories (even if not touched above)
        deps = data.get("dependencies", {})
        if isinstance(deps, dict):
            for cat in list(deps.keys()):
                if isinstance(deps[cat], dict) and not deps[cat]:
                    del deps[cat]
                    changes_made = True

        if changes_made:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
            fixed_count += 1
            print(f"Fixed {filename}")

    print(f"\nTotal files fixed: {fixed_count}")


if __name__ == "__main__":
    main()
