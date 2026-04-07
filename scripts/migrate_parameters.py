#!/usr/bin/env python3
"""
Migrate parameters from string format to object format (Rule 4.2).

String format: "name: Type [range] (description)"
Object format: {"name": "name", "type": "Type", "range": "[range]", "description": "description"}
"""

import json
import re
from pathlib import Path


def parse_parameter_string(param_str: str) -> dict | None:
    """Parse a parameter string into an object.

    Formats supported:
    - "name: Type [range] (description)"
    - "name: Type {range} (description)"
    - "name: Type (description)"
    - "name: Type"
    """
    # Pattern: name: Type [range or {range}] (description)
    # All parts after name: Type are optional

    # First, extract the name and the rest
    match = re.match(r"^([a-z_][a-z0-9_]*)\s*:\s*(.+)$", param_str.strip(), re.IGNORECASE)
    if not match:
        print(f"  ⚠️  Could not parse: {param_str}")
        return None

    name = match.group(1)
    rest = match.group(2).strip()

    # Try to extract type, range, and description
    # Pattern: Type [range] (description) or Type {range} (description)
    # Range can use [] or {}

    type_str = None
    range_str = None
    desc_str = None

    # Try pattern with range and description
    range_desc_match = re.match(
        r"^([A-Za-z][A-Za-z0-9_<>,\[\]]*)\s*"  # Type (e.g., "Enum", "List<Float>")
        r"([\[\{][^\]\}]+[\]\}])?\s*"  # Optional range in [] or {}
        r"(?:\((.+)\))?$",  # Optional description in ()
        rest,
    )

    if range_desc_match:
        type_str = range_desc_match.group(1).strip()
        range_str = range_desc_match.group(2).strip() if range_desc_match.group(2) else None
        desc_str = range_desc_match.group(3).strip() if range_desc_match.group(3) else None
    else:
        # Fallback: just take the whole thing as type
        type_str = rest

    # Build the object
    result = {
        "name": name,
        "type": type_str,
    }

    if range_str:
        result["range"] = range_str
    else:
        result["range"] = "unspecified"

    if desc_str:
        result["description"] = desc_str
    else:
        result["description"] = f"The {name} parameter"

    return result


def migrate_pattern(file_path: Path) -> bool:
    """Migrate a single pattern file. Returns True if modified."""
    with open(file_path) as f:
        data = json.load(f)

    if "parameters" not in data:
        return False

    params = data["parameters"]
    if not params:
        return False

    # Check if already migrated (first param is a dict)
    if isinstance(params[0], dict):
        # Already object format, but validate it has required fields
        modified = False
        for i, param in enumerate(params):
            if isinstance(param, dict):
                missing = {"name", "type", "range", "description"} - set(param.keys())
                if missing:
                    print(f"  ⚠️  {file_path.name}: param[{i}] missing {missing}")
                    # Add defaults for missing fields
                    if "range" not in param:
                        param["range"] = "unspecified"
                        modified = True
                    if "description" not in param:
                        param["description"] = f"The {param.get('name', 'unknown')} parameter"
                        modified = True
        if modified:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
        return modified

    # Convert string params to objects
    new_params = []
    for param in params:
        if isinstance(param, str):
            parsed = parse_parameter_string(param)
            if parsed:
                new_params.append(parsed)
            else:
                print(f"  ❌ Failed to parse in {file_path.name}: {param}")
                return False
        elif isinstance(param, dict):
            new_params.append(param)
        else:
            print(f"  ❌ Unknown param type in {file_path.name}: {type(param)}")
            return False

    data["parameters"] = new_params

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return True


def main():
    vocab_dir = Path(__file__).parent.parent / "data" / "vocabulary"

    print(f"Migrating parameters in {vocab_dir}...")

    migrated = 0
    failed = 0
    skipped = 0

    for pattern_file in sorted(vocab_dir.glob("*.json")):
        try:
            if migrate_pattern(pattern_file):
                print(f"  ✓ {pattern_file.name}")
                migrated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ❌ {pattern_file.name}: {e}")
            failed += 1

    print(f"\nDone: {migrated} migrated, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()
