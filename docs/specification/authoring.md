# Pattern Authoring Guide

## 0. The Prime Directive: Text is Code

In Sema, a pattern's definition is its cryptographic identity. To guarantee this:
**Every dependency you declare MUST be explicitly "welded" into the text.**

You cannot "silently import" a concept. If you depend on it, you must use it in the mechanism.

* **The Law:** Every key in `dependencies` must appear as `{{key}}` in `mechanism`, `invariants`, `preconditions`, or `postconditions`.
* **The Inverse Law:** Every `{{key}}` used in the text must exist in `dependencies`.

**Why?** The compiler hashes the text. By writing `{{lock}}`, you force the compiler to look up the specific SHA-256 hash of the `Lock` pattern and mix it into *your* pattern's hash. This makes your logic mathematically inseparable from its dependencies.

---

## 1. Workflow (CLI First)

**⚠️ The Database is the Source of Truth.** The `taxonomy.db` database is authoritative. Files in `data/vocabulary/` are **exports**, not sources.

**Never edit vocabulary files directly — use `sema apply` to make changes.**

### Adding a New Pattern

1.  **Create**: Write your new pattern JSON in `data/staging/`.
    ```bash
    # Example: data/staging/NewPattern.json
    ```
2.  **Validate**: Run `sema apply --add data/staging/NewPattern.json --check`.
    *   This catches dependency cycles and schema errors *before* applying.
3.  **Apply**: Run `sema apply --add data/staging/NewPattern.json`.
    *   This adds the pattern to `taxonomy.db`.
