#!/usr/bin/env python3
"""
Verify Speakability Script
Tests if patterns feel natural in sentences.
"""

import random

from sema.taxonomy_graph.graph_store import GraphStore, NodeType

TAXONOMY_DB = "data/taxonomy.db"


def check_speakability():
    print(f"Checking Speakability in {TAXONOMY_DB}...")
    print("")
    store = GraphStore(TAXONOMY_DB)

    solutions = store.get_nodes_by_type(NodeType.SOLUTION)

    # Templates for testing flow
    verb_templates = [
        "I need you to {handle} this connection.",
        "Did you {handle} the data?",
        "Let's {handle} before proceeding.",
    ]
    noun_templates = [
        "The {handle} is failing.",
        "We need a strong {handle} here.",
        "Waiting for {handle} to complete.",
    ]

    clunky_candidates = []

    print(f"{'HANDLE':<25} | {'SENTENCE SIMULATION'}")
    print("-" * 80)

    for _sol_id, data in solutions:
        handle = data["text"]

        # Heuristic: Is it short?
        is_long = len(handle) > 15

        # Pick a template
        # If it ends in 'Check' or 'Sync', it might be a noun/verb
        template = random.choice(noun_templates)
        if "Sync" in handle or "Tune" in handle or "Lock" in handle or "Check" in handle:
            template = random.choice(verb_templates)

        sentence = template.format(handle=handle)

        print(f"{handle:<25} | {sentence}")

        if is_long:
            clunky_candidates.append(handle)

    print("\n⚠️  Potential Clunky Handles (>15 chars):")
    for h in clunky_candidates:
        print(f"  - {h}")


if __name__ == "__main__":
    check_speakability()
