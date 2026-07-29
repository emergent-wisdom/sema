"""Tests for the multi-agent negotiation primitives.

Fills coverage gaps for:
- Per-pattern `sema_handshake` paths not covered by the vocab-root PR
  (unknown handle, embedded ref stub, your_hash + ref_stub precedence)
- `_compute_context_hash` algorithm — determinism, order-independence,
  digest length, empty set
- `sema_propose_context` + `sema_verify_context` end-to-end (matching,
  mismatched, missing handles)

Before this module, these tools shipped in production untested.
"""

import hashlib
import json

from sema.core.actions import _compute_context_hash
from sema.core.hashing import CATALOG_ROOT_SCHEME

# ───── Stub registry shared by the MCP-level tests ───────────────────────────


class _StubRegistry:
    """Drop-in for `sema.mcp.server.REGISTRY_MGR` with controllable content.

    Callers can override `self.registry` per-test to shape inputs.
    """

    db_path = "/tmp/stub-negotiation.db"

    def __init__(self):
        self.registry = {}

    def refresh(self):
        pass


def _install_stub(mcp_server, registry: dict) -> "_StubRegistry":
    """Swap in a stub registry with the given patterns; return it for teardown."""
    stub = _StubRegistry()
    stub.registry = registry
    mcp_server.REGISTRY_MGR = stub
    return stub


def _patched_get_pattern(registry: dict):
    """Simulate `RegistryManager.get_pattern`, which both context tools use."""

    def get(handle: str):
        return registry.get(handle)

    return get


# ───── Per-pattern handshake: gaps from the vocab-root PR ────────────────────


class TestHandshakePatternGaps:
    def setup_method(self):
        from sema.mcp import server as mcp_server

        self.mcp_server = mcp_server
        self._real = mcp_server.REGISTRY_MGR
        _install_stub(
            mcp_server,
            {
                "Alpha": {
                    "sema_stub": "aaaa",
                    "sema_ref": "Alpha#aaaa",
                    "sema_id": "sema:Alpha#mh:SHA-256:" + ("a" * 64),
                    "invariants": ["must-be-atomic"],
                    "tier": 1,
                }
            },
        )

    def teardown_method(self):
        self.mcp_server.REGISTRY_MGR = self._real

    def test_unknown_handle_halts(self):
        """Pattern not in vocabulary → HALT with 'Cannot coordinate'."""
        r = json.loads(self.mcp_server.sema_handshake(ref="NonexistentPattern"))
        assert r["verdict"] == "HALT"
        assert "NonexistentPattern" in r["reason"]
        assert "Cannot coordinate" in r["action"]

    def test_embedded_ref_stub_is_honored(self):
        """`sema_handshake(ref="Alpha#aaaa")` with no your_hash should PROCEED.

        The code at mcp/server.py:503 does `compare_hash = your_hash or ref_stub`,
        so the stub embedded in the ref becomes the comparison value.
        """
        r = json.loads(self.mcp_server.sema_handshake(ref="Alpha#aaaa"))
        assert r["verdict"] == "PROCEED"
        assert r["handle"] == "Alpha"

        # Wrong embedded stub → HALT
        r = json.loads(self.mcp_server.sema_handshake(ref="Alpha#zzzz"))
        assert r["verdict"] == "HALT"
        assert r["your_hash"] == "zzzz"
        assert r["canonical_hash"] == "aaaa"

    def test_your_hash_wins_over_ref_stub(self):
        """If both an embedded ref_stub AND your_hash are provided, your_hash
        is preferred. Code: `compare_hash = your_hash or ref_stub`.
        """
        # ref has wrong stub, but your_hash is correct → PROCEED
        r = json.loads(self.mcp_server.sema_handshake(ref="Alpha#zzzz", your_hash="aaaa"))
        assert r["verdict"] == "PROCEED"


# ───── Algorithm: _compute_context_hash ──────────────────────────────────────


