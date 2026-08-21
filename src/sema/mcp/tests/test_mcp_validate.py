"""Tests for the `sema_validate` MCP tool."""

import json
import unittest

try:
    from sema.mcp import server
except ModuleNotFoundError as exc:
    if exc.name == "mcp":
        raise unittest.SkipTest("mcp extra is not installed") from exc
    raise


class _StubRegistry:
    def __init__(self, handles: set[str] | None = None):
        self.registry = {handle: {} for handle in handles or set()}

    def refresh(self):
        pass


class TestSemaValidate(unittest.TestCase):
    def setUp(self):
        self.server = server
        self._real_registry = server.REGISTRY_MGR
        server.REGISTRY_MGR = _StubRegistry({"Task", "Result"})

    def tearDown(self):
        self.server.REGISTRY_MGR = self._real_registry

    def test_valid_current_schema_pattern_passes(self):
        pattern = {
            "handle": "MyPattern",
            "mechanism": "A concise mechanism.",
            "gloss": "One-line summary",
            "_meta": {
                "path": ["Mind", "Reasoning"],
                "ring": 1,
                "tier": 2,
            },
        }

        result = json.loads(self.server.sema_validate(json.dumps(pattern)))

        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])
        self.assertEqual(result["handle"], "MyPattern")

    def test_legacy_layer_category_meta_fails(self):
        pattern = {
            "handle": "MyPattern",
            "mechanism": "A concise mechanism.",
            "gloss": "One-line summary",
            "_meta": {
                "layer": "Mind",
                "category": "Reasoning",
                "ring": 1,
                "tier": 2,
            },
        }

        result = json.loads(self.server.sema_validate(json.dumps(pattern)))

        self.assertFalse(result["valid"])
        self.assertTrue(any("path" in err for err in result["errors"]))

    def test_missing_dependency_target_fails(self):
        missing_target_id = "sema:MissingTarget#mh:SHA-256:" + ("a" * 64)
        pattern = {
            "handle": "MyPattern",
            "mechanism": "Consumes {{missing_target}}.",
            "gloss": "One-line summary",
            "_meta": {
                "path": ["Mind", "Reasoning"],
                "ring": 1,
                "tier": 2,
            },
            "dependencies": {"accepts": {"missing_target": missing_target_id}},
        }

        result = json.loads(self.server.sema_validate(json.dumps(pattern)))

        self.assertFalse(result["valid"])
        self.assertTrue(any("MissingTarget" in err for err in result["errors"]))

    def test_invalid_json_fails(self):
        result = json.loads(self.server.sema_validate("{not-json"))

        self.assertFalse(result["valid"])
        self.assertTrue(any("Invalid JSON" in err for err in result["errors"]))

    def test_duplicate_json_member_fails(self):
        result = json.loads(
            self.server.sema_validate(
                '{"handle":"First","handle":"Second","mechanism":"A mechanism"}'
            )
        )

        self.assertFalse(result["valid"])
        self.assertTrue(any("duplicate key" in err for err in result["errors"]))

    def test_non_object_json_fails(self):
        result = json.loads(self.server.sema_validate("[]"))

        self.assertFalse(result["valid"])
        self.assertEqual(result["errors"], ["Pattern JSON must be an object"])

    def test_non_string_handles_fail_cleanly(self):
        for bad_handle in (1, None, ["Pattern"]):
            with self.subTest(handle=bad_handle):
                pattern = {
                    "handle": bad_handle,
                    "mechanism": "A mechanism.",
                    "_meta": {
                        "path": ["Infrastructure", "Primitives"],
                        "ring": 0,
                        "tier": 1,
                    },
                }
                result = json.loads(self.server.sema_validate(json.dumps(pattern)))
                self.assertFalse(result["valid"])
                self.assertTrue(result["errors"])


if __name__ == "__main__":
    unittest.main()
