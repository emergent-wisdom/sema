import json
import os
import sqlite3
import sys

# Add project root
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

DB_PATH = "data/taxonomy.db"

def show_novelty():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("✨ SEMA PATTERN NOVELTY SCAN ✨\n")
    
    # Query for Solutions and their 'what_is_new' content
    # We look for edges: SOLUTION -> CLAIMS_NOVELTY -> NOVELTY
    cursor.execute("""
        SELECT s.text as solution, n.text as novelty
        FROM nodes s
        JOIN edges e ON s.id = e.source_id
        JOIN nodes n ON e.target_id = n.id
        WHERE s.node_type = 'SOLUTION' 
          AND n.node_type = 'NOVELTY'
        ORDER BY s.text
    """)
    
    rows = cursor.fetchall()
    
    if not rows:
        print("No specific 'Novelty' nodes linked. Checking metadata text...")
        # Fallback: check the JSON metadata if not reified
        cursor.execute("SELECT text, metadata FROM nodes WHERE node_type='SOLUTION'")
        all_sols = cursor.fetchall()
        for text, meta_json in all_sols:
            meta = json.loads(meta_json)
            full_sol = meta.get('full_solution', {})
            novelty = full_sol.get('what_is_new')
            if novelty:
                print(f"🔹 {text}")
                print(f"   {novelty}\n")
    else:
        for sol, nov in rows:
            print(f"🔹 {sol}")
            print(f"   {nov}\n")

    conn.close()

if __name__ == "__main__":
    show_novelty()
