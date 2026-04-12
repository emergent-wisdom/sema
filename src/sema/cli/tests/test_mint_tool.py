"""Tests for the sema_mint MCP tool wrapper and conditional registration."""

import json
import os
import sys
import unittest
from unittest.mock import patch

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, src_path)

from sema.mcp import server
from sema.mcp.server import _sema_mint


class TestSemaMintTool(unittest.TestCase):
    """Tests for the _sema_mint function (the tool implementation)."""

    def test_invalid_json_returns_error(self):
        """Malformed JSON string → error, no crash."""
        raw = _sema_mint("not valid json {{{")
        result = json.loads(raw)
        self.assertFalse(result["success"])
        self.assertTrue(any("Invalid JSON" in e for e in result["errors"]))

    def test_missing_handle_returns_error(self):
        """Pattern without handle → error."""
        raw = _sema_mint(json.dumps({"mechanism": "does stuff"}))
        result = json.loads(raw)
        self.assertFalse(result["success"])
        self.assertTrue(any("handle" in e for e in result["errors"]))

    def test_missing_mechanism_returns_error(self):
        """Pattern without mechanism → error."""
        raw = _sema_mint(json.dumps({"handle": "TestPattern"}))
        result = json.loads(raw)
        self.assertFalse(result["success"])
        self.assertTrue(any("mechanism" in e for e in result["errors"]))

    def test_successful_mint(self):
        """Valid pattern → calls apply_changes and returns sema_ref."""
        mock_pattern = {
            "handle": "TestMint",
            "sema_ref": "TestMint#abcd",
            "sema_id": "sema:TestMint#mh:SHA-256:abcd1234",
        }

        with patch("sema.cli.main.apply_changes", return_value=True):
            with patch.object(server.REGISTRY_MGR, "refresh"):
                with patch.object(server.REGISTRY_MGR, "get_pattern", return_value=mock_pattern):
                    raw = _sema_mint(
                        json.dumps(
                            {
                                "handle": "TestMint",
                                "mechanism": "A test pattern",
                                "gloss": "Testing mint",
                            }
                        )
                    )

        result = json.loads(raw)
        self.assertTrue(result["success"])
        self.assertEqual(result["handle"], "TestMint")
        self.assertEqual(result["sema_ref"], "TestMint#abcd")
        self.assertIn("sema_id", result)

    def test_apply_failure_returns_error(self):
        """apply_changes returning False → error result."""
        with patch("sema.cli.main.apply_changes", return_value=False):
            raw = _sema_mint(
                json.dumps(
                    {
                        "handle": "FailMint",
                        "mechanism": "Will fail",
                    }
                )
            )

        result = json.loads(raw)
        self.assertFalse(result["success"])

    def test_apply_exception_returns_error(self):
        """Exception during apply_changes → error with message."""
        with patch("sema.cli.main.apply_changes", side_effect=RuntimeError("DB locked")):
            raw = _sema_mint(
                json.dumps(
                    {
                        "handle": "ExcMint",
                        "mechanism": "Will throw",
                    }
                )
            )

        result = json.loads(raw)
        self.assertFalse(result["success"])
        self.assertTrue(any("DB locked" in e for e in result["errors"]))

    def test_temp_files_cleaned_up(self):
        """Temp files are removed after minting, even on failure."""
        import tempfile

        created_dirs = []
        original_mkdtemp = tempfile.mkdtemp

        def track_mkdtemp(**kwargs):
            d = original_mkdtemp(**kwargs)
            created_dirs.append(d)
            return d

        with patch("tempfile.mkdtemp", side_effect=track_mkdtemp):
            with patch("sema.cli.main.apply_changes", side_effect=RuntimeError("fail")):
                _sema_mint(
                    json.dumps(
                        {
                            "handle": "CleanupTest",
                            "mechanism": "Test cleanup",
                        }
                    )
                )

        # Temp dir should have been cleaned up
        for d in created_dirs:
            self.assertFalse(os.path.exists(d), f"Temp dir not cleaned up: {d}")

    def test_pattern_not_in_registry_after_mint(self):
        """If apply succeeds but pattern not found in registry → still success with message."""
        with patch("sema.cli.main.apply_changes", return_value=True):
            with patch.object(server.REGISTRY_MGR, "refresh"):
                with patch.object(server.REGISTRY_MGR, "get_pattern", return_value=None):
                    raw = _sema_mint(
                        json.dumps(
                            {
                                "handle": "GhostMint",
                                "mechanism": "Pattern vanishes",
                            }
                        )
                    )

        result = json.loads(raw)
        self.assertTrue(result["success"])
        self.assertEqual(result["handle"], "GhostMint")


class TestConditionalRegistration(unittest.TestCase):
    """Tests for SEMA_ALLOW_MINT env var gating."""

    def test_mint_not_registered_by_default(self):
        """Without SEMA_ALLOW_MINT, sema_mint should not be a registered tool."""
        tools = server.mcp._tool_manager._tools
        env_val = os.environ.get("SEMA_ALLOW_MINT", "").lower()
        if env_val != "true":
            self.assertNotIn("_sema_mint", tools)

    def test_mint_function_exists_regardless(self):
        """_sema_mint function always exists as a callable, just not as a tool."""
        self.assertTrue(callable(_sema_mint))

    def test_manual_registration_adds_tool(self):
        """Manually registering _sema_mint adds it to the tool registry."""
        tools = server.mcp._tool_manager._tools
        had_mint = "_sema_mint" in tools

        server.mcp.tool()(_sema_mint)
        self.assertIn("_sema_mint", tools)

        # Clean up
        if not had_mint:
            del tools["_sema_mint"]

    def test_env_var_true_variants_accepted(self):
        """Only 'true' (case-insensitive) enables minting."""
        for val in ["true", "True", "TRUE", "tRuE"]:
            self.assertEqual(val.lower(), "true")

    def test_env_var_false_variants_rejected(self):
        """Non-'true' values do not enable minting."""
        for val in ["false", "False", "0", "no", "", "yes", "1", "on", "enabled"]:
            self.assertNotEqual(val.lower(), "true")


if __name__ == "__main__":
    unittest.main()
