"""Pure mint pipeline: validate → store (which hashes from edges).

No stdout, no files, no side-effects beyond the store write.
Used by both the MCP server and the CLI apply command.

Hashing is owned by GraphStore.add_pattern — it computes the Merkle hash
after edges exist, so dependency hashes are resolved from the actual graph
state rather than from whatever strings happen to be in the pattern dict.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .validator import validate_pattern


@dataclass
class MintResult:
    success: bool
    handle: str = ""
    sema_ref: str = ""
    sema_id: str = ""
    sema_stub: str = ""
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def mint_pattern(
    pattern: dict,
    store,
    known_handles: set[str] | None = None,
    skip_cascade: bool = False,
    validated_extends_batch: bool = False,
) -> MintResult:
    """Validate and store a pattern. Hashing is delegated to the store.

    Args:
        pattern: In-memory pattern dict (must have handle + mechanism).
        store: A GraphStore instance with an ``add_pattern`` method.
        known_handles: Optional set of existing handles for reference validation.
        skip_cascade: If True, do not trigger _cascade_dependents after store.
            Caller is responsible for running one final sweep. Used by
            sema pull to avoid O(N^2) write amplification.
        validated_extends_batch: Permit an active parent definition to move only
            when the caller has already validated the complete post-write corpus.

    Returns:
        Structured MintResult – no printing, no file I/O.
    """
    handle = pattern.get("handle", "")

    # 1. Validate
    is_valid, errors, warnings = validate_pattern(pattern, known_handles=known_handles)
    if not is_valid:
        return MintResult(success=False, handle=handle, errors=errors, warnings=warnings)

    # 2. Store (add_pattern computes hash from edges, promotes layer/category)
    result = store.add_pattern(
        pattern,
        skip_cascade=skip_cascade,
        validated_extends_batch=validated_extends_batch,
    )
    if not result.get("success"):
        return MintResult(
            success=False,
            handle=handle,
            errors=[result.get("error", "Unknown store error")],
            warnings=warnings,
        )

    # Read hash back from the mutated pattern dict (set by store.add_pattern)
    return MintResult(
        success=True,
        handle=handle,
        sema_ref=pattern.get("sema_ref", ""),
        sema_id=pattern.get("sema_id", ""),
        sema_stub=pattern.get("sema_stub", ""),
        errors=[],
        warnings=warnings,
    )
