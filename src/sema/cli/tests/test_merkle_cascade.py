#!/usr/bin/env python3
"""
Test Merkle DAG cascade functionality.

Verifies that:
1. Hashes are computed using the centralized generate_sema_hash()
2. Dependencies are stored as handles only (no hashes)
3. Hash changes cascade to all dependents
"""

import os
import shutil
import sys
import tempfile

import pytest

# Ensure we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from sema.taxonomy_graph.graph_store import GraphStore  # noqa: E402


class TestMerkleCascade:
    """Test Merkle DAG cascade integrity."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_cascade.db")
        yield db_path
        shutil.rmtree(temp_dir)

    def test_dependencies_stored_as_edges(self, temp_db):
        """Dependencies should be stored as graph edges, not in pattern content."""
        store = GraphStore(temp_db)

        # Create base pattern
        gate = {
            "handle": "Gate",
            "mechanism": "A binary control point.",
            "gloss": "Binary gate",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        result = store.add_pattern(gate)
        assert result["success"], f"Failed to add Gate: {result}"

        # Create pattern with full sema ID in dependency
        trigate = {
            "handle": "TriGate",
            "mechanism": "A trinary {{gate}} with Red/Yellow/Green.",
            "gloss": "Traffic light gate",
            "dependencies": {
                "references": {
                    "gate": "sema:Gate#mh:SHA-256:abc123def456..."  # Full sema ID
                }
            },
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        result = store.add_pattern(trigate)
        assert result["success"], f"Failed to add TriGate: {result}"

        # Verify dependencies are NOT stored in pattern content
        content = store._get_pattern_content("TriGate")
        assert content is not None
        deps_in_content = content.get("dependencies", {})
        assert deps_in_content == {}, (
            f"Dependencies should NOT be in content. Got: {deps_in_content}"
        )

        # Verify dependencies ARE stored as graph edges
        edge_deps = store.get_dependencies_from_edges("TriGate")
        assert "references" in edge_deps, f"Should have references edge. Got: {edge_deps}"
        gate_ref = edge_deps["references"].get("gate")
        # Now returns full sema_id format per Rule C
        assert gate_ref is not None and gate_ref.startswith("sema:Gate#"), (
            f"Edge should point to Gate with full sema_id. Got: {edge_deps}"
        )

        print("✅ Dependencies stored as edges, not in content")

    def test_hash_uses_dependency_hashes(self, temp_db):
        """Pattern hash should incorporate current dependency hashes."""
        store = GraphStore(temp_db)

        # Create base pattern
        gate = {
            "handle": "Gate",
            "mechanism": "A binary control point.",
            "gloss": "Binary gate",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        store.add_pattern(gate)
        gate_hash_v1 = store.get_pattern_hash("Gate")
        print(f"Gate hash v1: {gate_hash_v1[:16]}...")

        # Create dependent pattern
        trigate = {
            "handle": "TriGate",
            "mechanism": "A trinary gate.",
            "gloss": "Traffic light gate",
            "dependencies": {"references": {"gate": "Gate"}},
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        store.add_pattern(trigate)
        trigate_hash_v1 = store.get_pattern_hash("TriGate")
        print(f"TriGate hash v1: {trigate_hash_v1[:16]}...")

        # Update Gate
        gate_v2 = {
            "handle": "Gate",
            "mechanism": "A binary control point with explicit open/close.",  # Changed!
            "gloss": "Binary gate",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        result = store.add_pattern(gate_v2)
        gate_hash_v2 = store.get_pattern_hash("Gate")
        print(f"Gate hash v2: {gate_hash_v2[:16]}...")

        # Gate's hash should change
        assert gate_hash_v2 != gate_hash_v1, "Gate hash should change after update"

        # TriGate's hash should also change (cascade!)
        trigate_hash_v2 = store.get_pattern_hash("TriGate")
        print(f"TriGate hash v2: {trigate_hash_v2[:16]}...")

        assert trigate_hash_v2 != trigate_hash_v1, "TriGate hash should cascade after Gate update"

        # Verify cascade was reported
        assert "cascade" in result, "add_pattern should report cascade"
        assert "TriGate" in result["cascade"]["updated"], "TriGate should be in cascade list"

        print("✅ Hash cascade works correctly")

    def test_recursive_cascade(self, temp_db):
        """Cascade should be recursive: A -> B -> C."""
        store = GraphStore(temp_db)

        # Create chain: A <- B <- C
        a = {
            "handle": "PatternA",
            "mechanism": "Base pattern",
            "gloss": "A",
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
        }
        store.add_pattern(a)

        b = {
            "handle": "PatternB",
            "mechanism": "Depends on A",
            "gloss": "B",
            "dependencies": {"references": {"a": "PatternA"}},
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
        }
        store.add_pattern(b)

        c = {
            "handle": "PatternC",
            "mechanism": "Depends on B",
            "gloss": "C",
            "dependencies": {"references": {"b": "PatternB"}},
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
        }
        store.add_pattern(c)

        # Record original hashes
        hash_a1 = store.get_pattern_hash("PatternA")
        hash_b1 = store.get_pattern_hash("PatternB")
        hash_c1 = store.get_pattern_hash("PatternC")

        print(f"Before: A={hash_a1[:8]}, B={hash_b1[:8]}, C={hash_c1[:8]}")

        # Update A
        a_v2 = {
            "handle": "PatternA",
            "mechanism": "Updated base pattern",  # Changed!
            "gloss": "A",
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
        }
        result = store.add_pattern(a_v2)

        hash_a2 = store.get_pattern_hash("PatternA")
        hash_b2 = store.get_pattern_hash("PatternB")
        hash_c2 = store.get_pattern_hash("PatternC")

        print(f"After:  A={hash_a2[:8]}, B={hash_b2[:8]}, C={hash_c2[:8]}")

        # All should change
        assert hash_a2 != hash_a1, "A should change"
        assert hash_b2 != hash_b1, "B should cascade"
        assert hash_c2 != hash_c1, "C should cascade (recursive)"

        # Verify cascade list
        cascaded = result.get("cascade", {}).get("updated", [])
        assert "PatternB" in cascaded, "B should be in cascade"
        assert "PatternC" in cascaded, "C should be in cascade"

        print("✅ Recursive cascade works correctly")

    def test_validation_prevents_missing_deps(self, temp_db):
        """Adding pattern with missing dependency should fail."""
        store = GraphStore(temp_db)

        # Try to add pattern referencing non-existent dependency
        bad_pattern = {
            "handle": "BadPattern",
            "mechanism": "References missing",
            "gloss": "Bad",
            "dependencies": {"references": {"missing": "NonExistentPattern"}},
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
        }
        result = store.add_pattern(bad_pattern)

        assert result["success"] is False, "Should fail for missing dependency"
        assert "Missing dependency" in result.get("error", ""), (
            f"Should report missing dep. Got: {result}"
        )

        print("✅ Validation prevents missing dependencies")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
