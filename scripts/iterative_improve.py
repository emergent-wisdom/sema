#!/usr/bin/env python3
"""
Iterative Improvement
Runs rounds of sampling, analysis, and automatic hardening.
"""

import json
import os
import random
import sqlite3
import sys

# Add project root to path
sys.path.append(os.getcwd())

from sema.taxonomy_graph.graph_store import EdgeType, GraphStore, NodeType

TAXONOMY_DB = "data/taxonomy.db"

# Heuristics for auto-hardening common pattern types
HARDENING_TEMPLATES = {
    # Rationality / Bayesian Patterns
    "rate": {
        "invariants": ["Calculation must explicitly include the rate variable"],
        "preconditions": ["Reference class is defined"],
    },
    "bias": {
        "invariants": ["Correction magnitude > 0"],
        "preconditions": ["Bias detected in baseline"],
    },
    "cost": {
        "invariants": ["Utility > Cost", "Decision depends on Future, not Past"],
        "preconditions": ["Alternative actions exist"],
    },
    "replay": {
        "invariants": ["Replay order must match original recording"],
        "preconditions": ["History log exists"],
    },
    "context": {
        "invariants": ["Context boundary is explicit"],
        "preconditions": ["Context is loaded"],
    },
    "signal": {"invariants": ["Signal/Noise ratio > 1.0"], "preconditions": ["Channel open"]},
    "consensus": {"invariants": ["Quorum > 50%"], "preconditions": ["Participants known"]},
    # New Templates
    "auction": {
        "invariants": ["Bid > Reserve", "Highest/Lowest bid wins deterministically"],
        "preconditions": ["Asset is distinct", "Bidders have funds"],
    },
    "time": {
        "invariants": ["Duration <= Limit", "Action halts at T_max"],
        "preconditions": ["Clock is synchronized"],
    },
    "block": {
        "invariants": ["Action X is prevented", "Filter false-positive rate < epsilon"],
        "preconditions": ["Filter criteria defined"],
    },
    "check": {
        "invariants": ["Verification is binary (Pass/Fail)"],
        "preconditions": ["Input is verifiable"],
    },
    "proxy": {
        "invariants": ["Output ~= Input (Lossless Transform)", "Identity is masked"],
        "preconditions": ["Target is reachable"],
    },
    # Phase 2 Expansion
    "token": {
        "invariants": [
            "Token must be cryptographically signed",
            "Token has expiration or revocation mechanism",
        ],
        "preconditions": ["Issuer is trusted"],
    },
    "barrier": {
        "invariants": ["Events after barrier cannot happen before barrier"],
        "preconditions": ["Barrier condition is defined"],
    },
    "sync": {
        "invariants": ["State is consistent across partitions after sync"],
        "preconditions": ["Connection to peers is available"],
    },
    "shard": {
        "invariants": ["Union of shards equals global state", "Shard boundary is non-overlapping"],
        "preconditions": ["Sharding function is deterministic"],
    },
    "handshake": {
        "invariants": ["Mutual authentication completed", "Protocol version agreed upon"],
        "preconditions": ["Channel is established"],
    },
    "lock": {
        "invariants": [
            "Mutual exclusion: Only one holder at a time",
            "Deadlock freedom guaranteed (or timed out)",
        ],
        "preconditions": ["Resource exists"],
    },
    "counter": {
        "invariants": ["Value(t+1) >= Value(t) (Monotonic)", "Update is atomic"],
        "preconditions": ["Initial value >= 0"],
    },
    "audit": {
        "invariants": [
            "Auditor is distinct from Actor (Separation of Duties)",
            "Audit trail is immutable",
        ],
        "preconditions": ["Operation to audit has occurred"],
    },
}


def auto_harden(store, node_id, handle):
    """Attempt to apply a template based on the handle name."""
    handle_lower = handle.lower()

    applied = False

    # Determine which templates apply
    templates_to_apply = []
    for key, template in HARDENING_TEMPLATES.items():
        if key in handle_lower:
            templates_to_apply.append((key, template))

    if not templates_to_apply:
        return False

    print(f"    🛠️  Auto-hardening '{handle}' with {[t[0] for t in templates_to_apply]}...")

    # Fetch current metadata to update
    node_data = store.graph.nodes[node_id]
    metadata = node_data.get("metadata", {})
    pattern = metadata.get("pattern", {})

    # Ensure lists exist
    if "invariants" not in pattern:
        pattern["invariants"] = []
    if "preconditions" not in pattern:
        pattern["preconditions"] = []

    current_invs = set(pattern["invariants"])
    current_pres = set(pattern["preconditions"])

    for key, template in templates_to_apply:
        try:
            # Add Invariants (Graph + Metadata)
            for text in template["invariants"]:
                # Graph Node
                nid = store.create_node(NodeType.INVARIANT, text)
                store.create_edge(node_id, nid, EdgeType.HAS_INVARIANT)

                # Metadata
                if text not in current_invs:
                    pattern["invariants"].append(text)
                    current_invs.add(text)
                    applied = True

            # Add Preconditions (Graph + Metadata)
            for text in template["preconditions"]:
                # Graph Node
                nid = store.create_node(NodeType.PRECONDITION, text)
                store.create_edge(node_id, nid, EdgeType.HAS_PRECONDITION)

                # Metadata
                if text not in current_pres:
                    pattern["preconditions"].append(text)
                    current_pres.add(text)
                    applied = True

        except Exception as e:
            print(f"Error applying {key}: {e}")

    if applied:
        # Save back to DB
        metadata["pattern"] = pattern
        node_data["metadata"] = metadata  # Update in-memory

        conn = sqlite3.connect(store.db_path)
        conn.execute("UPDATE nodes SET metadata = ? WHERE id = ?", (json.dumps(metadata), node_id))
        conn.commit()
        conn.close()
        return True

    return False


def run_improvement_loop(rounds=10):
    if not os.path.exists(TAXONOMY_DB):
        print("Database not found.")
        return

    store = GraphStore(TAXONOMY_DB)
    solutions = store.get_nodes_by_type(NodeType.SOLUTION)

    total_hardened = 0

    # Iterate ALL solutions shuffled
    random.shuffle(solutions)

    print(f"Scanning {len(solutions)} patterns for improvements...")

    for nid, data in solutions:
        handle = data["text"]

        # Check status (heuristic: if no invariants, try to harden)
        # Or just try to harden anyway if it matches a template

        # Force check for templates (auto_harden itself is idempotent —
        # adds invariants only if the text isn't already present).
        if auto_harden(store, nid, handle):
            total_hardened += 1

    print(f"\n✅ Loop Complete. Hardened {total_hardened} patterns.")


if __name__ == "__main__":
    run_improvement_loop()
