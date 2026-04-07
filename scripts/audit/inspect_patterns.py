import json
import sqlite3

conn = sqlite3.connect('data/taxonomy.db')
cursor = conn.cursor()

# Get all solution nodes
cursor.execute("SELECT metadata FROM nodes WHERE node_type='SOLUTION'")
rows = cursor.fetchall()

patterns = []
for row in rows:
    try:
        data = json.loads(row[0])
        label = data.get('full_solution', {}).get('label')
        if label:
            patterns.append(label)
    except:
        pass

print(f"Total Patterns: {len(patterns)}")
print("Patterns:")
for p in sorted(patterns):
    print(f"- {p}")

conn.close()
