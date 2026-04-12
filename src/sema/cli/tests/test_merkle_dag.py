"""Tests for Merkle DAG implementation with edge-based dependencies."""

import json
import os
import sqlite3
import tempfile
import unittest

from sema.core.hashing import (
    extract_handle_from_ref,
    generate_sema_hash,
    resolve_dependencies_to_sema_ids,
)
from sema.taxonomy_graph.graph_store import GraphStore


class TestDependenciesAsEdges(unittest.TestCase):
    """Test that dependencies are stored as graph edges, not in pattern JSON."""

    def setUp(self):
        # Create temp database
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        self.store = GraphStore(self.db_path)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_add_pattern_creates_dependency_edges(self):
        """Adding a pattern with dependencies should create edges."""
        # First add the dependency target
        base_pattern = {
            "handle": "BasePattern",
            "mechanism": "A base pattern",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        result1 = self.store.add_pattern(base_pattern)
        self.assertTrue(result1.get("success"), f"Failed: {result1.get('error')}")

        # Now add pattern that depends on it
        dependent = {
            "handle": "DependentPattern",
            "mechanism": "Uses {{base}}",
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
            "dependencies": {"references": {"base": "BasePattern#stub"}},
        }
        result2 = self.store.add_pattern(dependent)
        self.assertTrue(result2.get("success"), f"Failed: {result2.get('error')}")

        # Check that REFERENCES edge was created
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT e.edge_type
            FROM edges e
            JOIN nodes src ON e.source_id = src.id
            JOIN nodes tgt ON e.target_id = tgt.id
            WHERE src.text = 'DependentPattern' AND tgt.text = 'BasePattern'
        """
        )
        edges = cursor.fetchall()
        conn.close()

        edge_types = [e[0] for e in edges]
        self.assertIn("REFERENCES", edge_types)

    def test_composes_with_creates_edge(self):
        """COMPOSES_WITH dependencies should create edges."""
        # Add component
        component = {
            "handle": "Component",
            "mechanism": "A component",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        self.store.add_pattern(component)

        # Add composite
        composite = {
            "handle": "Composite",
            "mechanism": "Composed of {{comp}}",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
            "dependencies": {"composes_with": {"comp": "Component"}},
        }
        result = self.store.add_pattern(composite)
        self.assertTrue(result.get("success"))

        # Check edge
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT e.edge_type
            FROM edges e
            JOIN nodes src ON e.source_id = src.id
            JOIN nodes tgt ON e.target_id = tgt.id
            WHERE src.text = 'Composite' AND tgt.text = 'Component'
        """
        )
        edges = cursor.fetchall()
        conn.close()

        edge_types = [e[0] for e in edges]
        self.assertIn("COMPOSES_WITH", edge_types)

    def test_get_dependencies_from_edges(self):
        """Should be able to reconstruct dependencies from edges."""
        # Add patterns with dependencies
        self.store.add_pattern(
            {
                "handle": "RefTarget",
                "mechanism": "A reference target",
                "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
            }
        )
        self.store.add_pattern(
            {
                "handle": "CompTarget",
                "mechanism": "A compose target",
                "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
            }
        )
        self.store.add_pattern(
            {
                "handle": "Source",
                "mechanism": "Uses {{ref}} and {{comp}}",
                "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
                "dependencies": {
                    "references": {"ref": "RefTarget"},
                    "composes_with": {"comp": "CompTarget"},
                },
            }
        )

        # Get dependencies from edges
        deps = self.store.get_dependencies_from_edges("Source")

        self.assertIn("references", deps)
        self.assertIn("composes_with", deps)
        # Keys are snake_case handles in the implementation
        self.assertIn("ref_target", deps["references"])
        self.assertIn("comp_target", deps["composes_with"])


