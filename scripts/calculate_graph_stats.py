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
        f"Patterns with formal invariants: {with_invariants} ({with_invariants / pattern_count:.0%})"
    )
    print(f"Patterns with preconditions: {with_pre} ({with_pre / pattern_count:.0%})")
    print(f"Patterns with postconditions: {with_post} ({with_post / pattern_count:.0%})")
    print(f"Patterns with typed I/O: {with_io} ({with_io / pattern_count:.0%})")
    print(f"Patterns with parameters: {with_params} ({with_params / pattern_count:.0%})")
    print(f"Total parameters: {total_params}")
    print(f"Patterns that compose: {with_compose} ({with_compose / pattern_count:.0%})")

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
        f.write(
            f"\\newcommand{{\\semaInvariantPct}}{{{with_invariants * 100 // pattern_count}\\%}}\n"
        )

        f.write(f"\\newcommand{{\\semaPatternsWithPre}}{{{with_pre}}}\n")
        f.write(f"\\newcommand{{\\semaPrePct}}{{{with_pre * 100 // pattern_count}\\%}}\n")

        f.write(f"\\newcommand{{\\semaPatternsWithPost}}{{{with_post}}}\n")
        f.write(f"\\newcommand{{\\semaPostPct}}{{{with_post * 100 // pattern_count}\\%}}\n")

        f.write(f"\\newcommand{{\\semaPatternsWithIO}}{{{with_io}}}\n")
        f.write(f"\\newcommand{{\\semaIOPct}}{{{with_io * 100 // pattern_count}\\%}}\n")

        f.write(f"\\newcommand{{\\semaPatternsWithParams}}{{{with_params}}}\n")
        f.write(f"\\newcommand{{\\semaParamPct}}{{{with_params * 100 // pattern_count}\\%}}\n")

        f.write(f"\\newcommand{{\\semaPatternsWithCompose}}{{{with_compose}}}\n")
        f.write(f"\\newcommand{{\\semaComposePct}}{{{with_compose * 100 // pattern_count}\\%}}\n")

        f.write(f"\\newcommand{{\\semaTotalParams}}{{{total_params}}}\n")

        # Tier and category counts
        from collections import Counter

        tier_counts = Counter()
        categories = set()
        for p in patterns:
            meta = p.get("_meta", {})
            tier = meta.get("tier")
            cat = meta.get("category") or p.get("sema_category")
            if tier is not None:
                tier_counts[tier] += 1
            if cat:
                categories.add(cat)
        f.write(f"\\newcommand{{\\semaTierOneCount}}{{{tier_counts.get(1, 0)}}}\n")
        f.write(f"\\newcommand{{\\semaCategoryCount}}{{{len(categories)}}}\n")

        # Compression stats — compute real token counts for representative
        # Tier-1 patterns using tiktoken (cl100k_base, same tokenizer as
        # GPT-4 / Claude). "Ref" = short reference form Handle#stub that
        # appears in the paper. "Full" = mechanism + invariants +
        # preconditions + postconditions + failure_modes (the semantic
        # payload an agent would need to transmit if content-addressing
        # were unavailable).
        import tiktoken

        enc = tiktoken.get_encoding("cl100k_base")

        representative = ["StateLock", "SpectralTune", "BayesUpdate", "SteelmanCheck"]
        pattern_by_handle = {p.get("handle"): p for p in patterns}

        comp_rows = []
        for handle in representative:
            p = pattern_by_handle.get(handle)
            if not p:
                raise RuntimeError(
                    f"Compression table references '{handle}' which is not in "
                    f"the default vocabulary. Update the representative list "
                    f"in calculate_graph_stats.py and the table in sema.tex."
                )
            stub = p["sema_id"].split(":SHA-256:")[-1][:4]
            ref_str = f"{handle}#{stub}"
            ref_tokens = len(enc.encode(ref_str))

            parts = [p.get("mechanism", "")]
            parts.extend(p.get("invariants", []))
            parts.extend(p.get("preconditions", []))
            parts.extend(p.get("postconditions", []))
            parts.extend(p.get("failure_modes", []))
            full_str = " ".join(s for s in parts if s)
            full_tokens = len(enc.encode(full_str))
            ratio = full_tokens / ref_tokens if ref_tokens else 0.0

            comp_rows.append((handle, stub, ref_tokens, full_tokens, ratio))

            f.write(f"\\newcommand{{\\semaComp{handle}Stub}}{{{stub}}}\n")
            f.write(f"\\newcommand{{\\semaComp{handle}Ref}}{{{ref_tokens}}}\n")
            f.write(f"\\newcommand{{\\semaComp{handle}Full}}{{{full_tokens}}}\n")
            f.write(f"\\newcommand{{\\semaComp{handle}Ratio}}{{{ratio:.1f}}}\n")

        comp_avg_ref = sum(r[2] for r in comp_rows) / len(comp_rows)
        comp_avg_full = sum(r[3] for r in comp_rows) / len(comp_rows)
        comp_avg_ratio = comp_avg_full / comp_avg_ref if comp_avg_ref else 0.0
        f.write(f"\\newcommand{{\\semaCompAvgRef}}{{{comp_avg_ref:.1f}}}\n")
        f.write(f"\\newcommand{{\\semaCompAvgFull}}{{{comp_avg_full:.1f}}}\n")
        f.write(f"\\newcommand{{\\semaCompAvgRatio}}{{{comp_avg_ratio:.1f}}}\n")

        # Per-layer compression: compute the same ref/full token counts
        # across the entire default library, then average by layer. This
        # reveals whether different layers carry different semantic weight
        # per hash: mind/society patterns tend to be denser (invariants,
        # failure modes) while infrastructure patterns are often terser.
        layer_buckets = {"Physics": [], "Infrastructure": [], "Mind": [], "Society": []}
        for p in patterns:
            handle = p.get("handle")
            layer = p.get("_meta", {}).get("layer") or p.get("sema_layer")
            if not handle or layer not in layer_buckets:
                continue
            stub = p["sema_id"].split(":SHA-256:")[-1][:4]
            ref_tokens = len(enc.encode(f"{handle}#{stub}"))
            parts = [p.get("mechanism", "")]
            parts.extend(p.get("invariants", []))
            parts.extend(p.get("preconditions", []))
            parts.extend(p.get("postconditions", []))
            parts.extend(p.get("failure_modes", []))
            full_tokens = len(enc.encode(" ".join(s for s in parts if s)))
            if ref_tokens and full_tokens:
                layer_buckets[layer].append((ref_tokens, full_tokens))

        for layer, rows in layer_buckets.items():
            if not rows:
                continue
            ar = sum(r[0] for r in rows) / len(rows)
            af = sum(r[1] for r in rows) / len(rows)
            rt = af / ar if ar else 0.0
            f.write(f"\\newcommand{{\\semaLayerComp{layer}Count}}{{{len(rows)}}}\n")
            f.write(f"\\newcommand{{\\semaLayerComp{layer}Ref}}{{{ar:.1f}}}\n")
            f.write(f"\\newcommand{{\\semaLayerComp{layer}Full}}{{{af:.1f}}}\n")
            f.write(f"\\newcommand{{\\semaLayerComp{layer}Ratio}}{{{rt:.1f}}}\n")

        # Library-wide average (across all default patterns, not just the 4)
        all_rows = [r for rows in layer_buckets.values() for r in rows]
        if all_rows:
            lib_ref = sum(r[0] for r in all_rows) / len(all_rows)
            lib_full = sum(r[1] for r in all_rows) / len(all_rows)
            lib_ratio = lib_full / lib_ref if lib_ref else 0.0
            f.write(f"\\newcommand{{\\semaLibCompRef}}{{{lib_ref:.1f}}}\n")
            f.write(f"\\newcommand{{\\semaLibCompFull}}{{{lib_full:.1f}}}\n")
            f.write(f"\\newcommand{{\\semaLibCompRatio}}{{{lib_ratio:.1f}}}\n")

        # Embedding similarity stats (from taxonomy.db)
        import sqlite3

        import numpy as np

        db_path = os.path.join(os.path.dirname(OUTPUT_TEX), "..", "data", "taxonomy.db")
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, embedding FROM nodes
                WHERE node_type = 'PATTERN' AND embedding IS NOT NULL
                """
            )
            vecs = []
            for _, blob in cursor.fetchall():
                if blob:
                    vecs.append(np.frombuffer(blob, dtype=np.float32))
            conn.close()

            n_emb = len(vecs)
            f.write(f"\\newcommand{{\\semaNodeEmbeddingCount}}{{{n_emb}}}\n")

            if n_emb > 1:
                # Compute pairwise cosine similarities
                mat = np.stack(vecs)
                norms = np.linalg.norm(mat, axis=1, keepdims=True)
                norms[norms == 0] = 1
                normed = mat / norms
                sim_matrix = normed @ normed.T

                # Extract upper triangle (exclude diagonal)
                upper = sim_matrix[np.triu_indices(n_emb, k=1)]
                total_pairs = len(upper)
                mean_sim = float(np.mean(upper))
                max_sim = float(np.max(upper))

                # Bins
                bin_a = int(np.sum((upper >= 0.0) & (upper < 0.3)))
                bin_b = int(np.sum((upper >= 0.3) & (upper < 0.5)))
                bin_c = int(np.sum((upper >= 0.5) & (upper < 0.7)))
                bin_d = int(np.sum((upper >= 0.7) & (upper < 1.0)))
                high_pairs = int(np.sum(upper >= 0.70))

                def pct(n: int) -> str:
                    return f"{n * 100 / total_pairs:.1f}\\%"

                f.write(f"\\newcommand{{\\semaEmbPairs}}{{{total_pairs:,}}}\n")
                f.write(f"\\newcommand{{\\semaEmbMean}}{{{mean_sim:.2f}}}\n")
                f.write(f"\\newcommand{{\\semaEmbMax}}{{{max_sim:.2f}}}\n")
                f.write(f"\\newcommand{{\\semaEmbBinA}}{{{bin_a:,}}}\n")
                f.write(f"\\newcommand{{\\semaEmbBinAPct}}{{{pct(bin_a)}}}\n")
                f.write(f"\\newcommand{{\\semaEmbBinB}}{{{bin_b:,}}}\n")
                f.write(f"\\newcommand{{\\semaEmbBinBPct}}{{{pct(bin_b)}}}\n")
                f.write(f"\\newcommand{{\\semaEmbBinC}}{{{bin_c:,}}}\n")
                f.write(f"\\newcommand{{\\semaEmbBinCPct}}{{{pct(bin_c)}}}\n")
                f.write(f"\\newcommand{{\\semaEmbBinD}}{{{bin_d:,}}}\n")
                f.write(f"\\newcommand{{\\semaEmbBinDPct}}{{{pct(bin_d)}}}\n")
                f.write(f"\\newcommand{{\\semaEmbHighPairs}}{{{high_pairs}}}\n")
                f.write(f"\\newcommand{{\\semaEmbHighPairPct}}{{{pct(high_pairs)}}}\n")

                print(
                    f"Embedding stats: {n_emb} vectors, mean={mean_sim:.2f}, max={max_sim:.2f}, {high_pairs} pairs >= 0.70"
                )
        else:
            print(f"WARNING: {db_path} not found, skipping embedding stats")

    print(f"Stats written to {OUTPUT_TEX}")


if __name__ == "__main__":
    calculate_stats()
