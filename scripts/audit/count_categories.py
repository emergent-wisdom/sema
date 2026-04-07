import json
import os
from collections import defaultdict

VOCAB_DIR = 'data/vocabulary'

def count_categories():
    layer_counts = defaultdict(int)
    category_counts = defaultdict(int)
    layer_category_map = defaultdict(set)
    
    total = 0
    
    for filename in os.listdir(VOCAB_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(VOCAB_DIR, filename)) as f:
                try:
                    data = json.load(f)
                    # Check both _meta and sema_ fields
                    meta = data.get('_meta', {})
                    layer = meta.get('layer') or data.get('sema_layer')
                    category = meta.get('category') or data.get('sema_category')
                    
                    if layer and category:
                        layer_counts[layer] += 1
                        category_counts[(layer, category)] += 1
                        layer_category_map[layer].add(category)
                        total += 1
                except json.JSONDecodeError:
                    pass

    print(f"Total Patterns: {total}")
    
    # Print in LaTeX table order (approximate)
    layers_order = ["Physics", "Mind", "Society", "Infrastructure"]
    
    for layer in layers_order:
        print(f"\n--- {layer} (Total: {layer_counts[layer]}) ---")
        categories = sorted(list(layer_category_map[layer]))
        for cat in categories:
            count = category_counts[(layer, cat)]
            print(f"{cat}: {count}")

if __name__ == "__main__":
    count_categories()
