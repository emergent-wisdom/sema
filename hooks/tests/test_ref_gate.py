"""Tests for the Claude Code ref-gate hook (hooks/ref_gate.py).

The gate runs as a standalone script, so it is loaded here via importlib and
driven in-process: stdin is monkeypatched with a hook payload, MODE with the
gate mode, and the registry is a temp DB with one pattern minted through the
real mint pipeline — the canonical stub is an honest content hash, not a
hardcoded fixture.

Covers:
- verdict behavior per mode (KNOWN pass, STALE block/warn, UNKNOWN note)
- the JSON-escaping regression: refs at line starts arrive as ``\\n<Handle>``
  on the wire, which destroys the ``\\b`` word boundary — the gate must scan
  decoded string values, not raw bytes (found live in the babel-hook pilot)
- fail-open when the registry is unavailable
- the SEMA_REF_GATE_LOG verdict log
"""

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

GATE_PATH = Path(__file__).parent.parent / "ref_gate.py"

_spec = importlib.util.spec_from_file_location("ref_gate", GATE_PATH)
ref_gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ref_gate)

HANDLE = "InclusivePaymentThreshold"

# A known-valid pattern (passes the pydantic mint schema); also used by the
# sema-evals babel-hook pilot.
PATTERN = {
    "handle": HANDLE,
    "mechanism": "Compare the integer payment amount with the configured minimum before accepting the task.",
    "gloss": "An inclusive minimum payment threshold in token base units.",
    "invariants": [
        "A payment of exactly 100000000 base units is accepted.",
        "A payment below 100000000 base units is rejected.",
    ],
    "parameters": [
        {
            "name": "minimum_base_units",
            "type": "integer",
            "range": [100000000],
            "value": 100000000,
            "description": "Minimum accepted payment in token base units.",
        },
        {
            "name": "comparison",
            "type": "enum",
            "range": ["greater-than-or-equal", "greater-than"],
            "value": "greater-than-or-equal",
            "description": "Comparator applied at the payment boundary.",
        },
    ],
    "failure_modes": [
        "Replacing the inclusive comparison with a strict comparison rejects the boundary value."
    ],
    "_meta": {"path": ["Society", "Protocols"], "ring": 2, "tier": 3},
}


@pytest.fixture(scope="session")
def registry(tmp_path_factory):
    """Temp registry DB with PATTERN minted; returns (db_path, canonical_stub)."""
    from sema.core.mint import mint_pattern
    from sema.taxonomy_graph.graph_store import GraphStore

    db_path = tmp_path_factory.mktemp("ref-gate") / "canon.db"
    result = mint_pattern(PATTERN, GraphStore(str(db_path)))
    assert result.success, result.errors
    stub = result.sema_ref.split("#")[1]
    return db_path, stub


def stale_stub(canonical: str) -> str:
    """A syntactically valid 4-hex stub guaranteed to differ from canonical."""
    return "0000" if canonical != "0000" else "0001"


def payload_with(prompt: str) -> str:
    return json.dumps(
        {"session_id": "test", "hook_event_name": "UserPromptSubmit", "prompt": prompt}
    )


def run_gate(monkeypatch, capsys, stdin_text, mode, db=None, log=None):
    monkeypatch.setattr(ref_gate, "MODE", mode)
    for var, value in (("SEMA_REF_GATE_DB", db), ("SEMA_REF_GATE_LOG", log)):
        if value is not None:
            monkeypatch.setenv(var, str(value))
        else:
            monkeypatch.delenv(var, raising=False)
    monkeypatch.setattr(sys, "stdin", io.StringIO(stdin_text))
    code = ref_gate.main()
    captured = capsys.readouterr()
    return code, captured.out, captured.err


