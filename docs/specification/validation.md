# Validation Rules

## 1. The "Text is Code" Invariants

In Sema, the text fields (`mechanism`, `invariants`, `failure_modes`) are treated as compiled code. The linter enforces strict referential integrity between the text and the dependency map.

### Rule A: The Explicit Dependency Standard

This is the most common validation error. It ensures that the definition's Identity Hash accurately reflects its logic.

1. **Forward Rule (No Magic Globals):** Every `{{key}}` placeholder used in the text MUST have a corresponding entry in the `dependencies` object. You cannot reference a concept you haven't imported.
2. **Inverse Rule (No Silent Imports):** Every key declared in `dependencies` MUST be used at least once in the text fields.
  * *Rationale:* Unused dependencies create "False Fragility"—changing the hash of a pattern without changing its actual logic.

### Rule B: Complete Categorization

Every dependency must belong to **exactly one** category. A pattern cannot simultaneously `yield` and `compose_with` the same object.

| Category | Logical Role | Runtime Implication |
| --- | --- | --- |
| **`accepts`** | **Passive Input** | The pattern reads this data. |
| **`yields`** | **Passive Output** | The pattern creates/modifies this data. |
| **`composes_with`** | **Active Tool** | The pattern executes this logic. |
| **`references`** | **Metadata** | The pattern cites this concept (no runtime effect). |

## 2. Structural Integrity Rules

### Rule C: The Gravity Rule (Dependency Direction)

Dependencies must flow from **Specific  General** or **High-Level  Fundamental**. This prevents circular dependency graphs.

* ✅ **Allowed:** `Toyota` depends on `Car`. (Specific depends on General).
* ✅ **Allowed:** `Society` pattern depends on `Physics` primitive.
* ❌ **Forbidden:** `Physics` primitive referencing `Society` pattern. (Fundamental cannot depend on Emergent).

**Cycle Breaking:** If A and B form a cycle, identify the **Noun** and the **Verb**. The Verb usually depends on the Noun (Action requires Object).

### Rule D: The Empty Field Rule

Never use empty arrays `[]`, empty objects `{}`, or `null` values. If a field has no content, **omit it entirely**.

* *Why?* Canonicalization. An empty field and a missing field should not produce different hashes.

### Rule E: The Noun Schema Requirement

Any pattern that serves as a **Noun** (Category: `Data Structures`, or is used in `accepts`/`yields`) MUST define a `data_schema`. This prevents "Schema Drift," where agents agree on the name "Task" but disagree on its required fields.

**The "Non-Vacuous" Clause:**
The schema must define at least one specific property. Generic definitions (e.g., `{"type": "object"}`) are **strictly forbidden** for Ring 0 Nouns. If the shape is truly arbitrary, use `{"type": "object", "additionalProperties": true}` and document *why* in the mechanism.

## 3. The "Deep Fix" Protocol

When the linter reports an **Unused Dependency** (Inverse Rule Violation), do NOT blindly delete it. The dependency represents a semantic signal from a previous author. You must triage the fix:

1. **Keep & Explain (Missing Text):** The relationship is real (e.g., `Task` yields `Solution`), but the text failed to describe it.
   * *Action:* Update `mechanism` to explicitly reference `{{solution}}`.
2. **Refine Link (Wrong Target):** The relationship is real, but the target pattern is imprecise.
   * *Action:* Swap dependency for a better existing pattern.
3. **Mint New (Missing Concept):** The relationship implies a concept that doesn't exist yet.
   * *Action:* Create a new pattern.
4. **Remove (Hallucination):** The relationship is truly irrelevant or legacy.
   * *Action:* Delete the dependency key.

## 4. Signature & Naming Rules

### Rule F: Signature Syntax (`signature`)

The `signature` field declares the **Type Constructor** or **Functional Interface** of the pattern. Every entry MUST have at least one argument.

**Valid Syntax Forms:**

1. **Single Argument:** `Intent(Target)` (e.g., `Check(Nature)`)
2. **Nested Arguments:** `Intent(Target(Subtarget))` (e.g., `Deep(Check(Proof))`)
3. **Multiple Arguments:** `Intent(Target, Modifier)` (e.g., `Transform(Input, Output)`)

**Forbidden:**

* `"signature": ["Check"]` — Bare name, no argument
* `"signature": ["Trace", "Validate"]` — Two bare names
* `"signature": ["Deep"]` — Even abstract intents need targets

**Rationale:** A bare signature like `["Check"]` is ambiguous—*what* does it check? The argument specifies the domain or target of the polymorphic behavior, enabling the compiler to resolve abstract intents to concrete patterns at runtime.

**The "Truth in Advertising" Invariant:**
If a Pattern claims a `signature`, it MUST fulfill that contract entirely. Do not claim `Act(Deploy)` if the pattern only writes a file but does not execute the deployment.

### Rule G: The Dependency Direction Rule

**The Fundamental Principle:** Dependencies always flow from specific to general. The more fundamental (more general, less specific) pattern is always upstream. Specific patterns depend on general patterns, never the reverse.

**The Rule:** A pattern may only declare dependencies on patterns that are **more fundamental** than itself.

| Pattern | Depends On | Rationale |
| --- | --- | --- |
| `Toyota` | `Car` | Toyota is a specific instance; Car is the general concept |
| `Car` | `Wheel` | Car is an assembly; Wheel is a component |
| `Wheel` | `Circle` | Wheel is a physical object; Circle is a geometric primitive |

**Violations:**

* **Bad:** `Car` depends on `Toyota`. (General cannot depend on specific)
* **Bad:** `Physics` layer referencing `Society` layer. (Lower layers are more fundamental)

### Rule H: The Concept Suspicion Rule

Any **Capitalized Concept** (e.g., "Creation Protocol", "FrameSpec", "MonitorReport") appearing in the text fields MUST be a linked dependency `{{key}}`.

* **Suspicious:** "Executes the Creation Protocol." (Unlinked Proper Noun).
* **Action:**

1. **Mint it:** If it's a real pattern, create it and link it: "Executes the {{creation_protocol}}."
2. **Lowercase it:** If it's just a description, lowercase it: "Executes the creation protocol."

### Rule I: The Half-Concept Ban

It is strictly forbidden to reference "half concepts" by splitting a compound term into separate parts.

* **Bad:** "The {{problem}} Statement..."
* **Good:** "The {{problem_statement}}..." (referencing `sema:ProblemStatement#...`)

### Rule J: Semantic Meaningfulness

Patterns must be semantically substantial and meaningful.

* **No Tautologies:** A pattern cannot define itself by itself.
* **No Vacuous Definitions:** Avoid vague corporate speak or fluff.

### Rule K: The Schema Requirement

Any pattern that serves as a **Data Structure** or a **State-Bearing Primitive** (e.g., `Work`, `Trace`) MUST explicitly define its structure via `data_schema`.

* **Field:** `data_schema` (JSON Schema standard).
* **Rationale:** This defines the "Shape of the Noun," not the "Signature of the Verb." Prevents "Schema Drift."
* **Do Not:** Define `input_schema` here. Inputs are defined by the `accepts` dependency. The verb inherits the schema from the Noun it accepts.