class TestComputeContextHash:
    """Pure-function tests for the context digest."""

    @staticmethod
    def _mk(handle: str, mechanism: str, gloss: str = "gloss") -> dict:
        digest = hashlib.sha256(f"{mechanism}\x00{gloss}".encode()).hexdigest()
        return {
            "mechanism": mechanism,
            "gloss": gloss,
            "sema_id": f"sema:{handle}#mh:SHA-256:{digest}",
        }

    def test_deterministic(self):
        a = self._mk("Alpha", "mech-a")
        b = self._mk("Bravo", "mech-b")
        handles = ["Alpha", "Bravo"]
        assert _compute_context_hash([a, b], handles) == _compute_context_hash([a, b], handles)

    def test_order_independent(self):
        """Order-independence is the defining property — two agents submitting
        the same SET in different orders must produce the same digest."""
        a = self._mk("Alpha", "mech-a")
        b = self._mk("Bravo", "mech-b")
        c = self._mk("Charlie", "mech-c")
        expected = _compute_context_hash([a, b, c], ["Alpha", "Bravo", "Charlie"])
        assert expected == _compute_context_hash([c, a, b], ["Charlie", "Alpha", "Bravo"])
        assert expected == _compute_context_hash([b, c, a], ["Bravo", "Charlie", "Alpha"])

    def test_different_sets_give_different_digests(self):
        a = self._mk("Alpha", "mech-a")
        b = self._mk("Bravo", "mech-b")
        c = self._mk("Charlie", "mech-c")
        assert _compute_context_hash([a, b], ["Alpha", "Bravo"]) != _compute_context_hash(
            [a, c], ["Alpha", "Charlie"]
        )

    def test_swapped_handle_bindings_give_different_digests(self):
        first = [
            {"sema_id": "sema:Alpha#mh:SHA-256:" + ("a" * 64)},
            {"sema_id": "sema:Bravo#mh:SHA-256:" + ("b" * 64)},
        ]
        swapped = [
            {"sema_id": "sema:Alpha#mh:SHA-256:" + ("b" * 64)},
            {"sema_id": "sema:Bravo#mh:SHA-256:" + ("a" * 64)},
        ]
        handles = ["Alpha", "Bravo"]
        assert _compute_context_hash(first, handles) != _compute_context_hash(swapped, handles)

    def test_digest_length_defaults_to_8_hex_chars(self):
        """The tool doc advertises a 32-bit digest (8 hex chars)."""
        digest = _compute_context_hash([self._mk("Fixture", "x")], ["Fixture"])
        assert len(digest) == 8
        # All hex characters
        assert all(c in "0123456789abcdef" for c in digest)

    def test_digest_length_configurable(self):
        pattern = self._mk("Fixture", "x")
        digest_full = _compute_context_hash([pattern], ["Fixture"], stub_length=64)
        digest_short = _compute_context_hash([pattern], ["Fixture"], stub_length=8)
        assert len(digest_full) == 64
        assert digest_full.startswith(digest_short)

    def test_empty_list(self):
        """Degenerate case: empty list hashes the empty string → well-known
        SHA-256 prefix `e3b0c442`."""
        digest = _compute_context_hash([], [])
        assert digest == "e3b0c442"

    def test_content_address_is_the_only_leaf_input(self):
        """Overlays cannot affect a context root once the pattern ID is fixed."""
        sema_id = "sema:Fixture#mh:SHA-256:" + ("a" * 64)
        p1 = {"sema_id": sema_id, "_meta": {"layer": "Physics"}}
        p2 = {"sema_id": sema_id, "_meta": {"layer": "Mind"}}
        p3 = {"sema_id": sema_id, "sema_stub": "beef"}
        assert _compute_context_hash([p1], ["Fixture"]) == _compute_context_hash([p2], ["Fixture"])
        assert _compute_context_hash([p1], ["Fixture"]) == _compute_context_hash([p3], ["Fixture"])

    def test_missing_content_address_fails_closed(self):
        try:
            _compute_context_hash([{"mechanism": "unaddressed"}], ["Fixture"])
        except ValueError as exc:
            assert "invalid sema_id" in str(exc)
        else:
            raise AssertionError("hashless context pattern must be rejected")


# ───── End-to-end: sema_propose_context → sema_verify_context ────────────────


