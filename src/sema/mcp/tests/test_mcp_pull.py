"""Tests for the `sema_pull` MCP tool and its env-var opt-out."""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

if importlib.util.find_spec("mcp") is None:
    raise unittest.SkipTest("mcp extra is not installed")


def _run_module_check(env_overrides: dict[str, str]) -> set[str]:
    """Import the MCP server module in a clean subprocess and return the set
    of symbols prefixed with `sema_` that the module exposes. Running in a
    subprocess guarantees a clean import — the MCP FastMCP singleton mutates
    on `@mcp.tool()` decoration, so reimporting in-process would leak state
    between tests.
    """
    repo_src = Path(__file__).resolve().parents[3]  # .../src
    env = {
        **os.environ,
        "PYTHONPATH": str(repo_src) + os.pathsep + os.environ.get("PYTHONPATH", ""),
        **env_overrides,
    }
    # Strip any inherited SEMA_* vars so the subprocess only sees what we set.
    for k in list(env):
        if k.startswith("SEMA_") and k not in env_overrides:
            env.pop(k, None)

    code = (
        "import sys; from sema.mcp import server; "
        "print(','.join(sorted(n for n in dir(server) if n.startswith('sema_'))))"
    )
    out = subprocess.check_output([sys.executable, "-c", code], env=env, text=True)
    return set(out.strip().split(","))


class TestSemaPullRegistration(unittest.TestCase):
    def test_pull_registered_by_default(self):
        """With no SEMA_DISABLE_PULL set, sema_pull is an exposed MCP tool."""
        symbols = _run_module_check({})
        self.assertIn("sema_pull", symbols)

    def test_mint_registered_by_default(self):
        """0.1.28+ flips mint from opt-in to opt-out. Default is exposed."""
        symbols = _run_module_check({})
        self.assertIn("sema_mint", symbols)

    def test_pull_disabled_by_env(self):
        """SEMA_DISABLE_PULL=true removes the tool from the registered set."""
        symbols = _run_module_check({"SEMA_DISABLE_PULL": "true"})
        self.assertNotIn("sema_pull", symbols)
        # Other tools unaffected.
        self.assertIn("sema_search", symbols)

    def test_mint_disabled_by_env(self):
        """SEMA_DISABLE_MINT=true removes the mint tool."""
        symbols = _run_module_check({"SEMA_DISABLE_MINT": "true"})
        self.assertNotIn("sema_mint", symbols)


