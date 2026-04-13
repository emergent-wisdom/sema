import hashlib
import json
from typing import Any


def _hash_bytes(data: bytes) -> str:
    """SHA-256 hash of bytes, returns full hex string."""
    return hashlib.sha256(data).hexdigest()


def _extract_semantic_fields(pattern: dict[str, Any]) -> dict[str, Any]:
    """Extract only the semantic fields that define meaning (not metadata)."""
    semantic_keys = [
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
        "derived_from",
    ]
    return {k: pattern[k] for k in semantic_keys if k in pattern}


def _canonicalize(data: dict[str, Any]) -> bytes:
    """Deterministic JSON bytes: sorted keys, no whitespace."""
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _compute_context_hash(patterns: list[dict[str, Any]], stub_length: int = 8) -> str:
    """
    Compute Merkle root of a set of patterns.

    1. Extract semantic fields from each pattern
    2. Canonicalize to bytes
    3. Hash each pattern
    4. SORT hashes (set-consistency: order doesn't matter)
    5. Hash the concatenated sorted hashes

    Returns stub of specified length.
    """
    item_hashes = []
    for pattern in patterns:
        semantic = _extract_semantic_fields(pattern)
        canonical = _canonicalize(semantic)
        item_hashes.append(_hash_bytes(canonical))

    # Sort for set-consistency: ["A", "B"] == ["B", "A"]
    item_hashes.sort()

    # Merkle root: hash of concatenated sorted hashes
    aggregate = "".join(item_hashes).encode("utf-8")
    root_hash = _hash_bytes(aggregate)

    return root_hash[:stub_length]
