import json
import os

VOCAB_DIR = "data/vocabulary"
OUTPUT_TEX = "paper/generated_stats.tex"


def calculate_stats():
    patterns = []
    for filename in os.listdir(VOCAB_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(VOCAB_DIR, filename)) as f:
                patterns.append(json.load(f))

    pattern_count = len(patterns)

    # Edges
    total_edges = 0
    pattern_edges = 0
    for p in patterns:
        deps = p.get("dependencies", {})
        for cat in deps:
            total_edges += len(deps[cat])
            pattern_edges += len(deps[cat])

        # Count _meta.related as edges
        total_edges += len(p.get("_meta", {}).get("related", []))

        # Also count links to Invariants etc if they are considered edges?
        # In the paper "Each pattern links to its mechanism, invariants... via typed edges"
        # So yes.
        total_edges += len(p.get("invariants", []))
        total_edges += len(p.get("preconditions", []))
        total_edges += len(p.get("postconditions", []))
        total_edges += len(p.get("failure_modes", []))
        # Mechanism is 1 per pattern? "Links to its mechanism".
        total_edges += 1

    # Nodes
    # Patterns are nodes.
    # Invariants, Pre/Post, Failures, Mechanisms are nodes?
    # Mechanisms are unique per pattern (407).

    unique_invariants = set()
    unique_preconditions = set()
    unique_postconditions = set()
    unique_failures = set()
    for p in patterns:
        for i in p.get("invariants", []):
            unique_invariants.add(i.strip().lower())
        for i in p.get("preconditions", []):
            unique_preconditions.add(i.strip().lower())
        for i in p.get("postconditions", []):
            unique_postconditions.add(i.strip().lower())
        for i in p.get("failure_modes", []):
            unique_failures.add(i.strip().lower())

    # Total nodes = patterns + unique constraints
    # (mechanisms are 1:1 with patterns, so just count pattern_count)
    total_nodes = (
        pattern_count
        + len(unique_invariants)
        + len(unique_preconditions)
        + len(unique_postconditions)
        + len(unique_failures)
        + pattern_count
    )

    # "Principles"?
    # Maybe "Principles" = Preconditions + Postconditions?
    principles_count = len(unique_preconditions) + len(unique_postconditions)

    avg_edges = total_edges / pattern_count if pattern_count else 0

    print(f"Total nodes: {total_nodes}")
    print(f"Total edges: {total_edges}")
    print(f"Solution patterns: {pattern_count}")
    print(f"Unique invariants: {len(unique_invariants)}")
    print(f"Principles (Pre+Post?): {principles_count}")
    # Table 3 Metrics
    with_invariants = 0
    with_pre = 0
    with_post = 0
    with_io = 0
    with_params = 0
    total_params = 0
    with_compose = 0

    for p in patterns:
        if p.get("invariants"):
            with_invariants += 1
        if p.get("preconditions"):
            with_pre += 1
        if p.get("postconditions"):
            with_post += 1

        deps = p.get("dependencies", {})
        if deps.get("accepts") or deps.get("yields"):
            with_io += 1
        if deps.get("composes_with"):
            with_compose += 1

        params = p.get("parameters", [])
        if params:
            with_params += 1
            total_params += len(params)

    print("\n--- Table 3 ---")
    print(f"Total patterns: {pattern_count}")
    print(
        f"Patterns with formal invariants: {with_invariants} ({with_invariants/pattern_count:.0%})"
    )
    print(f"Patterns with preconditions: {with_pre} ({with_pre/pattern_count:.0%})")
    print(f"Patterns with postconditions: {with_post} ({with_post/pattern_count:.0%})")
    print(f"Patterns with typed I/O: {with_io} ({with_io/pattern_count:.0%})")
    print(f"Patterns with parameters: {with_params} ({with_params/pattern_count:.0%})")
    print(f"Total parameters: {total_params}")
    print(f"Patterns that compose: {with_compose} ({with_compose/pattern_count:.0%})")

    # Generate LaTeX file
    with open(OUTPUT_TEX, "w") as f:
        f.write("% Auto-generated stats from calculate_graph_stats.py\n")
        f.write(f"\\newcommand{{\\semaPatternCount}}{{{pattern_count}}}\n")
        f.write(f"\\newcommand{{\\semaTotalNodes}}{{{total_nodes:,}}}\n")
        f.write(f"\\newcommand{{\\semaTotalEdges}}{{{total_edges:,}}}\n")
        f.write(f"\\newcommand{{\\semaAvgEdges}}{{{avg_edges:.1f}}}\n")
        f.write(f"\\newcommand{{\\semaInvariantCount}}{{{len(unique_invariants)}}}\n")
        f.write(f"\\newcommand{{\\semaPrinciplesCount}}{{{principles_count}}}\n")

        # Table 3 stats (use \% for LaTeX-escaped percent)
        f.write(f"\\newcommand{{\\semaPatternsWithInvariants}}{{{with_invariants}}}\n")
        f.write(f"\\newcommand{{\\semaInvariantPct}}{{{with_invariants*100//pattern_count}\\%}}\n")

        f.write(f"\\newcommand{{\\semaPatternsWithPre}}{{{with_pre}}}\n")
        f.write(f"\\newcommand{{\\semaPrePct}}{{{with_pre*100//pattern_count}\\%}}\n")

        f.write(f"\\newcommand{{\\semaPatternsWithPost}}{{{with_post}}}\n")
        f.write(f"\\newcommand{{\\semaPostPct}}{{{with_post*100//pattern_count}\\%}}\n")

        f.write(f"\\newcommand{{\\semaPatternsWithIO}}{{{with_io}}}\n")
        f.write(f"\\newcommand{{\\semaIOPct}}{{{with_io*100//pattern_count}\\%}}\n")

        f.write(f"\\newcommand{{\\semaPatternsWithParams}}{{{with_params}}}\n")
        f.write(f"\\newcommand{{\\semaParamPct}}{{{with_params*100//pattern_count}\\%}}\n")

        f.write(f"\\newcommand{{\\semaPatternsWithCompose}}{{{with_compose}}}\n")
        f.write(f"\\newcommand{{\\semaComposePct}}{{{with_compose*100//pattern_count}\\%}}\n")

        f.write(f"\\newcommand{{\\semaTotalParams}}{{{total_params}}}\n")

    print(f"Stats written to {OUTPUT_TEX}")


if __name__ == "__main__":
    calculate_stats()
