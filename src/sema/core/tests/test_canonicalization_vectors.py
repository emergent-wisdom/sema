"""Versioned interoperability vectors for semahash canonicalization v2."""

import hashlib
import json
import runpy
from pathlib import Path

import pytest

from sema.core.hashing import (
    canonical_json,
    generate_sema_hash,
    merkle_hash,
    normalize_string,
    strict_json_loads,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
VECTOR_PATH = REPO_ROOT / "docs" / "specification" / "canonicalization-v2-test-vectors.json"
VECTORS = json.loads(VECTOR_PATH.read_text(encoding="utf-8"))
REFERENCE = runpy.run_path(str(REPO_ROOT / "scripts" / "test_hash_verification.py"))
independent_canonicalize_dependency_keys = REFERENCE["canonicalize_dependency_keys"]
independent_merkle_hash = REFERENCE["merkle_hash"]
independent_strict_json_loads = REFERENCE["strict_json_loads"]


def _preimage(value):
    if isinstance(value, str):
        return b"s:" + normalize_string(value).encode("utf-8")
    if value is None or isinstance(value, bool | int | float):
        return b"p:" + canonical_json(value)
    if isinstance(value, list):
        return b"l:" + "".join(merkle_hash(item)[0] for item in value).encode("ascii")

    entries = []
    for key, item in value.items():
        normalized_key = normalize_string(key)
        entries.append((normalized_key, merkle_hash(key)[0], merkle_hash(item)[0]))
    entries.sort(key=lambda entry: entry[0])
    return b"d:" + "".join(key_hash + value_hash for _, key_hash, value_hash in entries).encode(
        "ascii"
    )


@pytest.mark.parametrize("vector", VECTORS["valid"], ids=lambda vector: vector["name"])
def test_valid_canonicalization_vector(vector):
    value = strict_json_loads(vector["input_json"], label=vector["name"])
    independent_value = independent_strict_json_loads(vector["input_json"].encode("utf-8"))
    digest, canonical = merkle_hash(value)
    independent_digest, independent_canonical = independent_merkle_hash(independent_value)
    preimage = _preimage(value)

    assert VECTORS["format"] == "sema-canonicalization-v2-test-vectors-v1"
    assert digest == independent_digest == vector["sha256"]
    assert canonical == independent_canonical
    assert (
        json.dumps(canonical, ensure_ascii=True, separators=(",", ":"), allow_nan=False)
        == vector["canonical_json"]
    )
    assert preimage.hex() == vector["preimage_hex"]
    assert hashlib.sha256(preimage).hexdigest() == vector["sha256"]


@pytest.mark.parametrize("vector", VECTORS["invalid"], ids=lambda vector: vector["name"])
def test_invalid_canonicalization_vector(vector):
    with pytest.raises(ValueError):
        value = strict_json_loads(vector["input_json"], label=vector["name"])
        merkle_hash(value)

    with pytest.raises(ValueError):
        value = independent_strict_json_loads(vector["input_json"].encode("utf-8"))
        independent_merkle_hash(value)


@pytest.mark.parametrize("vector", VECTORS["patterns"], ids=lambda vector: vector["name"])
def test_pattern_identity_vector(vector):
    pattern = strict_json_loads(vector["input_json"], label=vector["name"])
    result = generate_sema_hash(pattern)

    independent_pattern = independent_strict_json_loads(vector["input_json"].encode("utf-8"))
    semantic_fields = {
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
    content = {key: value for key, value in independent_pattern.items() if key in semantic_fields}
    if "derived_from" in independent_pattern:
        content["derived_from"] = independent_pattern["derived_from"]
    if "dependencies" in content:
        content["dependencies"] = independent_canonicalize_dependency_keys(content["dependencies"])
    independent_digest, _ = independent_merkle_hash(content)

    assert result["hash"] == independent_digest == vector["hash"]
    assert result["full_id"] == vector["full_id"]
    assert result["reference"] == vector["reference"]
    assert result["stub"] == vector["stub"]
