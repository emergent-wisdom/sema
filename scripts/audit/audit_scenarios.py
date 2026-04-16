#!/usr/bin/env python3
import os
import sys

sys.path.append(os.getcwd())
from sema.taxonomy_graph.graph_store import GraphStore, NodeType


def audit():
    store = GraphStore("data/taxonomy.db")
    scenarios = store.get_nodes_by_type(NodeType.SCENARIO)
    print(f"Auditing {len(scenarios)} scenarios...")

    found_overlap = False
    for sid, sdata in scenarios:
        solutions = []
        for pred in store.graph.predecessors(sid):
            if store.graph.nodes[pred]["node_type"] == NodeType.PATTERN:
                solutions.append(store.graph.nodes[pred]["text"])

        if len(solutions) > 1:
            found_overlap = True
            print(f'\nScenario: "{sdata["text"][:60]}..."')
            print(f"  Solved by ({len(solutions)}): {', '.join(solutions)}")

    if not found_overlap:
        print("No scenarios have multiple solutions (1:1 mapping currently).")


if __name__ == "__main__":
    audit()