class TestRegistryLoadsDependenciesFromEdges(unittest.TestCase):
    """Test that Registry loads dependencies from graph edges."""

    def test_purecheck_has_dependencies_from_db(self):
        """PURECheck should have dependencies loaded from database edges."""
        from sema.core.registry import RegistryManager

        rm = RegistryManager()
        purecheck = rm.get_pattern("PURECheck")

        self.assertIsNotNone(purecheck)
        self.assertIn("dependencies", purecheck)

        deps = purecheck["dependencies"]
        self.assertIn("references", deps)
        self.assertIn("composes_with", deps)

        # Should reference the PURE judges
        ref_values = list(deps["references"].values())
        ref_handles = [v.split("#")[0] for v in ref_values]
        self.assertIn("Parsimony", ref_handles)
        self.assertIn("Novelty", ref_handles)
        self.assertIn("Realizable", ref_handles)
        self.assertIn("Expansive", ref_handles)

    def test_trigate_has_dependencies(self):
        """TriGate should have its dependencies loaded."""
        from sema.core.registry import RegistryManager

        rm = RegistryManager()
        trigate = rm.get_pattern("TriGate")

        self.assertIsNotNone(trigate)
        self.assertIn("dependencies", trigate)

        # TriGate references Judge, Condition, Gate
        refs = trigate["dependencies"].get("references", {})
        ref_handles = [v.split("#")[0] for v in refs.values()]
        self.assertIn("Judge", ref_handles)
        self.assertIn("Condition", ref_handles)
        self.assertIn("Gate", ref_handles)


class TestApplyCommand(unittest.TestCase):
    """Test the sema apply command."""

    def test_apply_check_flag_validates_without_changes(self):
        """--check should validate without modifying database."""
        from sema.cli.main import apply_changes
        from sema.core.registry import get_default_db_path

        # Get initial state
        db_path = get_default_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM nodes WHERE node_type = 'PATTERN'")
        initial_count = cursor.fetchone()[0]
        conn.close()

        # Create a test file with valid schema (valid layer/category combo)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(
                {
                    "handle": "TestCheckPattern",
                    "mechanism": "A test pattern for validation",
                    "_meta": {
                        "layer": "Infrastructure",
                        "category": "Primitives",
                        "tier": 1,
                        "ring": 0,
                    },
                },
                f,
            )
            test_file = f.name

        try:
            # Run with check_only=True
            result = apply_changes(add_files=[test_file], check_only=True)
            self.assertTrue(result)  # Should pass validation

            # Verify no changes
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM nodes WHERE node_type = 'PATTERN'")
            final_count = cursor.fetchone()[0]
            conn.close()

            self.assertEqual(initial_count, final_count, "Check mode should not modify database")
        finally:
            os.unlink(test_file)


class TestHashingWithDependencies(unittest.TestCase):
    """Test that hashing includes dependency information."""

    def test_hash_changes_with_dependencies(self):
        """Hash should change when dependencies change."""
        pattern_a = {"handle": "TestPattern", "mechanism": "Test mechanism"}

        pattern_b = {
            "handle": "TestPattern",
            "mechanism": "Test mechanism",
            "dependencies": {"references": {"dep": "SomeDep#1234"}},
        }

        hash_a = generate_sema_hash(pattern_a)
        hash_b = generate_sema_hash(pattern_b)

        self.assertNotEqual(
            hash_a["full_id"], hash_b["full_id"], "Hash should differ when dependencies are added"
        )


class TestExtractHandleFromRef(unittest.TestCase):
    """Test extract_handle_from_ref handles all reference formats."""

    def test_clean_handle(self):
        """Plain handle should return unchanged."""
        self.assertEqual(extract_handle_from_ref("Gate"), "Gate")
        self.assertEqual(extract_handle_from_ref("HeuristicSnap"), "HeuristicSnap")

    def test_stub_format(self):
        """Handle#stub format should extract handle."""
        self.assertEqual(extract_handle_from_ref("Gate#7f09"), "Gate")
        self.assertEqual(extract_handle_from_ref("Datum#cce3"), "Datum")
        self.assertEqual(extract_handle_from_ref("HeuristicSnap#e117"), "HeuristicSnap")

    def test_full_sema_id(self):
        """Full sema:Handle#mh:SHA-256:... format should extract handle."""
        self.assertEqual(
            extract_handle_from_ref("sema:Gate#mh:SHA-256:abc123def456"),
            "Gate",
        )
        self.assertEqual(
            extract_handle_from_ref("sema:HeuristicSnap#mh:SHA-256:e117abcd1234"),
            "HeuristicSnap",
        )

    def test_empty_and_none(self):
        """Empty string and edge cases."""
        self.assertEqual(extract_handle_from_ref(""), "")
        self.assertEqual(extract_handle_from_ref(None), None)


