#!/usr/bin/env python3
"""
Audit Missing or Short Fields

Analyzes patterns in sema-core/src/sema/inventory/data/ for:
1. Missing essential fields (handle, gloss, mechanism, tier, category).
2. Very short content in gloss or mechanism, indicating potential low quality.
"""

import glob
import json
import os

INVENTORY_DIR = "nextvocabulary"

EXPECTED_FIELDS = [
    "handle",
    "gloss",
    "mechanism"
]

# Thresholds for "Short" content
MIN_GLOSS_LEN = 10
MIN_MECH_LEN = 50

def audit_patterns():
    files = glob.glob(os.path.join(INVENTORY_DIR, "*.json"))
    files.sort()
    
    print(f"Auditing {len(files)} patterns in {INVENTORY_DIR}...")
    
    issues_found = 0
    
    for filepath in files:
        filename = os.path.basename(filepath)
        try:
            with open(filepath) as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ {filename}: Invalid JSON")
            issues_found += 1
            continue
        except Exception as e:
            print(f"❌ {filename}: Error reading file: {e}")
            issues_found += 1
            continue
            
        handle = data.get("handle", filename.replace(".json", ""))
        missing = []
        short = []
        
        # Check Expected Top-Level Fields
        for field in EXPECTED_FIELDS:
            if field not in data or data[field] is None:
                missing.append(field)
            elif isinstance(data[field], str) and not data[field].strip():
                missing.append(f"{field} (empty)")

        # Check _meta fields
        meta = data.get("_meta")
        if not meta:
            missing.append("_meta")
        else:
            for field in ["tier", "layer", "category"]:
                if field not in meta or meta[field] is None:
                    missing.append(f"_meta.{field}")
        
        # Check Short Content
        if "gloss" in data and isinstance(data["gloss"], str):
            if len(data["gloss"].strip()) < MIN_GLOSS_LEN:
                short.append(f"gloss ({len(data['gloss'].strip())} chars)")
        
        if "mechanism" in data and isinstance(data["mechanism"], str):
             if len(data["mechanism"].strip()) < MIN_MECH_LEN:
                short.append(f"mechanism ({len(data['mechanism'].strip())} chars)")
                
        # Report
        if missing or short:
            issues_found += 1
            print(f"⚠️  {handle} ({filename})")
            if missing:
                print(f"   Missing: {', '.join(missing)}")
            if short:
                print(f"   Short:   {', '.join(short)}")
            print("")

    if issues_found == 0:
        print("✅ No issues found.")
    else:
        print(f"Found issues in {issues_found} patterns.")

if __name__ == "__main__":
    audit_patterns()
