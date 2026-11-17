"""Interoperability vectors for canonicalization v3 (placeholder bindings).

The library and the dependency-free reference verifier must both reproduce
every vector, so a third party can implement v3 from the specification alone.
"""

import json
import runpy
from pathlib import Path

import pytest

from sema.core.hashing import (
    CANONICALIZATION_V2,
    CANONICALIZATION_V3,
    generate_sema_hash,
    semantic_hash_input,
    strict_json_loads,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
VECTOR_PATH = REPO_ROOT / "docs" / "specification" / "canonicalization-v3-test-vectors.json"
VECTORS = json.loads(VECTOR_PATH.read_text(encoding="utf-8"))
REFERENCE = runpy.run_path(str(REPO_ROOT / "scripts" / "test_hash_verification.py"))

SEMANTIC_FIELDS = {
    "dependencies",
    "signature",
    "data_schema",
    "mechanism",
    "gloss",
    "invariants",
    "preconditions",
    "postconditions",
    "parameters",
    "failure_modes",
    "extends",
}


def _independent_v3(pattern: dict) -> tuple[str, dict]:
    content = {key: value for key, value in pattern.items() if key in SEMANTIC_FIELDS}
    if "dependencies" in content:
        content["dependencies"] = REFERENCE["canonicalize_dependency_bindings"](
            content["dependencies"]
        )
    digest, _ = REFERENCE["merkle_hash"](content)
    return digest, content


def test_vector_file_format():
    assert VECTORS["format"] == "sema-canonicalization-v3-test-vectors-v1"
    assert VECTORS["canonicalization"] == "semahash-v3"
    assert VECTORS["digest"] == "SHA-256"


@pytest.mark.parametrize("vector", VECTORS["patterns"], ids=lambda vector: vector["name"])
def test_pattern_identity_vector(vector):
    pattern = strict_json_loads(vector["input_json"], label=vector["name"])
    result = generate_sema_hash(pattern, canonicalization=CANONICALIZATION_V3)
    independent_digest, independent_content = _independent_v3(
        REFERENCE["strict_json_loads"](vector["input_json"].encode("utf-8"))
    )
    dependencies = semantic_hash_input(pattern, canonicalization=CANONICALIZATION_V3)[
        "dependencies"
    ]

    assert result["hash"] == independent_digest == vector["hash"]
    assert result["full_id"] == vector["full_id"]
    assert result["reference"] == vector["reference"]
    assert result["stub"] == vector["stub"]
    for canonical in (dependencies, independent_content["dependencies"]):
        assert (
            json.dumps(canonical, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
            == vector["canonical_dependencies_json"]
        )
    v2 = generate_sema_hash(pattern, canonicalization=CANONICALIZATION_V2)
    assert v2["hash"] == vector["v2_hash"]


def test_the_vectors_pin_the_gap_and_its_fix():
    by_name = {vector["name"]: vector for vector in VECTORS["patterns"]}
    implied, exchanged = by_name["implied-pairings-match-v2"], by_name["exchanged-targets"]
    assert implied["hash"] == implied["v2_hash"]
    assert exchanged["v2_hash"] == implied["v2_hash"]
    assert exchanged["hash"] != implied["hash"]

    across = by_name["names-folding-alike-across-categories"]
    across_exchanged = by_name["exchanged-across-categories"]
    assert across_exchanged["v2_hash"] == across["v2_hash"]
    assert across_exchanged["hash"] != across["hash"]

    same_name = by_name["one-name-two-categories"]
    assert same_name["hash"] == same_name["v2_hash"]


@pytest.mark.parametrize("vector", VECTORS["invalid"], ids=lambda vector: vector["name"])
def test_invalid_vector_fails_closed(vector):
    pattern = strict_json_loads(vector["input_json"], label=vector["name"])
    with pytest.raises(ValueError):
        generate_sema_hash(pattern, canonicalization=CANONICALIZATION_V3)
    with pytest.raises(ValueError):
        _independent_v3(REFERENCE["strict_json_loads"](vector["input_json"].encode("utf-8")))
