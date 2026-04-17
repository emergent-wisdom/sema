# Core Philosophy

## 1. The Central Dogma: Identity is Definition

Sema is a content-addressed vocabulary designed for autonomous safety. In traditional systems, a word like "Safety" points to a mutable definition that can drift over time. In Sema, the word **IS** the definition.

### Hash the Meaning, Get the Word

We apply the Git principle to semantics. To create a pattern, you define its logic, invariants, and dependencies, and then compute a Merkle Root hash of those fields.

* **The Hash is the Identifier.** If you change one byte of the logic, you get a different hash—and thus a different word.
* **Fail-Closed Coordination.** If Agent A and Agent B hold different definitions for the same handle, the hash comparison fails immediately. The system halts before execution begins, preventing silent misalignment.

## 2. The "Text is Code" Paradigm

In Sema, the text within a `mechanism` field is not a comment; it is a compilation instruction.

When you write:

> *"Performs the {{act}} of..."*

The compiler treats this as a hard mathematical operation:

1. **Lookup:** It finds `act` in your `dependencies` block.
2. **Resolution:** It retrieves the **Full SHA-256 Hash** of the `Act` pattern.
3. **Welding:** It hashes *that specific version* of `Act` into the identity of your new pattern.

**Consequence:** You have mathematically guaranteed that *this* version of your pattern depends on *that* specific version of `Act`. If the definition of `Act` evolves, your pattern's identity changes to reflect the new dependency.

## 3. The Civilization Stack (Layers)

The vocabulary is organized into four fundamental layers that mimic a civilization stack. Dependencies must strictly flow from **High-Level → Fundamental** (Gravity Rule).

| Layer | Domain | Function | The "Hardware" Analogy |
| --- | --- | --- | --- |
| **Infrastructure** (Layer 0) | **Constraints** | Safety rails, resource limits, and operational boundaries. Most fundamental. | **The Kernel.** (Budget, Sandbox, Gate) |
| **Physics** (Layer 1) | **Immutable Laws** | The substrate of consistency, state, and time. These patterns cannot be "wished away." | **The Hardware.** (State, Entropy, Lock) |
| **Mind** (Layer 2) | **Cognition** | Reasoning, planning, and self-correction. Decomposable processes for transforming information. | **The Software.** (Think, Reason, Interpret) |
| **Society** (Layer 3) | **Interaction** | Multi-agent coordination, economics, and trust. Patterns that emerge between agents. Most abstract. | **The Network.** (Vote, Consensus, Protocol) |

**Dependency Invariant:** `Infrastructure` constrains `Physics`, which supports `Mind`, which enables `Society`. Hard dependencies (`accepts`, `composes_with`) must flow from higher layers to lower. Soft citations (`references`) and outputs (`yields`) are exempt.

### 3.1 Tight Layer Definitions (the mechanism-sufficiency test)

The four-layer table names the layers; these definitions give the *test* that decides where a pattern belongs. The axis is **what the pattern's mechanism structurally requires to execute** — not what it is typically used for, and not what it conceptually operates on. Application context is deployment metadata; mechanism is the pattern.

| Layer | Tight definition | Test question |
|---|---|---|
| **Physics** | Substrate primitives that *obtain regardless of any author*. The given conditions on which cognition runs. Cannot be designed. | *Does this exist whether or not anyone thinks about it?* |
| **Infrastructure** | Authored structures and operations that *do not require cognition to execute*. Data types, computational primitives, control flow, schema validation. Mechanical. | *Can a program execute this without making any judgment?* |
| **Mind** | Operations that *require cognition* — judgment, reasoning, inference, strategy. Single party is sufficient. Cognition alone executes the mechanism. | *Does this require a knower to make a call that cannot be reduced to schema-matching? Can a single isolated agent execute it?* |
| **Society** | Operations that *structurally require ≥2 independent parties* — parties with separate state and potentially divergent interests. Cognition alone is insufficient; external parties are part of the mechanism. | *Does the mechanism structurally require another party whose state is outside this agent's control?* |

**Distinguishing axes**:
- *Physics vs. Infrastructure*: substrate (given) vs. authored (designed).
- *Infrastructure vs. Mind*: mechanical (no cognition) vs. cognitive (requires judgment).
- *Mind vs. Society*: single-party (cognition sufficient) vs. multi-party (external parties required by the mechanism).

**The mechanism-vs-deployment distinction** (critical for Mind vs. Society):
- A pattern whose mechanism is a single-agent rule but is *vulnerable to* adversarial inputs in multi-agent deployments is still **Mind**. The vulnerability is compositional: wrap it with Society-layer guards (ReceptivityGate, signed consultation, FailureTrace) to harden.
- A pattern whose mechanism *structurally assumes* ≥2 parties with divergent interests is **Society**. Consensus, Vote, Contract, ConfusedDeputy: these are incoherent with a single isolated agent.

**Worked examples**:
- `MarginalValueRule`: the mechanism is an arithmetic ratio test. A single isolated agent can apply it on its own Pathway Memory. Vulnerable to false estimates in adversarial deployment, but that is compositional hardening. → **Mind**.
- `ChainOfThought`: sequential cognitive derivation. No external party required. → **Mind**.
- `Consensus`: "multiple parties agree on a value" — incoherent with one party. → **Society**.
- `Lock`: atomicity of mutual exclusion is a substrate property (kernel/hardware level), not authored cognition. → **Physics**.
- `Validate`: matches an artifact against a schema — no judgment. → **Infrastructure**.
- `Judge`: produces a quality rating — cognitive judgment required. → **Mind**.
- `ConfusedDeputy`: the threat model *is* a 3-party interaction (agent + principal + attacker). → **Society**.

**The Parametric Exception (Smart Infrastructure):**
Fundamental layers (Infrastructure/Physics) may *wrap* High-Level patterns (Mind/Society) **only if** the High-Level pattern is treated as an opaque parameter (e.g., a `Condition` or `Metric`) that resolves to a strict value (Boolean/Scalar).
* *Rationale:* This allows the infrastructure to enforce *decisions* made by higher-order cognition (e.g., "Is this parsimonious?") without needing to understand the cognition itself.

## 4. Rings of Stability

To prevent "Cognitive Bloat," we distinguish between timeless laws and evolving tactics.

* **Ring 0: The Kernel (Immutable).** The "BIOS" of agency. Nouns (`Task`), Interfaces (`Trait`), and Physics (`StateLock`). These logic gates do not go out of style. Changes here require a hard fork.
* **Ring 1: The Standard Library (Stable).** The "LibC" of coordination. Established protocols like `Voting`, `Auctions`, and `Logging`. These evolve slowly over years.
* **Ring 2: Userland (Fluid).** Cognitive tactics and heuristics like `ChainOfThought` or `SteelmanCheck`. These evolve rapidly as model capabilities change.

## 5. The Bicameral Architecture

Sema splits a pattern into two distinct concepts to ensure both safety and discoverability.

### A. The Definition (The Truth)

* **Source:** `dependencies`, `mechanism`, `invariants`.
* **Role:** Defines *how* it works.
* **Behavior:** Hashed into the Identity. Rigid and immutable.

### B. The Type Signature (The Interface)

* **Source:** `signature` field (e.g., `Deep(Discover)`).
* **Role:** Defines *what* it does.
* **Behavior:** Used for polymorphic discovery. Allows an agent to ask for "Any pattern that implements Deep Discovery" without knowing the specific implementation hash.