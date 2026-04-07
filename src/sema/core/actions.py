import hashlib
import json
from typing import Any

from sema.core.config import get_config
from sema.core.registry import RegistryManager

# =============================================================================
# Helpers
# =============================================================================


def _get_registry_mgr(config_instance):
    profile = config_instance.get_active_profile()
    path = profile.get("registry_path")
    return RegistryManager(path)


def _hash_bytes(data: bytes) -> str:
    """SHA-256 hash of bytes, returns full hex string."""
    return hashlib.sha256(data).hexdigest()


def _extract_semantic_fields(pattern: dict[str, Any]) -> dict[str, Any]:
    """Extract only the semantic fields that define meaning (not metadata)."""
    semantic_keys = [
        "handle",
        "mechanism",
        "gloss",
        "invariants",
        "preconditions",
        "postconditions",
        "inputs",
        "outputs",
        "parameters",
        "interface",
        "dependencies",
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


def sema_search(query: str) -> str:
    """Search Sema patterns."""
    cfg = get_config()
    mgr = _get_registry_mgr(cfg)
    results = mgr.search(query)
    return json.dumps(results, indent=2)


def sema_resolve(handle: str, depth: int = 1) -> str:
    """Resolve pattern dependencies."""
    cfg = get_config()
    mgr = _get_registry_mgr(cfg)
    subgraph = mgr.resolve(handle, depth=depth)

    if not subgraph:
        return json.dumps({"error": f"Pattern '{handle}' not found"})

    return json.dumps(
        {"root": handle, "depth": depth, "patterns": subgraph, "count": len(subgraph)}, indent=2
    )


def sema_lookup(ref: str) -> str:
    """Lookup a pattern definition."""
    cfg = get_config()
    mgr = _get_registry_mgr(cfg)

    parts = ref.split("#")
    handle = parts[0]
    stub = parts[1] if len(parts) > 1 else None

    pattern = mgr.get_pattern(handle)
    if not pattern:
        return json.dumps({"error": f"Pattern '{handle}' not found"})

    if stub:
        pattern_stub = pattern.get("sema_stub", "")
        if stub != pattern_stub:
            return json.dumps(
                {
                    "warning": f"Stub mismatch: requested '{stub}' but pattern has '{pattern_stub}'",
                    "pattern": pattern,
                }
            )

    return json.dumps(pattern, indent=2)


def sema_handshake(ref: Any, your_hash: str | None = None) -> str:
    """
    Verify semantic alignment (SpectralTune protocol).

    Supports two modes:
    1. Single pattern: sema_handshake("StateLock#2f3c")
    2. Session-scoped: sema_handshake(["ChainOfThought", "StateLock"], "9f8b2a1c")

    For session-scoped mode, computes Merkle root of the pattern set.
    Order doesn't matter: ["A", "B"] == ["B", "A"]
    """
    cfg = get_config()
    mgr = _get_registry_mgr(cfg)

    # ==========================================================================
    # Session-Scoped Mode: List of patterns
    # ==========================================================================
    if isinstance(ref, list):
        patterns = []
        missing = []

        for handle in ref:
            pattern = mgr.get_pattern(handle)
            if pattern:
                patterns.append(pattern)
            else:
                missing.append(handle)

        if missing:
            return json.dumps(
                {
                    "verdict": "HALT",
                    "reason": "Patterns not found",
                    "missing": missing,
                    "action": "Cannot coordinate - patterns unknown",
                },
                indent=2,
            )

        # Compute context hash (Merkle root of sorted pattern hashes)
        local_hash = _compute_context_hash(patterns)

        if your_hash is None:
            return json.dumps(
                {
                    "verdict": "PROVIDE_HASH",
                    "patterns": ref,
                    "context_hash": local_hash,
                    "action": "Share this hash with remote agent for verification.",
                },
                indent=2,
            )

        if local_hash == your_hash:
            return json.dumps(
                {
                    "verdict": "PROCEED",
                    "patterns": ref,
                    "context_hash": local_hash,
                    "message": "Session context verified. Agents are semantically aligned.",
                },
                indent=2,
            )
        else:
            return json.dumps(
                {
                    "verdict": "HALT",
                    "patterns": ref,
                    "reason": "CONTEXT MISMATCH",
                    "local_hash": local_hash,
                    "remote_hash": your_hash,
                    "action": "Semantic drift detected. Do NOT proceed.",
                },
                indent=2,
            )

    # ==========================================================================
    # Single Pattern Mode: Backward compatible
    # ==========================================================================
    parts = ref.split("#")
    handle = parts[0]
    ref_stub = parts[1] if len(parts) > 1 else None

    pattern = mgr.get_pattern(handle)
    if not pattern:
        return json.dumps(
            {
                "verdict": "HALT",
                "reason": f"Pattern '{handle}' not found",
                "action": "Cannot coordinate - pattern unknown",
            },
            indent=2,
        )

    canonical_stub = pattern.get("sema_stub", "")
    canonical_ref = pattern.get("sema_ref", f"{handle}#{canonical_stub}")

    if your_hash is None and ref_stub is None:
        return json.dumps(
            {
                "verdict": "PROVIDE_HASH",
                "handle": handle,
                "canonical_stub": canonical_stub,
                "action": "Compare this hash with your local definition.",
            },
            indent=2,
        )

    compare_hash = your_hash or ref_stub

    if compare_hash == canonical_stub:
        return json.dumps(
            {
                "verdict": "PROCEED",
                "handle": handle,
                "verified_ref": canonical_ref,
                "tier": pattern.get("tier", 1),
            },
            indent=2,
        )
    else:
        return json.dumps(
            {
                "verdict": "HALT",
                "handle": handle,
                "reason": "SEMANTIC DRIFT DETECTED",
                "canonical_hash": canonical_stub,
            },
            indent=2,
        )
