"""Pure decision kernel for Sema's fail-closed handshake.

The corresponding Lean model and safety proofs live in
``verification/lean/SemaVerification/Handshake.lean``.  Keep this function
small and side-effect free: ``GraphWorkspace`` owns input normalization and
response payloads, while this module owns only the verdict.
"""

from __future__ import annotations

from enum import Enum


class HandshakeVerdict(str, Enum):
    """Possible outcomes of comparing a presented identity with Sema's."""

    PROVIDE_HASH = "PROVIDE_HASH"
    REQUIRE_FULL_HASH = "REQUIRE_FULL_HASH"
    PROCEED = "PROCEED"
    HALT = "HALT"


class HandshakeMode(str, Enum):
    """Trust policy applied to a matching truncated hash."""

    COOPERATIVE = "cooperative"
    STRICT = "strict"


def decide_handshake(
    *,
    available: bool,
    presented_hash: str | None,
    canonical_stub: str,
    canonical_full: str | None,
    mode: HandshakeMode = HandshakeMode.COOPERATIVE,
) -> HandshakeVerdict:
    """Return the handshake verdict for already-normalized inputs.

    Safety contract:

    - unavailable identities always halt;
    - an available identity with no presented hash asks the peer for one;
    - a full-hash match always proceeds;
    - a stub match proceeds in cooperative mode and requests the full hash in
      strict mode;
    - every other presented value halts.

    Empty strings are candidates, not missing values.  Callers decide whether
    blank user input should be normalized to ``None`` for their protocol scope.
    """

    if not available:
        return HandshakeVerdict.HALT
    if presented_hash is None:
        return HandshakeVerdict.PROVIDE_HASH
    if canonical_full is not None and presented_hash == canonical_full:
        return HandshakeVerdict.PROCEED
    if presented_hash == canonical_stub:
        if mode is HandshakeMode.STRICT:
            return HandshakeVerdict.REQUIRE_FULL_HASH
        return HandshakeVerdict.PROCEED
    return HandshakeVerdict.HALT
