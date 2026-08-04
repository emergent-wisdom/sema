"""
Sema Standard Library (Reference Implementation)
Executable Python classes for Tier 1 Sema patterns.
"""

import hashlib
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


class SemaContractError(Exception):
    """Raised when a pattern invariant is violated."""

    pass


@dataclass
class PatternContext:
    agent_id: str
    timestamp: float
    metadata: dict[str, Any]


class SemaPattern:
    """Base class for all executable patterns."""

    HANDLE = "BasePattern"
    HASH = "mh:none"

    def __init__(self, context: PatternContext):
        self.context = context

    def check_invariants(self, state: dict[str, Any]) -> bool:
        """Override to enforce logic."""
        return True


# --- Coordination Layer ---


class SpectralTune(SemaPattern):
    """
    Handle: SpectralTune#c0aa
    Invariant: Receiver.context_hash == Sender.context_hash
    """

    HANDLE = "SpectralTune"

    @staticmethod
    def generate_tuning_signal(system_prompt: str, nonce: str) -> str:
        """Sender: Generates the challenge hash."""
        payload = f"{system_prompt}:{nonce}"
        return hashlib.blake2b(payload.encode()).hexdigest()

    def verify_handshake(self, sender_signal: str, local_prompt: str, nonce: str) -> bool:
        """Receiver: Verifies alignment."""
        expected = self.generate_tuning_signal(local_prompt, nonce)
        if sender_signal != expected:
            raise SemaContractError(
                f"SpectralTune Failed: Context mismatch. "
                f"Local hash {expected[:8]} != Remote {sender_signal[:8]}"
            )
        return True


class StateLock(SemaPattern):
    """
    Handle: StateLock#c9c2
    Invariant: State S cannot be modified without Sign(A) + Sign(B)
    """

    HANDLE = "StateLock"

    def __init__(
        self, context: PatternContext, required_signers: list[str], timeout_sec: float = 5.0
    ):
        super().__init__(context)
        self.required_signers = set(required_signers)
        self.signatures = set()
        self.locked_at = time.time()
        self.timeout = timeout_sec

    def sign(self, agent_id: str):
        if time.time() - self.locked_at > self.timeout:
            raise SemaContractError("StateLock Timeout: Lock auto-dissolved.")

        if agent_id not in self.required_signers:
            raise SemaContractError(f"StateLock Violation: {agent_id} is not a required signer.")

        self.signatures.add(agent_id)

    def commit(self, operation: Callable):
        if self.signatures != self.required_signers:
            missing = self.required_signers - self.signatures
            raise SemaContractError(
                f"StateLock Invariant Failed: Missing signatures from {missing}"
            )

        return operation()


# --- Governance Layer ---


class GateParsimony(SemaPattern):
    """
    Handle: GateParsimony#f1d8
    Invariant: Length(Core) < Length(Original) * 0.5
    """

    HANDLE = "GateParsimony"

    def evaluate(self, original_text: str, reduced_text: str) -> bool:
        len_orig = len(original_text)
        len_new = len(reduced_text)

        # Check compression
        ratio = len_new / len_orig
        if ratio > 0.5:
            raise SemaContractError(
                f"Parsimony Failed: Compression ratio {ratio:.2f} > 0.5 threshold."
            )

        # Note: In a real system, we'd also check 'Functional Equivalence' via an LLM judge
        return True


# --- Ethical Layer ---


class ProphetFanOut(SemaPattern):
    """
    Handle: ProphetFanOut#8711
    Invariant: generation obeys the declared breadth or stopping rule
    """

    HANDLE = "ProphetFanOut"

    def validate_timelines(self, timelines: list[str]) -> bool:
        if len(timelines) < 3:
            raise SemaContractError("Prophet Invariant Failed: Must generate at least 3 timelines.")

        # Simple diversity check (heuristics)
        unique_words = len(set(" ".join(timelines).split()))
        total_words = len(" ".join(timelines).split())
        diversity_ratio = unique_words / total_words

        if diversity_ratio < 0.4:
            raise SemaContractError(
                f"Prophet Invariant Failed: Low entropy ({diversity_ratio:.2f}). "
                "Timelines are too similar."
            )

        return True


# --- Mind Layer ---


class CounterfactualAnchor(SemaPattern):
    """
    Handle: CounterfactualAnchor#placeholder
    Invariant: Anchor cannot be modified once Observation phase begins.
    """

    HANDLE = "CounterfactualAnchor"

    def __init__(self, context: PatternContext):
        super().__init__(context)
        self.anchor: Any | None = None
        self.anchor_frozen = False
        self.observation: Any | None = None

    def set_anchor(self, prediction: Any):
        """Step 1: Freeze the expectation."""
        if self.anchor_frozen:
            raise SemaContractError("Anchor Violation: Cannot modify anchor after it is frozen.")
        self.anchor = prediction
        self.anchor_frozen = True

    def observe(self, reality: Any) -> float:
        """
        Step 2: Observe reality and calculate delta.
        For this ref implementation, we assume numeric or basic comparable types.
        """
        if not self.anchor_frozen:
            raise SemaContractError("Ordering Violation: Must set anchor BEFORE observing reality.")

        self.observation = reality

        # Simple delta calculation (can be overridden for complex objects)
        if isinstance(self.anchor, int | float) and isinstance(reality, int | float):
            delta = abs(self.anchor - reality)
            return delta
        elif isinstance(self.anchor, str) and isinstance(reality, str):
            # Levenshtein distance placeholder (using set diff for simplicity)
            set_a = set(self.anchor.split())
            set_b = set(reality.split())
            delta = 1.0 - (len(set_a & set_b) / len(set_a | set_b)) if (set_a | set_b) else 0.0
            return delta
        else:
            # Fallback for objects: 0.0 if equal, 1.0 if not
            return 0.0 if self.anchor == reality else 1.0


# --- Usage Example ---

if __name__ == "__main__":
    # 1. Setup
    ctx = PatternContext("Agent_A", time.time(), {})
    print("🤖 Agent System Initialized")

    # 2. Coordination: SpectralTune
    tune = SpectralTune(ctx)
    prompt = "You are a helpful assistant."
    nonce = "12345"
    signal = tune.generate_tuning_signal(prompt, nonce)
    print(f"📡 Tuning Signal: {signal[:12]}...")

    try:
        tune.verify_handshake(signal, "You are a helpful assistant.", nonce)
        print("✅ Handshake Verified.")
    except SemaContractError as e:
        print(f"❌ Handshake Failed: {e}")

    # 3. Governance: GateParsimony
    gate = GateParsimony(ctx)
    idea = "We should utilize a distributed ledger technology to facilitate transactions."
    simple = "Use blockchain for payments."

    try:
        gate.evaluate(idea, simple)
        print(f"✅ Parsimony Passed: '{simple}'")
    except SemaContractError as e:
        print(f"❌ Parsimony Rejected: {e}")

    # 4. Mind: CounterfactualAnchor
    anchor = CounterfactualAnchor(ctx)
    anchor.set_anchor(100)  # Predicted value
    print("⚓ Anchor Frozen: 100")

    try:
        # Attempt to change anchor (should fail)
        # anchor.set_anchor(105)

        delta = anchor.observe(85)  # Reality
        print(f"✅ Learning Signal (Delta): {delta} (Expected 15)")

        if delta > 10:
            print("💡 Surprise detected! Triggering update...")
    except SemaContractError as e:
        print(f"❌ Anchor Failed: {e}")
