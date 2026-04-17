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

### 3.1 Layer Definitions — two axes: scope + shape

A pattern's layer is decided by **two axes together**: the scope of the mechanism (who / what the mechanism requires to execute) and the shape of the pattern (Noun component vs. Verb operation). The scope axis is the primary filter; the shape axis decides which category *within* a layer the pattern sits in.

**Scope (primary axis — decides the layer)**:

| Layer | Scope definition | Scope test |
|---|---|---|
| **Physics** | Foundational building blocks — the component-level primitives on which all higher mechanisms compose. Some are substrate (obtain regardless of authorship, e.g. `Entropy`, `Causation`); others are authored-but-foundational components (`Lock`, `Gate`, `Heartbeat`, `Branch`) that act as the low-level *things* every layer above assembles with. | *Is this a foundational component that higher layers compose with, rather than compose from higher-level parts?* |
| **Infrastructure** | Authored structures and operations that *do not require cognition to execute*. Data artifacts, composite topologies, mechanical Verbs (schema validation, sorting, tracing). Built on Physics components. | *Can a program execute this without making any judgment? Is it composed from Physics components rather than being one itself?* |
| **Mind** | Mechanisms that *require cognition* — judgment, reasoning, inference, strategy. Single party is sufficient; cognition alone executes the mechanism. | *Does this require a knower to make a call that cannot be reduced to schema-matching? Can a single isolated agent execute it?* |
| **Society** | Mechanisms that *structurally require ≥2 independent parties* — parties with separate state and potentially divergent interests. Cognition alone is insufficient; external parties are part of the mechanism. | *Does the mechanism structurally require another party whose state is outside this agent's control?* |

**Shape (secondary axis — decides the category within the layer)**:

Each layer contains both Nouns (things) and Verbs (operations):

- Physics Nouns live in `Physics/Primitives` (the default Physics category) and `Physics/Time` (temporal components).
- Infrastructure splits: `Data Structures` = Nouns; `Primitives` = Verbs; `Verification` = verification-Verbs.
- Mind splits: `Memory` / some `Data Structures` = Nouns; `Reasoning` / `Strategy` / `Inference` = Verbs-and-their-products.
- Society splits: `Protocols` / `Governance` = Nouns (rule-sets, contracts); `Coordination` / `Economics` = Verbs (acts between agents).

**Key refinement — Physics is components, not just substrate.** An earlier draft of this section defined Physics narrowly as "obtains regardless of any author." That was too strict — it would evict legitimate foundational components (`Gate`, `Heartbeat`, `Throttle`) that are authored but act as building-block Nouns the rest of the library composes with. The correct framing is: Physics is the **bottom of the compose-with stack** — whether a given component is substrate-given (`Lock`) or authored-but-foundational (`Gate`), it lives in Physics when its role is to be *a component other layers use* rather than *an assembly of other components*.

**Distinguishing axes**:
- *Physics vs. Infrastructure*: foundational component (built-with) vs. higher-level assembly (built-from). If removing the pattern would eliminate a category of building-block, it's Physics. If the pattern is composed from other patterns, it's Infrastructure.
- *Infrastructure vs. Mind*: mechanical (no cognition) vs. cognitive (requires judgment).
- *Mind vs. Society*: single-party (cognition sufficient) vs. multi-party (external parties required by the mechanism).

**The mechanism-vs-deployment distinction** (critical for Mind vs. Society):
- A pattern whose mechanism is a single-agent rule but is *vulnerable to* adversarial inputs in multi-agent deployments is still **Mind**. The vulnerability is compositional: wrap it with Society-layer guards (ReceptivityGate, signed consultation, FailureTrace) to harden.
- A pattern whose mechanism *structurally assumes* ≥2 parties with divergent interests is **Society**. Consensus, Vote, Contract, ConfusedDeputy: these are incoherent with a single isolated agent.

**Worked examples**:
- `Lock`: foundational synchronization component — a Noun at substrate level. → **Physics/Primitives**.
- `Gate`: foundational filter component — a Noun (the shape "condition-filter") that higher-level Verbs compose with. → **Physics/Primitives**.
- `Heartbeat`: foundational liveness-signal component. → **Physics/Time**.
- `Sign`: the *Verb* of attaching a signature. Not a component — an operation using the Identity + Artifact components. → **Infrastructure/Primitives**.
- `Compensate`: the *Verb* of running inverses. Operation, not component. → **Infrastructure/Primitives**.
- `Tree` / `Chain` / `DAG`: topology shapes — Nouns but composed *from* nodes and edges, higher-level assemblies. → **Infrastructure/Data Structures**.
- `MarginalValueRule`: cognitive ratio test. → **Mind**.
- `ChainOfThought`: sequential cognitive derivation. → **Mind**.
- `Consensus`: "multiple parties agree on a value" — incoherent with one party. → **Society**.
- `Validate`: matches an artifact against a schema — no judgment. → **Infrastructure/Verification**.
- `Judge`: produces a quality rating — cognitive judgment required. → **Infrastructure/Primitives** (Verb) or **Mind** depending on whether the judgment is schema-reducible; pattern currently in Infra as a scoring primitive.
- `ConfusedDeputy`: the threat model *is* a 3-party interaction. → **Society**.

**Practical heuristic** — when deciding between Physics and Infrastructure for a low-level pattern, ask: "Is this a *Noun*, a component I can name and compose with?" If yes and it sits at the bottom of the compose stack (not assembled from other patterns), Physics. If it's a Verb that uses Physics Nouns to do something, Infrastructure/Primitives.

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