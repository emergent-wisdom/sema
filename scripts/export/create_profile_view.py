import argparse
import json
import os
import shutil
import sqlite3
import sys

# Add project root
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from sema.core.config import get_config
CONFIG = get_config()

DB_PATH = "data/taxonomy.db"
BASE_OUTPUT_DIR = "data/profiles"

def create_view(name, layer=None, tier=None, has_invariants=False, lite_mode=False):
    print(f"🔧 Generatng Profile View: '{name}'")
    print(f"   Filters: Layer={layer}, Tier={tier}, Strict={has_invariants}, Lite={lite_mode}")
    
    conn = sqlite3.connect(DB_PATH)
    # ... (connection setup) ...
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # Base Query
    query = "SELECT id, text, metadata FROM nodes WHERE node_type='SOLUTION'"
    params = []
    
    # 1. Fetch Candidates
    cur.execute(query, params)
    candidates = cur.fetchall()
    
    selected = []
    
    # 2. Filter (Python side for complex logic check)
    for row in candidates:
        meta = json.loads(row['metadata']) if row['metadata'] else {}
        full_sol = meta.get('full_solution', {})
        
        # Filter: Layer
        if layer:
            if meta.get('layer') != layer:
                continue

        # Filter: Strict Rigor (Must have Invariants)
        if has_invariants:
            cur2 = conn.cursor()
            cur2.execute("SELECT 1 FROM edges WHERE source_id=? AND edge_type='HAS_INVARIANT'", (row['id'],))
            if not cur2.fetchone():
                continue
        
        # If passed filters
        selected.append(row)

    print(f"   Selected {len(selected)} patterns out of {len(candidates)}.")
    
    if not selected:
        print("❌ No patterns matched criteria. Aborting.")
        return

    # 3. Export
    out_dir = os.path.join(BASE_OUTPUT_DIR, name)
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    
    for row in selected:
        node_id = row['id']
        handle = row['text']
        meta = json.loads(row['metadata'])
        
        # Construct content
        pattern = {
            "handle": handle,
            "mechanism": meta.get('full_solution', {}).get('core_mechanism'),
            "gloss": meta.get('full_solution', {}).get('long_term_vision'),
        }
        
        if not lite_mode:
            pattern.update({
                "invariants": [],
                "preconditions": [],
                "postconditions": [],
                "links": {}
            })
        
        # Fetch Edges
        cur.execute("SELECT target_id, edge_type FROM edges WHERE source_id=?", (node_id,))
        for target_id, edge_type in cur.fetchall():
            # Get target info
            cur.execute("SELECT text, node_type FROM nodes WHERE id=?", (target_id,))
            tgt = cur.fetchone()
            if not tgt: continue
            
            t_text = tgt['text']
            t_type = tgt['node_type']
            
            # If Lite Mode, skip heavy contracts
            if lite_mode:
                if t_type in ['INVARIANT', 'PRECONDITION', 'POSTCONDITION']:
                    continue
            
            if t_type == 'INVARIANT': pattern['invariants'].append(t_text)
            elif t_type == 'PRECONDITION': pattern['preconditions'].append(t_text)
            elif t_type == 'POSTCONDITION': pattern['postconditions'].append(t_text)
            elif t_type == 'SOLUTION':
                if 'links' not in pattern: pattern['links'] = {}
                if edge_type not in pattern['links']: pattern['links'][edge_type] = []
                pattern['links'][edge_type].append(t_text)

        # Write File
        fname = f"{handle}.json"
        with open(os.path.join(out_dir, fname), 'w') as f:
            json.dump(pattern, f, indent=2)
            
    print(f"✅ Exported to {out_dir}")
    
    # 4. Register Profile
    abs_path = os.path.abspath(out_dir)
    CONFIG.add_profile(name, abs_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Profile name")
    parser.add_argument("--layer", help="Filter by Layer (Physics, Mind, Society, Infrastructure)")
    parser.add_argument("--strict", action="store_true", help="Only patterns with Invariants")
    parser.add_argument("--lite", action="store_true", help="Strip heavy contracts for prototyping")
    args = parser.parse_args()
    
    create_view(args.name, layer=args.layer, has_invariants=args.strict, lite_mode=args.lite)
