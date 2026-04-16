#!/usr/bin/env python3
"""
Calculate the Merkle root and generate vocabulary statistics.

This script:
1. Loads all patterns from the database (source of truth)
2. Computes the Merkle root
3. Calculates statistics (Layer/Category distribution)
4. Generates a comprehensive information page (docs/information/vocabulary_information.md)
5. Updates the website's merkle.json
"""

import datetime
import hashlib
import json
import os
from collections import defaultdict
from typing import Any

DB_PATH = os.environ.get("SEMA_DB_PATH", "data/taxonomy.db")
OUTPUT_FILE = "docs/information/vocabulary_information.md"


def sha256(data: bytes) -> str:
    """Compute SHA-256 hash. Kept for backward compat; new code should
    import `vocabulary_root` from sema.core.hashing."""
    return hashlib.sha256(data).hexdigest()


def extract_hash_from_sema_id(sema_id: str) -> str:
    """Extract the hash portion from a sema_id."""
    if not sema_id or "#mh:SHA-256:" not in sema_id:
        return ""
    return sema_id.split("#mh:SHA-256:")[1]


def load_patterns() -> list[dict[str, Any]]:
    """Load all patterns from the database (source of truth)."""
    import sqlite3

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT text as handle, metadata
        FROM nodes
        WHERE node_type = 'PATTERN'
        ORDER BY text
    """
    )

    patterns = []
    for row in cursor.fetchall():
        meta = json.loads(row["metadata"] or "{}")
        pattern_data = meta.get("pattern", {})
        pattern_data["handle"] = row["handle"]
        patterns.append(pattern_data)

    conn.close()

    if not patterns:
        raise ValueError("No patterns found in database")

    return patterns


def compute_merkle_root(patterns: list[dict[str, Any]]) -> str:
    """Compute Merkle root from pattern hashes.

    Delegates to `sema.core.hashing.vocabulary_root` for the canonical
    algorithm. Patterns must be pre-sorted by handle (the SQL query does
    this). Kept as a thin wrapper so the existing doc-generation pipeline
    doesn't have to reimport.
    """
    import sys
    from pathlib import Path as _Path

    sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "src"))
    from sema.core.hashing import vocabulary_root

    hashes = []
    for p in patterns:
        h = extract_hash_from_sema_id(p.get("sema_id", ""))
        if h:
            hashes.append(h)
    return vocabulary_root(hashes)


def calculate_stats(patterns: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Calculate counts per Layer and Category."""
    stats = defaultdict(lambda: defaultdict(int))

    for p in patterns:
        meta = p.get("_meta", {})
        layer = meta.get("layer", "Unclassified")
        category = meta.get("category", "Uncategorized")
        stats[layer][category] += 1

    return stats


def generate_markdown_content(
    merkle_root: str, patterns: list[dict[str, Any]], stats: dict[str, dict[str, int]]
) -> str:
    """Generate the content for vocabulary_information.md."""
    date_str = datetime.date.today().isoformat()
    total_patterns = len(patterns)

    content = f"""# Vocabulary Information

## System Status

- **Merkle Root**: `{merkle_root}`
- **Pattern Count**: {total_patterns}
- **Last Verified**: {date_str}

## Usage

### Handshake Protocol

Agents use the Merkle root for fail-closed semantic verification:

```python
# Agent A shares vocabulary root
R_context_A = "{merkle_root}"

# Agent B computes their vocabulary root
R_context_B = compute_vocabulary_merkle_root()

if R_context_A == R_context_B:
    print("✅ PROCEED - Shared semantics verified")
else:
    print("🚫 HALT - Vocabulary mismatch")
```

## Vocabulary Statistics

Breakdown of patterns by Civilization Layer and Functional Category.

"""

    # Sort layers logically if possible, else alphabetically
    layer_order = ["Physics", "Mind", "Society", "Infrastructure", "Unclassified"]
    sorted_layers = sorted(
        stats.keys(), key=lambda x: layer_order.index(x) if x in layer_order else 99
    )

    for layer in sorted_layers:
        categories = stats[layer]
        layer_total = sum(categories.values())
        content += f"### {layer} ({layer_total})\n\n"
        content += "| Category | Count |\n| :--- | :---: |\n"

        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            content += f"| {cat} | {count} |\n"
        content += "\n"

    return content


def main():
    print(f"📚 Loading patterns from database: {DB_PATH}\n")

    patterns = load_patterns()
    print(f"✓ Loaded {len(patterns)} patterns\n")

    merkle_root = compute_merkle_root(patterns)
    stats = calculate_stats(patterns)

    print("=" * 80)
    print("VOCABULARY INFORMATION")
    print("=" * 80)
    print(f"\nRoot: {merkle_root}")
    print(f"\nPattern count: {len(patterns)}")

    # Generate and write markdown file
    markdown_content = generate_markdown_content(merkle_root, patterns, stats)
    with open(OUTPUT_FILE, "w") as f:
        f.write(markdown_content)

    print(f"\n✓ Updated {OUTPUT_FILE}")

    # Write JSON for Website
    WEBSITE_JSON = "../../packages/sema-website/public/merkle.json"
    if os.path.exists(os.path.dirname(WEBSITE_JSON)):
        with open(WEBSITE_JSON, "w") as f:
            json.dump(
                {
                    "root": merkle_root,
                    "count": len(patterns),
                    "last_verified": datetime.date.today().isoformat(),
                },
                f,
                indent=2,
            )
        print(f"✓ Updated {WEBSITE_JSON}")
    else:
        print(f"⚠️  Skipped website update (dir not found): {WEBSITE_JSON}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
