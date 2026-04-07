#!/usr/bin/env python3
"""Show the Sema taxonomy tree with layers."""

import json
import sqlite3
from collections import defaultdict
from pathlib import Path

DB_PATH = Path(__file__).parent / "../../data/taxonomy.db"

def show_tree(by_layer=False):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT text, metadata FROM nodes WHERE node_type='PATTERN' ORDER BY text")

    patterns = []
    for name, meta_str in c.fetchall():
        meta = json.loads(meta_str) if meta_str else {}
        patterns.append({
            'name': name,
            'category': meta.get('category', 'UNCATEGORIZED'),
            'layer': meta.get('layer', 'Unknown')
        })
    conn.close()

    if by_layer:
        # Group by Layer -> Category -> Pattern
        layers = defaultdict(lambda: defaultdict(list))
        for p in patterns:
            layers[p['layer']][p['category']].append(p['name'])

        print("sema-vocabulary/")
        layer_order = ["Physics", "Mind", "Society", "Infrastructure"]
        for i, layer in enumerate(layer_order):
            if layer not in layers:
                continue
            is_last_layer = (i == len(layer_order) - 1)
            layer_prefix = "└── " if is_last_layer else "├── "
            layer_count = sum(len(v) for v in layers[layer].values())
            print(f"{layer_prefix}[{layer}]/ ({layer_count})")

            cats = sorted(layers[layer].keys())
            for j, cat in enumerate(cats):
                is_last_cat = (j == len(cats) - 1)
                cat_prefix = "    " if is_last_layer else "│   "
                cat_branch = "└── " if is_last_cat else "├── "
                count = len(layers[layer][cat])
                print(f"{cat_prefix}{cat_branch}{cat}/ ({count})")

                for k, p in enumerate(sorted(layers[layer][cat])):
                    is_last = (k == len(layers[layer][cat]) - 1)
                    inner = cat_prefix + ("    " if is_last_cat else "│   ")
                    branch = "└── " if is_last else "├── "
                    print(f"{inner}{branch}{p}")
    else:
        # Group by Category only
        categories = defaultdict(list)
        for p in patterns:
            categories[p['category']].append(p['name'])

        print("sema-vocabulary/")
        cats = sorted(categories.keys())
        for i, cat in enumerate(cats):
            is_last_cat = (i == len(cats) - 1)
            prefix = "└── " if is_last_cat else "├── "
            count = len(categories[cat])
            print(f"{prefix}{cat}/ ({count})")

            for j, p in enumerate(sorted(categories[cat])):
                is_last = (j == len(categories[cat]) - 1)
                inner = "    " if is_last_cat else "│   "
                branch = "└── " if is_last else "├── "
                print(f"{inner}{branch}{p}")

    total = len(patterns)
    num_cats = len(set(p['category'] for p in patterns))
    print(f"\n{total} patterns, {num_cats} categories, 4 layers")

if __name__ == "__main__":
    import sys
    # Layers view is default; use --flat or -f for category-only view
    flat = "--flat" in sys.argv or "-f" in sys.argv
    show_tree(by_layer=not flat)
