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
import sqlite3
from pathlib import Path

import pytest

from sema.core.hashing import (
    _SEMANTIC_ROOT_DOMAIN,
    CATALOG_ROOT_SCHEME,
    SEMANTIC_ROOT_SCHEME,
    catalog_root,
    vocabulary_info,
    vocabulary_root,
    vocabulary_roots,
)
from sema.core.workspace import GraphWorkspace, WorkspaceSource


class TestVocabularyRootAlgorithm:
    def test_empty_list(self):
        assert (
            vocabulary_root([]) == "e3b0c44298fc1c149afbf4c8996fb924"
            "27ae41e4649b934ca495991b7852b855"
        )

    def test_single_hash(self):
        assert (
            vocabulary_root([f"{1:064x}"]) == "025b931007a145dea3053df291741cf0"
            "ca9f33a628ed6299b0f1f8a0b1e8f9bd"
        )

    @pytest.mark.parametrize(
        "count,expected",
        [
            (
                2,
                "532e24e8cb62180acbf6b6c3977836b5b188beb2e58f0a273a35700c43a52f55",
            ),
            (
                3,
                "c34a173de740cc9b710007b7a2b2d306c29cd362600a762670e97993eb5b25b0",
            ),
            (
                5,
                "658755f68548d2e7cef7724b848c4285b66b8e85fcd81a7b42296dfb3723c8c1",
            ),
        ],
    )
    def test_golden_vectors_cover_non_full_tree_shapes(self, count, expected):
        hashes = [f"{value:064x}" for value in range(1, count + 1)]
        assert vocabulary_root(hashes) == expected

    def test_order_independent(self):
        a, b = "a" * 64, "b" * 64
        assert vocabulary_root([a, b]) == vocabulary_root([b, a])

    def test_three_leaf_shape_promotes_instead_of_duplicating_last_leaf(self):
        digests = [bytes.fromhex(f"{value:064x}") for value in range(1, 4)]
        leaves = [
            hashlib.sha256(b"\x00" + _SEMANTIC_ROOT_DOMAIN + digest).digest() for digest in digests
        ]
        left = hashlib.sha256(b"\x01" + leaves[0] + leaves[1]).digest()
        promoted = hashlib.sha256(b"\x01" + left + leaves[2]).hexdigest()
        duplicated_right = hashlib.sha256(b"\x01" + leaves[2] + leaves[2]).digest()
        duplicated = hashlib.sha256(b"\x01" + left + duplicated_right).hexdigest()

        actual = vocabulary_root([digest.hex() for digest in digests])
        assert actual == promoted
        assert actual != duplicated

    def test_duplicate_definitions_have_set_semantics(self):
        a, b = "a" * 64, "b" * 64
        assert vocabulary_root([a, a, b]) == vocabulary_root([a, b])

    @pytest.mark.parametrize(
        "invalid",
        [
            "a" * 63,
            "a" * 65,
            "A" * 64,
            "g" * 64,
            " " + ("a" * 64),
            None,
            1,
        ],
    )
    def test_invalid_pattern_hash_fails_closed(self, invalid):
        with pytest.raises(ValueError, match="64 lowercase hexadecimal"):
            vocabulary_root([invalid])

    def test_catalog_root_is_order_independent(self):
        bindings = [("Alpha", "a" * 64), ("Bravo", "b" * 64)]
        expected = "962f1fd21af71e752a4c826a5e5dafc5d2c09182c87daed31280d0c4553e47eb"
        assert catalog_root(bindings) == expected
        assert catalog_root(bindings) == catalog_root(list(reversed(bindings)))

    def test_catalog_root_commits_to_handle_bindings(self):
        original = [("Alpha", "a" * 64), ("Bravo", "b" * 64)]
        swapped = [("Alpha", "b" * 64), ("Bravo", "a" * 64)]
        renamed = [("Alpha", "a" * 64), ("Charlie", "b" * 64)]
        assert catalog_root(original) != catalog_root(swapped)
        assert catalog_root(original) != catalog_root(renamed)

    def test_catalog_preserves_aliases_while_semantic_root_deduplicates(self):
        roots = vocabulary_roots([("Alpha", "a" * 64), ("Alias", "a" * 64)])
        assert roots["pattern_count"] == 2
        assert roots["definition_count"] == 1
        assert roots["semantic_root"] == vocabulary_root(["a" * 64])

    def test_duplicate_catalog_handle_fails_closed(self):
        with pytest.raises(ValueError, match="duplicate catalog handle"):
            catalog_root([("Alpha", "a" * 64), ("Alpha", "b" * 64)])

    def test_noncanonical_catalog_handle_fails_closed(self):
        with pytest.raises(ValueError, match="catalog handle"):
            catalog_root([("not a handle", "a" * 64)])


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
        assert workspace_root["catalog_root"] == db_fingerprint["catalog_root"]
        assert workspace_root["pattern_count"] == db_fingerprint["pattern_count"]

    def test_db_fingerprint_rejects_hashless_pattern(self, tmp_path):
        db_path = tmp_path / "hashless.db"
        con = sqlite3.connect(db_path)
        con.execute("CREATE TABLE nodes (text TEXT, metadata TEXT, node_type TEXT)")
        con.execute(
            "INSERT INTO nodes VALUES (?, ?, 'PATTERN')",
            ("Hashless", json.dumps({"pattern": {"mechanism": "m"}})),
        )
        con.commit()
        con.close()

        with pytest.raises(ValueError, match="Hashless.*invalid sema_id"):
            vocabulary_info(str(db_path))

    def test_db_fingerprint_rejects_misbound_sema_id(self, tmp_path):
        db_path = tmp_path / "misbound.db"
        con = sqlite3.connect(db_path)
        con.execute("CREATE TABLE nodes (text TEXT, metadata TEXT, node_type TEXT)")
        con.execute(
            "INSERT INTO nodes VALUES (?, ?, 'PATTERN')",
            (
                "Alpha",
                json.dumps(
                    {
                        "pattern": {
                            "sema_id": "sema:Bravo#mh:SHA-256:" + ("a" * 64),
                        }
                    }
                ),
            ),
        )
        con.commit()
        con.close()

        with pytest.raises(ValueError, match="does not match catalog handle"):
            vocabulary_info(str(db_path))

    def test_workspace_root_reads_database_rows_instead_of_collapsed_registry(self, tmp_path):
        db_path = tmp_path / "malformed-row.db"
        con = sqlite3.connect(db_path)
        con.execute("CREATE TABLE nodes (id INTEGER, text TEXT, metadata TEXT, node_type TEXT)")
        con.execute(
            "INSERT INTO nodes VALUES (1, ?, ?, 'PATTERN')",
            (
                "Alpha",
                json.dumps(
                    {
                        "pattern": {
                            "sema_id": "sema:Alpha#mh:SHA-256:" + ("a" * 64),
                        }
                    }
                ),
            ),
        )
        con.execute("INSERT INTO nodes VALUES (2, 'Broken', '{', 'PATTERN')")
        con.commit()
        con.close()

        workspace = GraphWorkspace(WorkspaceSource(db_path=str(db_path)))
        with pytest.raises(ValueError, match="Broken.*invalid metadata JSON"):
            workspace.vocabulary_root()

    def test_workspace_root_rejects_duplicate_database_handles(self, tmp_path):
        db_path = tmp_path / "duplicate-handle.db"
        con = sqlite3.connect(db_path)
        con.execute("CREATE TABLE nodes (id INTEGER, text TEXT, metadata TEXT, node_type TEXT)")
        for node_id, digest in enumerate(("a", "b"), start=1):
            con.execute(
                "INSERT INTO nodes VALUES (?, ?, ?, 'PATTERN')",
                (
                    node_id,
                    "Duplicate",
                    json.dumps(
                        {
                            "pattern": {
                                "sema_id": ("sema:Duplicate#mh:SHA-256:" + (digest * 64)),
                            }
                        }
                    ),
                ),
            )
        con.commit()
        con.close()

        workspace = GraphWorkspace(WorkspaceSource(db_path=str(db_path)))
        with pytest.raises(ValueError, match="duplicate catalog handle"):
            workspace.vocabulary_root()

    def test_workspace_root_rejects_missing_configured_database(self, tmp_path):
        missing_db = tmp_path / "missing.db"
        workspace = GraphWorkspace(WorkspaceSource(db_path=str(missing_db)))

        with pytest.raises(FileNotFoundError, match="workspace database not found"):
            workspace.vocabulary_root()


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
        self.expected_root = vocabulary_root(["a" * 64, "b" * 64, "c" * 64])
        self.expected_catalog_root = catalog_root(
            [
                ("Alpha", "a" * 64),
                ("Bravo", "b" * 64),
                ("Charlie", "c" * 64),
            ]
        )

    def teardown_method(self):
        self.mcp_server.REGISTRY_MGR = self._real_registry

    def test_sema_root_tool_returns_expected_hash(self):
        result = json.loads(self.mcp_server.sema_root())
        assert result["hash"] == self.expected_root
        assert result["stub"] == self.expected_root[:16]
        assert result["pattern_count"] == 3
        assert result["definition_count"] == 3
        assert result["root_scheme"] == SEMANTIC_ROOT_SCHEME
        assert result["catalog_root"] == self.expected_catalog_root
        assert result["catalog_root_scheme"] == CATALOG_ROOT_SCHEME
        assert result["full_sema_id"] == f"sema:vocab#mh:SHA-256:{self.expected_root}"

    def test_handshake_vocab_provide_hash(self):
        """No your_hash → PROVIDE_HASH with the canonical stub."""
        result = json.loads(self.mcp_server.sema_handshake(ref="vocab"))
        assert result["verdict"] == "PROVIDE_HASH"
        assert result["scope"] == "vocab"
        assert result["canonical_stub"] == self.expected_root[:16]
        assert result["pattern_count"] == 3
        assert result["definition_count"] == 3
        assert result["root_scheme"] == SEMANTIC_ROOT_SCHEME

    def test_handshake_vocab_proceed_with_stub(self):
        """16-char stub match → PROCEED."""
        result = json.loads(
            self.mcp_server.sema_handshake(
                ref="vocab",
                your_hash=self.expected_root[:16],
                your_scheme=SEMANTIC_ROOT_SCHEME,
            )
        )
        assert result["verdict"] == "PROCEED"
        assert result["assurance"] == "prefix"
        assert result["mode"] == "cooperative"
        assert result["scope"] == "vocab"
        assert result["pattern_count"] == 3

    def test_handshake_catalog_uses_handle_binding_root(self):
        challenge = json.loads(self.mcp_server.sema_handshake(ref="catalog"))
        assert challenge["scope"] == "catalog"
        assert challenge["canonical_stub"] == self.expected_catalog_root[:16]
        assert challenge["root_scheme"] == CATALOG_ROOT_SCHEME

        result = json.loads(
            self.mcp_server.sema_handshake(
                ref="catalog",
                your_hash=self.expected_catalog_root,
                your_scheme=CATALOG_ROOT_SCHEME,
            )
        )
        assert result["verdict"] == "PROCEED"
        assert result["scope"] == "catalog"

    def test_handshake_root_scheme_mismatch_requires_upgrade(self):
        result = json.loads(
            self.mcp_server.sema_handshake(
                ref="vocab",
                your_hash=self.expected_root,
                your_scheme="legacy-flat-root",
            )
        )
        assert result["verdict"] == "HALT"
        assert result["reason"] == "ROOT SCHEME MISMATCH"
        assert "Upgrade" in result["action"]

    def test_handshake_root_scheme_is_required_for_comparison(self):
        result = json.loads(
            self.mcp_server.sema_handshake(
                ref="vocab",
                your_hash=self.expected_root,
            )
        )
        assert result["verdict"] == "HALT"
        assert result["reason"] == "ROOT SCHEME REQUIRED"

    def test_empty_root_cannot_proceed_without_scheme_even_in_strict_mode(self):
        self.mcp_server.REGISTRY_MGR.registry = {}
        legacy_collision = hashlib.sha256(b"").hexdigest()
        result = json.loads(
            self.mcp_server.sema_handshake(
                ref="vocab",
                your_hash=legacy_collision,
                strict=True,
            )
        )
        assert result["verdict"] == "HALT"
        assert result["reason"] == "ROOT SCHEME REQUIRED"

    def test_handshake_vocab_proceed_with_full_hash(self):
        """64-char full hash match → also PROCEED."""
        result = json.loads(
            self.mcp_server.sema_handshake(
                ref="vocab",
                your_hash=self.expected_root,
                your_scheme=SEMANTIC_ROOT_SCHEME,
            )
        )
        assert result["verdict"] == "PROCEED"
        assert result["assurance"] == "full_hash"

    def test_handshake_vocab_strict_stub_requires_full_hash(self):
        result = json.loads(
            self.mcp_server.sema_handshake(
                ref="vocab",
                your_hash=self.expected_root[:16],
                strict=True,
                your_scheme=SEMANTIC_ROOT_SCHEME,
            )
        )

        assert result["verdict"] == "REQUIRE_FULL_HASH"
        assert result["mode"] == "strict"
        assert result["full_sema_id"].endswith(self.expected_root)

    def test_handshake_vocab_strict_full_hash_proceeds(self):
        result = json.loads(
            self.mcp_server.sema_handshake(
                ref="vocab",
                your_hash=self.expected_root,
                strict=True,
                your_scheme=SEMANTIC_ROOT_SCHEME,
            )
        )

        assert result["verdict"] == "PROCEED"
        assert result["assurance"] == "full_hash"
        assert result["mode"] == "strict"

    def test_handshake_vocab_halt_on_drift(self):
        """Wrong hash → HALT with drift message."""
        result = json.loads(
            self.mcp_server.sema_handshake(
                ref="vocab",
                your_hash="0" * 16,
                your_scheme=SEMANTIC_ROOT_SCHEME,
            )
        )
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
