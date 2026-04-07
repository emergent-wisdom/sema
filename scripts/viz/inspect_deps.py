#!/usr/bin/env python3
"""
Inspect dependencies of a pattern in the Sema graph.
Prints the DAG reachable from the given pattern.
"""

import argparse
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from sema.taxonomy_graph.graph_store import EdgeType, GraphStore


def inspect_deps(handle: str, max_depth: int = 10):
    print("Loading graph...")
    try:
        store = GraphStore("data/taxonomy.db")
    except Exception as e:
        print(f"Error loading graph: {e}")
        return

    # Find start node
    start_node_id = None
    for node_id, data in store.graph.nodes(data=True):
        if data.get('text') == handle:
            start_node_id = node_id
            break
    
    if not start_node_id:
        # Try finding by partial match if exact match fails
        candidates = []
        for node_id, data in store.graph.nodes(data=True):
            if handle.lower() in data.get('text', '').lower():
                candidates.append(data.get('text'))
        
        print(f"Pattern '{handle}' not found.")
        if candidates:
            print(f"Did you mean: {', '.join(candidates[:5])}?")
        return

    print(f"\nDependency Graph for '{handle}' ({start_node_id[:8]}):\n")

    # BFS/DFS for tree printing
    # We want to print as a tree, but it's a DAG, so we track visited path to detect cycles
    # and visited nodes (global) to avoid re-printing entire subtrees if they appear again (optional)
    
    # Let's use a recursive DFS print function
    
    # Types of edges to follow
    DEP_EDGES = {
        EdgeType.ACCEPTS,
        EdgeType.YIELDS,
        EdgeType.COMPOSES_WITH,
        EdgeType.REFERENCES,
        EdgeType.IMPLEMENTS,
        EdgeType.USES_MECHANISM,
        EdgeType.PRODUCES_OUTCOME,
        EdgeType.FOLLOWS_PRINCIPLE
    }

    def print_tree(node_id, current_depth, visited_path, indent="", is_root=True):
        if current_depth > max_depth:
            print("... (max depth reached)")
            return

        node_data = store.graph.nodes[node_id]
        name = node_data.get('text')

        # Check for cycle
        if node_id in visited_path:
            print(f"{name} [CYCLE DETECTED]")
            return

        # Root node gets its own line; children continue on the edge line
        if is_root:
            print(f"{indent}{name}")
        else:
            print(name)

        # Get outgoing edges
        children = []
        for succ in store.graph.successors(node_id):
            edge_data = store.graph.get_edge_data(node_id, succ)
            edge_type = edge_data.get('edge_type')

            if edge_type in DEP_EDGES:
                children.append((succ, edge_type))

        # Sort children for consistent output (maybe by edge type then name)
        children.sort(key=lambda x: (x[1].name, store.graph.nodes[x[0]].get('text')))

        for i, (child_id, edge_type) in enumerate(children):
            is_last = (i == len(children) - 1)
            branch = "└── " if is_last else "├── "

            # Color/format edge type
            edge_str = f"[{edge_type.name}]"

            print(f"{indent}{branch}{edge_str} ", end="")

            # Recurse
            next_indent = indent + ("    " if is_last else "│   ")
            print_tree(child_id, current_depth + 1, visited_path | {node_id}, next_indent, is_root=False)

    print_tree(start_node_id, 0, set())
    print("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect pattern dependencies.")
    parser.add_argument("handle", help="The pattern handle (e.g., RecursiveIntelligence)")
    parser.add_argument("--depth", type=int, default=5, help="Max depth to traverse")
    
    args = parser.parse_args()
    inspect_deps(args.handle, args.depth)
