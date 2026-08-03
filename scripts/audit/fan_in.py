#!/usr/bin/env python3
"""Fan-in and cascade measurement for the vocabulary dependency graph.

Answers three specific questions rather than ranking the corpus:

    fan_in.py pattern <Handle>      what depends on this, and what it depends on
    fan_in.py cascade <Handle>...   how many patterns rehash if these are edited
    fan_in.py distribution          the shape of the graph, for calibration only

Why this exists: `dependencies` is nested as {"references": {placeholder: ref}},
so a traversal that does not descend one level silently reports zero dependents.
That bug produced two wrong cascade figures in review, including a claim that
editing Lock affected two patterns when it affects 112. Use this script instead
of writing extraction inline.

Reads the exports in data/vocabulary/. The database is authoritative for changes
(see AGENTS.md); for read-only measurement the exports are equivalent and need
no database.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VOCAB_DIR = REPO_ROOT / "data" / "vocabulary"

HASH_RE = re.compile(r"SHA-256:([0-9a-f]{64})")
HANDLE_RE = re.compile(r"^sema:([A-Za-z0-9_]+)")


def load() -> dict[str, dict]:
    patterns = {}
    for path in sorted(VOCAB_DIR.glob("*.json")):
        card = json.loads(path.read_text())
        patterns[card["handle"]] = card
    if not patterns:
        sys.exit(f"no pattern exports found in {VOCAB_DIR}")
    return patterns


def iter_strings(node):
    """Yield every string in a nested structure. The nesting is the whole point."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from iter_strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from iter_strings(value)


def dependency_targets(card: dict, known: set[str]) -> set[str]:
    targets = set()
    for ref in iter_strings(card.get("dependencies") or {}):
        match = HANDLE_RE.match(ref)
        if match and match.group(1) in known and match.group(1) != card["handle"]:
            targets.add(match.group(1))
    return targets


def build_graph(patterns: dict[str, dict]):
    known = set(patterns)
    out_edges = {h: dependency_targets(c, known) for h, c in patterns.items()}
    in_edges = defaultdict(set)
    for handle, targets in out_edges.items():
        for target in targets:
            in_edges[target].add(handle)
    return out_edges, in_edges


def transitive_dependents(seeds, in_edges) -> set[str]:
    """Everything that would rehash if `seeds` changed, excluding the seeds."""
    seen: set[str] = set()
    stack = list(seeds)
    while stack:
        for dependent in in_edges.get(stack.pop(), ()):
            if dependent not in seen:
                seen.add(dependent)
                stack.append(dependent)
    return seen - set(seeds)


def cmd_pattern(handles: list[str]) -> None:
    patterns = load()
    out_edges, in_edges = build_graph(patterns)
    for handle in handles:
        if handle not in patterns:
            print(f"{handle}: not found")
            continue
        card = patterns[handle]
        meta = card.get("_meta") or {}
        downstream = transitive_dependents([handle], in_edges)
        print(f"\n{handle}  layer={card.get('sema_layer')} tier={meta.get('tier')}")
        print(f"  direct dependents    {len(in_edges.get(handle, ()))}")
        print(f"  transitive dependents {len(downstream)}")
        print(f"  depends on           {len(out_edges[handle])} "
              f"{sorted(out_edges[handle]) if out_edges[handle] else ''}")
        if downstream:
            sample = sorted(downstream)[:8]
            more = "" if len(downstream) <= 8 else f" (+{len(downstream) - 8} more)"
            print(f"  dependents sample    {sample}{more}")


def cmd_cascade(handles: list[str]) -> None:
    patterns = load()
    _, in_edges = build_graph(patterns)
    missing = [h for h in handles if h not in patterns]
    if missing:
        sys.exit(f"not found: {', '.join(missing)}")
    downstream = transitive_dependents(handles, in_edges)
    total = len(handles) + len(downstream)
    print(f"editing a hashed field on {len(handles)} pattern(s) rehashes {total} "
          f"of {len(patterns)} ({100 * total // len(patterns)}%)")
    print(f"  edited      {sorted(handles)}")
    print(f"  cascaded    {len(downstream)}")
    if downstream:
        print(f"              {sorted(downstream)[:12]}"
              f"{'' if len(downstream) <= 12 else ' ...'}")
    print("\nA cascade above a few percent is a release-scale event. Batch such "
          "edits into one release rather than paying the rehash repeatedly.")


def cmd_distribution() -> None:
    patterns = load()
    out_edges, in_edges = build_graph(patterns)
    rows = [(h, len(transitive_dependents([h], in_edges)), len(out_edges[h]),
             patterns[h].get("sema_layer")) for h in patterns]

    print("Calibration only. Do not use this to rank patterns for review; the "
          "manual is read one pattern at a time.\n")
    buckets = [("0 (leaves)", lambda n: n == 0), ("1-9", lambda n: 1 <= n <= 9),
               ("10-99", lambda n: 10 <= n <= 99), ("100+", lambda n: n >= 100)]
    print(f"{'fan-in':12} {'n':>4} {'mean out-degree':>16}")
    for label, test in buckets:
        subset = [r for r in rows if test(r[1])]
        if subset:
            mean_out = sum(r[2] for r in subset) / len(subset)
            print(f"{label:12} {len(subset):4} {mean_out:16.1f}")

    print("\ntop fan-in")
    for handle, fan, out_degree, layer in sorted(rows, key=lambda r: -r[1])[:10]:
        print(f"  {handle:20} {fan:4} dependents  out-degree {out_degree}  {layer}")

    by_layer = defaultdict(list)
    for _, fan, _, layer in rows:
        by_layer[layer].append(fan)
    print("\nmedian fan-in by layer")
    for layer in ("Physics", "Infrastructure", "Mind", "Society"):
        values = sorted(by_layer.get(layer, []))
        if values:
            median = values[len(values) // 2]
            print(f"  {layer:16} n={len(values):3} median={median:4}")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    command, rest = args[0], args[1:]
    if command == "pattern" and rest:
        cmd_pattern(rest)
    elif command == "cascade" and rest:
        cmd_cascade(rest)
    elif command == "distribution":
        cmd_distribution()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
