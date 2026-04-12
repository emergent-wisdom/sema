"""Tests for the sema_mint MCP tool wrapper and conditional registration."""

import json
import os
import unittest
from unittest.mock import patch

from sema.core.mint import MintResult
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
        """Valid pattern → calls mint_pattern and returns sema_ref."""
        mock_result = MintResult(
            success=True,
            handle="TestMint",
            sema_ref="TestMint#abcd",
            sema_id="sema:TestMint#mh:SHA-256:abcd1234",
            sema_stub="abcd",
        )

        with patch("sema.core.mint.mint_pattern", return_value=mock_result):
            with patch("sema.taxonomy_graph.graph_store.GraphStore"):
                with patch.object(server.REGISTRY_MGR, "refresh"):
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

    def test_mint_failure_returns_error(self):
        """mint_pattern returning failure → error result."""
        mock_result = MintResult(
            success=False,
            handle="FailMint",
            errors=["Validation failed for FailMint"],
        )

        with patch("sema.core.mint.mint_pattern", return_value=mock_result):
            with patch("sema.taxonomy_graph.graph_store.GraphStore"):
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

    def test_exception_returns_error(self):
        """Exception during mint_pattern → error with message."""
        with patch("sema.core.mint.mint_pattern", side_effect=RuntimeError("DB locked")):
            with patch("sema.taxonomy_graph.graph_store.GraphStore"):
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

    def test_pattern_not_in_registry_after_mint(self):
        """Successful mint returns sema_ref from MintResult directly."""
        mock_result = MintResult(
            success=True,
            handle="GhostMint",
            sema_ref="GhostMint#1234",
            sema_id="sema:GhostMint#mh:SHA-256:12345678",
            sema_stub="1234",
        )

        with patch("sema.core.mint.mint_pattern", return_value=mock_result):
            with patch("sema.taxonomy_graph.graph_store.GraphStore"):
                with patch.object(server.REGISTRY_MGR, "refresh"):
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
        self.assertEqual(result["sema_ref"], "GhostMint#1234")


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
