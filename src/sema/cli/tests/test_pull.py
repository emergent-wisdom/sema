"""Tests for sema pull (topological DAG walk to update patterns)."""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from sema.cli.main import update_db
from sema.taxonomy_graph.graph_store import GraphStore, NodeType


class TestPull(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.upstream_db = os.path.join(self.temp_dir, "upstream.db")
        self.user_db = os.path.join(self.temp_dir, "user.db")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _add_pattern(self, db_path, handle, mechanism="Test mechanism", **kwargs):
        store = GraphStore(db_path)
        store.embedding_service.get_embedding = lambda _text: np.zeros(384, dtype=np.float32)
        pattern = {
            "handle": handle,
            "mechanism": mechanism,
            "gloss": kwargs.get("gloss", f"Gloss for {handle}"),
            "_meta": {
                "path": [
                    kwargs.get("layer", "Infrastructure"),
                    kwargs.get("category", "Primitives"),
                ],
                "ring": 0,
                "tier": 1,
            },
        }
        if "deps" in kwargs:
            pattern["dependencies"] = kwargs["deps"]
        if "extends" in kwargs:
            pattern["extends"] = kwargs["extends"]
        store.add_pattern(pattern)

    def _get_handles(self, db_path):
        store = GraphStore(db_path)
        return {
            data["text"]
            for _, data in store.get_nodes_by_type(NodeType.PATTERN)
            if data.get("text")
        }

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_pull_updates_existing_patterns(self, mock_bundled_check, mock_bundled, mock_db):
        """Pull updates patterns that exist in both upstream and target."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.upstream_db, "Alpha", "Updated mechanism")
        self._add_pattern(self.user_db, "Alpha", "Old mechanism")

        result = update_db()

        self.assertTrue(result["success"])
        self.assertIn("Alpha", self._get_handles(self.user_db))

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_pull_adds_new_upstream_patterns(self, mock_bundled_check, mock_bundled, mock_db):
        """New patterns in upstream appear in target after pull."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.upstream_db, "Alpha")
        self._add_pattern(self.upstream_db, "Beta", "Brand new")
        self._add_pattern(self.user_db, "Alpha")

        result = update_db()

        self.assertTrue(result["success"])
        handles = self._get_handles(self.user_db)
        self.assertIn("Alpha", handles)
        self.assertIn("Beta", handles)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_pull_preserves_user_only_patterns(self, mock_bundled_check, mock_bundled, mock_db):
        """Patterns only in the user DB are not removed by pull."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.upstream_db, "Alpha")
        self._add_pattern(self.user_db, "Alpha")
        self._add_pattern(self.user_db, "MyCustom", "My custom pattern")

        result = update_db()

        self.assertTrue(result["success"])
        handles = self._get_handles(self.user_db)
        self.assertIn("Alpha", handles)
        self.assertIn("MyCustom", handles)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_pull_rejects_parent_update_that_would_strand_user_child(
        self, mock_bundled_check, mock_bundled, mock_db
    ):
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.user_db, "Parent", "Parent version one")
        parent_v1 = self._sema_id(self.user_db, "Parent")
        self._add_pattern(self.user_db, "Child", extends=parent_v1)
        child_v1 = self._sema_id(self.user_db, "Child")
        self._add_pattern(self.upstream_db, "Parent", "Parent version two")

        result = update_db(verify=True)

        self.assertFalse(result["success"])
        self.assertIn("would strand Child", result["error"])
        self.assertEqual(self._sema_id(self.user_db, "Parent"), parent_v1)
        self.assertEqual(self._sema_id(self.user_db, "Child"), child_v1)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_pull_dry_run_no_changes(self, mock_bundled_check, mock_bundled, mock_db):
        """Dry run reports but doesn't modify the DB."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.upstream_db, "Alpha")
        self._add_pattern(self.upstream_db, "Beta")
        self._add_pattern(self.user_db, "Alpha")

        result = update_db(dry_run=True)

        self.assertTrue(result["success"])
        self.assertEqual(self._get_handles(self.user_db), {"Alpha"})

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_pull_rejects_bundled_target(self, mock_bundled_check, mock_db):
        """Cannot pull into the bundled (read-only) DB."""
        mock_db.return_value = self.user_db
        mock_bundled_check.return_value = True

        result = update_db()

        self.assertFalse(result["success"])

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_pull_topological_order(self, mock_bundled_check, mock_bundled, mock_db):
        """Patterns are applied in dependency order (leaves first)."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        # Leaf has no deps. Root depends on Leaf.
        self._add_pattern(self.upstream_db, "Leaf", "Leaf mechanism")
        self._add_pattern(
            self.upstream_db,
            "Root",
            mechanism="Uses {{leaf}}",
            deps={
                "references": {
                    "leaf": "sema:Leaf#mh:SHA-256:" + "a" * 64,
                }
            },
        )

        # Start with empty user DB
        GraphStore(self.user_db)

        result = update_db()

        self.assertTrue(result["success"])
        handles = self._get_handles(self.user_db)
        self.assertIn("Leaf", handles)
        self.assertIn("Root", handles)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_pull_same_source_and_target_rejected(self, mock_bundled_check, mock_bundled, mock_db):
        """Cannot pull from a DB into itself."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.user_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.user_db, "Alpha")

        result = update_db()

        self.assertFalse(result["success"])

    def _sema_id(self, db_path, handle):
        """Get the stored sema_id for a handle."""
        store = GraphStore(db_path)
        for _, data in store.get_nodes_by_type(NodeType.PATTERN):
            if data.get("text") == handle:
                meta = data.get("metadata", {})
                pattern = meta.get("pattern", {})
                return pattern.get("sema_id", "")
        return None

    def _run_hash_validity(self, db_path):
        """Run the hash validity check logic against a DB. Returns list of mismatches."""
        from sema.core.hashing import generate_sema_hash

        store = GraphStore(db_path)
        patterns = {}
        for _, data in store.get_nodes_by_type(NodeType.PATTERN):
            h = data.get("text")
            if not h:
                continue
            meta = data.get("metadata", {})
            p = meta.get("pattern", {}) or {}
            p["handle"] = h
            deps = store.get_dependencies_from_edges(h)
            if deps:
                p["dependencies"] = deps
            patterns[h] = p

        stored = {}
        for h, p in patterns.items():
            sid = p.get("sema_id", "")
            if "#mh:SHA-256:" in sid:
                stored[h] = sid.split("#mh:SHA-256:")[1]

        def lookup(h):
            return stored.get(h)

        mismatches = []
        for h, p in patterns.items():
            if h not in stored:
                continue
            computed = generate_sema_hash(p, lookup)["hash"]
            if computed != stored[h]:
                mismatches.append((h, stored[h][:12], computed[:12]))
        return mismatches

    # ---------- Priority 1: correctness ----------

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_T1_hash_cascade_three_levels(self, mock_bundled_check, mock_bundled, mock_db):
        """3-level chain Leaf→Mid→Root: every sema_id must match recomputed hash."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.upstream_db, "Leaf", "Leaf mechanism v2")
        self._add_pattern(
            self.upstream_db,
            "Mid",
            mechanism="Uses {{leaf}}",
            deps={"references": {"leaf": "sema:Leaf#mh:SHA-256:" + "a" * 64}},
        )
        self._add_pattern(
            self.upstream_db,
            "Root",
            mechanism="Uses {{mid}}",
            deps={"references": {"mid": "sema:Mid#mh:SHA-256:" + "b" * 64}},
        )
        GraphStore(self.user_db)

        result = update_db()

        self.assertTrue(result["success"])
        mismatches = self._run_hash_validity(self.user_db)
        self.assertEqual(mismatches, [], f"Hash validity failed: {mismatches}")

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_T2_user_pattern_cascades_when_upstream_changes(
        self, mock_bundled_check, mock_bundled, mock_db
    ):
        """UserX depends on Alpha. Alpha's content changes upstream.
        After pull, UserX's hash should also change (via cascade)."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.upstream_db, "Alpha", "Original mechanism")
        self._add_pattern(self.user_db, "Alpha", "Original mechanism")
        self._add_pattern(
            self.user_db,
            "UserX",
            mechanism="Uses {{alpha}}",
            deps={"references": {"alpha": "sema:Alpha#mh:SHA-256:" + "a" * 64}},
        )

        userx_before = self._sema_id(self.user_db, "UserX")

        # Now change Alpha in upstream
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        os.makedirs(self.temp_dir)
        self._add_pattern(self.upstream_db, "Alpha", "UPDATED mechanism with more detail")
        self._add_pattern(self.user_db, "Alpha", "Original mechanism")
        self._add_pattern(
            self.user_db,
            "UserX",
            mechanism="Uses {{alpha}}",
            deps={"references": {"alpha": "sema:Alpha#mh:SHA-256:" + "a" * 64}},
        )

        userx_before = self._sema_id(self.user_db, "UserX")
        result = update_db()

        self.assertTrue(result["success"])
        userx_after = self._sema_id(self.user_db, "UserX")
        self.assertIsNotNone(userx_before)
        self.assertIsNotNone(userx_after)
        self.assertNotEqual(
            userx_before,
            userx_after,
            "UserX's hash should change because Alpha's hash changed",
        )
        mismatches = self._run_hash_validity(self.user_db)
        self.assertEqual(mismatches, [], f"Hash validity failed: {mismatches}")

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_T3_diamond_dependency(self, mock_bundled_check, mock_bundled, mock_db):
        """Top→Left, Top→Right, Left→Bottom, Right→Bottom. Pull, verify hash validity."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.upstream_db, "Bottom", "Leaf of the diamond")
        self._add_pattern(
            self.upstream_db,
            "Left",
            mechanism="Uses {{bottom}}",
            deps={"references": {"bottom": "sema:Bottom#mh:SHA-256:" + "a" * 64}},
        )
        self._add_pattern(
            self.upstream_db,
            "Right",
            mechanism="Uses {{bottom}}",
            deps={"references": {"bottom": "sema:Bottom#mh:SHA-256:" + "a" * 64}},
        )
        self._add_pattern(
            self.upstream_db,
            "Top",
            mechanism="Uses {{left}} and {{right}}",
            deps={
                "references": {
                    "left": "sema:Left#mh:SHA-256:" + "b" * 64,
                    "right": "sema:Right#mh:SHA-256:" + "c" * 64,
                }
            },
        )
        GraphStore(self.user_db)

        result = update_db()

        self.assertTrue(result["success"])
        mismatches = self._run_hash_validity(self.user_db)
        self.assertEqual(mismatches, [], f"Diamond hash validity: {mismatches}")

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_T5_idempotence(self, mock_bundled_check, mock_bundled, mock_db):
        """Pulling twice produces identical sema_ids."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.upstream_db, "Alpha")
        self._add_pattern(
            self.upstream_db,
            "Beta",
            mechanism="Uses {{alpha}}",
            deps={"references": {"alpha": "sema:Alpha#mh:SHA-256:" + "a" * 64}},
        )
        GraphStore(self.user_db)

        self.assertTrue(update_db()["success"])
        first_ids = {h: self._sema_id(self.user_db, h) for h in self._get_handles(self.user_db)}

        self.assertTrue(update_db()["success"])
        second_ids = {h: self._sema_id(self.user_db, h) for h in self._get_handles(self.user_db)}

        self.assertEqual(first_ids, second_ids, "Pull should be idempotent")

    # ---------- Priority 2: edge cases ----------

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_T6_empty_source(self, mock_bundled_check, mock_bundled, mock_db):
        """Pulling from an empty upstream is a no-op."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        GraphStore(self.upstream_db)
        self._add_pattern(self.user_db, "Alpha")

        result = update_db()

        self.assertTrue(result["success"])
        self.assertEqual(self._get_handles(self.user_db), {"Alpha"})

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_T7_empty_target(self, mock_bundled_check, mock_bundled, mock_db):
        """Pulling into an empty target acts like a full install."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.upstream_db, "Alpha")
        self._add_pattern(self.upstream_db, "Beta")
        GraphStore(self.user_db)

        result = update_db()

        self.assertTrue(result["success"])
        self.assertEqual(self._get_handles(self.user_db), {"Alpha", "Beta"})

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_T10_deep_chain(self, mock_bundled_check, mock_bundled, mock_db):
        """10-level dependency chain A0→A1→...→A9 cascades correctly."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.upstream_db, "A0", "Bottom of chain")
        for i in range(1, 10):
            self._add_pattern(
                self.upstream_db,
                f"A{i}",
                mechanism=f"Uses {{{{a{i - 1}}}}}",
                deps={"references": {f"a{i - 1}": f"sema:A{i - 1}#mh:SHA-256:" + "a" * 64}},
            )
        GraphStore(self.user_db)

        result = update_db()

        self.assertTrue(result["success"])
        self.assertEqual(len(self._get_handles(self.user_db)), 10)
        mismatches = self._run_hash_validity(self.user_db)
        self.assertEqual(mismatches, [], f"Deep chain hash validity: {mismatches}")

    # ---------- Priority 3: field preservation ----------

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_T12_semantic_fields_preserved(self, mock_bundled_check, mock_bundled, mock_db):
        """All semantic fields survive the pull round-trip."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        store = GraphStore(self.upstream_db)
        store.add_pattern(
            {
                "handle": "RichPattern",
                "mechanism": "Full mechanism text",
                "gloss": "Full gloss",
                "invariants": ["Invariant 1", "Invariant 2"],
                "preconditions": ["Pre 1"],
                "postconditions": ["Post 1"],
                "failure_modes": ["Mode A", "Mode B"],
                "_meta": {
                    "path": ["Infrastructure", "Primitives"],
                    "ring": 0,
                    "tier": 1,
                },
            }
        )
        GraphStore(self.user_db)

        result = update_db()

        self.assertTrue(result["success"])
        target_store = GraphStore(self.user_db)
        for _, data in target_store.get_nodes_by_type(NodeType.PATTERN):
            if data.get("text") == "RichPattern":
                meta = data.get("metadata", {})
                p = meta.get("pattern", {})
                self.assertEqual(p.get("mechanism"), "Full mechanism text")
                self.assertEqual(p.get("gloss"), "Full gloss")
                self.assertEqual(p.get("invariants"), ["Invariant 1", "Invariant 2"])
                self.assertEqual(p.get("preconditions"), ["Pre 1"])
                self.assertEqual(p.get("postconditions"), ["Post 1"])
                self.assertEqual(p.get("failure_modes"), ["Mode A", "Mode B"])
                return
        self.fail("RichPattern not found after pull")

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_user_pattern_hash_unchanged_when_no_upstream_dep(
        self, mock_bundled_check, mock_bundled, mock_db
    ):
        """User pattern that doesn't depend on anything upstream keeps same hash after pull."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.upstream_db, "Alpha")
        self._add_pattern(self.user_db, "Alpha")
        self._add_pattern(self.user_db, "Standalone", "Self-contained, no deps")

        before_id = self._sema_id(self.user_db, "Standalone")

        result = update_db()

        self.assertTrue(result["success"])
        after_id = self._sema_id(self.user_db, "Standalone")
        self.assertEqual(
            before_id,
            after_id,
            "Standalone user pattern hash must not change after pull",
        )

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_user_removed_dep_restored_from_upstream(
        self, mock_bundled_check, mock_bundled, mock_db
    ):
        """User removed an upstream pattern. New upstream has something that depends on it.
        Pull should re-add the removed pattern and successfully mint the dependent."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.upstream_db, "Foundation", "Foundational pattern")
        self._add_pattern(
            self.upstream_db,
            "Building",
            mechanism="Uses {{foundation}}",
            deps={"references": {"foundation": "sema:Foundation#mh:SHA-256:" + "a" * 64}},
        )
        self._add_pattern(self.user_db, "Alpha")

        result = update_db()

        self.assertTrue(result["success"])
        handles = self._get_handles(self.user_db)
        self.assertIn("Foundation", handles)
        self.assertIn("Building", handles)
        self.assertIn("Alpha", handles)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_T13_caution_field_preserved(self, mock_bundled_check, mock_bundled, mock_db):
        """Unhashed _meta.caution survives the pull."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        store = GraphStore(self.upstream_db)
        store.add_pattern(
            {
                "handle": "CautionPattern",
                "mechanism": "Test mechanism",
                "gloss": "Test",
                "_meta": {
                    "path": ["Infrastructure", "Primitives"],
                    "ring": 0,
                    "tier": 1,
                    "caution": "This is a test caution notice",
                },
            }
        )
        GraphStore(self.user_db)

        result = update_db()

        self.assertTrue(result["success"])
        target_store = GraphStore(self.user_db)
        for _, data in target_store.get_nodes_by_type(NodeType.PATTERN):
            if data.get("text") == "CautionPattern":
                meta = data.get("metadata", {})
                p = meta.get("pattern", {})
                self.assertEqual(
                    p.get("_meta", {}).get("caution"),
                    "This is a test caution notice",
                )
                return
        self.fail("CautionPattern not found after pull")


class TestPullRealVocabulary(unittest.TestCase):
    """Test pull against the actual 427-pattern bundled vocabulary."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.user_db = os.path.join(self.temp_dir, "user.db")
        from pathlib import Path

        self.repo_db = str(Path(__file__).resolve().parents[4] / "data" / "taxonomy.db")
        if not os.path.exists(self.repo_db):
            self.skipTest(f"Repo DB not found at {self.repo_db}")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_T4_real_vocabulary_pull(self, mock_bundled_check, mock_bundled, mock_db):
        """Pull the actual 427-pattern vocabulary into a fresh DB, verify hash validity."""
        from sema.core.hashing import generate_sema_hash

        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.repo_db
        mock_bundled_check.return_value = False

        GraphStore(self.user_db)

        result = update_db()

        self.assertTrue(result["success"], "Pull failed on real vocabulary")

        store = GraphStore(self.user_db)
        patterns = {}
        for _, data in store.get_nodes_by_type(NodeType.PATTERN):
            h = data.get("text")
            if not h:
                continue
            meta = data.get("metadata", {})
            p = meta.get("pattern", {}) or {}
            p["handle"] = h
            deps = store.get_dependencies_from_edges(h)
            if deps:
                p["dependencies"] = deps
            patterns[h] = p

        self.assertGreaterEqual(len(patterns), 400, f"Only {len(patterns)} patterns pulled")

        stored = {}
        for h, p in patterns.items():
            sid = p.get("sema_id", "")
            if "#mh:SHA-256:" in sid:
                stored[h] = sid.split("#mh:SHA-256:")[1]

        def lookup(h):
            return stored.get(h)

        mismatches = []
        for h, p in patterns.items():
            if h not in stored:
                continue
            computed = generate_sema_hash(p, lookup)["hash"]
            if computed != stored[h]:
                mismatches.append(h)

        self.assertEqual(
            mismatches,
            [],
            f"{len(mismatches)} patterns have invalid hashes after pull: {mismatches[:5]}",
        )


class TestPullEdgeCases(unittest.TestCase):
    """Tests for the design issues Gemini Deep Think flagged."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.upstream_db = os.path.join(self.temp_dir, "upstream.db")
        self.user_db = os.path.join(self.temp_dir, "user.db")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _add(self, db, handle, mechanism="Test mechanism", **kwargs):
        store = GraphStore(db)
        pattern = {
            "handle": handle,
            "mechanism": mechanism,
            "gloss": kwargs.get("gloss", f"Gloss for {handle}"),
            "_meta": {
                "path": [
                    kwargs.get("layer", "Infrastructure"),
                    kwargs.get("category", "Primitives"),
                ],
                "ring": 0,
                "tier": 1,
                **kwargs.get("meta_extra", {}),
            },
        }
        if "deps" in kwargs:
            pattern["dependencies"] = kwargs["deps"]
        store.add_pattern(pattern)

    def _pattern(self, db, handle):
        store = GraphStore(db)
        for _, data in store.get_nodes_by_type(NodeType.PATTERN):
            if data.get("text") == handle:
                meta = data.get("metadata", {})
                return meta.get("pattern", {}) or {}
        return {}

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_alias_round_trip(self, mock_bundled_check, mock_bundled, mock_db):
        """Custom aliases (not snake_case of handle) survive a pull round-trip.

        Author writes `{"my_alias": "RefTarget"}` and references {{my_alias}}
        in the mechanism. After pull, the alias must still be `my_alias`,
        not regenerated as `ref_target`.
        """
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "RefTarget")
        self._add(
            self.upstream_db,
            "Source",
            mechanism="Uses {{my_alias}}",
            deps={"references": {"my_alias": "RefTarget"}},
        )
        GraphStore(self.user_db)

        result = update_db()
        self.assertTrue(result["success"])

        store = GraphStore(self.user_db)
        deps = store.get_dependencies_from_edges("Source")
        self.assertIn("my_alias", deps.get("references", {}))
        self.assertNotIn("ref_target", deps.get("references", {}))

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_multi_edge_same_target(self, mock_bundled_check, mock_bundled, mock_db):
        """Pattern with both `accepts` and `yields` of the same target preserves both edges.

        DiGraph would silently collapse to one edge, breaking the pattern's
        identity (Merkle hash). MultiDiGraph keeps both.
        """
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Task")
        self._add(
            self.upstream_db,
            "Transformer",
            mechanism="Reads {{input}} and writes {{output}}",
            deps={
                "accepts": {"input": "Task"},
                "yields": {"output": "Task"},
            },
        )
        GraphStore(self.user_db)

        result = update_db()
        self.assertTrue(result["success"])

        store = GraphStore(self.user_db)
        deps = store.get_dependencies_from_edges("Transformer")
        self.assertIn("input", deps.get("accepts", {}))
        self.assertIn("output", deps.get("yields", {}))

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_meta_overlay_preserved_on_update(self, mock_bundled_check, mock_bundled, mock_db):
        """User's local _meta.caution survives an upstream content update.

        Upstream changes the mechanism; user has set a local caution. After
        pull, mechanism is updated AND the user's caution is intact.
        """
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Foo", "v1 mechanism")
        self._add(
            self.user_db,
            "Foo",
            "v1 mechanism",
            meta_extra={"caution": "user-set-warning"},
        )

        # Now upstream evolves
        self._add(self.upstream_db, "Foo", "v2 UPDATED mechanism")

        result = update_db()
        self.assertTrue(result["success"])

        p = self._pattern(self.user_db, "Foo")
        self.assertIn("UPDATED", p.get("mechanism", ""))
        self.assertEqual(p.get("_meta", {}).get("caution"), "user-set-warning")

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_mid_pull_failure_rollback(self, mock_bundled_check, mock_bundled, mock_db):
        """If a pattern fails mid-pull, target DB is restored from backup."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Alpha")
        self._add(self.upstream_db, "Beta")
        self._add(self.user_db, "Original")

        # Patch mint_pattern to fail on the second call
        from sema.core.mint import MintResult

        call_count = {"n": 0}
        original_mint = __import__("sema.core.mint", fromlist=["mint_pattern"]).mint_pattern

        def flaky_mint(pattern, store, **kwargs):
            call_count["n"] += 1
            if call_count["n"] >= 2:
                return MintResult(
                    success=False,
                    handle=pattern.get("handle", ""),
                    errors=["simulated failure"],
                )
            return original_mint(pattern, store, **kwargs)

        with patch("sema.core.mint.mint_pattern", side_effect=flaky_mint):
            result = update_db()

        self.assertFalse(result["success"], "Pull should fail")
        # User DB should still contain its original pattern, no upstream patterns
        handles = {
            data["text"] for _, data in GraphStore(self.user_db).get_nodes_by_type(NodeType.PATTERN)
        }
        self.assertIn("Original", handles)
        # Backup file should be cleaned up after restore
        self.assertFalse(os.path.exists(self.user_db + ".pull_bak"))

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_fast_path_skip_when_unchanged(self, mock_bundled_check, mock_bundled, mock_db):
        """When upstream sema_id matches target sema_id, no mint happens.

        Trick: patch mint_pattern to fail. If pull skips correctly, mint
        is never called and pull succeeds; if it doesn't skip, pull fails.
        """
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Same")
        # User has the identical pattern (same content => same hash)
        self._add(self.user_db, "Same")

        from sema.core.mint import MintResult

        with patch(
            "sema.core.mint.mint_pattern",
            return_value=MintResult(success=False, handle="x", errors=["should not run"]),
        ):
            result = update_db()

        self.assertTrue(result["success"], "Pull should skip identical patterns via fast-path")


