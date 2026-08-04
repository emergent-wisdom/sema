"""Integration tests for mint_pattern with a real temp GraphStore DB."""

import os
import shutil
import tempfile

import numpy as np
import pytest

from sema.core.mint import MintResult, mint_pattern
from sema.taxonomy_graph.graph_store import EdgeType, GraphStore


@pytest.fixture
def temp_store():
    """Create a temporary GraphStore for testing."""
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_mint.db")
    store = GraphStore(db_path)
    yield store
    shutil.rmtree(temp_dir)


class TestMintPattern:
    """Test mint_pattern in isolation."""

    def test_valid_pattern_mints_successfully(self, temp_store):
        """Valid pattern produces correct sema_ref."""
        pattern = {
            "handle": "TestMint",
            "mechanism": "A test pattern for minting.",
            "gloss": "Test mint",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        result = mint_pattern(pattern, temp_store)
        assert result.success is True
        assert result.handle == "TestMint"
        assert result.sema_ref.startswith("TestMint#")
        assert result.sema_id.startswith("sema:TestMint#mh:SHA-256:")
        assert len(result.sema_stub) == 4
        assert result.errors == []

    def test_missing_mechanism_rejected(self, temp_store):
        """Pattern without mechanism fails validation."""
        pattern = {
            "handle": "NoMechanism",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        result = mint_pattern(pattern, temp_store)
        assert result.success is False
        assert len(result.errors) > 0

    def test_invalid_handle_rejected(self, temp_store):
        """Pattern with invalid handle (lowercase) fails validation."""
        pattern = {
            "handle": "lowercase",
            "mechanism": "Bad handle.",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        result = mint_pattern(pattern, temp_store)
        assert result.success is False
        assert any("CamelCase" in e for e in result.errors)

    def test_missing_extends_parent_rejected(self, temp_store):
        pattern = {
            "handle": "Child",
            "mechanism": "A specialised pattern.",
            "extends": "sema:MissingParent#mh:SHA-256:" + ("a" * 64),
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }

        result = mint_pattern(pattern, temp_store)

        assert result.success is False
        assert result.errors == ["Missing extends target: MissingParent"]

    def test_existing_parent_handle_with_unknown_version_is_rejected(self, temp_store):
        temp_store.embedding_service.get_embedding = lambda _text: np.zeros(384, dtype=np.float32)
        parent = {
            "handle": "Parent",
            "mechanism": "The active parent definition.",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        assert mint_pattern(parent, temp_store).success is True
        child = {
            "handle": "Child",
            "mechanism": "A specialised pattern.",
            "extends": "sema:Parent#mh:SHA-256:" + ("b" * 64),
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }

        result = mint_pattern(child, temp_store)

        assert result.success is False
        assert "Unresolvable extends target" in result.errors[0]

    def test_legacy_derived_from_is_read_without_new_relation_semantics(self, temp_store):
        temp_store.embedding_service.get_embedding = lambda _text: np.zeros(384, dtype=np.float32)
        legacy = {
            "handle": "LegacyChild",
            "mechanism": "A pre-0.4 card.",
            "derived_from": "sema:RetiredParent",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }

        result = mint_pattern(legacy, temp_store)

        assert result.success is True
        child_id = temp_store._find_pattern_id("LegacyChild")
        assert not any(
            edge.get("edge_type") == EdgeType.IS_A
            for target in temp_store.graph.successors(child_id)
            for edge in temp_store._edges_between(child_id, target)
        )

    def test_null_legacy_key_is_rejected_before_graph_mutation(self, temp_store):
        temp_store.embedding_service.get_embedding = lambda _text: np.zeros(384, dtype=np.float32)
        parent = {
            "handle": "Parent",
            "mechanism": "The parent definition.",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        parent_result = mint_pattern(parent, temp_store)
        child = {
            "handle": "Child",
            "mechanism": "A malformed child.",
            "extends": parent_result.sema_id,
            "derived_from": None,
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }

        result = temp_store.add_pattern(child)

        assert result["success"] is False
        assert "both extends and legacy derived_from" in result["error"]
        assert temp_store._find_pattern_id("Child") is None

    def test_direct_parent_update_cannot_strand_exact_child(self, temp_store):
        temp_store.embedding_service.get_embedding = lambda _text: np.zeros(384, dtype=np.float32)
        parent = {
            "handle": "Parent",
            "mechanism": "The first parent definition.",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        parent_result = mint_pattern(parent, temp_store)
        child = {
            "handle": "Child",
            "mechanism": "A specialised child.",
            "extends": parent_result.sema_id,
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        assert mint_pattern(child, temp_store).success is True

        updated_parent = {**parent, "mechanism": "The second parent definition."}
        result = mint_pattern(updated_parent, temp_store)

        assert result.success is False
        assert "would strand exact `extends`" in result.errors[0]
        assert temp_store.get_pattern_hash("Parent") == parent_result.sema_id.rsplit(":", 1)[-1]

    def test_direct_extends_mint_rejects_mixed_dependency_cycle(self, temp_store):
        temp_store.embedding_service.get_embedding = lambda _text: np.zeros(384, dtype=np.float32)
        beta = {
            "handle": "Beta",
            "mechanism": "The initial beta definition.",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        beta_result = mint_pattern(beta, temp_store)
        alpha = {
            "handle": "Alpha",
            "mechanism": "Uses {{beta}}.",
            "dependencies": {"references": {"beta": beta_result.sema_id}},
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        alpha_result = mint_pattern(alpha, temp_store)
        updated_beta = {**beta, "extends": alpha_result.sema_id}

        result = mint_pattern(updated_beta, temp_store)

        assert result.success is False
        assert "Cycle detected" in result.errors[0]
        assert temp_store.get_pattern_hash("Beta") == beta_result.sema_id.rsplit(":", 1)[-1]

    def test_store_rejects_bare_extends_reference_when_validation_is_bypassed(self, temp_store):
        child = {
            "handle": "Child",
            "mechanism": "A specialised pattern.",
            "extends": "Parent",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }

        result = temp_store.add_pattern(child)

        assert result["success"] is False
        assert result["error"] == "Invalid extends reference: expected full sema_id"

    def test_store_rejects_non_string_extends_when_validation_is_bypassed(self, temp_store):
        child = {
            "handle": "Child",
            "mechanism": "A specialised pattern.",
            "extends": 42,
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }

        result = temp_store.add_pattern(child)

        assert result["success"] is False
        assert result["error"] == "Invalid extends reference: expected full sema_id"

    def test_store_rejects_self_extends_when_validation_is_bypassed(self, temp_store):
        child = {
            "handle": "Child",
            "mechanism": "A specialised pattern.",
            "extends": "sema:Child#mh:SHA-256:" + ("a" * 64),
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }

        result = temp_store.add_pattern(child)

        assert result["success"] is False
        assert result["error"] == "Pattern 'Child' cannot extend itself"

    def test_warnings_propagated(self, temp_store):
        """Warnings from validation are propagated through result."""
        pattern = {
            "handle": "TestWarnings",
            "mechanism": "A test pattern.",
            "_meta": {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 1},
        }
        result = mint_pattern(pattern, temp_store)
        assert result.success is True
        # warnings field exists (may be empty for a clean pattern)
        assert isinstance(result.warnings, list)

    def test_result_dataclass_fields(self, temp_store):
        """MintResult has all expected fields."""
        result = MintResult(success=False, handle="X", errors=["err"])
        assert result.success is False
        assert result.handle == "X"
        assert result.sema_ref == ""
        assert result.sema_id == ""
        assert result.sema_stub == ""
        assert result.errors == ["err"]
        assert result.warnings == []