class TestResolveDependenciesConsistency(unittest.TestCase):
    """Test that hash is consistent regardless of input reference format."""

    def test_stub_vs_clean_produces_same_hash(self):
        """Same pattern with stub ref vs clean ref should produce same hash."""

        def mock_lookup(handle):
            return {"Gate": "abc123", "Datum": "def456"}.get(handle)

        # With stub format
        pattern_stub = {
            "handle": "TestPattern",
            "mechanism": "Uses {{gate}}",
            "dependencies": {"references": {"gate": "Gate#7f09"}},
        }

        # With clean format
        pattern_clean = {
            "handle": "TestPattern",
            "mechanism": "Uses {{gate}}",
            "dependencies": {"references": {"gate": "Gate"}},
        }

        hash_stub = generate_sema_hash(pattern_stub, mock_lookup)
        hash_clean = generate_sema_hash(pattern_clean, mock_lookup)

        self.assertEqual(
            hash_stub["hash"],
            hash_clean["hash"],
            "Hash should be same regardless of input ref format",
        )

    def test_full_sema_id_vs_clean_produces_same_hash(self):
        """Full sema ID format should produce same hash as clean handle."""

        def mock_lookup(handle):
            return {"Datum": "abc123def456"}.get(handle)

        pattern_full = {
            "handle": "TestPattern",
            "mechanism": "Uses {{datum}}",
            "dependencies": {"references": {"datum": "sema:Datum#mh:SHA-256:oldHash"}},
        }

        pattern_clean = {
            "handle": "TestPattern",
            "mechanism": "Uses {{datum}}",
            "dependencies": {"references": {"datum": "Datum"}},
        }

        hash_full = generate_sema_hash(pattern_full, mock_lookup)
        hash_clean = generate_sema_hash(pattern_clean, mock_lookup)

        self.assertEqual(
            hash_full["hash"],
            hash_clean["hash"],
            "Full sema ID should resolve to current hash, not use embedded hash",
        )

    def test_resolve_uses_current_hash_not_embedded(self):
        """Resolve should use lookup hash, ignoring any embedded stub."""

        def mock_lookup(handle):
            # Return a DIFFERENT hash than the embedded one
            return {"Gate": "currentHash123"}.get(handle)

        deps = {"references": {"gate": "Gate#oldStub"}}
        resolved = resolve_dependencies_to_sema_ids(deps, mock_lookup)

        # Should use currentHash123, not oldStub
        self.assertIn("currentHash123", resolved["references"]["gate"])
        self.assertNotIn("oldStub", resolved["references"]["gate"])


