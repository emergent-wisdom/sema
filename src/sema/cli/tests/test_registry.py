import unittest
from unittest.mock import patch

from sema.core.registry import RegistryManager, list_dbs


class TestRegistryManager(unittest.TestCase):
    def setUp(self):
        self.manager = RegistryManager()
        # clear any auto-loaded registry for pure unit testing
        self.manager.registry = {}
        if hasattr(self.manager, "_lower_map"):
            del self.manager._lower_map

    def test_stub_formatting(self):
        """Test that if sema_ref is missing, we construct Handle#stub."""
        mock_registry = {
            "Dynamic": {
                "handle": "Dynamic",
                "stub": "a1b2",  # Field used in patterns.json
                "mechanism": "Just a stub",
            },
            "Alt": {
                "handle": "Alt",
                "sema_stub": "c3d4",  # Field used in some contexts
                "mechanism": "Alt stub",
            },
        }
        self.manager.registry = mock_registry

        # Test Dynamic (using 'stub')
        res1 = self.manager.resolve_templates("{{Dynamic}}")
        self.assertEqual(res1, "Dynamic#a1b2")

        # Test Alt (using 'sema_stub')
        res2 = self.manager.resolve_templates("{{Alt}}")
        self.assertEqual(res2, "Alt#c3d4")

    def test_local_dependency_substitution(self):
        """
        Test that placeholders like {{source_content}} are resolved using the pattern's
        local 'dependencies' map (e.g. 'accepts' -> 'source_content'), not just global lookups.
        """
        mock_registry = {
            "Translate": {
                "handle": "Translate",
                "sema_ref": "Translate#123",  # Explicit sema_ref
                "mechanism": "Convert {{source_content}} using {{protocol}}.",
                "dependencies": {
                    "accepts": {"source_content": "Datum#cce3"},
                    "references": {"protocol": "Protocol#9e5e"},
                },
            },
            "Datum": {
                "handle": "Datum",
                "stub": "456",  # No sema_ref, should construct Datum#456
            },
            "Protocol": {
                "handle": "Protocol",
                "stub": "789",  # No sema_ref, should construct Protocol#789
            },
        }
        self.manager.registry = mock_registry

        # Fetch the pattern through the manager to trigger resolution
        translate = self.manager.get_pattern("Translate")
        mechanism = translate.get("mechanism", "")

        # Verify substitutions
        self.assertIn("Datum#456", mechanism, "{{source_content}} should resolve to Datum#456")
        self.assertIn("Protocol#789", mechanism, "{{protocol}} should resolve to Protocol#789")

        # Verify it didn't leave the raw placeholder
        self.assertNotIn("{{source_content}}", mechanism)
        self.assertNotIn("{{protocol}}", mechanism)

    def test_global_substitution_still_works(self):
        """Test that standard global substitutions (referencing a handle directly) still work."""
        mock_registry = {
            "Base": {"handle": "Base", "sema_ref": "sema:Base#mh:111", "mechanism": "I am base."},
            "Derived": {
                "handle": "Derived",
                "sema_ref": "sema:Derived#mh:222",
                "mechanism": "Extends {{Base}}.",
                # No local dependency named 'Base' defined in 'dependencies' map,
                # relies on global lookup.
                "dependencies": {},
            },
        }
        self.manager.registry = mock_registry

        derived = self.manager.get_pattern("Derived")
        self.assertIn("sema:Base#mh:111", derived["mechanism"])

    def test_local_overrides_global(self):
        """Test that a local dependency alias takes precedence over a global handle."""
        mock_registry = {
            "Common": {
                "handle": "Common",
                "sema_ref": "sema:Common#mh:Global",
                "mechanism": "Global Common",
            },
            "User": {
                "handle": "User",
                "sema_ref": "sema:User#mh:999",
                "mechanism": "Uses {{Common}}.",
                "dependencies": {
                    "references": {
                        # Map 'Common' locally to something else entirely.
                        # This proves we look at this dict before the global registry key "Common".
                        "Common": "sema:Special#mh:LocalOverride"
                    }
                },
            },
        }
        self.manager.registry = mock_registry

        # Here 'Common' in dependencies points to "sema:Special#mh:LocalOverride"
        # The resolution should pick this up from local context, ignoring that "Common" exists globally.
        user = self.manager.get_pattern("User")
        self.assertIn("sema:Special#mh:LocalOverride", user["mechanism"])
        self.assertNotIn("sema:Common#mh:Global", user["mechanism"])

    def test_underscore_keys_in_preconditions_postconditions(self):
        """
        Test that underscore-named keys like 'user_request' and 'final_outcome'
        in preconditions/postconditions are properly resolved to their target patterns.

        This was a regression where edge-based dependency loading used lowercase
        target handles as keys (e.g., 'message') instead of preserving the original
        placeholder names (e.g., 'user_request').
        """
        mock_registry = {
            "Message": {"handle": "Message", "sema_ref": "Message#047a", "mechanism": "A message."},
            "Outcome": {
                "handle": "Outcome",
                "sema_ref": "Outcome#cd52",
                "mechanism": "An outcome.",
            },
            "CreationProtocol": {
                "handle": "CreationProtocol",
                "sema_ref": "CreationProtocol#ae0f",
                "mechanism": "Orchestrates {{user_request}}.",
                "preconditions": ["{{user_request}} received", "Agent Team available"],
                "postconditions": ["{{final_outcome}} Shipped", "Process Logged"],
                "dependencies": {
                    "accepts": {
                        # Key is 'user_request', not 'message'
                        "user_request": "sema:Message#mh:SHA-256:abc123"
                    },
                    "yields": {
                        # Key is 'final_outcome', not 'outcome'
                        "final_outcome": "sema:Outcome#mh:SHA-256:def456"
                    },
                },
            },
        }
        self.manager.registry = mock_registry

        pattern = self.manager.get_pattern("CreationProtocol")

        # Check mechanism
        self.assertIn("Message#047a", pattern["mechanism"])
        self.assertNotIn("{{user_request}}", pattern["mechanism"])

        # Check preconditions - the key issue from the bug report
        self.assertIn("Message#047a received", pattern["preconditions"][0])
        self.assertNotIn("{{user_request}}", pattern["preconditions"][0])

        # Check postconditions
        self.assertIn("Outcome#cd52 Shipped", pattern["postconditions"][0])
        self.assertNotIn("{{final_outcome}}", pattern["postconditions"][0])


def test_environment_override_is_the_only_active_database(tmp_path, monkeypatch):
    configured = tmp_path / "configured.db"
    overridden = tmp_path / "overridden.db"
    configured.touch()
    overridden.touch()
    records = {
        str(configured): {"name": "configured", "path": str(configured)},
        str(overridden): {"name": "overridden", "path": str(overridden)},
    }
    monkeypatch.setenv("SEMA_DB_PATH", str(overridden))

    with (
        patch("sema.core.registry._get_active_db_config", return_value=str(configured)),
        patch("sema.core.registry.get_bundled_db_path", return_value=None),
        patch("sema.core.registry._load_db_registry", return_value=records),
    ):
        databases = list_dbs()

    assert [database["name"] for database in databases if database["active"]] == ["overridden"]


if __name__ == "__main__":
    unittest.main()