class TestTaxonomyOverlay(unittest.TestCase):
    """The paper's 'Mutable Overlay' semantics: upstream owns layer/category/tier/ring;
    user owns caution/related. Pull must propagate upstream taxonomy reorganizations
    even though they don't change the sema_id (since _meta is unhashed)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.upstream_db = os.path.join(self.temp_dir, "upstream.db")
        self.user_db = os.path.join(self.temp_dir, "user.db")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _add(self, db, handle, mechanism="Test", **kwargs):
        store = GraphStore(db)
        pattern = {
            "handle": handle,
            "mechanism": mechanism,
            "gloss": kwargs.get("gloss", f"Gloss for {handle}"),
            "_meta": {
                "path": [
                    kwargs.get("layer", "Infrastructure"),
                    kwargs.get("category", "Primitives"),
                ],
                "ring": kwargs.get("ring", 0),
                "tier": kwargs.get("tier", 1),
                **kwargs.get("meta_extra", {}),
            },
        }
        store.add_pattern(pattern)

    def _pattern_meta(self, db, handle):
        store = GraphStore(db)
        for _, data in store.get_nodes_by_type(NodeType.PATTERN):
            if data.get("text") == handle:
                meta = data.get("metadata", {})
                p = meta.get("pattern", {}) or {}
                return p.get("_meta", {})
        return {}

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_upstream_taxonomy_change_propagates_despite_same_hash(
        self, mock_bundled_check, mock_bundled, mock_db
    ):
        """Upstream re-categorizes a pattern (Physics → Society). Same content,
        same sema_id. Pull must NOT skip via fast-path — it must propagate
        the new layer/category to the user's DB."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        # Both DBs start with Foo as Physics/Time
        self._add(self.upstream_db, "Foo", layer="Physics", category="Time")
        self._add(self.user_db, "Foo", layer="Physics", category="Time")

        # Upstream re-categorizes to Society/Protocols (sema_id unchanged)
        self._add(self.upstream_db, "Foo", layer="Society", category="Protocols")

        result = update_db()
        self.assertTrue(result["success"])

        meta = self._pattern_meta(self.user_db, "Foo")
        self.assertEqual(
            meta.get("path"),
            ["Society", "Protocols"],
            "User's path must reflect upstream re-categorization",
        )

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_user_caution_survives_upstream_taxonomy_update(
        self, mock_bundled_check, mock_bundled, mock_db
    ):
        """Combined: upstream changes layer; user has local caution. After pull:
        - layer updated from upstream
        - caution preserved from user
        """
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Foo", layer="Mind", category="Strategy")
        self._add(
            self.user_db,
            "Foo",
            layer="Mind",
            category="Strategy",
            meta_extra={"caution": "user note"},
        )
        self._add(self.upstream_db, "Foo", layer="Society", category="Protocols")

        update_db()

        meta = self._pattern_meta(self.user_db, "Foo")
        self.assertEqual(meta.get("path"), ["Society", "Protocols"])
        self.assertEqual(meta.get("caution"), "user note")

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_user_layer_override_loses_to_upstream(self, mock_bundled_check, mock_bundled, mock_db):
        """If a user manually changed _meta.layer locally, pull replaces it
        with upstream's value. Layer is upstream-owned; only caution/related
        are user-owned. Documents the intentional behavior."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Foo", layer="Society", category="Protocols")
        self._add(self.user_db, "Foo", layer="Mind", category="Strategy")  # user moved it

        update_db()

        meta = self._pattern_meta(self.user_db, "Foo")
        self.assertEqual(
            meta.get("path"),
            ["Society", "Protocols"],
            "User's local path override must be reverted to upstream",
        )


class TestMergeNodesMultiEdge(unittest.TestCase):
    """merge_nodes must dedupe by (edge_type, alias) not just edge_type.
    Otherwise parallel edges with distinct aliases collapse to one."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "merge.db")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_merge_preserves_parallel_aliases(self):
        """Two ACCEPTS edges with different aliases survive a node merge."""
        from sema.taxonomy_graph.graph_store import EdgeType

        store = GraphStore(self.db_path)
        src = store.create_node(NodeType.PATTERN, "Source")
        tgt_keep = store.create_node(NodeType.PATTERN, "Keep")
        tgt_remove = store.create_node(NodeType.PATTERN, "Remove")

        # Two parallel ACCEPTS edges to the remove-node, different aliases
        store.create_edge(src, tgt_remove, EdgeType.ACCEPTS, alias="task1")
        store.create_edge(src, tgt_remove, EdgeType.ACCEPTS, alias="task2")

        ok = store.merge_nodes(tgt_keep, tgt_remove)
        self.assertTrue(ok)

        # Both aliases must appear on the surviving edges
        edges_kept = store._edges_between(src, tgt_keep)
        aliases = {e.get("alias") for e in edges_kept if e.get("edge_type") == EdgeType.ACCEPTS}
        self.assertEqual(
            aliases,
            {"task1", "task2"},
            "merge_nodes must preserve distinct aliases on parallel edges",
        )


