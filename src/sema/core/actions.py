from typing import Any

from .hashing import catalog_root, pattern_hash_from_sema_id


def _compute_context_hash(
    patterns: list[dict[str, Any]],
    handles: list[str],
    stub_length: int = 8,
) -> str:
    """
    Compute the catalog Merkle root of a set of resolved handle bindings.

    Context negotiation starts from human-readable handles, so it must bind
    each requested handle to the exact stored content address. A digest-only
    set would miss a swap such as ``Alpha -> x, Bravo -> y`` versus
    ``Alpha -> y, Bravo -> x``. Returns a prefix of the full root for
    cooperative drift detection.
    """
    if len(patterns) != len(handles):
        raise ValueError("context patterns and handles must have the same length")

    bindings = []
    for index, (pattern, handle) in enumerate(zip(patterns, handles, strict=True)):
        try:
            pattern_hash = pattern_hash_from_sema_id(
                pattern.get("sema_id"),
                expected_handle=handle,
            )
        except ValueError as exc:
            raise ValueError(
                f"context pattern at index {index} has an invalid sema_id: {exc}"
            ) from exc
        bindings.append((handle, pattern_hash))

    return catalog_root(bindings)[:stub_length]