class TestSemaPullOutput(unittest.TestCase):
    """The tool should return structured JSON with the expected keys so an
    agent can act on the result programmatically, not just read a human blurb.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.upstream_db = os.path.join(self.temp_dir, "upstream.db")
        self.user_db = os.path.join(self.temp_dir, "user.db")

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _add_pattern(self, db_path, handle, supersedes=None, mechanism="mechanism text"):
        from sema.taxonomy_graph.graph_store import GraphStore

        store = GraphStore(db_path)
        pattern = {
            "handle": handle,
            "mechanism": mechanism,
            "gloss": f"Gloss for {handle}",
            "_meta": {
                "path": ["Infrastructure", "Primitives"],
                "ring": 0,
                "tier": 1,
            },
        }
        if supersedes:
            pattern["_meta"]["supersedes"] = supersedes
        store.add_pattern(pattern)

    def _sema_id(self, db_path, handle):
        from sema.taxonomy_graph.graph_store import GraphStore, NodeType

        store = GraphStore(db_path)
        for _, data in store.get_nodes_by_type(NodeType.PATTERN):
            if data.get("text") == handle:
                return data.get("metadata", {}).get("pattern", {}).get("sema_id", "")
        return ""

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_sema_pull_returns_structured_output(self, mock_bundled_check, mock_bundled, mock_db):
        """Call _sema_pull directly; verify it returns JSON with the fields an
        MCP agent would rely on (success, added, updated, superseded_removed,
        etc.). We assert presence of keys, not exact counts — those vary by
        pull content and are covered in the CLI-level tests.
        """
        from sema.mcp.server import _sema_pull

        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.user_db, "OldHandle")
        old_sema_id = self._sema_id(self.user_db, "OldHandle")
        self._add_pattern(self.upstream_db, "NewHandle", supersedes=[old_sema_id])

        raw = _sema_pull(source=self.upstream_db)
        result = json.loads(raw)

        # Required top-level fields for programmatic consumers.
        expected_keys = {
            "success",
            "added",
            "updated",
            "skipped",
            "cascaded_user",
            "superseded_removed",
            "superseded_kept_orphan",
            "upstream_removed",
            "vocabulary_root_before",
            "vocabulary_root_after",
            "vocabulary_root_scheme",
        }
        self.assertLessEqual(
            expected_keys,
            set(result.keys()),
            f"Missing expected keys: {expected_keys - set(result.keys())}",
        )

        # Pull succeeded and did the supersession cleanup.
        self.assertTrue(result["success"])
        superseded = result["superseded_removed"]
        self.assertEqual(len(superseded), 1)
        old_h, new_handles = superseded[0]
        self.assertEqual(old_h, "OldHandle")
        self.assertIn("NewHandle", new_handles)

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_post_pull_root_failure_cannot_report_success(
        self,
        mock_bundled_check,
        mock_bundled,
        mock_db,
    ):
        import numpy as np

        from sema.core import hashing
        from sema.mcp.server import _sema_pull

        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        real_vocabulary_info = hashing.vocabulary_info
        call_count = 0

        def fail_post_pull_fingerprint(db_path):
            nonlocal call_count
            call_count += 1
            if call_count == 3:
                raise ValueError("malformed post-pull catalog")
            return real_vocabulary_info(db_path)

        zero_embedding = np.zeros(384, dtype=np.float32)
        with patch(
            "sema.taxonomy_graph.embedding_service.EmbeddingService.get_embedding",
            return_value=zero_embedding,
        ):
            self._add_pattern(self.user_db, "Existing")
            before_id = self._sema_id(self.user_db, "Existing")
            self._add_pattern(
                self.upstream_db,
                "Existing",
                mechanism="changed upstream mechanism",
            )

            with patch.object(
                hashing,
                "vocabulary_info",
                side_effect=fail_post_pull_fingerprint,
            ):
                result = json.loads(_sema_pull(source=self.upstream_db))

        self.assertFalse(result["success"])
        self.assertIsNone(result["vocabulary_root_after"])
        self.assertIn("Post-pull aggregate-root verification failed", result["error"])
        self.assertEqual(self._sema_id(self.user_db, "Existing"), before_id)
        self.assertFalse(os.path.exists(self.user_db + ".pull_bak"))

    @patch("sema.cli.main.get_default_db_path")
    @patch("sema.cli.main.get_bundled_db_path")
    @patch("sema.cli.main.is_bundled_db")
    def test_sema_pull_dry_run(self, mock_bundled_check, mock_bundled, mock_db):
        """dry_run=True previews supersession removals without writing."""
        from sema.mcp.server import _sema_pull

        mock_db.return_value = self.user_db
        mock_bundled.return_value = self.upstream_db
        mock_bundled_check.return_value = False

        self._add_pattern(self.user_db, "OldHandle")
        old_sema_id = self._sema_id(self.user_db, "OldHandle")
        self._add_pattern(self.upstream_db, "NewHandle", supersedes=[old_sema_id])

        raw = _sema_pull(source=self.upstream_db, dry_run=True)
        result = json.loads(raw)

        self.assertTrue(result["success"])
        self.assertTrue(result.get("dry_run"))
        # Preview is populated.
        self.assertGreaterEqual(len(result.get("superseded_removed") or []), 1)

        # Nothing was written: the user DB still has OldHandle.
        from sema.taxonomy_graph.graph_store import GraphStore, NodeType

        handles = {
            d["text"] for _, d in GraphStore(self.user_db).get_nodes_by_type(NodeType.PATTERN)
        }
        self.assertIn("OldHandle", handles, "dry_run must not mutate the target DB")


if __name__ == "__main__":
    unittest.main()
