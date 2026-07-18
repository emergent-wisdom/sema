/-
Copyright (c) 2026 Emergent Wisdom.
Released under the MIT license described in the repository LICENSE file.

Formal decision model for Sema's content-identity handshake. Normalization,
lookup, and response formatting remain adapter responsibilities. This model
owns the verdict and makes the cooperative/strict trust policy explicit.
-/

set_option autoImplicit false

namespace SemaVerification.Handshake

inductive Mode where
  | cooperative
  | strict
  deriving DecidableEq, Repr

inductive Verdict where
  | provideHash
  | requireFullHash
  | proceed
  | halt
  deriving DecidableEq, Repr

structure CanonicalIdentity where
  stub : String
  full : Option String
  deriving DecidableEq, Repr

def MatchesStub (candidate : String) (canonical : CanonicalIdentity) : Prop :=
  candidate = canonical.stub

def MatchesFull (candidate : String) (canonical : CanonicalIdentity) : Prop :=
  canonical.full = some candidate

def MatchesEither (candidate : String) (canonical : CanonicalIdentity) : Prop :=
  MatchesStub candidate canonical ∨ MatchesFull candidate canonical

instance matchesStubDecidable (candidate : String) (canonical : CanonicalIdentity) :
    Decidable (MatchesStub candidate canonical) := by
  unfold MatchesStub
  infer_instance

instance matchesFullDecidable (candidate : String) (canonical : CanonicalIdentity) :
    Decidable (MatchesFull candidate canonical) := by
  unfold MatchesFull
  infer_instance

def decideHandshake
    (mode : Mode)
    (available : Bool)
    (presented : Option String)
    (canonical : CanonicalIdentity) : Verdict :=
  match available, presented with
  | false, _ => .halt
  | true, none => .provideHash
  | true, some candidate =>
      if MatchesFull candidate canonical then
        .proceed
      else if MatchesStub candidate canonical then
        match mode with
        | .cooperative => .proceed
        | .strict => .requireFullHash
      else
        .halt

@[simp] theorem unknownAlwaysHalts
    (mode : Mode)
    (presented : Option String)
    (canonical : CanonicalIdentity) :
    decideHandshake mode false presented canonical = .halt := by
  cases presented <;> rfl

@[simp] theorem missingHashRequestsCanonical
    (mode : Mode)
    (canonical : CanonicalIdentity) :
    decideHandshake mode true none canonical = .provideHash := by
  rfl

theorem mismatchHalts
    (mode : Mode)
    (candidate : String)
    (canonical : CanonicalIdentity)
    (hNotStub : ¬MatchesStub candidate canonical)
    (hNotFull : ¬MatchesFull candidate canonical) :
    decideHandshake mode true (some candidate) canonical = .halt := by
  simp [decideHandshake, hNotStub, hNotFull]

theorem fullHashAlwaysProceeds
    (mode : Mode)
    (candidate : String)
    (canonical : CanonicalIdentity)
    (hFull : MatchesFull candidate canonical) :
    decideHandshake mode true (some candidate) canonical = .proceed := by
  simp [decideHandshake, hFull]

theorem cooperativeStubProceeds
    (candidate : String)
    (canonical : CanonicalIdentity)
    (hStub : MatchesStub candidate canonical) :
    decideHandshake .cooperative true (some candidate) canonical = .proceed := by
  by_cases hFull : MatchesFull candidate canonical
  · simp [decideHandshake, hFull]
  · simp [decideHandshake, hFull, hStub]

theorem strictStubRequiresFull
    (candidate : String)
    (canonical : CanonicalIdentity)
    (hStub : MatchesStub candidate canonical)
    (hNotFull : ¬MatchesFull candidate canonical) :
    decideHandshake .strict true (some candidate) canonical = .requireFullHash := by
  simp [decideHandshake, hNotFull, hStub]

theorem cooperativeProceedIffAvailableAndAnyMatch
    (available : Bool)
    (presented : Option String)
    (canonical : CanonicalIdentity) :
    decideHandshake .cooperative available presented canonical = .proceed ↔
      available = true ∧
        ∃ candidate, presented = some candidate ∧ MatchesEither candidate canonical := by
  cases available with
  | false => simp [decideHandshake]
  | true =>
      cases presented with
      | none => simp [decideHandshake]
      | some candidate =>
          by_cases hFull : MatchesFull candidate canonical
          · simp [decideHandshake, hFull, MatchesEither]
          · by_cases hStub : MatchesStub candidate canonical
            · simp [decideHandshake, hFull, hStub, MatchesEither]
            · simp [decideHandshake, hFull, hStub, MatchesEither]

theorem strictProceedIffAvailableAndFullMatch
    (available : Bool)
    (presented : Option String)
    (canonical : CanonicalIdentity) :
    decideHandshake .strict available presented canonical = .proceed ↔
      available = true ∧
        ∃ candidate, presented = some candidate ∧ MatchesFull candidate canonical := by
  cases available with
  | false => simp [decideHandshake]
  | true =>
      cases presented with
      | none => simp [decideHandshake]
      | some candidate =>
          by_cases hFull : MatchesFull candidate canonical
          · simp [decideHandshake, hFull]
          · by_cases hStub : MatchesStub candidate canonical
            · simp [decideHandshake, hFull, hStub]
            · simp [decideHandshake, hFull, hStub]

theorem strictProceedRequiresFullIdentity
    (available : Bool)
    (presented : Option String)
    (canonical : CanonicalIdentity)
    (hProceed : decideHandshake .strict available presented canonical = .proceed) :
    ∃ candidate, presented = some candidate ∧ MatchesFull candidate canonical := by
  exact (strictProceedIffAvailableAndFullMatch available presented canonical).mp hProceed |>.2

end SemaVerification.Handshake