class TestVerdicts:
    def test_known_ref_passes_silently(self, registry, monkeypatch, capsys):
        db, stub = registry
        code, out, err = run_gate(
            monkeypatch, capsys, payload_with(f"Implement per {HANDLE}#{stub}."), "enforce", db=db
        )
        assert code == 0
        assert out == "" and err == ""

    def test_stale_ref_blocks_in_enforce(self, registry, monkeypatch, capsys):
        db, stub = registry
        bad = stale_stub(stub)
        code, out, err = run_gate(
            monkeypatch, capsys, payload_with(f"Implement per {HANDLE}#{bad}."), "enforce", db=db
        )
        assert code == 2
        assert "STALE" in err
        assert f"{HANDLE}#{bad}" in err
        assert f"#{stub}" in err  # repair message carries the canonical stub
        assert "sema_handshake" in err

    def test_stale_ref_warns_but_passes_in_warn(self, registry, monkeypatch, capsys):
        db, stub = registry
        bad = stale_stub(stub)
        code, out, err = run_gate(
            monkeypatch, capsys, payload_with(f"Implement per {HANDLE}#{bad}."), "warn", db=db
        )
        assert code == 0
        assert "STALE" in out  # stdout: model-visible context, never a block
        assert err == ""

    def test_off_mode_never_blocks(self, registry, monkeypatch, capsys):
        db, stub = registry
        bad = stale_stub(stub)
        code, out, err = run_gate(
            monkeypatch, capsys, payload_with(f"Implement per {HANDLE}#{bad}."), "off", db=db
        )
        assert code == 0
        assert out == "" and err == ""

    def test_unknown_handle_notes_but_passes(self, registry, monkeypatch, capsys):
        db, _ = registry
        code, out, err = run_gate(
            monkeypatch,
            capsys,
            payload_with("Fix regression from PR#12ab please."),
            "enforce",
            db=db,
        )
        assert code == 0
        assert "PR#12ab" in out  # noted as unrecognized, never blocked
        assert err == ""

    def test_no_refs_is_a_noop(self, registry, monkeypatch, capsys):
        db, _ = registry
        code, out, err = run_gate(
            monkeypatch, capsys, payload_with("No refs anywhere in this prompt."), "enforce", db=db
        )
        assert code == 0
        assert out == "" and err == ""


class TestPayloadDecoding:
    def test_ref_at_line_start_survives_json_escaping(self, registry, monkeypatch, capsys):
        """Regression: ``\\n`` before a ref fuses with the handle in raw wire
        bytes, killing the word boundary. Scanning decoded strings must catch it."""
        db, stub = registry
        bad = stale_stub(stub)
        prompt = f"Authoritative pattern:\n{HANDLE}#{bad}\nImplement accordingly."
        # The buggy raw-bytes scan misses this exact payload: \n escaping fuses
        # "n" with the handle, so no \b boundary exists on the wire form.
        assert not ref_gate.REF_RE.findall(payload_with(prompt))
        code, _, err = run_gate(monkeypatch, capsys, payload_with(prompt), "enforce", db=db)
        assert code == 2
        assert f"{HANDLE}#{bad}" in err

    def test_refs_found_in_nested_payload_values(self, registry, monkeypatch, capsys):
        db, stub = registry
        bad = stale_stub(stub)
        nested = json.dumps(
            {"tool_input": {"prompt": [f"step one\nrelay {HANDLE}#{bad}"], "depth": 2}}
        )
        code, _, err = run_gate(monkeypatch, capsys, nested, "enforce", db=db)
        assert code == 2
        assert f"{HANDLE}#{bad}" in err

    def test_non_json_stdin_falls_back_to_raw_scan(self, registry, monkeypatch, capsys):
        db, stub = registry
        bad = stale_stub(stub)
        code, _, err = run_gate(
            monkeypatch, capsys, f"plain text mentioning {HANDLE}#{bad}", "enforce", db=db
        )
        assert code == 2


class TestFailureModes:
    def test_registry_unavailable_fails_open(self, registry, monkeypatch, capsys):
        db, stub = registry
        bad = stale_stub(stub)
        monkeypatch.setitem(sys.modules, "sema.core.registry", None)  # forces ImportError
        code, out, err = run_gate(
            monkeypatch, capsys, payload_with(f"per {HANDLE}#{bad}"), "enforce", db=db
        )
        assert code == 0  # never brick the harness over gate infrastructure
        assert "registry unavailable" in err


class TestVerdictLog:
    def test_log_records_verdicts_per_invocation(self, registry, monkeypatch, capsys, tmp_path):
        db, stub = registry
        bad = stale_stub(stub)
        log = tmp_path / "gate.jsonl"
        run_gate(monkeypatch, capsys, payload_with(f"per {HANDLE}#{bad}"), "warn", db=db, log=log)
        run_gate(
            monkeypatch, capsys, payload_with(f"per {HANDLE}#{bad}"), "enforce", db=db, log=log
        )
        entries = [json.loads(line) for line in log.read_text().splitlines()]
        assert [e["mode"] for e in entries] == ["warn", "enforce"]
        assert all(e["stale"] == [f"{HANDLE}#{bad}"] for e in entries)
        assert [e["blocked"] for e in entries] == [False, True]