class TestExclusionList(unittest.TestCase):
    """Pull respects ~/.config/sema/excluded and --exclude flag.

    A user who deletes a pattern can opt-out of having pull re-add it
    on the next sync, by listing the handle.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.upstream_db = os.path.join(self.temp_dir, "upstream.db")
        self.user_db = os.path.join(self.temp_dir, "user.db")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _add(self, db, handle, mechanism="Test"):
        store = GraphStore(db)
        store.add_pattern(
            {
                "handle": handle,
                "mechanism": mechanism,
                "gloss": handle,
                "_meta": {
                    "path": ["Infrastructure", "Primitives"],
                    "ring": 0,
                    "tier": 1,
                },
            }
        )

    def _handles(self, db):
        return {
            data["text"]
            for _, data in GraphStore(db).get_nodes_by_type(NodeType.PATTERN)
            if data.get("text")
        }

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_exclude_arg_skips_handle(self, mock_bundled_check, mock_bundled, mock_db):
        """An --exclude arg prevents pull from re-adding the handle."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Alpha")
        self._add(self.upstream_db, "Beta")
        # User has only Beta locally (deleted Alpha or never had it)
        self._add(self.user_db, "Beta")

        result = update_db(exclude=["Alpha"])

        self.assertTrue(result["success"])
        handles = self._handles(self.user_db)
        self.assertNotIn("Alpha", handles, "Alpha was excluded; must not be re-added")
        self.assertIn("Beta", handles)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_exclusion_file_skips_handle(self, mock_bundled_check, mock_bundled, mock_db):
        """A handle in ~/.config/sema/excluded is skipped."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Alpha")
        self._add(self.upstream_db, "Beta")
        self._add(self.user_db, "Beta")

        # Patch _load_exclusions to simulate the file
        with patch("sema.cli.main._load_exclusions", return_value={"Alpha"}):
            result = update_db()

        self.assertTrue(result["success"])
        self.assertNotIn("Alpha", self._handles(self.user_db))

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_exclusion_file_and_arg_combine(self, mock_bundled_check, mock_bundled, mock_db):
        """File exclusions and --exclude args are unioned."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        for h in ("Alpha", "Beta", "Gamma"):
            self._add(self.upstream_db, h)
        # Empty user DB

        with patch("sema.cli.main._load_exclusions", return_value={"Alpha"}):
            update_db(exclude=["Beta"])

        handles = self._handles(self.user_db)
        self.assertNotIn("Alpha", handles)
        self.assertNotIn("Beta", handles)
        self.assertIn("Gamma", handles)

    def test_exclusion_file_format(self):
        """_load_exclusions correctly parses comments and blank lines."""
        from sema.cli.main import _load_exclusions

        with tempfile.TemporaryDirectory() as tmp:
            cfg_dir = os.path.join(tmp, ".config", "sema")
            os.makedirs(cfg_dir)
            with open(os.path.join(cfg_dir, "excluded"), "w") as f:
                f.write("# This is a comment\n")
                f.write("\n")
                f.write("Alpha\n")
                f.write("Beta # inline comment\n")
                f.write("   Gamma   \n")
            with patch("pathlib.Path.home", return_value=__import__("pathlib").Path(tmp)):
                # Ensure XDG_CONFIG_HOME isn't set (would override Path.home)
                with patch.dict(os.environ, {}, clear=False) as _:
                    os.environ.pop("XDG_CONFIG_HOME", None)
                    result = _load_exclusions()
            self.assertEqual(result, {"Alpha", "Beta", "Gamma"})

    def test_exclusion_file_xdg_config_home(self):
        """Honor $XDG_CONFIG_HOME when set."""
        from sema.cli.main import _load_exclusions

        with tempfile.TemporaryDirectory() as tmp:
            cfg_dir = os.path.join(tmp, "sema")
            os.makedirs(cfg_dir)
            with open(os.path.join(cfg_dir, "excluded"), "w") as f:
                f.write("XdgPattern\n")
            with patch.dict(os.environ, {"XDG_CONFIG_HOME": tmp}):
                result = _load_exclusions()
            self.assertEqual(result, {"XdgPattern"})

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_transitive_exclusion_prevents_abort(self, mock_bundled_check, mock_bundled, mock_db):
        """If Alpha is excluded AND missing locally, Beta (which depends on
        Alpha) must be safely auto-skipped to prevent the whole pull from
        aborting via transaction rollback."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Alpha")
        # Beta depends on Alpha
        store = GraphStore(self.upstream_db)
        store.add_pattern(
            {
                "handle": "Beta",
                "mechanism": "Uses {{a}}",
                "gloss": "Beta",
                "_meta": {
                    "path": ["Infrastructure", "Primitives"],
                    "ring": 0,
                    "tier": 1,
                },
                "dependencies": {"references": {"a": "Alpha"}},
            }
        )
        # Gamma is unrelated, should succeed
        self._add(self.upstream_db, "Gamma")

        # User has nothing locally
        GraphStore(self.user_db)

        result = update_db(exclude=["Alpha"])

        self.assertTrue(result["success"], "Pull must not abort when an excluded dep cascades")
        handles = self._handles(self.user_db)
        self.assertNotIn("Alpha", handles)
        self.assertNotIn("Beta", handles, "Beta needs missing Alpha and must be auto-skipped")
        self.assertIn("Gamma", handles, "Unrelated patterns still succeed")

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_extends_exclusion_prevents_abort(self, mock_bundled_check, mock_bundled, mock_db):
        """An excluded parent also auto-skips its extending child."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        # Keep this regression test independent of the process-wide embedding
        # cache, which may be read-only or contain different warmed entries.
        with patch(
            "sema.taxonomy_graph.embedding_service.EmbeddingService.get_embedding",
            return_value=np.zeros(384, dtype=np.float32),
        ):
            self._add(self.upstream_db, "Parent")
            store = GraphStore(self.upstream_db)
            parent_hash = store.get_pattern_hash("Parent")
            store.add_pattern(
                {
                    "handle": "Child",
                    "mechanism": "A specialised child.",
                    "gloss": "Child",
                    "extends": f"sema:Parent#mh:SHA-256:{parent_hash}",
                    "_meta": {
                        "path": ["Infrastructure", "Primitives"],
                        "ring": 0,
                        "tier": 1,
                    },
                }
            )
            self._add(self.upstream_db, "Unrelated")
            GraphStore(self.user_db)

            result = update_db(exclude=["Parent"])

        self.assertTrue(result["success"])
        handles = self._handles(self.user_db)
        self.assertNotIn("Parent", handles)
        self.assertNotIn("Child", handles)
        self.assertIn("Unrelated", handles)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_exclusion_acts_as_version_pin(self, mock_bundled_check, mock_bundled, mock_db):
        """Emergent feature: if Alpha is excluded BUT exists locally, dependents
        link to the local frozen Alpha. Excluding without deleting = version pin."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        # Upstream has v2 of Alpha
        self._add(self.upstream_db, "Alpha", "v2 upstream")
        store = GraphStore(self.upstream_db)
        store.add_pattern(
            {
                "handle": "Beta",
                "mechanism": "Uses {{a}}",
                "gloss": "Beta",
                "_meta": {
                    "path": ["Infrastructure", "Primitives"],
                    "ring": 0,
                    "tier": 1,
                },
                "dependencies": {"references": {"a": "Alpha"}},
            }
        )

        # User has v1 of Alpha frozen locally
        self._add(self.user_db, "Alpha", "v1 frozen")

        result = update_db(exclude=["Alpha"])

        self.assertTrue(result["success"])
        handles = self._handles(self.user_db)
        self.assertIn("Alpha", handles)
        self.assertIn("Beta", handles, "Beta links to local frozen Alpha")

        # Verify Alpha was NOT overwritten — version pin worked
        store = GraphStore(self.user_db)
        for _, data in store.get_nodes_by_type(NodeType.PATTERN):
            if data.get("text") == "Alpha":
                p = data.get("metadata", {}).get("pattern", {})
                self.assertEqual(
                    p.get("mechanism"),
                    "v1 frozen",
                    "Local Alpha must not be overwritten by upstream v2",
                )
                return
        self.fail("Alpha not found")


class TestRecovery(unittest.TestCase):
    """Pre-pull snapshot retention and --undo restore."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.upstream_db = os.path.join(self.temp_dir, "upstream.db")
        self.user_db = os.path.join(self.temp_dir, "user.db")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _add(self, db, handle, mechanism="Test"):
        store = GraphStore(db)
        store.add_pattern(
            {
                "handle": handle,
                "mechanism": mechanism,
                "gloss": handle,
                "_meta": {
                    "path": ["Infrastructure", "Primitives"],
                    "ring": 0,
                    "tier": 1,
                },
            }
        )

    def _handles(self, db):
        return {
            data["text"]
            for _, data in GraphStore(db).get_nodes_by_type(NodeType.PATTERN)
            if data.get("text")
        }

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_successful_pull_keeps_snapshot(self, mock_bundled_check, mock_bundled, mock_db):
        """After a pull that changes something, .pull_previous exists."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Alpha")
        self._add(self.user_db, "OldPattern")  # ensure change: Alpha added

        update_db()

        self.assertTrue(os.path.exists(self.user_db + ".pull_previous"))
        self.assertFalse(os.path.exists(self.user_db + ".pull_bak"))

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_noop_pull_does_not_overwrite_snapshot(self, mock_bundled_check, mock_bundled, mock_db):
        """Critical: running pull twice must NOT erase the real safety net.
        Second pull (all skipped via fast-path) must preserve the snapshot
        created by the first pull."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Alpha")
        self._add(self.user_db, "Legacy")

        # First pull: Alpha gets added, snapshot of (Legacy only) is saved
        update_db()
        first_snapshot = self.user_db + ".pull_previous"
        self.assertTrue(os.path.exists(first_snapshot))
        size_after_first = os.path.getsize(first_snapshot)

        # Second pull: no changes. Must NOT overwrite.
        update_db()
        self.assertTrue(os.path.exists(first_snapshot), "Snapshot erased by no-op pull")
        self.assertEqual(
            os.path.getsize(first_snapshot),
            size_after_first,
            "Snapshot was overwritten by no-op pull",
        )

        # And verify the snapshot still represents the pre-first-pull state
        # (only Legacy, no Alpha)
        snap_handles = self._handles(first_snapshot)
        self.assertEqual(snap_handles, {"Legacy"})

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_undo_restores_via_sqlite_backup(self, mock_bundled_check, mock_bundled, mock_db):
        """--undo restores the active DB to the pre-pull snapshot."""
        from sema.cli.main import undo_pull

        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Alpha")
        self._add(self.user_db, "OnlyMine")

        # Pre-pull state has only OnlyMine
        update_db()
        post_pull_handles = self._handles(self.user_db)
        self.assertIn("Alpha", post_pull_handles)
        self.assertIn("OnlyMine", post_pull_handles)

        # Undo
        self.assertTrue(undo_pull())

        restored = self._handles(self.user_db)
        self.assertEqual(restored, {"OnlyMine"}, "Undo must restore pre-pull state")
        # Snapshot consumed
        self.assertFalse(os.path.exists(self.user_db + ".pull_previous"))

    @patch("sema.cli.main.get_default_db_path")
    def test_undo_without_snapshot_fails_cleanly(self, mock_db):
        """--undo with no snapshot reports clearly and returns False."""
        from sema.cli.main import undo_pull

        mock_db.return_value = self.user_db
        GraphStore(self.user_db)  # create empty DB

        self.assertFalse(undo_pull())

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_stranded_backup_aborts_next_pull(self, mock_bundled_check, mock_bundled, mock_db):
        """A stranded .pull_bak indicates a prior catastrophic rollback failure.
        The next pull must NOT overwrite it (that would destroy the user's
        only recoverable state). It must abort and warn."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Alpha")
        self._add(self.user_db, "OldPattern")

        # Simulate a stranded backup from a prior catastrophic failure.
        # Touch an empty file — the abort check only inspects existence,
        # so we don't need a real DB copy here.
        backup_path = self.user_db + ".pull_bak"
        open(backup_path, "w").close()
        self.assertTrue(os.path.exists(backup_path))
        pre_size = os.path.getsize(backup_path)

        result = update_db()

        self.assertFalse(result["success"], "Pull must refuse when a stranded backup exists")
        # Stranded backup must be preserved untouched
        self.assertTrue(os.path.exists(backup_path))
        self.assertEqual(
            os.path.getsize(backup_path), pre_size, "Stranded backup was modified — data loss risk"
        )

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_locked_db_does_not_strand_backup(self, mock_bundled_check, mock_bundled, mock_db):
        """If the initial sqlite3.backup() fails (e.g. target DB locked by
        another agent), the partial 0-byte .pull_bak file must be cleaned
        up — otherwise the next pull will mistake it for a stranded backup
        from a catastrophic rollback failure and refuse to proceed."""
        import sqlite3 as _sqlite3

        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Alpha")
        self._add(self.user_db, "OldPattern")

        backup_path = self.user_db + ".pull_bak"
        self.assertFalse(os.path.exists(backup_path))

        # sqlite3.Connection is an immutable C type — can't monkeypatch
        # `.backup` directly. Wrap _sqlite3.connect so the source-side
        # connection raises on backup(), simulating a locked DB.
        original_connect = _sqlite3.connect
        target_db = self.user_db

        class FailingBackupConn(_sqlite3.Connection):
            def backup(self, *args, **kwargs):
                raise _sqlite3.OperationalError("database is locked")

        def fake_connect(path, *args, **kwargs):
            if path == target_db and "factory" not in kwargs:
                kwargs["factory"] = FailingBackupConn
            return original_connect(path, *args, **kwargs)

        with patch.object(_sqlite3, "connect", fake_connect):
            result = update_db()

        self.assertFalse(result["success"], "Pull must fail when initial backup fails")
        self.assertFalse(
            os.path.exists(backup_path),
            "Locked-DB error must clean up the 0-byte .pull_bak — otherwise next pull "
            "false-positives as 'stranded backup from catastrophic rollback'",
        )


class TestPullSupersessionCleanup(unittest.TestCase):
    """Supersession cleanup: upstream declares a pattern's old sema_id
    retired; the local copy at that sema_id gets removed on pull."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.upstream_db = os.path.join(self.temp_dir, "upstream.db")
        self.user_db = os.path.join(self.temp_dir, "user.db")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _add(self, db, handle, mechanism="m", supersedes=None, deps=None, extends=None):
        store = GraphStore(db)
        store.embedding_service.get_embedding = lambda _text: np.zeros(384, dtype=np.float32)
        pat = {
            "handle": handle,
            "mechanism": mechanism,
            "gloss": f"Gloss {handle}",
            "_meta": {
                "path": ["Infrastructure", "Primitives"],
                "ring": 0,
                "tier": 1,
            },
        }
        if supersedes:
            pat["_meta"]["supersedes"] = supersedes
        if deps:
            pat["dependencies"] = deps
        if extends:
            pat["extends"] = extends
        store.add_pattern(pat)

    def _sema_id(self, db, handle):
        store = GraphStore(db)
        for _, data in store.get_nodes_by_type(NodeType.PATTERN):
            if data.get("text") == handle:
                return data.get("metadata", {}).get("pattern", {}).get("sema_id")
        return None

    def _handles(self, db):
        store = GraphStore(db)
        return {
            data["text"]
            for _, data in store.get_nodes_by_type(NodeType.PATTERN)
            if data.get("text")
        }

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_superseded_handle_removed_on_pull(self, mock_bundled_check, mock_bundled, mock_db):
        """User has OldName at hash X. Upstream has NewName with
        _meta.supersedes=[OldName#X]. After pull: OldName is gone."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.user_db, "OldName", mechanism="original")
        old_sid = self._sema_id(self.user_db, "OldName")
        self.assertIsNotNone(old_sid)

        self._add(self.upstream_db, "NewName", mechanism="replacement", supersedes=[old_sid])

        result = update_db()
        self.assertTrue(result["success"])

        handles = self._handles(self.user_db)
        self.assertNotIn("OldName", handles, "supersession cleanup should remove OldName")
        self.assertIn("NewName", handles, "successor should be present")

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_preserve_superseded_flag_keeps_both(self, mock_bundled_check, mock_bundled, mock_db):
        """With preserve_superseded=True, the old handle is retained
        alongside the new one."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.user_db, "OldName")
        old_sid = self._sema_id(self.user_db, "OldName")

        self._add(self.upstream_db, "NewName", supersedes=[old_sid])

        result = update_db(preserve_superseded=True)
        self.assertTrue(result["success"])

        handles = self._handles(self.user_db)
        self.assertIn("OldName", handles, "preserve_superseded should retain the old handle")
        self.assertIn("NewName", handles)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_orphan_guard_blocks_removal(self, mock_bundled_check, mock_bundled, mock_db):
        """If a USER-ONLY local pattern depends on OldName, pull must
        NOT remove OldName — the orphan guard kicks in."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.user_db, "OldName")
        old_sid = self._sema_id(self.user_db, "OldName")
        self._add(
            self.user_db,
            "UserOnly",
            deps={"references": {"oldname": old_sid}},
        )

        self._add(self.upstream_db, "NewName", supersedes=[old_sid])

        result = update_db()
        self.assertTrue(result["success"])

        handles = self._handles(self.user_db)
        self.assertIn(
            "OldName",
            handles,
            "orphan guard should keep OldName — UserOnly still depends on it",
        )
        self.assertIn("UserOnly", handles)
        self.assertIn("NewName", handles)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_orphan_guard_counts_exact_specializing_children(
        self, mock_bundled_check, mock_bundled, mock_db
    ):
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.user_db, "OldName")
        old_sid = self._sema_id(self.user_db, "OldName")
        self._add(self.user_db, "UserChild", extends=old_sid)
        self._add(self.upstream_db, "NewName", supersedes=[old_sid])

        result = update_db()

        self.assertTrue(result["success"])
        self.assertIn("OldName", self._handles(self.user_db))
        self.assertIn("UserChild", self._handles(self.user_db))
        self.assertEqual(len(result["superseded_kept_orphan"]), 1)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_dry_run_reports_exact_child_as_supersession_orphan(
        self, mock_bundled_check, mock_bundled, mock_db
    ):
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.user_db, "OldName")
        old_sid = self._sema_id(self.user_db, "OldName")
        self._add(self.user_db, "UserChild", extends=old_sid)
        self._add(self.upstream_db, "NewName", supersedes=[old_sid])

        result = update_db(dry_run=True)

        self.assertTrue(result["success"])
        self.assertEqual(result["superseded_removed"], [])
        self.assertEqual(
            result["superseded_kept_orphan"],
            [("OldName", ["NewName"], ["UserChild"])],
        )
        self.assertEqual(result["upstream_removed"], ["OldName", "UserChild"])
        self.assertEqual(self._handles(self.user_db), {"OldName", "UserChild"})

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_superseded_removal_runs_before_cascade(
        self, mock_bundled_check, mock_bundled, mock_db
    ):
        """Supersession cleanup must run BEFORE the cascade sweep —
        otherwise cascade rewrites the local sema_id and the match misses.

        Regression guard for the experimental.db pull: AbductiveLeap at
        v0.1.27's sema_id got its hash rewritten by cascade (because its
        dep Leaf changed upstream) BEFORE supersession check ran, so the
        cleanup missed it. Test: OldName depends on Leaf, Leaf changes
        upstream — OldName must still get cleaned up."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.upstream_db, "Leaf", mechanism="leaf v2")

        self._add(self.user_db, "Leaf", mechanism="leaf v1")
        leaf_sid_local = self._sema_id(self.user_db, "Leaf")
        self._add(
            self.user_db,
            "OldName",
            deps={"references": {"leaf": leaf_sid_local}},
        )
        old_sid = self._sema_id(self.user_db, "OldName")

        self._add(self.upstream_db, "NewName", supersedes=[old_sid])

        result = update_db()
        self.assertTrue(result["success"])

        handles = self._handles(self.user_db)
        self.assertNotIn(
            "OldName",
            handles,
            "OldName must be removed even though Leaf change would've cascaded it",
        )
        self.assertIn("NewName", handles)
        self.assertIn("Leaf", handles)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_non_superseded_user_patterns_retained(self, mock_bundled_check, mock_bundled, mock_db):
        """User-only patterns NOT in any supersedes list must survive."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.user_db, "OldName")
        old_sid = self._sema_id(self.user_db, "OldName")
        self._add(self.user_db, "PurelyLocal", mechanism="user-only")

        self._add(self.upstream_db, "NewName", supersedes=[old_sid])

        result = update_db()
        self.assertTrue(result["success"])

        handles = self._handles(self.user_db)
        self.assertNotIn("OldName", handles, "supersession should fire")
        self.assertIn("PurelyLocal", handles, "unrelated user pattern must survive")

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_supersedes_entry_for_different_hash_no_op(
        self, mock_bundled_check, mock_bundled, mock_db
    ):
        """Upstream's supersedes entry points at a hash the user doesn't
        have: the entry is a no-op, OldName survives as user-only."""
        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add(self.user_db, "OldName", mechanism="current-local")
        current_local_sid = self._sema_id(self.user_db, "OldName")

        fake_old_sid = (
            "sema:OldName#mh:SHA-256:"
            "deadbeefcafebabe0000000000000000000000000000000000000000000000aa"
        )
        self.assertNotEqual(current_local_sid, fake_old_sid)

        self._add(self.upstream_db, "NewName", supersedes=[fake_old_sid])

        result = update_db()
        self.assertTrue(result["success"])

        handles = self._handles(self.user_db)
        self.assertIn("OldName", handles, "sema_id mismatch — no supersession fires")
        self.assertIn("NewName", handles)


if __name__ == "__main__":
    unittest.main()