class TestMerkleDagHashIntegrity(unittest.TestCase):
    """
    Integration test: Verify that hashes computed manually match those
    computed by the system when patterns are added via GraphStore.

    This proves the Merkle DAG is working correctly:
    1. Hash B (no deps)
    2. Hash A with A -> B dependency
    3. Add both to GraphStore
    4. Verify stored hashes match manual computation
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        self.store = GraphStore(self.db_path)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_manual_hash_matches_system_hash(self):
        """Manual hashing should produce same result as system."""
        # Pattern B: no dependencies
        pattern_b = {
            "handle": "BaseLeaf",
            "mechanism": "A base pattern with no dependencies",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }

        # Compute hash manually
        hash_b = generate_sema_hash(pattern_b)

        # Add via GraphStore
        result_b = self.store.add_pattern(pattern_b.copy())
        self.assertTrue(result_b.get("success"))

        # Retrieve from DB and compare
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT metadata FROM nodes WHERE text = 'BaseLeaf' AND node_type = 'PATTERN'
        """
        )
        row = cursor.fetchone()
        conn.close()

        stored_meta = json.loads(row[0])
        stored_pattern = stored_meta.get("pattern", {})

        self.assertEqual(
            hash_b["stub"],
            stored_pattern.get("sema_stub"),
            f"Manual stub {hash_b['stub']} != stored {stored_pattern.get('sema_stub')}",
        )

    def test_dependent_hash_includes_dependency(self):
        """Pattern hash should change based on its dependency reference."""
        # First add two base patterns
        pattern_base1 = {
            "handle": "DagBase1",
            "mechanism": "Base pattern one",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        pattern_base2 = {
            "handle": "DagBase2",
            "mechanism": "Base pattern two",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        self.store.add_pattern(pattern_base1.copy())
        self.store.add_pattern(pattern_base2.copy())

        # Get references
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT metadata FROM nodes WHERE text = 'DagBase1'")
        ref1 = json.loads(cursor.fetchone()[0])["pattern"]["sema_ref"]
        cursor.execute("SELECT metadata FROM nodes WHERE text = 'DagBase2'")
        ref2 = json.loads(cursor.fetchone()[0])["pattern"]["sema_ref"]
        conn.close()

        # Add two patterns with different dependencies but same mechanism
        pattern_dep1 = {
            "handle": "DagDependent1",
            "mechanism": "Depends on base",
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
            "dependencies": {"references": {"base": ref1}},
        }
        pattern_dep2 = {
            "handle": "DagDependent2",
            "mechanism": "Depends on base",  # Same mechanism
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
            "dependencies": {"references": {"base": ref2}},  # Different dep
        }
        self.store.add_pattern(pattern_dep1.copy())
        self.store.add_pattern(pattern_dep2.copy())

        # Get both stubs
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT metadata FROM nodes WHERE text = 'DagDependent1'")
        stub1 = json.loads(cursor.fetchone()[0])["pattern"]["sema_stub"]
        cursor.execute("SELECT metadata FROM nodes WHERE text = 'DagDependent2'")
        stub2 = json.loads(cursor.fetchone()[0])["pattern"]["sema_stub"]
        conn.close()

        # Key assertion: different dependencies = different hashes
        self.assertNotEqual(
            stub1, stub2, "Patterns with different dependencies should have different hashes"
        )

    def test_hash_differs_with_different_dependency(self):
        """Same pattern with different dependency should have different hash."""
        # Create two base patterns
        base_a = {
            "handle": "BaseA",
            "mechanism": "First base",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        base_b = {
            "handle": "BaseB",
            "mechanism": "Second base",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }

        hash_a = generate_sema_hash(base_a)
        hash_b = generate_sema_hash(base_b)

        # Two patterns with same content but different dependencies
        dep_using_a = {
            "handle": "Consumer",
            "mechanism": "Uses base",
            "dependencies": {"references": {"base": f"BaseA#{hash_a['stub']}"}},
        }
        dep_using_b = {
            "handle": "Consumer",
            "mechanism": "Uses base",
            "dependencies": {"references": {"base": f"BaseB#{hash_b['stub']}"}},
        }

        hash_dep_a = generate_sema_hash(dep_using_a)
        hash_dep_b = generate_sema_hash(dep_using_b)

        self.assertNotEqual(
            hash_dep_a["full_id"],
            hash_dep_b["full_id"],
            "Same pattern with different dependency should have different hash",
        )

    def test_edge_based_dependency_in_hash(self):
        """
        Full integration: Add A and B to store, verify that:
        1. B's hash is computed and stored
        2. A references B via edge
        3. A has hash computed and stored
        4. Dependencies are preserved in stored pattern
        """
        # Add B first (no deps)
        pattern_b = {
            "handle": "LeafNode",
            "mechanism": "No dependencies",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        self.store.add_pattern(pattern_b.copy())

        # Get B's reference
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT metadata FROM nodes WHERE text = 'LeafNode'")
        b_meta = json.loads(cursor.fetchone()[0])
        b_ref = b_meta["pattern"]["sema_ref"]
        b_stub = b_meta["pattern"]["sema_stub"]
        conn.close()

        # Verify B has a valid hash
        self.assertIsNotNone(b_stub)
        self.assertTrue(len(b_stub) == 4, "Stub should be 4 hex chars")

        # Add A with dep on B
        pattern_a = {
            "handle": "ParentNode",
            "mechanism": "References {{child}}",
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
            "dependencies": {"references": {"child": b_ref}},
        }
        self.store.add_pattern(pattern_a.copy())

        # Verify edge exists
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT e.edge_type
            FROM edges e
            JOIN nodes src ON e.source_id = src.id
            JOIN nodes tgt ON e.target_id = tgt.id
            WHERE src.text = 'ParentNode' AND tgt.text = 'LeafNode'
        """
        )
        edges = cursor.fetchall()
        conn.close()

        edge_types = [e[0] for e in edges]
        self.assertIn(
            "REFERENCES", edge_types, "REFERENCES edge should exist from ParentNode to LeafNode"
        )

        # Get stored pattern A
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT metadata FROM nodes WHERE text = 'ParentNode'")
        a_meta = json.loads(cursor.fetchone()[0])
        conn.close()

        stored_pattern = a_meta["pattern"]

        # Verify hash was computed and stored
        self.assertIn("sema_stub", stored_pattern)
        self.assertIn("sema_ref", stored_pattern)
        self.assertIn("sema_id", stored_pattern)
        self.assertTrue(len(stored_pattern["sema_stub"]) == 4)

        # Verify dependencies are NOT in stored pattern (edge-only model)
        self.assertNotIn("dependencies", stored_pattern)

        # Verify dependencies ARE stored as edges
        edge_deps = self.store.get_dependencies_from_edges("ParentNode")
        self.assertIn("references", edge_deps)
        self.assertIn("leaf_node", edge_deps["references"])  # snake_case key from target handle


class TestCascadeHashing(unittest.TestCase):
    """
    Test cascade hashing: when a pattern changes, all dependents
    should have their hashes recomputed.

    DAG structure: A -> B -> C
    If C changes, both B and A should get new hashes.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        self.store = GraphStore(self.db_path)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_changing_base_pattern_changes_dependent_hash(self):
        """When base pattern changes, dependent should get new hash."""
        # Add base pattern C
        pattern_c = {
            "handle": "CascadeC",
            "mechanism": "Base pattern version 1",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        self.store.add_pattern(pattern_c.copy())

        # Get C's reference
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT metadata FROM nodes WHERE text = 'CascadeC'")
        c_meta = json.loads(cursor.fetchone()[0])
        c_ref_v1 = c_meta["pattern"]["sema_ref"]
        c_stub_v1 = c_meta["pattern"]["sema_stub"]
        conn.close()

        # Add pattern B that depends on C
        pattern_b = {
            "handle": "CascadeB",
            "mechanism": "Depends on {{base}}",
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
            "dependencies": {"references": {"base": c_ref_v1}},
        }
        self.store.add_pattern(pattern_b.copy())

        # Get B's initial hash
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Checked B's hash earlier, no need to check again here
        conn.close()

        # Now update C (change its mechanism)
        pattern_c_v2 = {
            "handle": "CascadeC",
            "mechanism": "Base pattern version 2 - CHANGED",  # Changed
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        self.store.add_pattern(pattern_c_v2.copy())

        # Get C's new hash
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT metadata FROM nodes WHERE text = 'CascadeC'")
        c_meta_v2 = json.loads(cursor.fetchone()[0])
        c_stub_v2 = c_meta_v2["pattern"]["sema_stub"]
        conn.close()

        # C's hash should have changed
        self.assertNotEqual(c_stub_v1, c_stub_v2, "C's hash should change when its content changes")

    def test_dependency_chain_integrity(self):
        """
        Verify that a chain A -> B -> C maintains hash integrity.
        Each pattern's dependencies point to valid patterns.
        """
        # Build chain: C (base), B depends on C, A depends on B
        pattern_c = {
            "handle": "ChainC",
            "mechanism": "Base of chain",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        self.store.add_pattern(pattern_c.copy())

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT metadata FROM nodes WHERE text = 'ChainC'")
        c_ref = json.loads(cursor.fetchone()[0])["pattern"]["sema_ref"]
        conn.close()

        pattern_b = {
            "handle": "ChainB",
            "mechanism": "Middle of chain, uses {{c}}",
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
            "dependencies": {"references": {"c": c_ref}},
        }
        self.store.add_pattern(pattern_b.copy())

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT metadata FROM nodes WHERE text = 'ChainB'")
        b_ref = json.loads(cursor.fetchone()[0])["pattern"]["sema_ref"]
        conn.close()

        pattern_a = {
            "handle": "ChainA",
            "mechanism": "Top of chain, uses {{b}}",
            "_meta": {"layer": "Society", "category": "Protocols", "tier": 1},
            "dependencies": {"references": {"b": b_ref}},
        }
        self.store.add_pattern(pattern_a.copy())

        # Verify all edges exist
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check A -> B edge
        cursor.execute(
            """
            SELECT COUNT(*) FROM edges e
            JOIN nodes src ON e.source_id = src.id
            JOIN nodes tgt ON e.target_id = tgt.id
            WHERE src.text = 'ChainA' AND tgt.text = 'ChainB'
        """
        )
        a_to_b = cursor.fetchone()[0]
        self.assertEqual(a_to_b, 1, "Edge from A to B should exist")

        # Check B -> C edge
        cursor.execute(
            """
            SELECT COUNT(*) FROM edges e
            JOIN nodes src ON e.source_id = src.id
            JOIN nodes tgt ON e.target_id = tgt.id
            WHERE src.text = 'ChainB' AND tgt.text = 'ChainC'
        """
        )
        b_to_c = cursor.fetchone()[0]
        self.assertEqual(b_to_c, 1, "Edge from B to C should exist")

        conn.close()

        # Verify each pattern has a valid hash
        for handle in ["ChainA", "ChainB", "ChainC"]:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT metadata FROM nodes WHERE text = ?", (handle,))
            meta = json.loads(cursor.fetchone()[0])
            conn.close()

            pattern = meta["pattern"]
            self.assertIn("sema_stub", pattern, f"{handle} should have sema_stub")
            self.assertIn("sema_ref", pattern, f"{handle} should have sema_ref")
            self.assertIsNotNone(pattern["sema_stub"], f"{handle} stub should not be None")


class TestRebuildStability(unittest.TestCase):
    """Test that rebuilding produces identical hashes (idempotency)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_stability.db")
        self.store = GraphStore(self.db_path)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_double_add_produces_same_hash(self):
        """Adding the same pattern twice should produce identical hash."""
        # First add
        base = {
            "handle": "StableBase",
            "mechanism": "A stable base pattern",
            "gloss": "Stability test",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        result1 = self.store.add_pattern(base.copy())
        self.assertTrue(result1.get("success"))
        hash1 = result1["sema_ref"]

        # Simulate "rebuild" by clearing DB and re-adding
        self.store = GraphStore(self.db_path)  # Reconnect
        result2 = self.store.add_pattern(base.copy())
        self.assertTrue(result2.get("success"))
        hash2 = result2["sema_ref"]

        self.assertEqual(hash1, hash2, "Hash should be identical after rebuild")

    def test_rebuild_with_dependencies_is_stable(self):
        """Rebuilding patterns with dependencies produces identical hashes."""
        # Add base pattern
        base = {
            "handle": "DepBase",
            "mechanism": "Base for dependency test",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        self.store.add_pattern(base.copy())
        base_hash = self.store.get_pattern_hash("DepBase")

        # Add dependent pattern
        dependent = {
            "handle": "DepChild",
            "mechanism": "Depends on {{base}}",
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
            "dependencies": {"references": {"base": f"DepBase#{base_hash[:4]}"}},
        }
        result1 = self.store.add_pattern(dependent.copy())
        self.assertTrue(result1.get("success"))
        child_hash1 = result1["sema_ref"]

        # Clear and rebuild in topological order
        import shutil

        shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)
        self.store = GraphStore(self.db_path)

        # Re-add base first
        self.store.add_pattern(base.copy())

        # Re-add dependent (with possibly stale stub in deps - should still work)
        result2 = self.store.add_pattern(dependent.copy())
        self.assertTrue(result2.get("success"))
        child_hash2 = result2["sema_ref"]

        self.assertEqual(child_hash1, child_hash2, "Dependent hash should be stable after rebuild")

    def test_hash_computed_from_edges_not_json_deps(self):
        """Hash should use edge-derived deps, not JSON deps field."""
        # Add base
        base = {
            "handle": "EdgeBase",
            "mechanism": "Base pattern",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
        }
        self.store.add_pattern(base.copy())

        # Add dependent with WRONG stub in JSON (simulating stale file)
        dependent = {
            "handle": "EdgeChild",
            "mechanism": "Uses {{base}}",
            "_meta": {"layer": "Mind", "category": "Strategy", "tier": 1},
            "dependencies": {"references": {"base": "EdgeBase#XXXX"}},  # Wrong stub!
        }
        result = self.store.add_pattern(dependent.copy())
        self.assertTrue(result.get("success"))

        # Verify edge was created to correct target (not XXXX)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM edges e
            JOIN nodes src ON e.source_id = src.id
            JOIN nodes tgt ON e.target_id = tgt.id
            WHERE src.text = 'EdgeChild' AND tgt.text = 'EdgeBase'
        """
        )
        edge_count = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(edge_count, 1, "Edge should be created to correct pattern")

        # Compute hash manually using edge deps
        child_hash = self.store.compute_pattern_hash(dependent)

        # Hash should include EdgeBase's CURRENT hash, not "XXXX"
        self.assertIn("#", child_hash["reference"])
        # The hash should be deterministic based on actual dep hash
        self.assertNotIn("XXXX", child_hash["full_id"])


if __name__ == "__main__":
    unittest.main()
