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

import json

from sema.core.actions import _compute_context_hash

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
    def _mk(mechanism: str, gloss: str = "gloss") -> dict:
        return {"mechanism": mechanism, "gloss": gloss}

    def test_deterministic(self):
        a = self._mk("mech-a")
        b = self._mk("mech-b")
        assert _compute_context_hash([a, b]) == _compute_context_hash([a, b])

    def test_order_independent(self):
        """Order-independence is the defining property — two agents submitting
        the same SET in different orders must produce the same digest."""
        a = self._mk("mech-a")
        b = self._mk("mech-b")
        c = self._mk("mech-c")
        assert _compute_context_hash([a, b, c]) == _compute_context_hash([c, a, b])
        assert _compute_context_hash([a, b, c]) == _compute_context_hash([b, c, a])

    def test_different_sets_give_different_digests(self):
        a = self._mk("mech-a")
        b = self._mk("mech-b")
        c = self._mk("mech-c")
        assert _compute_context_hash([a, b]) != _compute_context_hash([a, c])

    def test_digest_length_defaults_to_8_hex_chars(self):
        """The tool doc advertises a 32-bit digest (8 hex chars)."""
        digest = _compute_context_hash([self._mk("x")])
        assert len(digest) == 8
        # All hex characters
        assert all(c in "0123456789abcdef" for c in digest)

    def test_digest_length_configurable(self):
        digest_full = _compute_context_hash([self._mk("x")], stub_length=64)
        digest_short = _compute_context_hash([self._mk("x")], stub_length=8)
        assert len(digest_full) == 64
        assert digest_full.startswith(digest_short)

    def test_empty_list(self):
        """Degenerate case: empty list hashes the empty string → well-known
        SHA-256 prefix `e3b0c442`."""
        digest = _compute_context_hash([])
        assert digest == "e3b0c442"

    def test_semantic_fields_only(self):
        """Metadata (_meta, sema_ref, etc.) must not affect the digest —
        two patterns with identical semantic fields but different metadata
        should hash to the same thing."""
        p1 = {"mechanism": "m", "gloss": "g", "_meta": {"layer": "Physics"}}
        p2 = {"mechanism": "m", "gloss": "g", "_meta": {"layer": "Mind"}}
        p3 = {"mechanism": "m", "gloss": "g", "sema_stub": "beef"}
        assert _compute_context_hash([p1]) == _compute_context_hash([p2])
        assert _compute_context_hash([p1]) == _compute_context_hash([p3])


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
                "sema_ref": "Gate#aaaa",
            },
            "Vote": {
                "mechanism": "vote-mech",
                "gloss": "tally",
                "sema_ref": "Vote#bbbb",
            },
            "Task": {
                "mechanism": "task-mech",
                "gloss": "unit-of-work",
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

        verified = json.loads(self.mcp_server.sema_verify_context(handles, digest))
        assert verified["verdict"] == "PROCEED"
        assert verified["count"] == 2

    def test_verify_different_digest_halts(self):
        """B sends wrong remote_hash → HALT with drift message."""
        handles = ["Gate", "Vote"]
        r = json.loads(self.mcp_server.sema_verify_context(handles, remote_hash="deadbeef"))
        assert r["verdict"] == "HALT"
        assert r["reason"] == "Context digest mismatch"
        assert r["remote_hash"] == "deadbeef"
        # Local hash must be present for manual debugging
        assert "local_hash" in r
        assert r["local_hash"] != "deadbeef"

    def test_missing_handle_halts_on_propose(self):
        """Propose with an unknown handle → HALT with `missing` populated."""
        r = json.loads(self.mcp_server.sema_propose_context(["Gate", "Nonexistent"]))
        assert r["verdict"] == "HALT"
        assert r["reason"] == "Patterns not found"
        assert "Nonexistent" in r["missing"]
        assert "Gate" not in r.get("missing", [])

    def test_missing_handle_halts_on_verify(self):
        """Verify with an unknown handle → HALT before digest comparison."""
        r = json.loads(
            self.mcp_server.sema_verify_context(["Gate", "Nonexistent"], remote_hash="whatever")
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
