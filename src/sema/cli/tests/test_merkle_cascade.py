"""
Test Merkle DAG cascade functionality.

Verifies that:
1. Hashes are computed using the centralized generate_sema_hash()
2. Dependencies are stored as handles only (no hashes)
3. Hash changes cascade to all dependents
"""

import os
import shutil
import tempfile

import pytest

from sema.taxonomy_graph.graph_store import GraphStore


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

    def test_middle_update_cascades_up_not_sideways(self, temp_db):
        """Updating a middle node cascades to dependents (up) but not siblings (sideways).

        Structure:
            Root depends on MidA, MidB, MidC
            MidA depends on LeafA1, LeafA2, LeafA3
            MidB depends on LeafB1, LeafB2, LeafB3
            MidC depends on LeafC1, LeafC2, LeafC3

        Update MidA. Expect:
          - Root changes (depends on MidA)
          - MidA changes (updated)
          - MidB, MidC unchanged (siblings, no dep relationship)
          - All leaves unchanged (MidA doesn't affect its children)
        """
        store = GraphStore(temp_db)

        # Leaves (9 total)
        for branch in ("A", "B", "C"):
            for n in (1, 2, 3):
                store.add_pattern(
                    {
                        "handle": f"Leaf{branch}{n}",
                        "mechanism": f"Leaf {branch}{n}",
                        "gloss": f"Leaf {branch}{n}",
                        "_meta": {
                            "layer": "Infrastructure",
                            "category": "Primitives",
                            "tier": 1,
                        },
                    }
                )

        # Middles
        for branch in ("A", "B", "C"):
            store.add_pattern(
                {
                    "handle": f"Mid{branch}",
                    "mechanism": (
                        f"Uses {{{{leaf_{branch.lower()}1}}}} and "
                        f"{{{{leaf_{branch.lower()}2}}}} and "
                        f"{{{{leaf_{branch.lower()}3}}}}"
                    ),
                    "gloss": f"Mid {branch}",
                    "dependencies": {
                        "references": {
                            f"leaf_{branch.lower()}1": f"Leaf{branch}1",
                            f"leaf_{branch.lower()}2": f"Leaf{branch}2",
                            f"leaf_{branch.lower()}3": f"Leaf{branch}3",
                        }
                    },
                    "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
                }
            )

        # Root
        store.add_pattern(
            {
                "handle": "Root",
                "mechanism": "Uses {{mid_a}} and {{mid_b}} and {{mid_c}}",
                "gloss": "Root",
                "dependencies": {"references": {"mid_a": "MidA", "mid_b": "MidB", "mid_c": "MidC"}},
                "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
            }
        )

        handles = [f"Leaf{b}{n}" for b in "ABC" for n in (1, 2, 3)] + [
            "MidA",
            "MidB",
            "MidC",
            "Root",
        ]
        before = {h: store.get_pattern_hash(h) for h in handles}

        # Update MidA
        result = store.add_pattern(
            {
                "handle": "MidA",
                "mechanism": ("UPDATED middle — uses {{leaf_a1}} and {{leaf_a2}} and {{leaf_a3}}"),
                "gloss": "Mid A",
                "dependencies": {
                    "references": {
                        "leaf_a1": "LeafA1",
                        "leaf_a2": "LeafA2",
                        "leaf_a3": "LeafA3",
                    }
                },
                "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
            }
        )

        after = {h: store.get_pattern_hash(h) for h in handles}

        # Changed
        assert after["MidA"] != before["MidA"], "MidA updated"
        assert after["Root"] != before["Root"], "Root depends on MidA, must cascade"

        # Unchanged — siblings
        assert after["MidB"] == before["MidB"], "MidB is a sibling, must NOT cascade"
        assert after["MidC"] == before["MidC"], "MidC is a sibling, must NOT cascade"

        # Unchanged — MidA's own children (leaves)
        for n in (1, 2, 3):
            h = f"LeafA{n}"
            assert after[h] == before[h], f"{h} is a child of MidA, must NOT cascade"

        # Unchanged — other branches' leaves
        for b in ("B", "C"):
            for n in (1, 2, 3):
                h = f"Leaf{b}{n}"
                assert after[h] == before[h], f"{h} is unrelated, must NOT cascade"

        # Cascade report should contain only Root (and MidA itself)
        cascaded = set(result.get("cascade", {}).get("updated", []))
        assert "Root" in cascaded, "Root must be in cascade"
        assert "MidB" not in cascaded, "MidB leaked into cascade"
        assert "MidC" not in cascaded, "MidC leaked into cascade"
        assert not any(h.startswith("Leaf") for h in cascaded), "No leaf should cascade"

    def test_diamond_dependency_leaves_no_stale_hashes(self, temp_db):
        """Diamond: Top -> {Left, Right} -> Base. Updating Base must leave
        every stored hash equal to a fresh recompute.

        Regression: a DFS cascade with a visited set rehashes Top after
        only one of Left/Right has its new hash, then the visited set
        blocks the second, correct recompute — leaving Top's stored hash
        permanently stale.
        """
        store = GraphStore(temp_db)

        store.add_pattern(
            {
                "handle": "Base",
                "mechanism": "The base mechanism",
                "gloss": "Base",
                "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
            }
        )
        for side in ("Left", "Right"):
            store.add_pattern(
                {
                    "handle": side,
                    "mechanism": f"{side} arm uses {{{{base}}}}",
                    "gloss": side,
                    "dependencies": {"references": {"base": "Base"}},
                    "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
                }
            )
        store.add_pattern(
            {
                "handle": "Top",
                "mechanism": "Joins {{left}} and {{right}}",
                "gloss": "Top",
                "dependencies": {"references": {"left": "Left", "right": "Right"}},
                "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
            }
        )

        content = store._get_pattern_content("Base")
        content["mechanism"] = "The base mechanism, updated"
        result = store.update_pattern_with_cascade("Base", content)

        assert result.get("success"), result.get("error")
        assert set(result["updated"]) == {"Base", "Left", "Right", "Top"}, result["updated"]

        # The invariant: every stored hash matches a fresh recompute.
        for handle in ("Base", "Left", "Right", "Top"):
            stored = store.get_pattern_hash(handle)
            fresh = store.compute_pattern_hash(store._get_pattern_content(handle))["hash"]
            assert stored == fresh, (
                f"stale hash on '{handle}': stored={stored[:12]} fresh={fresh[:12]}"
            )

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