4.  **Commit**: Git commit your changes.
5.  **Clean**: Delete the staging file (it's now in the database).

### Modifying an Existing Pattern

1.  **Copy**: Copy the pattern from `data/vocabulary/` to `data/staging/`.
2.  **Edit**: Modify the file in `data/staging/`.
3.  **Apply**: Run `sema apply --add data/staging/PatternName.json`.
4.  **Commit**: Git commit your changes.
5.  **Clean**: Delete the staging file.

### Verification

*   To check for collisions or duplicates: `sema search "term"`
*   To resolve dependencies: `sema resolve <Handle>`

## 2. Core Philosophy

Sema is a content-addressed vocabulary designed for autonomous safety. A pattern is not defined by its name, but by its content.

* **Identity = Definition.** Changing the logic changes the hash.
* **Safety > Convenience.** We use **Hard Links** (Concrete Full Hashes) for all dependencies. No stubs.
* **Single Source of Truth.** All pattern references live in categorized `dependencies` object.
* **Complete Categorization.** Every dependency MUST be in exactly one category: `accepts`, `yields`, `composes_with`, or `references`.
* **Composition = Explicit Wiring.** We map local keys to specific hashes, allowing the mechanism text to reference *specific* inputs, outputs, and tools.

## 2.1 The "Text is Code" Paradigm

In a content-addressed system, "simple text" becomes "hard math." When you write `"Performs the {{act}}..."` in the mechanism, it is not a comment.

1. **Lookup:** The compiler sees `{{act}}` and finds the entry in your `dependencies` block.
2. **Resolution:** It retrieves the **Full SHA-256 Hash** of the `Act` pattern.
3. **Welding:** It hashes **that specific SHA-256** into the definition of the current pattern.

**The Consequence:** You have mathematically guaranteed that **this specific version** of your pattern depends on **that specific version** of `Act`. If `Act` changes, your pattern's Identity Hash changes. This is the "Cryptographic Anchor."

## 2.2 The Bicameral Architecture (Type vs. Definition)

We split the concepts of "Type Identity" and "Internal Logic" to ensure both discoverability and safety.

| Field | Purpose | Analogy | Role |
| --- | --- | --- | --- |
| **`signature`** | **Type Definition (Search)** | The function signature: `Deep(Discover)` | Tells agents *what* structural type this pattern satisfies. Used for polymorphic search. |
| **`dependencies`** | **Internal Wiring (Truth)** | The imports list: `import Detect from '...'` | Tells the compiler *how* it works by importing specific atoms. |

**The Explicit Wiring Rule:**
To strictly prove you satisfy the signature `Act(Deploy)`, you must:

1. **Declare:** Add `Act` and `Deploy` to `dependencies`.
2. **Wire:** Explicitly reference `{{act}}` and `{{deploy}}` in the `mechanism` text.

This "welds" the atoms to your logic, proving the signature is backed by implementation.

## 3. The Schema

Every pattern must adhere to this JSON structure.

```json
{
  "handle": "PascalCaseName",
  "derived_from": "sema:AncestorHandle#mh:SHA-256:...", // Optional: Evolutionary lineage (Full Hash)

  // --- HASHED FIELDS (The Definition) ---

  // 1. Dependencies: Categorized hard links to ALL referenced patterns
  // VALIDATION REQUIRED: Every pattern reference must be in exactly one category
  "dependencies": {
    "accepts": {
      "input_type": "sema:InputType#mh:SHA-256:..."     // Input data/parameters
    },
    "yields": {
      "output_type": "sema:OutputType#mh:SHA-256:..."   // Output data/results
    },
    "composes_with": {
      "tool_key": "sema:ToolHandle#mh:SHA-256:..."      // Patterns actively invoked
    },
    "references": {
      "related_concept": "sema:RelatedConcept#mh:SHA-256:..."  // Conceptual citations
    }
  },

  // 2. Signature: The Structural Types or Functional Interfaces satisfied
  "signature": [
    "AbstractIntent(Noun)",
    "Deep(Discover)"
  ],

  // 3. Data Schema (Persistent Structure)
  // REQUIRED for Nouns (Data Structures) and State-Bearing Primitives (e.g., Work, Trace).
  // Defines the internal structure of this pattern when stored or serialized.
  // DO NOT define function arguments here (use 'dependencies' or 'parameters').
  "data_schema": {
    "type": "object",
    "required": ["field1"],
    "properties": {
      "field1": { "type": "string" }
    }
  },

  // 4. Mechanism: The Logic
  // References dependencies via {{snake_case_key}}
  "mechanism": "Process {{input_type}} using {{tool_key}} to produce {{output_type}}...",

  // 5. Gloss: The Embedding Anchor (Hashed)
  "gloss": "Short summary for search and vector embedding",

  "invariants": ["String describing safety constraint"],
  "preconditions": ["Logical state requirement"],
  "postconditions": ["Logical state guarantee"],
  "failure_modes": ["Known risks and failure scenarios"],

  // 6. Parameters (Identity Configuration)
  // Variables that change the Hash/Identity of the pattern (Control Plane).
  // Defaults are OPTIONAL. The base pattern represents the abstract capability.
  "parameters": [
    {
      "name": "strictness",
      "type": "Enum",
      "range": "{Lenient, Normal, Strict}",
      // "default": "Normal",  <-- OPTIONAL. Omit for abstract type.
      "description": "Configures the tolerance level."
    }
  ],

  // --- METADATA (Unhashed / Mutable) ---
  "sema_id": "sema:Handle#mh:SHA-256:...", // The computed ID
  "sema_ref": "Handle#stub",               // Short reference
  "sema_stub": "stub",                     // 4-char hash prefix
  "sema_layer": "Physics",                 // Flattened for easy access
  "sema_category": "Primitives",           // Flattened for easy access

  "_meta": {
    "layer": "Physics | Mind | Society | Infrastructure", // The Civilization Stack
    "ring": 0 | 1 | 2,                                    // Stability Ring
    "category": "String",                                 // MUST MATCH Standard Taxonomy (See Section 5)
    "tier": 0 | 1 | 2 | 3,                                // Formal Rigor Tier
    "related": ["Pattern#stub1", "Pattern#stub2"],        // Semantically similar patterns
    "suggested_config": []
  }
}

```

## 4. Validation Rules

### Rule A: Complete Categorization

Every dependency MUST be in exactly one category within the `dependencies` object:

```python
all_keys = (
    set(dependencies.accepts.keys()) |
    set(dependencies.yields.keys()) |
    set(dependencies.composes_with.keys()) |
    set(dependencies.references.keys())
)
assert len(all_keys) == total_count, "Keys cannot appear in multiple categories"

```

**Category Definitions & Rules:**

1. **`accepts` (Input/Passive)**

* **Rule:** The pattern requires this data *object* to exist before it can start. It reads/consumes it.
* **Target Type:** Noun (Data, State, Artifact).
* **Mechanism Test:** "Process {{x}}", "Analyze {{x}}", "Requires {{x}}".
* **Runtime:** Read Access.

2. **`yields` (Output/Passive)**

* **Rule:** The pattern guarantees the creation or modification of this data *object* upon completion.
* **Target Type:** Noun (Result, Outcome, Artifact).
* **Mechanism Test:** "Produces {{x}}", "Returns {{x}}", "Generates {{x}}".
* **Runtime:** Write Access.

3. **`composes_with` (Active/Execution)**

* **Rule:** The pattern actively *invokes* or *delegates to* this pattern as a subroutine.
* **Target Type:** Verb (Tool, Function, Process).
* **Mechanism Test:** "Uses {{x}} to...", "Invokes {{x}}", "Calls {{x}}".
* **Runtime:** Execution Call.

4. **`references` (Conceptual/Citation)**

* **Rule:** The pattern's definition relies on the *concept* of the other pattern, but does not invoke it or pass data.
* **Target Type:** Any.
* **Mechanism Test:** "Implements logic from {{x}}", "Contrast with {{x}}", "Based on {{x}}".
* **Runtime:** None (Static metadata).

**Global Constraint: DAG Requirement**

ALL dependency categories (`accepts`, `yields`, `composes_with`, `references`) MUST form a Directed Acyclic Graph. No cycles allowed in any category.

* **Rationale:** Dependencies are hashed into the pattern's identity via Merkle tree. A cycle creates infinite hash recursion: A's hash depends on B's hash, which depends on A's hash.
* **Fix for Cycles:** If two patterns are conceptually related but create a cycle, one direction must be removed. Use `_meta.related` for non-hashed semantic associations.

### Rule B: The "Explicit Dependency" Standard

**1. Forward Rule: Used Keys Must Be Declared**
Every `{{key}}` placeholder in `mechanism`, `failure_modes`, `preconditions`, or `postconditions` MUST have a corresponding entry in the categorized `dependencies` object.

**2. Inverse Rule: Declared Keys Must Be Used**
Every key defined in the `dependencies` object MUST be referenced via `{{key}}` in at least one of the hashed text fields (`mechanism`, `invariants`, `preconditions`, `postconditions`, `failure_modes`).

* **Rationale:** Dependencies are part of the identity hash. Unused dependencies create "False Fragility" (changing hash without changing logic). "Silent imports" are forbidden.

**The "Deep Fix" Protocol (Handling Violations)**
When fixing an Inverse Rule violation (unused dependency), do NOT blindly delete it. The dependency represents a Semantic Signal from a previous author. You must triage:

1. **Keep & Explain (Missing Text):** The relationship is real (e.g., Task yields Solution), but the text failed to describe it. *Action: Update mechanism to explicitly reference the dependency.*
2. **Refine Link (Wrong Target):** The relationship is real, but the target pattern is imprecise. *Action: Swap dependency for a better existing pattern.*
3. **Mint New (Missing Concept):** The relationship implies a concept that doesn't exist yet. *Action: Create a new pattern.*
4. **Remove (Hallucination):** The relationship is truly irrelevant or legacy. *Action: Delete.*

Use **snake_case keys** (Field Style) for dependency keys.

* **Bad:** `mechanism: "Uses {{sema:Trace#...}}"` (embedding raw hash)
* **Bad:** `dependencies: { "composes_with": { "Logger": "..." } }, mechanism: "Uses {{Logger}}"` (PascalCase key)
* **Good:** `dependencies: { "composes_with": { "logger": "sema:Trace#..." } }, mechanism: "Uses {{logger}}"`

**Validation:** The ingester will reject patterns where:

* `{{key}}` is used but `key` is not in dependencies.
* `key` is in dependencies but never used in text.

### Rule C: The Four-Field Architecture

We strictly distinguish four types of fields based on their purpose:

| Field | Plane | Purpose | Hashed? |
|-------|-------|---------|---------|
| **`parameters`** | Control | Pattern configuration (changes identity) | YES |
| **`accepts`** | Dependency | Input patterns this pattern consumes | YES |
| **`yields`** | Dependency | Output patterns this pattern produces | YES |
| **`data_schema`** | Data | Runtime payload structure | YES |

#### 1. `parameters` (Control Plane)
* **Definition:** Configuration variables that alter the behavior or identity of the pattern (e.g., `timeout`, `strictness`).
* **Effect:** Changing a parameter value changes the Pattern's Hash (creates a derived instance).
* **Requirement:** Each parameter object must have `name`, `type`, `range`, `description`. The `default` field is **optional**.
* **Rationale:** The base pattern (e.g., `AcceptSpec`) represents the **Abstract Type**. Concrete values are applied at usage time (e.g., `AcceptSpec(strictness=Strict)`).

#### 2. `accepts` / `yields` (Dependency Plane)
* **Definition:** Patterns that this pattern takes as input (`accepts`) or produces as output (`yields`).
* **Effect:** Changing these creates different graph edges and changes the hash.
* **Target Type:** Typically Nouns (Data Structures).
* **Rationale:** Defines the "function signature" of the pattern: what goes in, what comes out.

#### 3. `data_schema` (Data Plane)
* **Definition:** JSON Schema defining the structure of the runtime data payload.
* **Effect:** Changing the schema changes the Pattern's Hash.
* **Requirement:** Must be valid JSON Schema. Required for Nouns and patterns in `accepts`/`yields`.

### Rule D: The "Full Hash" Standard

Every reference to another pattern MUST be a **Full Sema ID** (`sema:Handle#mh:SHA-256:...`). Stubs (`Handle#1234`) are strictly forbidden in hashed fields.

### Rule E: Metadata Enums (The Constitution)

The `_meta` fields allow the system to organize the graph. Values MUST adhere to these definitions:

**Layer (The Civilization Stack)**

* `Infrastructure`: The foundational data structures and primitives. (e.g., Bid, Trace, Category).
* `Physics`: The rules governing state and behavior. (e.g., Entropy, State, Event).
* `Mind`: Cognitive processes and reasoning. (e.g., Reason, Plan, Optimize).
* `Society`: Multi-agent coordination and governance. (e.g., Vote, Auction, Negotiate).

**The "Game Engine" Analogy:**

Think of it like building a video game:

| Layer | Index | What It Is | Examples | Why This Order |
|-------|-------|------------|----------|----------------|
| **Infrastructure** | 0 | The Code & Data | `Bid`, `Trace`, `Category`, `Vector` | Before "gravity" exists, you need to define what an `Object` is |
| **Physics** | 1 | The Rules of the Simulation | `Entropy`, `State`, `Event`, `Causation` | Rules govern the stuff; stuff must exist first |
| **Mind** | 2 | The AI Players | `Reason`, `Plan`, `Optimize` | Agents think about a world that has rules |
| **Society** | 3 | The Multiplayer Game | `Vote`, `Auction`, `Negotiate` | Agents must exist before they can coordinate |

**The Layer Direction Guideline (Rule 7.6):**

Dependencies **should** generally flow from higher to lower layers. A pattern that heavily depends on upper-layer concepts may be misclassified and should be reviewed. However, some cross-layer references are semantically necessary (e.g., `Belief` (Infrastructure) referencing `Agent` (Mind) — beliefs are held by agents).

* ✅ `Society` → `Mind` → `Physics` → `Infrastructure` (preferred: downward references)
* ⚠️ `Infrastructure` → `Mind` (permitted if semantically necessary and acyclic)
* ❌ Any cycle: `A` → `B` → `A` (forbidden: breaks Merkle hashing)

**The hard constraint is the DAG (no cycles). The layer direction is a style guide.**

**Ring (Stability)**

* `0` (Kernel): Timeless primitives (Logic, State, Arithmetic). Changes require a hard fork.
* `1` (Standard Lib): Established protocols (Voting, Logging). Stable for years.
* `2` (Userland): Evolving cognitive tactics (Prompts, heuristics). Stable for months.

**Tier (Rigor)**

* `0` (Primitive): Atomic Nouns/Verbs (e.g., Check, Agent).
* `1` (Ironclad): Complete formal contracts (Pre/Post/Invariants). Safe for autonomous use.
* `2` (Honesty-Dependent): Assumes alignment-seeking agents. Vulnerable to collusion.
* `3` (Experimental): Novel or incomplete. Use with human oversight.

### Rule F: Signature Syntax (`signature`)

The `signature` field declares the **Type Constructor** or **Functional Interface** of the pattern. Every entry MUST have at least one argument.

**Valid Syntax Forms:**

1. **Single Argument:** `Intent(Target)` (e.g., `Check(Nature)`)
2. **Nested Arguments:** `Intent(Target(Subtarget))` (e.g., `Deep(Check(Proof))`)
3. **Multiple Arguments:** `Intent(Target, Modifier)` (e.g., `Transform(Input, Output)`)

**Forbidden:**

* ❌ `"signature": ["Check"]` — Bare name, no argument
* ❌ `"signature": ["Trace", "Validate"]` — Two bare names
* ❌ `"signature": ["Deep"]` — Even abstract intents need targets

**Rationale:** A bare signature like `["Check"]` is ambiguous—*what* does it check? The argument specifies the domain or target of the polymorphic behavior, enabling the compiler to resolve abstract intents to concrete patterns at runtime.

**The "Truth in Advertising" Invariant:**
If a Pattern claims a `signature`, it MUST fulfill that contract entirely. Do not claim `Act(Deploy)` if the pattern only writes a file but does not execute the deployment.

### Rule G: The Dependency Direction Rule

**The Fundamental Principle:** Dependencies always flow from specific → general. The more fundamental (more general, less specific) pattern is always upstream. Specific patterns depend on general patterns, never the reverse.

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

## 5. The Hashing Protocol (Merkle Tree)

Sema uses a **Recursive Merkle Tree** strategy (PDF Section 3.2), not a flat JSON hash. This ensures that every field has a unique hash, enabling Partial Alignment.

1. **Hashed Fields:**
   * `mechanism`, `gloss`, `derived_from`
   * `dependencies` (Recursive Hashes)
   * `parameters` (Name, Type, Range, Default [if defined])
   * `data_schema` (The defined structure)
   * `signature`, `invariants`, `preconditions`, `postconditions`, `failure_modes`
2. **Excluded Metadata:** `handle`, `sema_id`, `sema_ref`, `sema_stub`, `_meta` (including `related`).
3. **Identity Generation:**

* **Primitives:** `SHA-256(canonical(value))`
* **Lists:** `SHA-256(H(item1) || H(item2)...)`
* **Dictionaries:** `SHA-256(Sort(H(key)||H(val))...)`
* **Root:** `id(d) = sema:<Handle>#mh:SHA-256:<RootHash>`

*Note: The system handles the calculation, but you must ensure the content in Hashed Fields is strictly accurate. Whitespace or punctuation changes will alter the Identity.*

*Note: Adding, removing, or changing a `default` value of a `parameter`, or modifying `data_schema`, changes the Identity Hash.*

## 6. Naming Morphology & Style

Pattern names must be self-documenting. Use the structure: **`[SpecificNuance][ReusableType]`**.

### 6.1 The Verification Stack (The "Check" Spectrum)

We strictly distinguish between four types of verification patterns. Choose the one that matches the *nature of the activity* and its *effect on flow*.

| Pattern Type | Role | Output | The Question | Example |
| --- | --- | --- | --- | --- |
| **Gate** | **Enforcer (Flow Control)** | **Decision** (Open/Close/Debt) | *"Do we proceed?"* | `PUREGate`, `AuthGate` |
| **Check** | **Investigator (Fact Finding)** | **Status** (Verified/Falsified) | *"Is this true?"* | `SteelmanCheck`, `FactCheck` |
| **Judge** | **Evaluator (Valuation)** | **Score** (0.0 to 1.0) | *"Is this good?"* | `Parsimony`, `Aesthetics` |
| **Validate** | **Clerk (Compliance)** | **Boolean** (Pass/Fail) | *"Does it fit?"* | `SchemaValidate`, `InputGuard` |

### 6.2 Naming Suffixes

#### A. Control Structures (Flow)
*Use these suffixes to define "How does it run?"*

* **...Loop**: Cycle/Recursion (`SocraticLoop`).
* **...Mode**: Configuration/State (`SynergisticMode`).
* **...Protocol**: Multi-step interaction (`ForkingProtocol`).
* **...Sim**: Virtual Execution (`MentalSim`).
* **...Switch**: Transition (`ContextSwitch`).

#### B. Data Containers (Nouns)
*Use these suffixes to define "What is this object?"*

* **...Spec**: Requirements (`FrameSpec`).
* **...Manifest**: Inventory (`SolverManifest`).
* **...Log**: Immutable History (`AuditLog`).
* **...Anchor**: Reference Point (`ConceptAnchor`).
* **...Map**: Topology (`UncertaintyMap`).

#### C. Operators (Verbs)
*Use these suffixes to define "What action?"*

* **...Search**: Exploration (`BeamSearch`).
* **...Update**: Modification (`BayesUpdate`).
* **...Trace**: Lineage (`SimulationTrace`).

### 6.3 The Namespace Stewardship Rule

Before claiming a short, general Handle (e.g., `Parsimony`), apply the **Occupancy Test**: *"Would a future user expect this Handle to mean something broader?"*
* If **YES**: Rename to `SpecificParsimony`.
* If **NO**: Claim it.

## 7. Standard Taxonomy

To prevent vocabulary fragmentation, the `_meta.category` field MUST be selected from the following standard list (enforced by the compiler in `src/sema/core/schema.py`):

### Physics Layer

* **Dynamics**
* **Primitives**
* **Time**

### Mind Layer

* **Inference**
* **Memory**
* **Reasoning**
* **Strategy**

### Society Layer

* **Coordination**
* **Economics**
* **Governance**
* **Protocols**
* **Roles**

### Infrastructure Layer

* **Data Structures**
* **Primitives**
* **Safety**
* **Verification**

---

*End of Instructions. Proceed to Mint.*
