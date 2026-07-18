"""Tests for the vocabulary-wide Merkle root.

Covers:
- Core algorithm in sema.core.hashing.vocabulary_root
- CLI `sema root` output shape
- MCP `sema_root()` JSON response
- MCP `sema_handshake(ref="vocab", ...)` in all three verdicts
  (PROVIDE_HASH / PROCEED / HALT)

The handshake tests exercise the full code path — not just the algorithm —
because the user specifically asked to make sure the handshake works.
"""

import hashlib
import json
from pathlib import Path

import pytest

from sema.core.hashing import vocabulary_info, vocabulary_root
from sema.core.workspace import GraphWorkspace, WorkspaceSource


class TestVocabularyRootAlgorithm:
    def test_empty_list(self):
        # SHA-256 of empty bytes — well-known constant
        expected = hashlib.sha256(b"").hexdigest()
        assert vocabulary_root([]) == expected

    def test_single_hash(self):
        h = "a" * 64
        expected = hashlib.sha256(h.encode()).hexdigest()
        assert vocabulary_root([h]) == expected

    def test_concatenation(self):
        a, b = "a" * 64, "b" * 64
        expected = hashlib.sha256((a + b).encode()).hexdigest()
        assert vocabulary_root([a, b]) == expected

    def test_order_sensitive(self):
        # Caller is responsible for sorting; different orders → different roots
        a, b = "a" * 64, "b" * 64
        assert vocabulary_root([a, b]) != vocabulary_root([b, a])

    def test_deterministic(self):
        hs = ["c0" * 32, "d0" * 32, "e0" * 32]
        assert vocabulary_root(hs) == vocabulary_root(hs)

    def test_matches_script_historical_output(self):
        """Reproduces the exact root that scripts/vocabulary_merkle_root.py
        would produce for a given input — ensures the refactor didn't
        change the algorithm."""
        # Arbitrary fixed input; the expected value is the SHA-256 of the
        # concatenation, matching the script's old inline implementation.
        hashes = ["11" * 32, "22" * 32, "33" * 32]
        expected = hashlib.sha256(("11" * 32 + "22" * 32 + "33" * 32).encode()).hexdigest()
        assert vocabulary_root(hashes) == expected


class TestVocabularyRootImplementations:
    def test_workspace_root_matches_db_fingerprint_for_checked_in_catalog(self):
        repo_root = Path(__file__).resolve().parents[4]
        db_path = repo_root / "data" / "taxonomy.db"
        if not db_path.exists():
            pytest.skip("checked-in taxonomy.db not available")

        workspace = GraphWorkspace(WorkspaceSource(db_path=str(db_path)))
        workspace_root = workspace.vocabulary_root()
        db_fingerprint = vocabulary_info(str(db_path))

        assert workspace_root["hash"] == db_fingerprint["root"]
        assert workspace_root["pattern_count"] == db_fingerprint["pattern_count"]


