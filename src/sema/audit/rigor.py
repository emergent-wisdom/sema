import json

from sema.taxonomy_graph.graph_store import EdgeType, GraphStore, NodeType


def audit_rigor():
    db_path = "data/taxonomy.db"
    store = GraphStore(db_path)

    solutions = store.get_nodes_by_type(NodeType.PATTERN)

    stats = {
        "total": len(solutions),
        "with_invariants": 0,
        "with_preconditions": 0,
        "with_postconditions": 0,
        "with_all_contract_fields": 0,
        "without_explicit_contracts": 0,
    }

    patterns_without_contracts = []

    for sol_id, data in solutions:
        has_inv = False
        has_pre = False
        has_post = False

        # Check edges. MultiDiGraph.get_edge_data returns {key: attrs}; iterate
        # over values so parallel edges of different types are all checked.
        for succ in store.graph.successors(sol_id):
            for edge_data in (store.graph.get_edge_data(sol_id, succ) or {}).values():
                edge_type = edge_data.get("edge_type")

                if edge_type == EdgeType.HAS_INVARIANT:
                    has_inv = True
                if edge_type == EdgeType.HAS_PRECONDITION:
                    has_pre = True
                if edge_type == EdgeType.HAS_POSTCONDITION:
                    has_post = True

        if has_inv:
            stats["with_invariants"] += 1
        if has_pre:
            stats["with_preconditions"] += 1
        if has_post:
            stats["with_postconditions"] += 1

        if has_inv and has_pre and has_post:
            stats["with_all_contract_fields"] += 1

        if not (has_inv or has_pre or has_post):
            stats["without_explicit_contracts"] += 1
            if len(patterns_without_contracts) < 15:
                patterns_without_contracts.append(data["text"])

    print(json.dumps(stats, indent=2))
    print(
        "\nSample patterns without explicit contracts (review only; omission may be intentional):"
    )
    for ex in patterns_without_contracts:
        print(f"- {ex}")


if __name__ == "__main__":
    audit_rigor()
