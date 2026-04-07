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

