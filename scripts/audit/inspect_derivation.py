import json
import os
import sqlite3
import sys

# Add project root
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

DB_PATH = "data/taxonomy.db"

def inspect_derivation():
    print("🔍 Scanning graph for derivation/lineage signals...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Search for 'origin', 'derived', 'source' in metadata
    print("\n--- Metadata Analysis ---")
    cursor.execute("SELECT text, metadata FROM nodes WHERE node_type='SOLUTION'")
    found_count = 0
    for text, meta_json in cursor.fetchall():
        meta = json.loads(meta_json) if meta_json else {}
        full_sol = meta.get('full_solution', {})
        
        # Check explicit fields if they exist (unlikely based on schema, but worth checking)
        signals = []
        if 'origin' in meta or 'origin' in full_sol: signals.append('origin')
        if 'derived_from' in meta or 'derived_from' in full_sol: signals.append('derived_from')
        if 'source' in meta or 'source' in full_sol: signals.append('source')
        
        # Check text content for "derived from" or "based on"
        mechanism = full_sol.get('core_mechanism', '')
        novelty = full_sol.get('what_is_new', '')
        
        if "derived from" in mechanism.lower() or "based on" in mechanism.lower():
            signals.append("mechanism_text")
        
        if "response to" in novelty.lower() or "evolution of" in novelty.lower():
            signals.append("novelty_text")

        if signals:
            print(f"🔹 {text} [{', '.join(signals)}]")
            if 'origin' in meta: print(f"   Origin: {meta['origin']}")
            if 'mechanism_text' in signals: print(f"   Mech: {mechanism[:100]}...")
            if 'novelty_text' in signals: print(f"   Nov: {novelty[:100]}...")
            found_count += 1
            
    if found_count == 0:
        print("No explicit derivation metadata found.")

    # 2. Check for SIMILAR_TO edges which might imply derivation
    print("\n--- SIMILAR_TO Edges (Potential Cousins) ---")
    cursor.execute("""
        SELECT s1.text, s2.text 
        FROM edges e 
        JOIN nodes s1 ON e.source_id = s1.id 
        JOIN nodes s2 ON e.target_id = s2.id 
        WHERE e.edge_type = 'SIMILAR_TO'
        LIMIT 20
    """)
    similar_rows = cursor.fetchall()
    if similar_rows:
        for s1, s2 in similar_rows:
            print(f"  {s1} <~> {s2}")
    else:
        print("No SIMILAR_TO edges found.")

    conn.close()

if __name__ == "__main__":
    inspect_derivation()
