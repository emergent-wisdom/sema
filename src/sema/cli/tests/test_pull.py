"""Tests for sema pull (topological DAG walk to update patterns)."""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

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
        pattern = {
            "handle": handle,
            "mechanism": mechanism,
            "gloss": kwargs.get("gloss", f"Gloss for {handle}"),
            "_meta": {
                "layer": kwargs.get("layer", "Infrastructure"),
                "category": kwargs.get("category", "Primitives"),
                "ring": 0,
                "tier": 1,
            },
        }
        if "deps" in kwargs:
            pattern["dependencies"] = kwargs["deps"]
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

        self.assertTrue(result)
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

        self.assertTrue(result)
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

        self.assertTrue(result)
        handles = self._get_handles(self.user_db)
        self.assertIn("Alpha", handles)
        self.assertIn("MyCustom", handles)

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

        self.assertTrue(result)
        self.assertEqual(self._get_handles(self.user_db), {"Alpha"})

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_pull_rejects_bundled_target(self, mock_bundled_check, mock_db):
        """Cannot pull into the bundled (read-only) DB."""
        mock_db.return_value = self.user_db
        mock_bundled_check.return_value = True

        result = update_db()

        self.assertFalse(result)

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

        self.assertTrue(result)
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

        self.assertFalse(result)

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

        self.assertTrue(result)
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

        self.assertTrue(result)
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

        self.assertTrue(result)
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

        self.assertTrue(update_db())
        first_ids = {h: self._sema_id(self.user_db, h) for h in self._get_handles(self.user_db)}

        self.assertTrue(update_db())
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

        self.assertTrue(result)
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

        self.assertTrue(result)
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

        self.assertTrue(result)
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
                    "layer": "Infrastructure",
                    "category": "Primitives",
                    "ring": 0,
                    "tier": 1,
                },
            }
        )
        GraphStore(self.user_db)

        result = update_db()

        self.assertTrue(result)
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

        self.assertTrue(result)
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

        self.assertTrue(result)
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
                    "layer": "Infrastructure",
                    "category": "Primitives",
                    "ring": 0,
                    "tier": 1,
                    "caution": "This is a test caution notice",
                },
            }
        )
        GraphStore(self.user_db)

        result = update_db()

        self.assertTrue(result)
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

        self.assertTrue(result, "Pull failed on real vocabulary")

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
                "layer": kwargs.get("layer", "Infrastructure"),
                "category": kwargs.get("category", "Primitives"),
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
        self.assertTrue(result)

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
        self.assertTrue(result)

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
        self.assertTrue(result)

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

        self.assertFalse(result, "Pull should fail")
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

        self.assertTrue(result, "Pull should skip identical patterns via fast-path")


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
                "layer": kwargs.get("layer", "Infrastructure"),
                "category": kwargs.get("category", "Primitives"),
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
        self.assertTrue(result)

        meta = self._pattern_meta(self.user_db, "Foo")
        self.assertEqual(
            meta.get("layer"), "Society", "User's layer must reflect upstream re-categorization"
        )
        self.assertEqual(meta.get("category"), "Protocols")

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
        self.assertEqual(meta.get("layer"), "Society")
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
            meta.get("layer"), "Society", "User's local layer override must be reverted to upstream"
        )


if __name__ == "__main__":
    unittest.main()
