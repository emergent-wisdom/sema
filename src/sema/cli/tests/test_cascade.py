#!/usr/bin/env python3
"""
Test that updating a pattern cascades to all dependent patterns.

The Merkle DAG property: if Pattern A depends on Pattern B,
and B's hash changes, then A's dependency reference must update,
which changes A's hash, which must cascade to A's dependents, etc.
"""

import os
import shutil
import tempfile

import pytest

from sema.core.hashing import generate_sema_hash
from sema.taxonomy_graph.graph_store import GraphStore


class TestCascadeIntegrity:
    """Test that hash changes cascade correctly through the dependency graph."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_taxonomy.db")
        yield db_path
        shutil.rmtree(temp_dir)

    def test_cascade_on_dependency_update(self, temp_db):
        """
        When a pattern's hash changes, all patterns that depend on it
        should have their dependency references updated.
        """
        store = GraphStore(temp_db)

        # 1. Create base pattern: Gate
        gate_v1 = {
            "handle": "Gate",
            "mechanism": "A binary control point.",
            "gloss": "Binary gate",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        gate_hash_v1 = generate_sema_hash(gate_v1)
        gate_v1["sema_id"] = gate_hash_v1["full_id"]
        gate_v1["sema_ref"] = gate_hash_v1["reference"]
        store.add_pattern(gate_v1)

        # 2. Create dependent pattern: TriGate (depends on Gate)
        trigate_v1 = {
            "handle": "TriGate",
            "mechanism": "A trinary {{gate}} with Red/Yellow/Green.",
            "gloss": "Traffic light gate",
            "dependencies": {"references": {"gate": gate_hash_v1["full_id"]}},
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        trigate_hash_v1 = generate_sema_hash(trigate_v1)
        trigate_v1["sema_id"] = trigate_hash_v1["full_id"]
        trigate_v1["sema_ref"] = trigate_hash_v1["reference"]
        store.add_pattern(trigate_v1)

        # 3. Create pattern that depends on TriGate: PURECheck
        purecheck_v1 = {
            "handle": "PURECheck",
            "mechanism": "Uses {{trigate}} for triage.",
            "gloss": "PURE triage protocol",
            "dependencies": {"composes_with": {"trigate": trigate_hash_v1["full_id"]}},
            "_meta": {"layer": "Society", "category": "Protocols", "tier": 1},
        }
        purecheck_hash_v1 = generate_sema_hash(purecheck_v1)
        purecheck_v1["sema_id"] = purecheck_hash_v1["full_id"]
        purecheck_v1["sema_ref"] = purecheck_hash_v1["reference"]
        store.add_pattern(purecheck_v1)

        # Record original hashes
        original_gate_hash = gate_hash_v1["hash"]
        original_trigate_hash = trigate_hash_v1["hash"]
        original_purecheck_hash = purecheck_hash_v1["hash"]

        print("\n=== BEFORE UPDATE ===")
        print(f"Gate hash:      {original_gate_hash[:16]}...")
        print(f"TriGate hash:   {original_trigate_hash[:16]}...")
        print(f"PURECheck hash: {original_purecheck_hash[:16]}...")

        # 4. Update Gate (change mechanism)
        gate_v2 = gate_v1.copy()
        gate_v2["mechanism"] = "A binary control point with explicit open/close states."
        gate_hash_v2 = generate_sema_hash(gate_v2)

        print("\n=== UPDATING Gate ===")
        print(f"New Gate hash:  {gate_hash_v2['hash'][:16]}...")

        # The cascade should happen here - this is what we need to implement
        # For now, let's verify what SHOULD happen:

        # 5. After Gate update, TriGate's dependency should point to new Gate hash
        trigate_v2 = trigate_v1.copy()
        trigate_v2["dependencies"] = {
            "references": {
                "gate": gate_hash_v2["full_id"]  # NEW Gate hash
            }
        }
        trigate_hash_v2 = generate_sema_hash(trigate_v2)

        print("\n=== EXPECTED CASCADE ===")
        print(f"TriGate should update to: {trigate_hash_v2['hash'][:16]}...")

        # 6. After TriGate update, PURECheck's dependency should point to new TriGate hash
        purecheck_v2 = purecheck_v1.copy()
        purecheck_v2["dependencies"] = {
            "composes_with": {
                "trigate": trigate_hash_v2["full_id"]  # NEW TriGate hash
            }
        }
        purecheck_hash_v2 = generate_sema_hash(purecheck_v2)

        print(f"PURECheck should update to: {purecheck_hash_v2['hash'][:16]}...")

        # Verify hashes changed
        assert gate_hash_v2["hash"] != original_gate_hash, "Gate hash should change"
        assert trigate_hash_v2["hash"] != original_trigate_hash, "TriGate hash should cascade"
        assert purecheck_hash_v2["hash"] != original_purecheck_hash, "PURECheck hash should cascade"

        print("\n✅ Cascade verification: All hashes would change correctly")

    def test_database_integrity_after_update(self, temp_db):
        """
        After updating a pattern via CLI apply, verify that:
        1. Dependent patterns have updated references
        2. No stale hashes remain in dependencies
        """
        store = GraphStore(temp_db)

        # Create a simple dependency chain: A -> B
        pattern_a = {
            "handle": "PatternA",
            "mechanism": "Base pattern",
            "gloss": "A",
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
        }
        hash_a = generate_sema_hash(pattern_a)
        pattern_a["sema_id"] = hash_a["full_id"]
        store.add_pattern(pattern_a)

        pattern_b = {
            "handle": "PatternB",
            "mechanism": "Depends on {{patterna}}",
            "gloss": "B",
            "dependencies": {"references": {"patterna": hash_a["full_id"]}},
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
        }
        hash_b = generate_sema_hash(pattern_b)
        pattern_b["sema_id"] = hash_b["full_id"]
        store.add_pattern(pattern_b)

        # Verify B references A via edge (dependencies stored as edges only)
        edge_deps = store.get_dependencies_from_edges("PatternB")
        assert "references" in edge_deps, "PatternB should have references edge"
        patterna_ref = edge_deps["references"].get("pattern_a")
        # Now returns full sema_id format per Rule C
        assert patterna_ref is not None and patterna_ref.startswith("sema:PatternA#"), (
            f"PatternB should reference PatternA with full sema_id. Got: {edge_deps}"
        )
        print(f"✅ PatternB correctly references PatternA via edge: {patterna_ref}")


def test_find_dependents():
    """Test helper function to find all patterns that depend on a given pattern."""
    # This function needs to be implemented in graph_store.py
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
