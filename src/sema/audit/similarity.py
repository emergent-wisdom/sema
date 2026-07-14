import sqlite3

import numpy as np

DB_PATH = "data/taxonomy.db"


def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def audit_similarity():
    print("🔍 Computing pairwise similarities to find missing SIMILAR_TO links...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Fetch Solution -> Mechanism -> Embedding
    # We join nodes (solution) -> edges -> nodes (mechanism)
    cursor.execute("""
        SELECT DISTINCT s.id, s.text, m.embedding
        FROM nodes s
        JOIN edges e ON s.id = e.source_id
        JOIN nodes m ON e.target_id = m.id
        WHERE s.node_type = 'PATTERN'
          AND m.node_type = 'MECHANISM'
          AND m.embedding IS NOT NULL
    """)
    nodes = []
    for nid, text, blob in cursor.fetchall():
        if blob:
            vec = np.frombuffer(blob, dtype=np.float32)
            nodes.append({"id": nid, "text": text, "vec": vec})

    print(f"Loaded {len(nodes)} patterns with embeddings.")

    # 2. Fetch existing SIMILAR_TO edges
    cursor.execute("SELECT source_id, target_id FROM edges WHERE edge_type='SIMILAR_TO'")
    existing_links = set()
    for src, tgt in cursor.fetchall():
        existing_links.add(tuple(sorted((src, tgt))))  # Store as sorted tuple for undirected check

    # 3. Compare All Pairs
    missing_links = []

    # Threshold from GraphStore is 0.75
    THRESHOLD = 0.75

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            n1 = nodes[i]
            n2 = nodes[j]

            sim = cosine_similarity(n1["vec"], n2["vec"])

            if sim > THRESHOLD:
                pair_key = tuple(sorted((n1["id"], n2["id"])))

                if pair_key not in existing_links:
                    missing_links.append({"pair": f"{n1['text']} <-> {n2['text']}", "score": sim})

    # 4. Report
    print(f"\nFound {len(missing_links)} pairs with High Similarity (> {THRESHOLD}) but NO link.\n")

    # Sort by score desc
    missing_links.sort(key=lambda x: x["score"], reverse=True)

    for m in missing_links[:50]:  # Show top 50
        print(f"🔹 {m['score']:.4f}: {m['pair']}")

    conn.close()


if __name__ == "__main__":
    audit_similarity()
