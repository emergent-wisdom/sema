/-
Copyright (c) 2026 Emergent Wisdom.
Released under the MIT license described in the repository LICENSE file.

Proof of the domain-separation property used by semahash canonicalization v2.
SHA-256 is intentionally abstract: Lean proves that values of different node
kinds have distinct hash preimages.  Equal digests would therefore require a
collision in the selected digest function.
-/

set_option autoImplicit false

namespace SemaVerification.CanonicalEncoding

inductive NodeKind where
  | string
  | primitive
  | list
  | dictionary
  deriving DecidableEq, Repr

-- ASCII bytes for the production tags: s:, p:, l:, and d:.
def tagByte : NodeKind → Nat
  | .string => 115
  | .primitive => 112
  | .list => 108
  | .dictionary => 100

def tag (kind : NodeKind) : List Nat := [tagByte kind, 58]

def hashPreimage (kind : NodeKind) (payload : List Nat) : List Nat :=
  tag kind ++ payload

theorem tagByteInjective
    {left right : NodeKind}
    (hEqual : tagByte left = tagByte right) :
    left = right := by
  cases left <;> cases right <;> simp_all [tagByte]

theorem nodeKindsAreDomainSeparated
    {left right : NodeKind}
    (hDifferent : left ≠ right)
    (leftPayload rightPayload : List Nat) :
    hashPreimage left leftPayload ≠ hashPreimage right rightPayload := by
  intro hPreimages
  have hHeads := congrArg List.head? hPreimages
  have hTags : tagByte left = tagByte right := by
    simpa [hashPreimage, tag] using hHeads
  exact hDifferent (tagByteInjective hTags)

theorem crossKindDigestEqualityRequiresCollision
    {Digest : Type}
    (digest : List Nat → Digest)
    {left right : NodeKind}
    (hDifferent : left ≠ right)
    (leftPayload rightPayload : List Nat)
    (hDigestEqual :
      digest (hashPreimage left leftPayload) = digest (hashPreimage right rightPayload)) :
    ∃ first second,
      first ≠ second ∧ digest first = digest second := by
  exact ⟨
    hashPreimage left leftPayload,
    hashPreimage right rightPayload,
    nodeKindsAreDomainSeparated hDifferent leftPayload rightPayload,
    hDigestEqual
  ⟩

end SemaVerification.CanonicalEncoding
