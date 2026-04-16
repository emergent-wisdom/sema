import os
import sys
from collections import defaultdict

import networkx as nx

# Add project root to path
sys.path.append(os.getcwd())

from sema.taxonomy_graph.graph_store import EdgeType, GraphStore, NodeType


def audit_graph():
    print("Loading graph...")
    try:
        store = GraphStore("data/taxonomy.db")
    except Exception as e:
        print(f"Error loading graph: {e}")
        return

    print(
        f"Graph loaded with {store.graph.number_of_nodes()} nodes and {store.graph.number_of_edges()} edges."
    )

    problems = []

    # 1. Check for Orphaned Patterns (no edges at all)
    print("Checking for orphaned patterns...")
    solutions = store.get_nodes_by_type(NodeType.PATTERN)
    for sol_id, data in solutions:
        degree = store.graph.degree(sol_id)
        if degree == 0:
            problems.append(f"[ORPHAN] Pattern '{data['text']}' ({sol_id}) has 0 edges.")

    # 2. Check for Orphaned Components (not linked to any Pattern)
    # Most components should be reachable from a Pattern (Pattern -> Component or Component -> Pattern)
    # Actually, components like MECHANISM, OUTCOME are linked FROM Pattern.
    # INVARIANT, PRECONDITION, POSTCONDITION are linked FROM Pattern.
    # So incoming degree should be > 0.
    print("Checking for orphaned components...")
    component_types = [
        NodeType.MECHANISM,
        NodeType.OUTCOME,
        NodeType.PRINCIPLE,
        NodeType.CRITICISM,
        NodeType.JUSTIFICATION,
        NodeType.NOVELTY,
        NodeType.INVARIANT,
        NodeType.PRECONDITION,
        NodeType.POSTCONDITION,
    ]

    for c_type in component_types:
        nodes = store.get_nodes_by_type(c_type)
        for node_id, data in nodes:
            in_degree = store.graph.in_degree(node_id)
            if in_degree == 0:
                problems.append(
                    f"[ORPHAN] {c_type.name} '{data['text'][:50]}...' ({node_id}) has no incoming edges."
                )

    # 3. Check for Missing Metadata (Layer/Category)
    print("Checking for missing metadata...")
    for _sol_id, data in solutions:
        meta = data.get("metadata", {})
        category = meta.get("category")
        layer = meta.get("layer")

        if not category:
            problems.append(f"[MISSING_META] Pattern '{data['text']}' missing 'category'.")
        if not layer:
            problems.append(f"[MISSING_META] Pattern '{data['text']}' missing 'layer'.")

    # 4. Check for Cycles in Hierarchy (PARENT_OF)
    print("Checking for hierarchy cycles...")
    hierarchy_graph = nx.DiGraph()
    for u, v, data in store.graph.edges(data=True):
        if data.get("edge_type") == EdgeType.PARENT_OF:
            hierarchy_graph.add_edge(u, v)

    try:
        cycles = list(nx.simple_cycles(hierarchy_graph))
        if cycles:
            for cycle in cycles:
                names = [store.graph.nodes[n]["text"] for n in cycle]
                problems.append(f"[CYCLE] Hierarchy cycle detected: {' -> '.join(names)}")
    except Exception as e:
        print(f"Error checking cycles: {e}")

    # 5. Check for Duplicate Names
    print("Checking for duplicate names...")
    name_counts = defaultdict(list)
    for node_id, data in store.graph.nodes(data=True):
        if data.get("node_type") == NodeType.PATTERN:
            name_counts[data["text"]].append(node_id)

    for name, ids in name_counts.items():
        if len(ids) > 1:
            problems.append(
                f"[DUPLICATE] Pattern '{name}' appears {len(ids)} times (IDs: {', '.join(ids)})."
            )

    # 6. Check Rigor (Missing Invariants/Pre/Post)
    print("Checking rigor...")
    for sol_id, data in solutions:
        has_inv = False
        has_pre = False
        has_post = False

        # MultiDiGraph.get_edge_data returns {key: attrs}; iterate values.
        for succ in store.graph.successors(sol_id):
            for edge_data in (store.graph.get_edge_data(sol_id, succ) or {}).values():
                edge_type = edge_data.get("edge_type")
                if edge_type == EdgeType.HAS_INVARIANT:
                    has_inv = True
                if edge_type == EdgeType.HAS_PRECONDITION:
                    has_pre = True
                if edge_type == EdgeType.HAS_POSTCONDITION:
                    has_post = True

        if not (has_inv or has_pre or has_post):
            problems.append(
                f"[NO_CONTRACTS] Pattern '{data['text']}' has no Invariants, Preconditions, or Postconditions."
            )

    # Report
    print(f"\nAudit Complete. Found {len(problems)} problems.\n")
    if problems:
        for p in problems:
            print(p)
    else:
        print("No problems found!")


if __name__ == "__main__":
    audit_graph()
