"""Conformance tests for the Lean-verified handshake decision model.

Lean proves the model for arbitrary strings.  This suite checks a representative
cross-product against the Python kernel used by ``GraphWorkspace.handshake``.
See ``verification/README.md`` for the assurance boundary.
"""

from itertools import product

import pytest

from sema.core.handshake import HandshakeMode, HandshakeVerdict, decide_handshake

STUB = "a" * 4
FULL = "a" * 64


def lean_model_verdict(
    *,
    available: bool,
    presented_hash: str | None,
    canonical_stub: str,
    canonical_full: str | None,
    mode: HandshakeMode,
) -> HandshakeVerdict:
    """Executable transcription of ``Handshake.decideHandshake`` in Lean."""

    if not available:
        return HandshakeVerdict.HALT
    if presented_hash is None:
        return HandshakeVerdict.PROVIDE_HASH
    if canonical_full == presented_hash:
        return HandshakeVerdict.PROCEED
    if presented_hash == canonical_stub:
        if mode is HandshakeMode.STRICT:
            return HandshakeVerdict.REQUIRE_FULL_HASH
        return HandshakeVerdict.PROCEED
    return HandshakeVerdict.HALT


CONFORMANCE_CASES = list(
    product(
        [False, True],
        [None, "", STUB, FULL, "b" * 4, "b" * 64],
        [None, FULL],
        [HandshakeMode.COOPERATIVE, HandshakeMode.STRICT],
    )
)


@pytest.mark.parametrize(
    ("available", "presented_hash", "canonical_full", "mode"), CONFORMANCE_CASES
)
def test_python_kernel_conforms_to_verified_model(
    available: bool,
    presented_hash: str | None,
    canonical_full: str | None,
    mode: HandshakeMode,
):
    expected = lean_model_verdict(
        available=available,
        presented_hash=presented_hash,
        canonical_stub=STUB,
        canonical_full=canonical_full,
        mode=mode,
    )

    actual = decide_handshake(
        available=available,
        presented_hash=presented_hash,
        canonical_stub=STUB,
        canonical_full=canonical_full,
        mode=mode,
    )

    assert actual is expected


@pytest.mark.parametrize("presented_hash", [None, "", STUB, FULL, "b" * 64])
def test_unavailable_identity_always_halts(presented_hash: str | None):
    assert (
        decide_handshake(
            available=False,
            presented_hash=presented_hash,
            canonical_stub=STUB,
            canonical_full=FULL,
        )
        is HandshakeVerdict.HALT
    )


@pytest.mark.parametrize("presented_hash", ["", "b" * 4, "b" * 64])
def test_mismatch_never_proceeds(presented_hash: str):
    assert (
        decide_handshake(
            available=True,
            presented_hash=presented_hash,
            canonical_stub=STUB,
            canonical_full=FULL,
        )
        is HandshakeVerdict.HALT
    )


def test_cooperative_mode_accepts_stub_with_prefix_assurance_contract():
    assert (
        decide_handshake(
            available=True,
            presented_hash=STUB,
            canonical_stub=STUB,
            canonical_full=FULL,
            mode=HandshakeMode.COOPERATIVE,
        )
        is HandshakeVerdict.PROCEED
    )


def test_strict_mode_requires_full_hash_after_stub_match():
    assert (
        decide_handshake(
            available=True,
            presented_hash=STUB,
            canonical_stub=STUB,
            canonical_full=FULL,
            mode=HandshakeMode.STRICT,
        )
        is HandshakeVerdict.REQUIRE_FULL_HASH
    )


def test_strict_mode_accepts_full_hash():
    assert (
        decide_handshake(
            available=True,
            presented_hash=FULL,
            canonical_stub=STUB,
            canonical_full=FULL,
            mode=HandshakeMode.STRICT,
        )
        is HandshakeVerdict.PROCEED
    )
