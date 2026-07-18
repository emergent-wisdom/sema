# Sema formal-verification pilot

This directory contains Sema's first machine-checked safety proofs. The pilot
uses Lean 4 to verify two properties at the trusted coordination boundary:

1. **Handshake trust modes and fail-closure.** An unknown identity or
   mismatched hash cannot produce `PROCEED`. Cooperative mode accepts a
   matching truncated prefix for ordinary drift detection. Strict mode proves
   that `PROCEED` requires the full canonical hash; a matching prefix instead
   returns `REQUIRE_FULL_HASH`.
2. **Canonicalization domain separation.** String, primitive, list, and
   dictionary nodes produce distinct preimages before hashing because their
   `s:`, `p:`, `l:`, and `d:` tags have distinct first bytes. Equal SHA-256
   outputs across node kinds would therefore require a SHA-256 collision.

## Assurance boundary

These are real, universal proofs of the Lean models, but they are not a proof
of the entire Python application.

- `SemaVerification/Handshake.lean` is the authoritative decision contract.
- `src/sema/core/handshake.py` is the pure production kernel corresponding to
  that contract.
- `test_handshake_contract.py` checks a representative cross-product for
  conformance between the verified model and the Python kernel.
- `test_hashing.py` checks that the production type-tag bytes remain identical
  to those used by the canonical-encoding proof.
- Existing workspace and MCP tests exercise that kernel through Sema's public
  handshake boundary.

`proof-manifest.json` records the verifier version, theorem names, production
surfaces, conformance tests, and assumptions in a machine-readable form.

The trusted computing base still includes Lean's kernel, the Python runtime,
input normalization and registry lookup in `GraphWorkspace`, and the
collision-resistance assumption for SHA-256. The proof does not establish that
natural-language pattern invariants are true or that every Sema component is
formally verified.

Cooperative prefix matching is intentionally not presented as cryptographic
identity proof. A 4-hex pattern stub has 16 bits of targeted-prefix resistance;
it is a compact signal for non-adversarial drift detection. Strict mode uses
the full 256-bit digest when proof-grade identity is required.

## Verification

Lean is pinned by `lean-toolchain`. With `elan` installed:

```bash
cd verification/lean
lake build --wfail
```

`--wfail` makes incomplete `sorry` proofs fail the build. CI runs this as a
blocking job in addition to the Python conformance and integration tests.

## Proven theorems

Handshake:

- `unknownAlwaysHalts`
- `missingHashRequestsCanonical`
- `mismatchHalts`
- `fullHashAlwaysProceeds`
- `cooperativeStubProceeds`
- `strictStubRequiresFull`
- `cooperativeProceedIffAvailableAndAnyMatch`
- `strictProceedIffAvailableAndFullMatch`
- `strictProceedRequiresFullIdentity`

Canonical encoding:

- `tagByteInjective`
- `nodeKindsAreDomainSeparated`
- `crossKindDigestEqualityRequiresCollision`
