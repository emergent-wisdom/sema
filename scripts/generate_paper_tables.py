import json
import os
from collections import defaultdict

VOCAB_DIR = "data/vocabulary"


def load_vocab():
    patterns = {}
    for filename in os.listdir(VOCAB_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(VOCAB_DIR, filename)) as f:
                data = json.load(f)
                handle = data.get("handle")
                meta = data.get("_meta", {})
                patterns[handle] = meta
    return patterns


def escape_latex(text):
    return text.replace("&", "\\&").replace("_", "\\_")


def generate_tex():
    patterns = load_vocab()

    # Organize by Layer -> Category -> List[Handle]
    taxonomy = defaultdict(lambda: defaultdict(list))

    for handle, meta in patterns.items():
        path = meta.get("path") or []
        layer = path[0] if len(path) >= 1 else meta.get("layer", "Unknown")
        category = path[1] if len(path) >= 2 else meta.get("category", "Unknown")
        taxonomy[layer][category].append(handle)

    for layer in taxonomy:
        for cat in taxonomy[layer]:
            taxonomy[layer][cat].sort()

    # Output paths
    rows_path = "paper/generated_table_rows.tex"
    appendix_path = "paper/generated_appendix.tex"

    # --- Generate Table Rows ---
    with open(rows_path, "w") as f:
        layers_order = ["Physics", "Infrastructure", "Mind", "Society"]

        for layer in layers_order:
            if layer not in taxonomy:
                continue

            categories = sorted(taxonomy[layer].keys())

            # Multirow for layer name
            f.write(f"\\multirow{{{len(categories)}}}{{*}}{{{escape_latex(layer)}}}\n")

            for cat in categories:
                count = len(taxonomy[layer][cat])
                examples = ", ".join(taxonomy[layer][cat][:3])  # First 3
                f.write(f"& {escape_latex(cat)} & {count} & {escape_latex(examples)} \\\\\n")
            f.write("\\midrule\n")

        f.write(f"& \\textbf{{Total}} & \\textbf{{{len(patterns)}}} & \\\\\n")

    print(f"✅ Generated {rows_path}")

    # --- Generate Appendix ---
    with open(appendix_path, "w") as f:
        # Calculate unique category names separately from layer/category paths:
        # "Primitives" exists under both Physics and Infrastructure.
        unique_cats = {cat for categories in taxonomy.values() for cat in categories}
        total_paths = sum(len(taxonomy[layer]) for layer in taxonomy)

        f.write(
            f"The {len(patterns)} patterns are organized into {len(unique_cats)} "
            f"category names across {total_paths} layer-category paths and 4 fundamental layers:\n"
        )

        descriptions = {
            "Physics": "The immutable substrate.",
            "Mind": "Hybrid cognition---always decomposable and delegatable.",
            "Society": "Multi-agent coordination.",
            "Infrastructure": "Operational constraints.",
        }

        for layer in layers_order:
            if layer not in taxonomy:
                continue

            layer_count = sum(len(taxonomy[layer][cat]) for cat in taxonomy[layer])
            desc = descriptions.get(layer, "")

            f.write(
                f"\n\\paragraph{{{escape_latex(layer)} Layer ({layer_count} patterns)}} {desc}\n"
            )
            f.write("\\begin{itemize}\n")

            for cat in sorted(taxonomy[layer].keys()):
                handles = taxonomy[layer][cat]
                count = len(handles)
                handle_str = ", ".join([escape_latex(h) for h in handles])
                f.write(f"    \\item \\textbf{{{escape_latex(cat)}}} ({count}): {handle_str}.\n")

            f.write("\\end{itemize}\n")

    print(f"✅ Generated {appendix_path}")


if __name__ == "__main__":
    generate_tex()
