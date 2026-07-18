import json
import os
import re
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from sema.core.registry import RegistryManager  # noqa: E402

OUTPUT_FILE = "data/shorthand/all_patterns_short.md"


def pattern_path(pattern):
    """Return the canonical taxonomy path, with legacy metadata fallback."""
    meta = pattern.get("_meta", {})
    path = meta.get("path")
    if path:
        return tuple(path)

    legacy_path = [meta.get("layer"), meta.get("category")]
    return tuple(part for part in legacy_path if part) or ("Unclassified",)


def pattern_sort_key(pattern):
    return pattern_path(pattern), pattern.get("handle", "")


def load_patterns():
    """Load all patterns from the registry (DB is source of truth)."""
    db_path = os.environ.get("SEMA_DB_PATH", "data/taxonomy.db")

    registry = RegistryManager(db_path=db_path)

    patterns = []
    for handle, data in registry.registry.items():
        data["handle"] = handle
        patterns.append(data)

    return patterns


def build_lookup(patterns):
    id_lookup = {}
    handle_lookup = {}
    handle_to_short = {}  # Heuristic lookup: Handle -> ShortRef

    for p in patterns:
        handle = p.get("handle")
        stub = p.get("sema_stub", "????")
        if not stub or stub == "????":
            if p.get("sema_id") and "SHA-256:" in p["sema_id"]:
                stub = p["sema_id"].split("SHA-256:")[-1][:4]

        short_ref = f"{handle}#{stub}"

        if p.get("sema_id"):
            id_lookup[p["sema_id"]] = short_ref

        if handle:
            handle_lookup[handle] = short_ref
            handle_to_short[handle] = short_ref

    return id_lookup, handle_lookup, handle_to_short


def shorten_text(text, id_lookup, handle_lookup, handle_to_short):
    if not isinstance(text, str):
        return text

    # 1. Replace Full IDs (Exact match)
    for full_id, short_ref in id_lookup.items():
        if full_id in text:
            text = text.replace(full_id, short_ref)

    # 2. Heuristic: Replace stale IDs (sema:Handle#...)
    # Regex to find sema:Handle#...
    # matches sema:([A-Za-z0-9]+)#mh:SHA-256:[a-f0-9]+

    def replace_stale(match):
        h = match.group(1)
        if h in handle_to_short:
            return handle_to_short[h]
        return match.group(0)  # Keep original if handle unknown

    text = re.sub(r"sema:([A-Za-z0-9]+)#mh:SHA-256:[a-f0-9]+", replace_stale, text)

    # 3. Replace Handles (Word boundary match)
    sorted_handles = sorted(handle_lookup.keys(), key=len, reverse=True)
    escaped_handles = [re.escape(h) for h in sorted_handles]

    # Exclude matches already part of a Short Ref (Handle followed by #)
    # OR matches preceded by sema: (though step 2 should catch those)
    pattern = r"(?<!sema:)\b(" + "|".join(escaped_handles) + r")\b(?!#)"

    def replace_match(match):
        return handle_lookup[match.group(1)]

    text = re.sub(pattern, replace_match, text)

    return text


def shorten_obj(obj, id_lookup, handle_lookup, handle_to_short, key_context=None):
    # Skip these keys entirely - don't modify them
    SKIP_KEYS = {
        "handle",
        "sema_id",
        "sema_ref",
        "sema_stub",
        "path",
        "layer",
        "category",
        "ring",
    }

    # Keys where we should only replace full sema IDs, not bare handle names
    # This prevents "AcceptSpec defines..." from becoming "AcceptSpec#6a50 defines..."
    TEXT_CONTENT_KEYS = {
        "mechanism",
        "gloss",
        "invariants",
        "failure_modes",
        "preconditions",
        "postconditions",
        "description",
    }

    if key_context in SKIP_KEYS:
        return obj

    if isinstance(obj, str):
        if key_context in TEXT_CONTENT_KEYS:
            # Only replace full sema IDs in mechanism/text fields, not bare handles
            return shorten_text_ids_only(obj, id_lookup)
        return shorten_text(obj, id_lookup, handle_lookup, handle_to_short)
    elif isinstance(obj, list):
        return [shorten_obj(x, id_lookup, handle_lookup, handle_to_short, key_context) for x in obj]
    elif isinstance(obj, dict):
        return {
            k: shorten_obj(v, id_lookup, handle_lookup, handle_to_short, k) for k, v in obj.items()
        }
    return obj


def shorten_text_ids_only(text, id_lookup):
    """Only replace full sema IDs in text, not bare handle names."""
    if not isinstance(text, str):
        return text

    # Replace Full IDs (Exact match)
    for full_id, short_ref in id_lookup.items():
        if full_id in text:
            text = text.replace(full_id, short_ref)

    return text


def main():
    patterns = load_patterns()
    id_lookup, handle_lookup, handle_to_short = build_lookup(patterns)

    patterns.sort(key=pattern_sort_key)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# Sema Vocabulary (Short Hand JSON)\n\n")
        f.write(f"**Total Patterns:** {len(patterns)}\n")
        f.write("**Format:** JSON with short-hand references.\n\n")
        f.write("---\n\n")

        current_path = ()

        for p in patterns:
            path = pattern_path(p)
            if path != current_path:
                f.write(f"# Path: {' / '.join(path)}\n\n")
                current_path = path

            handle = p.get("handle", "Unknown")
            short_p = shorten_obj(p, id_lookup, handle_lookup, handle_to_short)

            # Remove links for cleaner output
            if "links" in short_p:
                del short_p["links"]

            stub = p.get("sema_stub", "????")
            if not stub or stub == "????":
                if p.get("sema_id") and "SHA-256:" in p["sema_id"]:
                    stub = p["sema_id"].split("SHA-256:")[-1][:4]
            ref = f"{handle}#{stub}"

            f.write(f"## {ref}\n\n")
            f.write("```json\n")
            f.write(json.dumps(short_p, indent=2))
            f.write("\n```\n\n")
            f.write("---\n\n")

    print(f"Exported {len(patterns)} patterns to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
