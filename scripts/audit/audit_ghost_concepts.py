import glob
import json
import os
import re
import sys

VOCAB_DIR = "nextvocabulary"

def load_patterns():
    """Returns a dict of {lowercase_handle: actual_handle} and map of handle -> content."""
    patterns_map = {}
    content_map = {}
    
    files = glob.glob(os.path.join(VOCAB_DIR, "*.json"))
    # print(f"📂 Loading {len(files)} pattern files...")
    
    for fpath in files:
        try:
            with open(fpath) as f:
                data = json.load(f)
                handle = data.get("handle") or data.get("pattern", {}).get("handle")
                if handle:
                    patterns_map[handle.lower()] = handle
                    content_map[handle] = data
        except Exception as e:
            print(f"❌ Error reading {fpath}: {e}")
            
    return patterns_map, content_map

def find_ghost_references():
    patterns_map, content_map = load_patterns()
    ghosts_found = 0
    
    target_handle = sys.argv[1] if len(sys.argv) > 1 else None
    
    if target_handle:
        print(f"👻 Hunting for Ghost References in '{target_handle}'...\n")
    else:
        print(f"👻 Hunting for Ghost References across {len(content_map)} patterns...\n")

    for handle, data in content_map.items():
        if target_handle and handle != target_handle:
            continue
            
        # Handle different structures (flat or nested under "pattern")
        p_data = data if "mechanism" in data else data.get("pattern", {})
        
        mechanism = p_data.get("mechanism", "")
        failure_modes = p_data.get("failure_modes", [])
        if isinstance(failure_modes, list):
            failure_modes = "\n".join(failure_modes)
            
        text_content = (mechanism or "") + "\n" + (failure_modes or "")
        
        # 1. Remove existing valid links {{handle}}
        clean_text = re.sub(r'\{\{.*?\}\}', '', text_content)

        # 2. Iterate through all known patterns
        found_ghosts = []

        for p_lower, p_real in patterns_map.items():
            if p_real == handle: 
                continue 
            
            # Simple heuristic: exact word match, case-insensitive
            # \b ensures we don't match "Plan" inside "Planet"
            if re.search(r'\b' + re.escape(p_lower) + r'\b', clean_text, re.IGNORECASE):
                found_ghosts.append(p_real)

        if found_ghosts:
            print(f"⚠️  {handle}:")
            for ghost in sorted(found_ghosts):
                print(f"   • Mentions '{ghost}' (unlinked). Should it be '{{{{{{ghost}}}}}}'?")
            ghosts_found += 1
        elif target_handle:
            print(f"✅ No ghost references found in {handle}.")

    if not target_handle:
        print(f"\n👻 Scan complete. Found potential ghost references in {ghosts_found} patterns.")

if __name__ == "__main__":
    find_ghost_references()