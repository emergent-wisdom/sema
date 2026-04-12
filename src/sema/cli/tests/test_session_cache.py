"""Tests for the MCP server session cache (compact already-seen patterns)."""

import json
import os
import sys
import unittest
from unittest.mock import patch

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, src_path)


def _make_search_result(handle, stub="ab12", gloss="A pattern", score=0.9, **extra):
    """Helper: build a search result dict like RegistryManager.search() returns."""
    ref = f"{handle}#{stub}"
    return {
        "handle": handle,
        "sema_ref": ref,
        "sema_stub": stub,
        "gloss": gloss,
        "score": score,
        "mechanism": f"Mechanism for {handle}",
        **extra,
    }


class TestSessionCache(unittest.TestCase):
    """Tests for _served_patterns session cache in sema_search and sema_resolve."""

    def setUp(self):
        """Reset the module-level session cache before each test."""
        from sema.mcp import server

        server._served_patterns.clear()
        self.server = server

    # ── sema_search compaction ──────────────────────────────────────────

    def test_first_search_returns_full_results(self):
        """First time seeing a pattern → full result (no _seen flag)."""
        results = [_make_search_result("Alpha")]

        with patch.object(self.server.REGISTRY_MGR, "search", return_value=results):
            with patch.object(self.server.REGISTRY_MGR, "refresh"):
                with patch.object(
                    self.server.REGISTRY_MGR,
                    "get_context",
                    return_value={"dependencies": [], "used_by": []},
                ):
                    raw = self.server.sema_search("alpha")

        parsed = json.loads(raw)
        self.assertEqual(len(parsed), 1)
        self.assertNotIn("_seen", parsed[0])
        self.assertIn("mechanism", parsed[0])

    def test_second_search_returns_compact(self):
        """Seeing the same pattern again → compact result with _seen: True."""
        results = [_make_search_result("Alpha")]

        with patch.object(self.server.REGISTRY_MGR, "search", return_value=results):
            with patch.object(self.server.REGISTRY_MGR, "refresh"):
                with patch.object(
                    self.server.REGISTRY_MGR,
                    "get_context",
                    return_value={"dependencies": [], "used_by": []},
                ):
                    self.server.sema_search("alpha")  # first call
                    raw = self.server.sema_search("alpha")  # second call

        parsed = json.loads(raw)
        self.assertEqual(len(parsed), 1)
        self.assertTrue(parsed[0]["_seen"])
        self.assertNotIn("mechanism", parsed[0])
        self.assertEqual(parsed[0]["handle"], "Alpha")
        self.assertEqual(parsed[0]["gloss"], "A pattern")

    def test_compact_preserves_handle_gloss_score_ref(self):
        """Compact results keep exactly: handle, sema_ref, gloss, score, _seen."""
        results = [_make_search_result("Beta", stub="ff00", gloss="Beta gloss", score=0.75)]

        with patch.object(self.server.REGISTRY_MGR, "search", return_value=results):
            with patch.object(self.server.REGISTRY_MGR, "refresh"):
                with patch.object(
                    self.server.REGISTRY_MGR,
                    "get_context",
                    return_value={"dependencies": [], "used_by": []},
                ):
                    self.server.sema_search("beta")
                    raw = self.server.sema_search("beta")

        parsed = json.loads(raw)[0]
        self.assertEqual(parsed["handle"], "Beta")
        self.assertEqual(parsed["sema_ref"], "Beta#ff00")
        self.assertEqual(parsed["gloss"], "Beta gloss")
        self.assertEqual(parsed["score"], 0.75)
        self.assertTrue(parsed["_seen"])
        # No extra keys leaked
        self.assertEqual(set(parsed.keys()), {"handle", "sema_ref", "gloss", "score", "_seen"})

    def test_mixed_new_and_seen(self):
        """Search returning both new and already-seen patterns compacts only the seen ones."""
        alpha = _make_search_result("Alpha")
        beta = _make_search_result("Beta", stub="cc33")

        with patch.object(self.server.REGISTRY_MGR, "refresh"):
            with patch.object(
                self.server.REGISTRY_MGR,
                "get_context",
                return_value={"dependencies": [], "used_by": []},
            ):
                # First search: only Alpha
                with patch.object(self.server.REGISTRY_MGR, "search", return_value=[alpha]):
                    self.server.sema_search("alpha")

                # Second search: Alpha (seen) + Beta (new)
                with patch.object(self.server.REGISTRY_MGR, "search", return_value=[alpha, beta]):
                    raw = self.server.sema_search("both")

        parsed = json.loads(raw)
        alpha_result = next(r for r in parsed if r["handle"] == "Alpha")
        beta_result = next(r for r in parsed if r["handle"] == "Beta")

        self.assertTrue(alpha_result["_seen"])
        self.assertNotIn("mechanism", alpha_result)
        self.assertNotIn("_seen", beta_result)
        self.assertIn("mechanism", beta_result)

    # ── sema_resolve marks patterns as served ───────────────────────────

    def test_resolve_marks_served(self):
        """sema_resolve marks all resolved patterns as served for future searches."""
        resolved_subgraph = {
            "Gamma#1234": {"handle": "Gamma", "sema_ref": "Gamma#1234", "mechanism": "..."},
            "Delta#5678": {"handle": "Delta", "sema_ref": "Delta#5678", "mechanism": "..."},
        }

        with patch.object(self.server.REGISTRY_MGR, "refresh"):
            with patch.object(self.server.REGISTRY_MGR, "resolve", return_value=resolved_subgraph):
                with patch.object(
                    self.server.REGISTRY_MGR,
                    "get_pattern",
                    side_effect=lambda h: resolved_subgraph.get(f"{h}#1234")
                    or resolved_subgraph.get(f"{h}#5678"),
                ):
                    self.server.sema_resolve("Gamma")

        self.assertIn("Gamma#1234", self.server._served_patterns)
        self.assertIn("Delta#5678", self.server._served_patterns)

    def test_resolve_then_search_compacts(self):
        """After resolving a pattern, searching for it returns compact form."""
        resolved_subgraph = {
            "Gamma#1234": {"handle": "Gamma", "sema_ref": "Gamma#1234", "mechanism": "..."},
        }
        search_results = [_make_search_result("Gamma", stub="1234")]

        with patch.object(self.server.REGISTRY_MGR, "refresh"):
            with patch.object(self.server.REGISTRY_MGR, "resolve", return_value=resolved_subgraph):
                with patch.object(
                    self.server.REGISTRY_MGR,
                    "get_pattern",
                    return_value=resolved_subgraph["Gamma#1234"],
                ):
                    self.server.sema_resolve("Gamma")

            with patch.object(self.server.REGISTRY_MGR, "search", return_value=search_results):
                with patch.object(
                    self.server.REGISTRY_MGR,
                    "get_context",
                    return_value={"dependencies": [], "used_by": []},
                ):
                    raw = self.server.sema_search("gamma")

        parsed = json.loads(raw)
        self.assertTrue(parsed[0]["_seen"])

    # ── sema_reset_session ──────────────────────────────────────────────

    def test_reset_clears_cache(self):
        """sema_reset_session clears served patterns so next search returns full results."""
        results = [_make_search_result("Alpha")]

        with patch.object(self.server.REGISTRY_MGR, "refresh"):
            with patch.object(
                self.server.REGISTRY_MGR,
                "get_context",
                return_value={"dependencies": [], "used_by": []},
            ):
                with patch.object(self.server.REGISTRY_MGR, "search", return_value=results):
                    self.server.sema_search("alpha")  # mark as seen

                # Reset
                raw_reset = self.server.sema_reset_session()
                reset = json.loads(raw_reset)
                self.assertTrue(reset["reset"])
                self.assertEqual(reset["patterns_cleared"], 1)

                # Search again — should get full result, not compact
                with patch.object(self.server.REGISTRY_MGR, "search", return_value=results):
                    raw = self.server.sema_search("alpha")

        parsed = json.loads(raw)
        self.assertNotIn("_seen", parsed[0])
        self.assertIn("mechanism", parsed[0])

    def test_reset_empty_cache(self):
        """Resetting an empty cache returns 0 cleared."""
        raw = self.server.sema_reset_session()
        parsed = json.loads(raw)
        self.assertTrue(parsed["reset"])
        self.assertEqual(parsed["patterns_cleared"], 0)

    def test_double_reset(self):
        """Second reset after first returns 0 cleared."""
        self.server._served_patterns.add("Foo#1234")
        self.server.sema_reset_session()
        raw = self.server.sema_reset_session()
        parsed = json.loads(raw)
        self.assertEqual(parsed["patterns_cleared"], 0)

    # ── Graph context enrichment ────────────────────────────────────────

    def test_graph_context_only_for_top_3_new(self):
        """Graph context enrichment applies only to the first 3 new patterns."""
        results = [_make_search_result(f"P{i}", stub=f"00{i}0") for i in range(5)]
        context_calls = []

        def track_context(handle):
            context_calls.append(handle)
            return {"dependencies": ["dep"], "used_by": []}

        with patch.object(self.server.REGISTRY_MGR, "refresh"):
            with patch.object(self.server.REGISTRY_MGR, "search", return_value=results):
                with patch.object(
                    self.server.REGISTRY_MGR, "get_context", side_effect=track_context
                ):
                    raw = self.server.sema_search("patterns")

        parsed = json.loads(raw)
        # Only first 3 should have graph_context
        with_context = [r for r in parsed if "graph_context" in r]
        self.assertEqual(len(with_context), 3)
        # Last 2 should not
        without_context = [r for r in parsed if "graph_context" not in r]
        self.assertEqual(len(without_context), 2)

    # ── Edge: sema_ref fallback to handle ───────────────────────────────

    def test_fallback_to_handle_when_no_sema_ref(self):
        """If search result has no sema_ref, fall back to handle for cache key."""
        result = {"handle": "Orphan", "gloss": "No ref", "score": 0.5, "mechanism": "..."}

        with patch.object(self.server.REGISTRY_MGR, "refresh"):
            with patch.object(self.server.REGISTRY_MGR, "search", return_value=[result]):
                with patch.object(
                    self.server.REGISTRY_MGR,
                    "get_context",
                    return_value={"dependencies": [], "used_by": []},
                ):
                    self.server.sema_search("orphan")

        self.assertIn("Orphan", self.server._served_patterns)

    # ── Session isolation ───────────────────────────────────────────────

    def test_cache_is_module_level(self):
        """_served_patterns is shared across calls (module-level singleton)."""
        results = [_make_search_result("Shared")]

        with patch.object(self.server.REGISTRY_MGR, "refresh"):
            with patch.object(self.server.REGISTRY_MGR, "search", return_value=results):
                with patch.object(
                    self.server.REGISTRY_MGR,
                    "get_context",
                    return_value={"dependencies": [], "used_by": []},
                ):
                    self.server.sema_search("shared")

        # Verify the module-level set was populated
        self.assertIn("Shared#ab12", self.server._served_patterns)


if __name__ == "__main__":
    unittest.main()