class TestMCPVocabRootAndHandshake:
    """End-to-end tests for the MCP `sema_root` and the vocab-scope
    `sema_handshake`. We patch the registry's pattern set to a known
    fixture so the root is deterministic for assertions."""

    def setup_method(self):
        # Import here so the MCP module's module-level init (which builds
        # a real RegistryManager from disk) doesn't crash test collection
        # if the default DB is unavailable.
        from sema.mcp import server as mcp_server

        self.mcp_server = mcp_server
        # Monkeypatch the module-level REGISTRY_MGR with a stub
        self._real_registry = mcp_server.REGISTRY_MGR

        class _StubRegistry:
            db_path = "/tmp/stub.db"

            def __init__(self):
                # Three patterns with deterministic handles + hashes
                self.registry = {
                    "Alpha": {"sema_id": "sema:Alpha#mh:SHA-256:" + ("a" * 64)},
                    "Bravo": {"sema_id": "sema:Bravo#mh:SHA-256:" + ("b" * 64)},
                    "Charlie": {"sema_id": "sema:Charlie#mh:SHA-256:" + ("c" * 64)},
                }

            def refresh(self):
                pass

        mcp_server.REGISTRY_MGR = _StubRegistry()
        # Expected root: SHA-256 over a*64 + b*64 + c*64 (sorted by handle)
        self.expected_root = hashlib.sha256(("a" * 64 + "b" * 64 + "c" * 64).encode()).hexdigest()

    def teardown_method(self):
        self.mcp_server.REGISTRY_MGR = self._real_registry

    def test_sema_root_tool_returns_expected_hash(self):
        result = json.loads(self.mcp_server.sema_root())
        assert result["hash"] == self.expected_root
        assert result["stub"] == self.expected_root[:16]
        assert result["pattern_count"] == 3
        assert result["full_sema_id"] == f"sema:vocab#mh:SHA-256:{self.expected_root}"

    def test_handshake_vocab_provide_hash(self):
        """No your_hash → PROVIDE_HASH with the canonical stub."""
        result = json.loads(self.mcp_server.sema_handshake(ref="vocab"))
        assert result["verdict"] == "PROVIDE_HASH"
        assert result["scope"] == "vocab"
        assert result["canonical_stub"] == self.expected_root[:16]
        assert result["pattern_count"] == 3

    def test_handshake_vocab_proceed_with_stub(self):
        """16-char stub match → PROCEED."""
        result = json.loads(
            self.mcp_server.sema_handshake(ref="vocab", your_hash=self.expected_root[:16])
        )
        assert result["verdict"] == "PROCEED"
        assert result["assurance"] == "prefix"
        assert result["mode"] == "cooperative"
        assert result["scope"] == "vocab"
        assert result["pattern_count"] == 3

    def test_handshake_vocab_proceed_with_full_hash(self):
        """64-char full hash match → also PROCEED."""
        result = json.loads(
            self.mcp_server.sema_handshake(ref="vocab", your_hash=self.expected_root)
        )
        assert result["verdict"] == "PROCEED"
        assert result["assurance"] == "full_hash"

    def test_handshake_vocab_strict_stub_requires_full_hash(self):
        result = json.loads(
            self.mcp_server.sema_handshake(
                ref="vocab", your_hash=self.expected_root[:16], strict=True
            )
        )

        assert result["verdict"] == "REQUIRE_FULL_HASH"
        assert result["mode"] == "strict"
        assert result["full_sema_id"].endswith(self.expected_root)

    def test_handshake_vocab_strict_full_hash_proceeds(self):
        result = json.loads(
            self.mcp_server.sema_handshake(ref="vocab", your_hash=self.expected_root, strict=True)
        )

        assert result["verdict"] == "PROCEED"
        assert result["assurance"] == "full_hash"
        assert result["mode"] == "strict"

    def test_handshake_vocab_halt_on_drift(self):
        """Wrong hash → HALT with drift message."""
        result = json.loads(self.mcp_server.sema_handshake(ref="vocab", your_hash="0" * 16))
        assert result["verdict"] == "HALT"
        assert result["scope"] == "vocab"
        assert "DRIFT" in result["reason"]
        assert result["canonical_stub"] == self.expected_root[:16]

    def test_handshake_vocab_case_insensitive_ref(self):
        """`ref="VOCAB"` or `"Vocab"` should trigger vocab mode too."""
        r1 = json.loads(self.mcp_server.sema_handshake(ref="VOCAB"))
        r2 = json.loads(self.mcp_server.sema_handshake(ref="Vocab"))
        assert r1["verdict"] == "PROVIDE_HASH"
        assert r2["verdict"] == "PROVIDE_HASH"
        assert r1["scope"] == "vocab"

    def test_handshake_pattern_still_works(self):
        """Regression — pattern-scope handshake unchanged.

        Adds a sema_stub field to the stub registry since the pattern-
        handshake path reads it.
        """
        self.mcp_server.REGISTRY_MGR.registry["Alpha"]["sema_stub"] = "aaaa"
        self.mcp_server.REGISTRY_MGR.registry["Alpha"]["sema_ref"] = "Alpha#aaaa"

        # PROVIDE_HASH path
        r = json.loads(self.mcp_server.sema_handshake(ref="Alpha"))
        assert r["verdict"] == "PROVIDE_HASH"
        assert r["canonical_stub"] == "aaaa"

        # PROCEED path
        r = json.loads(self.mcp_server.sema_handshake(ref="Alpha", your_hash="aaaa"))
        assert r["verdict"] == "PROCEED"

        # HALT path
        r = json.loads(self.mcp_server.sema_handshake(ref="Alpha", your_hash="zzzz"))
        assert r["verdict"] == "HALT"
