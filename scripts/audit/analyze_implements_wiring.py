import glob
import json
import os
import re

VOCAB_DIR = "nextvocabulary"

def load_patterns():
    patterns = {}
    files = glob.glob(os.path.join(VOCAB_DIR, "*.json"))
    for f in files:
        try:
            with open(f) as fd:
                data = json.load(fd)
                patterns[data['handle']] = data
        except Exception as e:
            print(f"Error loading {f}: {e}")
    return patterns

def extract_atoms(implements_list):
    atoms = set()
    for item in implements_list:
        # Simple regex to catch PascalCase words
        # This is a heuristic, but should work for "Act(Deploy)", "Deep(Check(Proof))"
        # It might catch "Deep", "Check", "Proof".
        found = re.findall(r'\b[A-Z][a-zA-Z0-9]*\b', item)
        atoms.update(found)
    return atoms

def check_pattern(pattern, all_handles):
    handle = pattern['handle']
    if 'implements' not in pattern:
        return None

    atoms = extract_atoms(pattern['implements'])
    
    missing_deps = []
    missing_refs = []
    
    dependencies = pattern.get('dependencies', {})
    all_deps = set()
    for cat in dependencies:
        for key, val in dependencies[cat].items():
            # Extract handle from sema:Handle#hash
            # val is like "sema:Act#mh:..."
            match = re.match(r'sema:([A-Z][a-zA-Z0-9]*)#', val)
            if match:
                all_deps.add(match.group(1))

    mechanism = pattern.get('mechanism', "")
    
    # Check each atom
    for atom in atoms:
        if atom == handle:
            continue # Don't need to depend on self
            
        if atom not in all_handles:
            # print(f"[{handle}] skipping {atom} (not in vocab)")
            continue

        # Check if in dependencies
        if atom not in all_deps:
            missing_deps.append(atom)
        
        # Check if in mechanism text
        # We look for {{key}} where dependencies[cat][key] points to atom
        # First find the key for this atom
        found_key = None
        for cat in dependencies:
            for key, val in dependencies[cat].items():
                 if f"sema:{atom}#" in val:
                     found_key = key
                     break
        
        if found_key:
            if f"{{{{{found_key}}}}}" not in mechanism:
                missing_refs.append(atom)
        else:
            # If it's missing from deps, it's definitely missing from text (effectively)
            missing_refs.append(atom)

    if missing_deps or missing_refs:
        return {
            'handle': handle,
            'implements': pattern['implements'],
            'missing_deps': missing_deps,
            'missing_refs': missing_refs
        }
    return None

def main():
    patterns = load_patterns()
    all_handles = set(patterns.keys())
    
    print(f"Loaded {len(patterns)} patterns.")
    
    results = []
    for handle, p in patterns.items():
        res = check_pattern(p, all_handles)
        if res:
            results.append(res)
            
    print(f"Found {len(results)} patterns needing updates.")
    
    for r in results:
        print(f"\nPattern: {r['handle']}")
        print(f"  Implements: {r['implements']}")
        if r['missing_deps']:
            print(f"  Missing Dependencies: {', '.join(r['missing_deps'])}")
        if r['missing_refs']:
            print(f"  Missing Text Refs: {', '.join(r['missing_refs'])}")

if __name__ == "__main__":
    main()