class TestContextNegotiation:
    """Drives the MCP tools against a controlled stub registry."""

    def setup_method(self):
        from sema.mcp import server as mcp_server

        self.mcp_server = mcp_server
        self._real = mcp_server.REGISTRY_MGR

        # Three patterns with distinct mechanisms so hashes differ
        registry = {
            "Gate": {
                "mechanism": "gate-mech",
                "gloss": "allow-or-block",
                "sema_id": "sema:Gate#mh:SHA-256:" + ("a" * 64),
                "sema_ref": "Gate#aaaa",
            },
            "Vote": {
                "mechanism": "vote-mech",
                "gloss": "tally",
                "sema_id": "sema:Vote#mh:SHA-256:" + ("b" * 64),
                "sema_ref": "Vote#bbbb",
            },
            "Task": {
                "mechanism": "task-mech",
                "gloss": "unit-of-work",
                "sema_id": "sema:Task#mh:SHA-256:" + ("c" * 64),
                "sema_ref": "Task#cccc",
            },
        }
        stub = _install_stub(mcp_server, registry)
        # Patch the registry so `sema_propose_context` and `sema_verify_context`
        # can resolve handles. The MCP tools call REGISTRY_MGR.get_pattern(clean).
        stub.get_pattern = _patched_get_pattern(registry)

    def teardown_method(self):
        self.mcp_server.REGISTRY_MGR = self._real

    def test_propose_then_verify_matches(self):
        """Happy path — A proposes, B verifies with the same handles → PROCEED."""
        handles = ["Gate", "Vote"]

        proposed = json.loads(self.mcp_server.sema_propose_context(handles))
        assert "context_hash" in proposed
        digest = proposed["context_hash"]
        assert proposed["count"] == 2
        assert proposed["root_scheme"] == CATALOG_ROOT_SCHEME

        verified = json.loads(
            self.mcp_server.sema_verify_context(
                handles,
                digest,
                remote_scheme=proposed["root_scheme"],
            )
        )
        assert verified["verdict"] == "PROCEED"
        assert verified["count"] == 2
        assert verified["root_scheme"] == CATALOG_ROOT_SCHEME

    def test_verify_different_digest_halts(self):
        """B sends wrong remote_hash → HALT with drift message."""
        handles = ["Gate", "Vote"]
        r = json.loads(
            self.mcp_server.sema_verify_context(
                handles,
                remote_hash="deadbeef",
                remote_scheme=CATALOG_ROOT_SCHEME,
            )
        )
        assert r["verdict"] == "HALT"
        assert r["reason"] == "Context digest mismatch"
        assert r["remote_hash"] == "deadbeef"
        # Local hash must be present for manual debugging
        assert "local_hash" in r
        assert r["local_hash"] != "deadbeef"

    def test_verify_different_root_scheme_halts_before_comparison(self):
        r = json.loads(
            self.mcp_server.sema_verify_context(
                ["Gate"],
                remote_hash="irrelevant",
                remote_scheme="legacy-flat-root",
            )
        )
        assert r["verdict"] == "HALT"
        assert r["reason"] == "ROOT SCHEME MISMATCH"
        assert r["root_scheme"] == CATALOG_ROOT_SCHEME

    def test_verify_missing_root_scheme_halts_before_comparison(self):
        r = json.loads(self.mcp_server.sema_verify_context(["Gate"], remote_hash="irrelevant"))
        assert r["verdict"] == "HALT"
        assert r["reason"] == "ROOT SCHEME REQUIRED"
        assert r["root_scheme"] == CATALOG_ROOT_SCHEME

    def test_missing_handle_halts_on_propose(self):
        """Propose with an unknown handle → HALT with `missing` populated."""
        r = json.loads(self.mcp_server.sema_propose_context(["Gate", "Nonexistent"]))
        assert r["verdict"] == "HALT"
        assert r["reason"] == "Patterns not found"
        assert "Nonexistent" in r["missing"]
        assert "Gate" not in r.get("missing", [])

    def test_hashless_context_pattern_returns_structured_halt(self):
        del self.mcp_server.REGISTRY_MGR.registry["Gate"]["sema_id"]
        r = json.loads(self.mcp_server.sema_propose_context(["Gate"]))
        assert r["verdict"] == "HALT"
        assert r["reason"] == "Invalid context identity"
        assert "invalid sema_id" in r["error"]

    def test_missing_handle_halts_on_verify(self):
        """Verify with an unknown handle → HALT before digest comparison."""
        r = json.loads(
            self.mcp_server.sema_verify_context(
                ["Gate", "Nonexistent"],
                remote_hash="whatever",
                remote_scheme=CATALOG_ROOT_SCHEME,
            )
        )
        assert r["verdict"] == "HALT"
        assert r["reason"] == "Patterns not found locally"
        assert "Nonexistent" in r["missing"]

    def test_propose_is_order_independent(self):
        """Two agents proposing the same SET in different orders get the
        same digest — the algorithm's core invariant."""
        r1 = json.loads(self.mcp_server.sema_propose_context(["Gate", "Vote", "Task"]))
        r2 = json.loads(self.mcp_server.sema_propose_context(["Task", "Gate", "Vote"]))
        assert r1["context_hash"] == r2["context_hash"]
