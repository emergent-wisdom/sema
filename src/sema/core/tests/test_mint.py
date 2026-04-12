"""Integration tests for mint_pattern with a real temp GraphStore DB."""

import os
import shutil
import tempfile

import pytest

from sema.core.mint import MintResult, mint_pattern
from sema.taxonomy_graph.graph_store import GraphStore


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
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "ring": 0, "tier": 1},
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
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "ring": 0, "tier": 1},
        }
        result = mint_pattern(pattern, temp_store)
        assert result.success is False
        assert len(result.errors) > 0

    def test_invalid_handle_rejected(self, temp_store):
        """Pattern with invalid handle (lowercase) fails validation."""
        pattern = {
            "handle": "lowercase",
            "mechanism": "Bad handle.",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "ring": 0, "tier": 1},
        }
        result = mint_pattern(pattern, temp_store)
        assert result.success is False
        assert any("CamelCase" in e for e in result.errors)

    def test_warnings_propagated(self, temp_store):
        """Warnings from validation are propagated through result."""
        pattern = {
            "handle": "TestWarnings",
            "mechanism": "A test pattern.",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "ring": 0, "tier": 1},
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
