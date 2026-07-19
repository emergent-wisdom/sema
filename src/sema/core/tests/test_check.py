"""Conformance tests for ``sema.core.check`` (ref extraction and verdicts).

The fixture set in ``fixtures/refcheck_conformance.json`` is the shared contract
for harness shims: Claude Code hooks, and future non-Python shims, replay these
payloads against whatever adapter feeds text into ``check_text`` (or an
equivalent). Claiming that a shim "supports harness X" means it passes this
conformance set — not that it reimplements extraction or verdict logic.

Placeholders ``{CANON}`` and ``{STALE}`` stand in for the content-hash stub of
the session-minted InclusivePaymentThreshold pattern and a deliberately wrong
4-hex stub; the suite substitutes them at runtime so the fixture stays
authorable without knowing the hash ahead of time.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sema.core.check import (
    CHECK_SCHEMA_VERSION,
    REF_RE,
    check_text,
    extract_refs,
)
from sema.core.mint import mint_pattern
from sema.core.registry import RegistryManager
from sema.taxonomy_graph.graph_store import GraphStore

HANDLE = "InclusivePaymentThreshold"

# Known-valid against the mint schema (also used by the babel-hook pilot).
PATTERN = {
    "handle": HANDLE,
    "mechanism": (
        "Compare the integer payment amount with the configured minimum before accepting the task."
    ),
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

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "refcheck_conformance.json"


def _load_cases() -> list[dict]:
    return json.loads(FIXTURE_PATH.read_text())


def _subst(text: str, canon: str, stale: str) -> str:
    return text.replace("{CANON}", canon).replace("{STALE}", stale)


@pytest.fixture(scope="session")
def check_registry(tmp_path_factory):
    """Mint one real pattern into a temp DB; return (registry, canon, stale)."""
    db_path = tmp_path_factory.mktemp("refcheck") / "canon.db"
    result = mint_pattern(PATTERN, GraphStore(str(db_path)))
    assert result.success, result.errors
    canon = result.sema_ref.split("#")[1]
    stale = "0000" if canon != "0000" else "0001"
    registry = RegistryManager(db_path=str(db_path))
    return registry, canon, stale


@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: c["name"])
def test_conformance_case(case, check_registry):
    registry, canon, stale = check_registry
    payload = _subst(case["payload"], canon, stale)
    expected = {
        "known": {_subst(r, canon, stale) for r in case["expected"]["known"]},
        "stale": {_subst(r, canon, stale) for r in case["expected"]["stale"]},
        "unknown": {_subst(r, canon, stale) for r in case["expected"]["unknown"]},
    }

    doc = check_text(payload, registry)

    known = {r["ref"] for r in doc["refs"] if r["verdict"] == "KNOWN"}
    stale_refs = {r["ref"] for r in doc["stale"]}
    unknown_refs = {r["ref"] for r in doc["unknown"]}

    assert known == expected["known"]
    assert stale_refs == expected["stale"]
    assert unknown_refs == expected["unknown"]
    assert doc["schema"] == CHECK_SCHEMA_VERSION

    if not expected["stale"]:
        assert doc["repair"] is None
    else:
        assert doc["repair"] is not None
        for ref in expected["stale"]:
            assert ref in doc["repair"]
        assert canon in doc["repair"]
        assert "sema_handshake" in doc["repair"]


def test_extract_refs_sorted_unique():
    text = "Bbb#bbbb Aaa#aaaa Bbb#bbbb Aaa#aaaa"
    assert extract_refs(text) == [("Aaa", "aaaa"), ("Bbb", "bbbb")]


def test_extract_refs_json_decode_path():
    """JSON payloads are scanned on decoded string values, not wire bytes."""
    event = {
        "session_id": "x",
        "prompt": f"Authoritative pattern:\n{HANDLE}#abcd\nImplement.",
    }
    payload = json.dumps(event)
    # Wire form fuses ``\\n`` with the handle — raw regex must miss.
    assert REF_RE.findall(payload) == []
    assert extract_refs(payload) == [(HANDLE, "abcd")]


def test_extract_refs_raw_text_fallback():
    """Non-JSON text is scanned as-is."""
    text = f"plain text mentioning {HANDLE}#abcd"
    assert extract_refs(text) == [(HANDLE, "abcd")]


def test_regression_raw_bytes_miss_line_start_ref(check_registry):
    """The JSON line-start regression: raw REF_RE must not see the ref."""
    _, canon, stale = check_registry
    cases = {c["name"]: c for c in _load_cases()}
    payload = _subst(cases["json_line_start_stale"]["payload"], canon, stale)
    assert REF_RE.findall(payload) == []
    assert extract_refs(payload) == [(HANDLE, stale)]


def test_verdict_canonical_fields(check_registry):
    registry, canon, stale = check_registry
    text = f"{HANDLE}#{canon} {HANDLE}#{stale} PR#12ab"
    doc = check_text(text, registry)

    by_verdict = {r["verdict"]: r for r in doc["refs"]}
    assert by_verdict["KNOWN"]["canonical"] == by_verdict["KNOWN"]["stub"] == canon
    assert by_verdict["STALE"]["canonical"] == canon
    assert by_verdict["STALE"]["stub"] == stale
    assert by_verdict["UNKNOWN"]["canonical"] is None
    assert by_verdict["UNKNOWN"]["ref"] == "PR#12ab"
