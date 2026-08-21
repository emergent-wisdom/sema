"""Tests for the atomic apply command."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from sema.cli.main import _validate_pattern_file, apply_changes
from sema.core.hashing import generate_sema_hash
from sema.taxonomy_graph.graph_store import EdgeType, GraphStore, NodeType


def make_sema_id(handle: str, suffix: str = "a") -> str:
    """Helper to create a valid full sema ID for testing (Rule 2.4)."""
    return f"sema:{handle}#mh:SHA-256:{suffix * 64}"


class TestApplyCommand(unittest.TestCase):
    """Test the atomic apply command with a temporary database."""

    def setUp(self):
        """Create a temporary database for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_taxonomy.db")
        self.store = GraphStore(self.db_path)

        # Create temp directory for pattern files
        self.patterns_dir = os.path.join(self.temp_dir, "patterns")
        os.makedirs(self.patterns_dir)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_pattern_file(
        self,
        handle: str,
        mechanism: str = "Test mechanism",
        gloss: str = "Test gloss",
        deps: dict = None,
    ) -> Path:
        """Helper to create a valid pattern file."""
        pattern = {
            "handle": handle,
            "mechanism": mechanism,
            "gloss": gloss,
            "_meta": {
                "path": ["Infrastructure", "Primitives"],  # Valid category for Infrastructure
                "ring": 0,
                "tier": 1,
            },
        }
        if deps:
            pattern["dependencies"] = deps

        file_path = Path(self.patterns_dir) / f"{handle}.json"
        with open(file_path, "w") as f:
            json.dump(pattern, f)
        return file_path

    def _add_pattern_to_db(self, handle: str, mechanism: str = "Test mechanism"):
        """Helper to add a pattern directly to the test DB."""
        pattern = {
            "handle": handle,
            "mechanism": mechanism,
            "gloss": "Test gloss",
            "_meta": {"path": ["Infrastructure", "Primitives"]},
            "sema_layer": "Infrastructure",
            "sema_category": "Primitives",
        }
        self.store.add_pattern(pattern)

    def _pattern_exists(self, handle: str) -> bool:
        """Check if a pattern exists in the DB (fresh read)."""
        # Create fresh store to read current DB state
        fresh_store = GraphStore(self.db_path)
        for _, data in fresh_store.get_nodes_by_type(NodeType.PATTERN):
            if data["text"] == handle:
                return True
        return False

    @patch("sema.cli.main.get_default_db_path")
    def test_add_single_pattern(self, mock_db_path):
        """Test adding a single pattern."""
        mock_db_path.return_value = self.db_path

        file_path = self._create_pattern_file("TestPattern")

        result = apply_changes(add_files=[str(file_path)])

        self.assertTrue(result)
        self.assertTrue(self._pattern_exists("TestPattern"))

    @patch("sema.cli.main.get_default_db_path")
    def test_remove_single_pattern(self, mock_db_path):
        """Test removing a single pattern."""
        mock_db_path.return_value = self.db_path

        # First add a pattern
        self._add_pattern_to_db("PatternToRemove")
        self.assertTrue(self._pattern_exists("PatternToRemove"))

        # Now remove it
        result = apply_changes(remove_handles=["PatternToRemove"])

        self.assertTrue(result)
        self.assertFalse(self._pattern_exists("PatternToRemove"))

    @patch("sema.cli.main.get_default_db_path")
    def test_remove_nonexistent_fails(self, mock_db_path):
        """Test that removing a non-existent pattern fails validation."""
        mock_db_path.return_value = self.db_path

        result = apply_changes(remove_handles=["NonExistent"])

        self.assertFalse(result)

    @patch("sema.cli.main.get_default_db_path")
    def test_add_invalid_json_fails(self, mock_db_path):
        """Test that adding invalid JSON fails validation."""
        mock_db_path.return_value = self.db_path

        invalid_file = Path(self.patterns_dir) / "invalid.json"
        with open(invalid_file, "w") as f:
            f.write("not valid json {{{")

        result = apply_changes(add_files=[str(invalid_file)])

        self.assertFalse(result)

    @patch("sema.cli.main.get_default_db_path")
    def test_add_duplicate_json_member_fails(self, mock_db_path):
        """Local apply uses the same strict JSON boundary as remote libraries."""
        mock_db_path.return_value = self.db_path

        invalid_file = Path(self.patterns_dir) / "duplicate.json"
        invalid_file.write_text(
            '{"handle":"First","handle":"Second","mechanism":"m",'
            '"_meta":{"path":["Infrastructure","Primitives"],"ring":0,"tier":1}}'
        )

        self.assertFalse(apply_changes(add_files=[str(invalid_file)]))
        self.assertFalse(self._pattern_exists("First"))
        self.assertFalse(self._pattern_exists("Second"))

    @patch("sema.cli.main.get_default_db_path")
    def test_add_non_string_handles_fails_cleanly(self, mock_db_path):
        mock_db_path.return_value = self.db_path

        for index, bad_handle in enumerate((1, None, ["Pattern"])):
            with self.subTest(handle=bad_handle):
                invalid_file = Path(self.patterns_dir) / f"bad-handle-{index}.json"
                invalid_file.write_text(
                    json.dumps(
                        {
                            "handle": bad_handle,
                            "mechanism": "A mechanism.",
                            "_meta": {
                                "path": ["Infrastructure", "Primitives"],
                                "ring": 0,
                                "tier": 1,
                            },
                        }
                    )
                )
                self.assertFalse(apply_changes(add_files=[str(invalid_file)]))

        self.assertEqual(list(GraphStore(self.db_path).get_nodes_by_type(NodeType.PATTERN)), [])

    @patch("sema.cli.main.get_default_db_path")
    def test_add_missing_file_fails(self, mock_db_path):
        """Test that adding a non-existent file fails validation."""
        mock_db_path.return_value = self.db_path

        result = apply_changes(add_files=["/nonexistent/path/file.json"])

        self.assertFalse(result)

    @patch("sema.cli.main.get_default_db_path")
    def test_add_missing_required_fields_fails(self, mock_db_path):
        """Test that adding a pattern without required fields fails."""
        mock_db_path.return_value = self.db_path

        # Pattern missing 'mechanism'
        invalid_pattern = Path(self.patterns_dir) / "incomplete.json"
        with open(invalid_pattern, "w") as f:
            json.dump({"handle": "Incomplete", "gloss": "No mechanism"}, f)

        result = apply_changes(add_files=[str(invalid_pattern)])

        self.assertFalse(result)

    @patch("sema.cli.main.get_default_db_path")
    def test_atomic_remove_and_add(self, mock_db_path):
        """Test atomic remove + add (rename scenario)."""
        mock_db_path.return_value = self.db_path

        # Add old pattern
        self._add_pattern_to_db("OldName")
        self.assertTrue(self._pattern_exists("OldName"))

        # Create new pattern file
        new_file = self._create_pattern_file("NewName")

        # Atomic remove old, add new
        result = apply_changes(remove_handles=["OldName"], add_files=[str(new_file)])

        self.assertTrue(result)
        self.assertFalse(self._pattern_exists("OldName"))
        self.assertTrue(self._pattern_exists("NewName"))

    @patch("sema.cli.main.get_default_db_path")
    def test_add_directory(self, mock_db_path):
        """Test adding all patterns from a directory."""
        mock_db_path.return_value = self.db_path

        # Create multiple pattern files
        self._create_pattern_file("Pattern1")
        self._create_pattern_file("Pattern2")
        self._create_pattern_file("Pattern3")

        result = apply_changes(add_files=[self.patterns_dir])

        self.assertTrue(result)
        self.assertTrue(self._pattern_exists("Pattern1"))
        self.assertTrue(self._pattern_exists("Pattern2"))
        self.assertTrue(self._pattern_exists("Pattern3"))

    @patch("sema.cli.main.get_default_db_path")
    def test_nothing_to_do_fails(self, mock_db_path):
        """Test that calling apply with no arguments fails."""
        mock_db_path.return_value = self.db_path

        result = apply_changes()

        self.assertFalse(result)

    @patch("sema.cli.main.get_default_db_path")
    def test_validation_before_execution(self, mock_db_path):
        """Test that all validation happens before any changes."""
        mock_db_path.return_value = self.db_path

        # Add a pattern we'll try to remove
        self._add_pattern_to_db("ValidRemove")

        # Create one valid file and one invalid
        valid_file = self._create_pattern_file("ValidAdd")
        invalid_file = Path(self.patterns_dir) / "invalid.json"
        with open(invalid_file, "w") as f:
            f.write("not json")

        # This should fail validation and NOT remove ValidRemove
        result = apply_changes(
            remove_handles=["ValidRemove"], add_files=[str(valid_file), str(invalid_file)]
        )

        self.assertFalse(result)
        # ValidRemove should still exist because validation failed
        self.assertTrue(self._pattern_exists("ValidRemove"))

    @patch("sema.cli.main.get_default_db_path")
    def test_topological_sort_order(self, mock_db_path):
        """Test that patterns are added in dependency order."""
        mock_db_path.return_value = self.db_path

        # Create pattern B that depends on A
        file_a = self._create_pattern_file("PatternA", mechanism="Base pattern")
        file_b = self._create_pattern_file(
            "PatternB",
            mechanism="Depends on {{pattern_a}}",
            deps={"references": {"pattern_a": make_sema_id("PatternA")}},
        )

        # Add B first in the list - should still work due to topo sort
        result = apply_changes(add_files=[str(file_b), str(file_a)])

        self.assertTrue(result)
        self.assertTrue(self._pattern_exists("PatternA"))
        self.assertTrue(self._pattern_exists("PatternB"))

    def test_updating_pattern_replaces_schema_edges(self):
        """Superseded contracts must not remain linked in the graph."""
        original = {
            "handle": "ChangingContract",
            "mechanism": "A contract that changes",
            "gloss": "Changing contract",
            "invariants": ["The old invariant"],
            "preconditions": ["The old precondition"],
            "postconditions": ["The old postcondition"],
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        updated = {
            **original,
            "invariants": ["The replacement invariant"],
            "postconditions": ["The replacement postcondition"],
        }
        updated.pop("preconditions")

        # Exact node creation keeps this test focused on edge lifecycle rather
        # than embedding similarity.
        with (
            patch.object(self.store, "find_similar_node", return_value=None),
            patch.object(
                self.store.embedding_service,
                "get_embedding",
                return_value=np.zeros(1, dtype=np.float32),
            ),
        ):
            self.store.add_pattern(original)
            self.store.add_pattern(updated)

        fresh = GraphStore(self.db_path)
        pattern_id = fresh._find_pattern_id("ChangingContract")

        def linked_texts(edge_type):
            return {
                fresh.graph.nodes[target_id]["text"]
                for target_id in fresh.graph.successors(pattern_id)
                if fresh.has_edge_of_type(pattern_id, target_id, edge_type)
            }

        self.assertEqual(linked_texts(EdgeType.HAS_INVARIANT), {"The replacement invariant"})
        self.assertEqual(linked_texts(EdgeType.HAS_PRECONDITION), set())
        self.assertEqual(
            linked_texts(EdgeType.HAS_POSTCONDITION), {"The replacement postcondition"}
        )

        schema_texts = {
            data["text"]
            for _, data in fresh.graph.nodes(data=True)
            if data.get("node_type")
            in {NodeType.INVARIANT, NodeType.PRECONDITION, NodeType.POSTCONDITION}
        }
        self.assertNotIn("The old invariant", schema_texts)
        self.assertNotIn("The old precondition", schema_texts)
        self.assertNotIn("The old postcondition", schema_texts)

    def test_updating_pattern_reconciles_signature_and_related_edges(self):
        """Signature and related replacements remove only their stale edge types."""
        original = {
            "handle": "ChangingLinks",
            "mechanism": "Uses {{output}} while exposing an interface",
            "gloss": "Changing links",
            "signature": ["Input(Output)"],
            "dependencies": {"references": {"output": "Output#test"}},
            "_meta": {
                "path": ["Infrastructure", "Primitives"],
                "ring": 0,
                "tier": 1,
                "related": ["Output"],
            },
        }
        updated = {
            **original,
            "signature": ["Input(State)"],
            "_meta": {**original["_meta"], "related": ["State"]},
        }

        with patch.object(
            self.store.embedding_service,
            "get_embedding",
            return_value=np.zeros(1, dtype=np.float32),
        ):
            for handle in ["Input", "Output", "State"]:
                self._add_pattern_to_db(handle)
            self.store.add_pattern(original)
            self.store.add_pattern(updated)

        source_id = self.store._find_pattern_id("ChangingLinks")
        input_id = self.store._find_pattern_id("Input")
        output_id = self.store._find_pattern_id("Output")
        state_id = self.store._find_pattern_id("State")

        self.assertTrue(self.store.has_edge_of_type(source_id, input_id, EdgeType.HAS_SIGNATURE))
        self.assertFalse(self.store.has_edge_of_type(source_id, output_id, EdgeType.HAS_SIGNATURE))
        self.assertTrue(self.store.has_edge_of_type(source_id, state_id, EdgeType.HAS_SIGNATURE))
        self.assertFalse(self.store.has_edge_of_type(source_id, output_id, EdgeType.RELATED_TO))
        self.assertTrue(self.store.has_edge_of_type(source_id, state_id, EdgeType.RELATED_TO))
        self.assertTrue(self.store.has_edge_of_type(source_id, output_id, EdgeType.REFERENCES))

    def test_removing_signature_and_related_edges_persists_after_reopen(self):
        """Empty declarations prune their edges while parallel dependencies survive."""
        original = {
            "handle": "RemovingLinks",
            "mechanism": "Uses {{output}} while exposing an interface",
            "gloss": "Removing links",
            "signature": ["Input(Output)"],
            "dependencies": {"references": {"output": "Output#test"}},
            "_meta": {
                "path": ["Infrastructure", "Primitives"],
                "ring": 0,
                "tier": 1,
                "related": ["Output"],
            },
        }
        updated = {**original, "_meta": {**original["_meta"]}}
        updated.pop("signature")
        updated["_meta"].pop("related")

        with patch.object(
            self.store.embedding_service,
            "get_embedding",
            return_value=np.zeros(1, dtype=np.float32),
        ):
            for handle in ["Input", "Output"]:
                self._add_pattern_to_db(handle)
            self.store.add_pattern(original)
            self.store.add_pattern(updated)
            self.store.add_pattern(updated)

        fresh = GraphStore(self.db_path)
        source_id = fresh._find_pattern_id("RemovingLinks")
        input_id = fresh._find_pattern_id("Input")
        output_id = fresh._find_pattern_id("Output")

        self.assertFalse(fresh.has_edge_of_type(source_id, input_id, EdgeType.HAS_SIGNATURE))
        self.assertFalse(fresh.has_edge_of_type(source_id, output_id, EdgeType.HAS_SIGNATURE))
        self.assertFalse(fresh.has_edge_of_type(source_id, output_id, EdgeType.RELATED_TO))
        self.assertTrue(fresh.has_edge_of_type(source_id, output_id, EdgeType.REFERENCES))
        reference_edges = [
            edge
            for edge in fresh._edges_between(source_id, output_id)
            if edge.get("edge_type") == EdgeType.REFERENCES
        ]
        self.assertEqual(len(reference_edges), 1)


class TestValidatePatternFile(unittest.TestCase):
    """Test the pattern file validation helper."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_valid_pattern(self):
        """Test validation of a valid pattern file."""
        file_path = Path(self.temp_dir) / "valid.json"
        pattern = {
            "handle": "Valid",
            "mechanism": "Test",
            "gloss": "Test",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        with open(file_path, "w") as f:
            json.dump(pattern, f)

        result = _validate_pattern_file(file_path)

        self.assertIsNone(result["error"])
        self.assertIsNotNone(result["data"])

    def test_invalid_json(self):
        """Test validation catches invalid JSON."""
        file_path = Path(self.temp_dir) / "invalid.json"
        with open(file_path, "w") as f:
            f.write("{not valid}")

        result = _validate_pattern_file(file_path)

        self.assertIsNotNone(result["error"])
        self.assertIn("Invalid JSON", result["error"])

    def test_missing_handle(self):
        """Test validation catches missing handle."""
        file_path = Path(self.temp_dir) / "no_handle.json"
        with open(file_path, "w") as f:
            json.dump({"mechanism": "test"}, f)

        result = _validate_pattern_file(file_path)

        self.assertIsNotNone(result["error"])


class TestDanglingReferences(unittest.TestCase):
    """Test that removing a pattern fails if other patterns depend on it."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_taxonomy.db")
        self.store = GraphStore(self.db_path)
        self.patterns_dir = os.path.join(self.temp_dir, "patterns")
        os.makedirs(self.patterns_dir)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _add_pattern_to_db(self, handle: str, deps: dict = None):
        """Add pattern to DB with optional dependencies."""
        pattern = {
            "handle": handle,
            "mechanism": f"Mechanism for {handle}",
            "gloss": f"Gloss for {handle}",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
            "sema_layer": "Infrastructure",
            "sema_category": "Primitives",
        }
        if deps:
            pattern["dependencies"] = deps
        self.store.add_pattern(pattern)

    def _create_pattern_file(self, handle: str, deps: dict = None) -> Path:
        """Create a pattern file."""
        pattern = {
            "handle": handle,
            "mechanism": f"Mechanism for {handle}",
            "gloss": f"Gloss for {handle}",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        if deps:
            pattern["dependencies"] = deps
        file_path = Path(self.patterns_dir) / f"{handle}.json"
        with open(file_path, "w") as f:
            json.dump(pattern, f)
        return file_path

    @patch("sema.cli.main.get_default_db_path")
    def test_remove_with_dependents_fails(self, mock_db_path):
        """Test that removing a pattern fails if others depend on it."""
        mock_db_path.return_value = self.db_path

        # Add Base and Dependent (which depends on Base)
        self._add_pattern_to_db("Base")
        self._add_pattern_to_db("Dependent", deps={"references": {"Base": "Base#test"}})

        # Try to remove just Base - should fail
        result = apply_changes(remove_handles=["Base"])

        self.assertFalse(result)

    @patch("sema.cli.main.get_default_db_path")
    def test_remove_with_dependents_and_dependents_succeeds(self, mock_db_path):
        """Test that removing both pattern and its dependents succeeds."""
        mock_db_path.return_value = self.db_path

        # Add Base and Dependent
        self._add_pattern_to_db("Base")
        self._add_pattern_to_db("Dependent", deps={"references": {"Base": "Base#test"}})

        # Remove both - should succeed
        result = apply_changes(remove_handles=["Base", "Dependent"])

        self.assertTrue(result)

    @patch("sema.cli.main.get_default_db_path")
    def test_remove_with_updated_dependent_succeeds(self, mock_db_path):
        """Test that removing pattern succeeds if dependent is re-added without the dep."""
        mock_db_path.return_value = self.db_path

        # Add Base and Dependent
        self._add_pattern_to_db("Base")
        self._add_pattern_to_db("Dependent", deps={"references": {"Base": "Base#test"}})

        # Create updated Dependent without the dependency
        updated_file = self._create_pattern_file("Dependent")  # No deps

        # Remove Base, add updated Dependent - should succeed
        result = apply_changes(remove_handles=["Base"], add_files=[str(updated_file)])

        self.assertTrue(result)

    @patch("sema.cli.main.get_default_db_path")
    def test_remove_unused_pattern_succeeds(self, mock_db_path):
        """Test that removing a pattern with no dependents succeeds."""
        mock_db_path.return_value = self.db_path

        # Add standalone pattern
        self._add_pattern_to_db("Standalone")

        result = apply_changes(remove_handles=["Standalone"])

        self.assertTrue(result)


class TestCycleDetection(unittest.TestCase):
    """Test cycle detection in pattern dependencies."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_taxonomy.db")
        self.patterns_dir = os.path.join(self.temp_dir, "patterns")
        os.makedirs(self.patterns_dir)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_pattern(self, handle: str, deps: dict = None) -> Path:
        """Create a pattern file with optional dependencies."""
        pattern = {
            "handle": handle,
            "mechanism": f"Mechanism for {handle}",
            "gloss": f"Gloss for {handle}",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        if deps:
            pattern["dependencies"] = deps
        file_path = Path(self.patterns_dir) / f"{handle}.json"
        with open(file_path, "w") as f:
            json.dump(pattern, f)
        return file_path

    @patch("sema.cli.main.get_default_db_path")
    def test_direct_cycle_fails(self, mock_db_path):
        """Test that A -> B -> A cycle is detected."""
        mock_db_path.return_value = self.db_path

        # A depends on B, B depends on A
        self._create_pattern("CycleA", deps={"references": {"cycle_b": make_sema_id("CycleB")}})
        self._create_pattern("CycleB", deps={"references": {"cycle_a": make_sema_id("CycleA")}})

        result = apply_changes(add_files=[self.patterns_dir])

        # Should fail due to cycle
        self.assertFalse(result)

    @patch("sema.cli.main.get_default_db_path")
    def test_self_reference_fails(self, mock_db_path):
        """Test that A -> A self-reference is detected."""
        mock_db_path.return_value = self.db_path

        self._create_pattern("SelfRef", deps={"references": {"self_ref": make_sema_id("SelfRef")}})

        result = apply_changes(add_files=[self.patterns_dir])

        # Should fail due to self-reference
        self.assertFalse(result)

    @patch("sema.cli.main.get_default_db_path")
    def test_transitive_cycle_fails(self, mock_db_path):
        """Test that A -> B -> C -> A cycle is detected."""
        mock_db_path.return_value = self.db_path

        self._create_pattern("TransA", deps={"references": {"trans_b": make_sema_id("TransB")}})
        self._create_pattern("TransB", deps={"references": {"trans_c": make_sema_id("TransC")}})
        self._create_pattern("TransC", deps={"references": {"trans_a": make_sema_id("TransA")}})

        result = apply_changes(add_files=[self.patterns_dir])

        # Should fail due to cycle
        self.assertFalse(result)

    @patch("sema.cli.main.get_default_db_path")
    def test_valid_dag_succeeds(self, mock_db_path):
        """Test that a valid DAG (no cycles) succeeds."""
        mock_db_path.return_value = self.db_path

        # A -> B -> C (no cycle), with deps used in mechanism
        self._create_pattern("DagC")  # No deps
        self._create_pattern("DagB", deps={"references": {"dag_c": make_sema_id("DagC")}})
        self._create_pattern("DagA", deps={"references": {"dag_b": make_sema_id("DagB")}})

        # Fix mechanism to use the deps (validator requires it)
        for name, dep_key in [("DagB", "dag_c"), ("DagA", "dag_b")]:
            file_path = Path(self.patterns_dir) / f"{name}.json"
            with open(file_path) as f:
                data = json.load(f)
            data["mechanism"] = f"Uses {{{{{dep_key}}}}}"
            with open(file_path, "w") as f:
                json.dump(data, f)

        result = apply_changes(add_files=[self.patterns_dir])

        self.assertTrue(result)


class TestLayerDirectionInApply(unittest.TestCase):
    """Rule 7.6 enforcement through the apply pipeline.

    Verifies that apply_changes rejects additions that violate layer direction
    on hard dependency buckets (accepts, composes_with), and accepts upward
    linkage via yields/references.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_taxonomy.db")
        self.patterns_dir = os.path.join(self.temp_dir, "patterns")
        os.makedirs(self.patterns_dir)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_pattern(
        self,
        handle: str,
        layer: str,
        category: str,
        deps: dict = None,
        mechanism: str = None,
    ) -> Path:
        pattern = {
            "handle": handle,
            "mechanism": mechanism or f"Mechanism for {handle}",
            "gloss": f"Gloss for {handle}",
            "_meta": {"path": [layer, category], "ring": 1, "tier": 1},
        }
        if deps:
            pattern["dependencies"] = deps
        file_path = Path(self.patterns_dir) / f"{handle}.json"
        with open(file_path, "w") as f:
            json.dump(pattern, f)
        return file_path

    @patch("sema.cli.main.get_default_db_path")
    def test_violation_in_composes_with_is_rejected(self, mock_db_path):
        """7.6: apply rejects Infrastructure composes_with Society."""
        mock_db_path.return_value = self.db_path

        self._create_pattern("SocietyDep", layer="Society", category="Protocols")
        self._create_pattern(
            "InfraPattern",
            layer="Infrastructure",
            category="Primitives",
            mechanism="Uses {{society_dep}}",
            deps={"composes_with": {"society_dep": make_sema_id("SocietyDep")}},
        )

        result = apply_changes(add_files=[self.patterns_dir])
        self.assertFalse(result)
        self.assertFalse(self._pattern_in_db("InfraPattern"))

    @patch("sema.cli.main.get_default_db_path")
    def test_violation_in_accepts_is_rejected(self, mock_db_path):
        """7.6: apply rejects Physics accepting a Society input."""
        mock_db_path.return_value = self.db_path

        self._create_pattern("SocietyInput", layer="Society", category="Protocols")
        self._create_pattern(
            "PhysicsPattern",
            layer="Physics",
            category="Primitives",
            mechanism="Reads {{society_input}}",
            deps={"accepts": {"society_input": make_sema_id("SocietyInput")}},
        )

        result = apply_changes(add_files=[self.patterns_dir])
        self.assertFalse(result)

    @patch("sema.cli.main.get_default_db_path")
    def test_upward_yields_is_accepted(self, mock_db_path):
        """7.6: apply accepts Mind yielding a Society artifact (emergence)."""
        mock_db_path.return_value = self.db_path

        self._create_pattern("SocietyArtifact", layer="Society", category="Economics")
        self._create_pattern(
            "MindProducer",
            layer="Mind",
            category="Reasoning",
            mechanism="Produces {{society_artifact}}",
            deps={"yields": {"society_artifact": make_sema_id("SocietyArtifact")}},
        )

        result = apply_changes(add_files=[self.patterns_dir])
        self.assertTrue(result)
        self.assertTrue(self._pattern_in_db("MindProducer"))

    @patch("sema.cli.main.get_default_db_path")
    def test_upward_references_is_accepted(self, mock_db_path):
        """7.6: apply accepts Infrastructure referencing a Society pattern."""
        mock_db_path.return_value = self.db_path

        self._create_pattern("SocietyConcept", layer="Society", category="Governance")
        self._create_pattern(
            "InfraCitation",
            layer="Infrastructure",
            category="Primitives",
            mechanism="Cites {{society_concept}}",
            deps={"references": {"society_concept": make_sema_id("SocietyConcept")}},
        )

        result = apply_changes(add_files=[self.patterns_dir])
        self.assertTrue(result)
        self.assertTrue(self._pattern_in_db("InfraCitation"))

    def _pattern_in_db(self, handle: str) -> bool:
        fresh = GraphStore(self.db_path)
        for _, data in fresh.get_nodes_by_type(NodeType.PATTERN):
            if data["text"] == handle:
                return True
        return False


class TestFullRoundTrip(unittest.TestCase):
    """Test full export → remove all → add all → verify identical state."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_taxonomy.db")
        self.store = GraphStore(self.db_path)
        self.patterns_dir = os.path.join(self.temp_dir, "patterns")
        os.makedirs(self.patterns_dir)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _add_pattern_to_db(
        self,
        handle: str,
        deps: dict = None,
        layer: str = "Infrastructure",
        category: str = "Primitives",
    ):
        """Add pattern directly to DB with full metadata."""
        from sema.core.hashing import generate_sema_hash

        # Build mechanism text - must reference ALL dependencies
        mechanism = f"Mechanism for {handle}"
        if deps:
            for dep_type in ["references", "composes_with", "accepts", "yields"]:
                for dep_key in deps.get(dep_type, {}).keys():
                    mechanism += f". Uses {{{{{dep_key}}}}}"

        pattern = {
            "handle": handle,
            "mechanism": mechanism,
            "gloss": f"Gloss for {handle}",
            "_meta": {"path": [layer, category], "ring": 0, "tier": 1},
        }
        if deps:
            pattern["dependencies"] = deps

        # Compute hash
        computed = generate_sema_hash(pattern)
        pattern["sema_ref"] = computed["reference"]
        pattern["sema_id"] = computed["full_id"]
        pattern["sema_stub"] = computed["stub"]
        pattern["sema_layer"] = layer
        pattern["sema_category"] = category

        self.store.add_pattern(pattern)
        return pattern

    def _export_all_patterns(self) -> dict:
        """Export all patterns from DB, return dict {handle: pattern_data}."""
        fresh_store = GraphStore(self.db_path)
        patterns = {}
        for _, data in fresh_store.get_nodes_by_type(NodeType.PATTERN):
            handle = data["text"]
            # Use _get_pattern_content with include_deps=True to get complete pattern
            pattern = fresh_store._get_pattern_content(handle, include_deps=True)
            if pattern:
                patterns[handle] = pattern
        return patterns

    def _write_pattern_file(self, pattern: dict) -> Path:
        """Write a pattern dict to a file for re-import."""
        handle = pattern["handle"]
        file_path = Path(self.patterns_dir) / f"{handle}.json"
        with open(file_path, "w") as f:
            json.dump(pattern, f)
        return file_path

    @patch("sema.cli.main.get_default_db_path")
    def test_full_round_trip_with_dependencies(self, mock_db_path):
        """
        Test the full round-trip:
        1. Add patterns with dependencies to DB
        2. Export all patterns
        3. Remove ALL patterns
        4. Add ALL patterns back from exported files
        5. Verify DB state is identical
        """
        mock_db_path.return_value = self.db_path

        # ============ STEP 1: Create patterns with dependencies ============
        # Create a complex dependency graph:
        #   Gate (base)
        #   TriGate -> Gate (references)
        #   Taper -> Gate, TriGate (composes_with)
        #   Buffer (standalone)
        #   Compress -> Buffer (references)

        p_gate = self._add_pattern_to_db("Gate")
        p_trigate = self._add_pattern_to_db(
            "TriGate", deps={"references": {"gate": f"Gate#{p_gate['sema_stub']}"}}
        )
        self._add_pattern_to_db(
            "Taper",
            deps={
                "composes_with": {
                    "gate": f"Gate#{p_gate['sema_stub']}",
                    "tri_gate": f"TriGate#{p_trigate['sema_stub']}",
                }
            },
        )
        p_buffer = self._add_pattern_to_db("Buffer", layer="Mind", category="Strategy")
        self._add_pattern_to_db(
            "Compress",
            deps={"references": {"buffer": f"Buffer#{p_buffer['sema_stub']}"}},
            layer="Mind",
            category="Strategy",
        )

        # ============ STEP 2: Export all patterns ============
        original_patterns = self._export_all_patterns()
        self.assertEqual(len(original_patterns), 5)

        # Store original state for comparison
        original_hashes = {h: p.get("sema_id") for h, p in original_patterns.items()}
        original_layers = {h: p.get("sema_layer") for h, p in original_patterns.items()}
        original_categories = {h: p.get("sema_category") for h, p in original_patterns.items()}

        # ============ STEP 3: Remove ALL patterns ============
        # Must remove in reverse dependency order (or all at once)
        all_handles = list(original_patterns.keys())
        result = apply_changes(remove_handles=all_handles)
        self.assertTrue(result, "Failed to remove all patterns")

        # Verify DB is empty
        fresh_store = GraphStore(self.db_path)
        remaining = list(fresh_store.get_nodes_by_type(NodeType.PATTERN))
        self.assertEqual(len(remaining), 0, "DB should be empty after removing all")

        # ============ STEP 4: Write exported patterns to files and re-add ============

        # Write each pattern to a file
        pattern_files = []
        for _, pattern in original_patterns.items():
            # Remove sema_* fields - they'll be recomputed
            clean_pattern = {k: v for k, v in pattern.items() if not k.startswith("sema_")}
            file_path = self._write_pattern_file(clean_pattern)
            pattern_files.append(str(file_path))

        # Add all patterns (topological sort should handle order)
        result = apply_changes(add_files=[self.patterns_dir])
        self.assertTrue(result, "Failed to add all patterns back")

        # ============ STEP 5: Verify identical state ============
        restored_patterns = self._export_all_patterns()
        self.assertEqual(len(restored_patterns), 5, "Should have 5 patterns after restore")

        # Verify each pattern
        for handle in original_hashes:
            self.assertIn(handle, restored_patterns, f"Missing pattern: {handle}")

            # Check hash is identical (content-addressable!)
            self.assertEqual(
                restored_patterns[handle].get("sema_id"),
                original_hashes[handle],
                f"Hash mismatch for {handle}",
            )

            # Check layer is identical
            self.assertEqual(
                restored_patterns[handle].get("sema_layer"),
                original_layers[handle],
                f"Layer mismatch for {handle}",
            )

            # Check category is identical
            self.assertEqual(
                restored_patterns[handle].get("sema_category"),
                original_categories[handle],
                f"Category mismatch for {handle}",
            )

    @patch("sema.cli.main.get_default_db_path")
    def test_round_trip_preserves_all_metadata(self, mock_db_path):
        """Test that ALL metadata fields survive the round-trip."""
        mock_db_path.return_value = self.db_path

        # Create dependencies required for signature
        deps = {}
        for handle in ["Input", "Output", "State", "Change"]:
            p = self._add_pattern_to_db(handle)
            deps[handle.lower()] = f"{handle}#{p['sema_stub']}"

        # Create a pattern with all optional fields
        full_pattern = {
            "handle": "FullPattern",
            "gloss": "A complete pattern with all fields",
            "mechanism": (
                "Does something complex with {{input}}, {{output}}, {{state}}, and {{change}}"
            ),
            "signature": ["Input(Output)", "State(Change)"],
            "invariants": ["Must be valid", "Cannot fail"],
            "parameters": [
                {
                    "name": "threshold",
                    "type": "Float",
                    "range": "[0, 1]",
                    "description": "Cutoff value",
                }
            ],
            "dependencies": {"references": deps},
            "_meta": {"path": ["Society", "Governance"], "ring": 2, "tier": 3},
        }

        # Compute hash and add
        from sema.core.hashing import generate_sema_hash

        computed = generate_sema_hash(full_pattern)
        full_pattern["sema_ref"] = computed["reference"]
        full_pattern["sema_id"] = computed["full_id"]
        full_pattern["sema_stub"] = computed["stub"]
        full_pattern["sema_layer"] = "Society"
        full_pattern["sema_category"] = "Governance"

        self.store.add_pattern(full_pattern)

        # Export
        original = self._export_all_patterns()["FullPattern"]

        # Remove
        result = apply_changes(remove_handles=["FullPattern"])
        self.assertTrue(result)

        # Write clean version (without sema_* fields)
        clean = {k: v for k, v in original.items() if not k.startswith("sema_")}
        self._write_pattern_file(clean)

        # Add back
        result = apply_changes(add_files=[self.patterns_dir])
        self.assertTrue(result)

        # Verify ALL fields
        restored = self._export_all_patterns()["FullPattern"]

        self.assertEqual(restored.get("handle"), original.get("handle"))
        self.assertEqual(restored.get("gloss"), original.get("gloss"))
        self.assertEqual(restored.get("mechanism"), original.get("mechanism"))
        self.assertEqual(restored.get("signature"), original.get("signature"))
        self.assertEqual(restored.get("invariants"), original.get("invariants"))
        self.assertEqual(restored.get("parameters"), original.get("parameters"))
        self.assertEqual(restored.get("_meta"), original.get("_meta"))
        self.assertEqual(restored.get("sema_id"), original.get("sema_id"))
        self.assertEqual(restored.get("sema_ref"), original.get("sema_ref"))
        self.assertEqual(restored.get("sema_stub"), original.get("sema_stub"))


class TestExtendsVersionPins(unittest.TestCase):
    """`extends` names an exact immutable parent definition.

    Parent edits may move the active handle through an ordinary dependency cascade,
    but they must not silently retarget a child's specialization claim. Apply rejects
    a stranded pin before mutation; an author can explicitly retarget staged children
    after review.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_taxonomy.db")
        self.patterns_dir = os.path.join(self.temp_dir, "patterns")
        os.makedirs(self.patterns_dir)
        self.store = GraphStore(self.db_path)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _card(self, handle, mechanism="Test mechanism", deps=None, extends=None):
        pattern = {
            "handle": handle,
            "mechanism": mechanism,
            "gloss": "Test gloss",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        if deps:
            pattern["dependencies"] = deps
        if extends:
            pattern["extends"] = extends
        return pattern

    def _commit(self, *patterns):
        """Put patterns in the DB the way apply would, in the given order."""
        for pattern in patterns:
            path = Path(self.patterns_dir) / f"{pattern['handle']}.json"
            path.write_text(json.dumps(pattern))
        with patch("sema.cli.main.get_default_db_path", return_value=self.db_path):
            self.assertTrue(apply_changes(add_files=[self.patterns_dir]))
        for pattern in patterns:
            (Path(self.patterns_dir) / f"{pattern['handle']}.json").unlink()

    def _stage_and_run(self, *patterns, retarget_extends=False):
        for pattern in patterns:
            path = Path(self.patterns_dir) / f"{pattern['handle']}.json"
            path.write_text(json.dumps(pattern))
        with patch("sema.cli.main.get_default_db_path", return_value=self.db_path):
            with patch("builtins.print") as printed:
                result = apply_changes(
                    add_files=[self.patterns_dir],
                    retarget_extends=retarget_extends,
                )
        output = "\n".join(str(c.args[0]) for c in printed.call_args_list if c.args)
        return result, output

    def _active_ref(self, handle):
        current_hash = GraphStore(self.db_path).get_pattern_hash(handle)
        return f"sema:{handle}#mh:SHA-256:{current_hash}"

    def test_check_rejects_missing_extends_parent(self):
        child = self._card("Child", extends=make_sema_id("MissingParent"))
        path = Path(self.patterns_dir) / "Child.json"
        path.write_text(json.dumps(child))

        with patch("sema.cli.main.get_default_db_path", return_value=self.db_path):
            self.assertFalse(apply_changes(add_files=[str(path)], check_only=True))

    def test_parent_in_same_batch_satisfies_extends_target_check(self):
        parent = self._card("Parent")
        authored_parent_ref = generate_sema_hash(parent)["full_id"]
        child = self._card("Child", extends=authored_parent_ref)
        for pattern in (parent, child):
            path = Path(self.patterns_dir) / f"{pattern['handle']}.json"
            path.write_text(json.dumps(pattern))

        with patch("sema.cli.main.get_default_db_path", return_value=self.db_path):
            self.assertTrue(apply_changes(add_files=[self.patterns_dir]))

        fresh = GraphStore(self.db_path)
        child_id = fresh._find_pattern_id("Child")
        parent_id = fresh._find_pattern_id("Parent")
        self.assertTrue(fresh.has_edge_of_type(child_id, parent_id, EdgeType.IS_A))
        is_a_edges = [
            edge
            for edge in fresh._edges_between(child_id, parent_id)
            if edge.get("edge_type") == EdgeType.IS_A
        ]
        self.assertEqual(is_a_edges[0]["metadata"]["parent_sema_id"], authored_parent_ref)

    def test_batch_apply_preserves_authored_parent_version_by_default(self):
        parent = self._card("Parent")
        authored_parent_ref = generate_sema_hash(parent)["full_id"]
        child = self._card("Child", extends=authored_parent_ref)
        for pattern in (parent, child):
            path = Path(self.patterns_dir) / f"{pattern['handle']}.json"
            path.write_text(json.dumps(pattern))

        with patch("sema.cli.main.get_default_db_path", return_value=self.db_path):
            self.assertTrue(apply_changes(add_files=[self.patterns_dir]))

        stored_child = json.loads((Path(self.patterns_dir) / "Child.json").read_text())
        self.assertEqual(stored_child["extends"], authored_parent_ref)

    def test_existing_handle_does_not_make_fabricated_parent_version_resolvable(self):
        self._commit(self._card("Parent"))
        child = self._card("Child", extends=make_sema_id("Parent", "b"))
        path = Path(self.patterns_dir) / "Child.json"
        path.write_text(json.dumps(child))

        with patch("sema.cli.main.get_default_db_path", return_value=self.db_path):
            self.assertFalse(apply_changes(add_files=[str(path)], check_only=True))

    def test_retarget_requires_explicit_option(self):
        parent = self._card("Parent")
        authored_parent_ref = make_sema_id("Parent", "b")
        child = self._card("Child", extends=authored_parent_ref)
        for pattern in (parent, child):
            path = Path(self.patterns_dir) / f"{pattern['handle']}.json"
            path.write_text(json.dumps(pattern))

        with patch("sema.cli.main.get_default_db_path", return_value=self.db_path):
            self.assertTrue(apply_changes(add_files=[self.patterns_dir], retarget_extends=True))

        fresh = GraphStore(self.db_path)
        stored_child = json.loads((Path(self.patterns_dir) / "Child.json").read_text())
        current_parent_ref = f"sema:Parent#mh:SHA-256:{fresh.get_pattern_hash('Parent')}"
        self.assertEqual(stored_child["extends"], current_parent_ref)

    def test_parent_edit_is_rejected_before_stranding_unstaged_child(self):
        self._commit(self._card("Parent"))
        self._commit(self._card("Child", extends=self._active_ref("Parent")))
        before = GraphStore(self.db_path).get_pattern_hash("Parent")

        result, out = self._stage_and_run(self._card("Parent", mechanism="Rewritten mechanism"))

        self.assertFalse(result)
        self.assertIn("would strand Child", out)
        self.assertEqual(GraphStore(self.db_path).get_pattern_hash("Parent"), before)

    def test_cascade_is_rejected_before_stranding_unstaged_child(self):
        """Grandparent -> Parent -> Child. Staging only the grandparent moves Parent's
        active hash through the ordinary dependency cascade. Child remains pinned and
        the parent editor is told about the choice. Nothing else is staged.
        """
        self._commit(self._card("Grandparent"))
        self._commit(
            self._card(
                "Parent",
                mechanism="Uses {{grandparent}} internally",
                deps={"composes_with": {"grandparent": self._active_ref("Grandparent")}},
            )
        )
        self._commit(self._card("Child", extends=self._active_ref("Parent")))
        before = GraphStore(self.db_path).get_pattern_hash("Grandparent")

        result, out = self._stage_and_run(
            self._card("Grandparent", mechanism="Rewritten grandparent mechanism")
        )

        self.assertFalse(result)
        self.assertIn("would strand Child", out)
        self.assertEqual(GraphStore(self.db_path).get_pattern_hash("Grandparent"), before)

    def test_retarget_runs_after_indirectly_moved_unstaged_parent(self):
        self._commit(self._card("Grandparent"))
        self._commit(
            self._card(
                "Parent",
                mechanism="Uses {{grandparent}} internally",
                deps={"composes_with": {"grandparent": self._active_ref("Grandparent")}},
            )
        )
        self._commit(self._card("Child", extends=self._active_ref("Parent")))
        child = self._card("Child", extends=self._active_ref("Parent"))

        result, _out = self._stage_and_run(
            child,
            self._card("Grandparent", mechanism="Rewritten grandparent mechanism"),
            retarget_extends=True,
        )

        self.assertTrue(result)
        stored_child = json.loads((Path(self.patterns_dir) / "Child.json").read_text())
        self.assertEqual(stored_child["extends"], self._active_ref("Parent"))

    @patch(
        "sema.taxonomy_graph.embedding_service.EmbeddingService.get_embedding",
        return_value=np.zeros(384, dtype=np.float32),
    )
    def test_retarget_with_missing_ordinary_dependency_fails_before_parent_moves(
        self, _mock_embedding
    ):
        self._commit(self._card("Parent", mechanism="Parent version one"))
        original_parent_ref = self._active_ref("Parent")
        self._commit(self._card("Child", extends=original_parent_ref))
        reviewed_child = self._card(
            "Child",
            mechanism="Uses {{missing}}.",
            deps={"references": {"missing": make_sema_id("Missing")}},
            extends=original_parent_ref,
        )

        result, out = self._stage_and_run(
            self._card("Parent", mechanism="Parent version two"),
            reviewed_child,
            retarget_extends=True,
        )

        self.assertFalse(result)
        self.assertIn("Missing dependency target", out)
        self.assertNotIn("Applying...", out)
        self.assertEqual(self._active_ref("Parent"), original_parent_ref)
        fresh = GraphStore(self.db_path)
        stored_child = fresh.graph.nodes[fresh._find_pattern_id("Child")]["metadata"]["pattern"]
        self.assertEqual(stored_child["extends"], original_parent_ref)

    def test_silent_when_no_extends_parent_moved(self):
        self._commit(self._card("Parent"))
        self._commit(self._card("Child", extends=self._active_ref("Parent")))

        result, out = self._stage_and_run(self._card("Unrelated"))

        self.assertTrue(result)
        self.assertNotIn("would strand", out)


if __name__ == "__main__":
    unittest.main()
