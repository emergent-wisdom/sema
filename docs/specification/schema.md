# Schema Spec

## 1. The Pattern Card Schema

Every Sema pattern is a JSON object adhering to this strict schema. This structure ensures that every definition is machine-verifiable, content-addressable, and type-safe.

```json
{
  "handle": "PascalCaseName",
  "derived_from": "sema:AncestorHandle#mh:SHA-256:...", // [Optional] Phylogeny: The evolutionary parent

  // --- HASHED FIELDS (The Definition) ---
  // These fields constitute the Identity. Changing one byte changes the Pattern ID.

  // 1. Dependencies: The "Imports" list.
  // CRITICAL: Every {{key}} in the text MUST map to a full hash here.
  "dependencies": {
    "accepts": {
      "input_noun": "sema:NounType#mh:SHA-256:..."      // Read-only inputs
    },
    "yields": {
      "output_noun": "sema:NounType#mh:SHA-256:..."     // Guaranteed outputs
    },
    "composes_with": {
      "active_tool": "sema:VerbPattern#mh:SHA-256:..."  // Subroutines invoked
    },
    "references": {
      "concept": "sema:ConceptPattern#mh:SHA-256:..."   // Citation/Comparison
    }
  },

  // 2. Signature: The Polymorphic Interface
  // Defines "What kind of thing is this?" for discovery.
  "signature": [
    "Deep(Check(Proof))",  // Nested syntax allowed
    "Gate(Flow)"
  ],

  // 3. Mechanism: The Logic (Source Code)
  // MUST reference dependencies using {{snake_case_keys}}.
  "mechanism": "Executes {{active_tool}} on {{input_noun}} to produce {{output_noun}}...",

  // 4. Contracts: The Unit Tests
  "invariants": ["Safety constraint that always holds true"],
  "preconditions": ["State required before execution"],
  "postconditions": ["State guaranteed after execution"],
  "failure_modes": ["Known risks"],

  // 5. Gloss: The Embedding Anchor
  "gloss": "Short summary for vector search",

  // 6. Data Schema: Required for Nouns (Ring 0)
  "data_schema": {
    "type": "object",
    "properties": { ... } // JSON Schema or Zod definition
  },

  // 7. Parameters: Identity Configuration (Control Plane)
  // Variables that change the Hash/Identity of the pattern.
  // Defaults are OPTIONAL — the base pattern represents the abstract capability.
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
  // These fields help organization but do not change the Identity.
  "sema_id": "sema:Handle#mh:SHA-256:...",  // The computed Merkle Root
  "sema_ref": "Handle#stub",                // Short reference (handle + 4-char hash prefix)
  "sema_stub": "stub",                      // 4-char hash prefix alone
  "sema_layer": "Society",                  // Flattened layer for easy access
  "sema_category": "Governance",            // Flattened category for easy access
  "_meta": {
    "layer": "Society",                   // Stack Layer
    "category": "Governance",             // Functional Group
    "ring": 1,                            // Stability Ring (0=Kernel, 1=StdLib, 2=User)
    "tier": 2,                            // Rigor Tier (0=Primitive, 1=Hard, 2=Soft)
    "related": ["Pattern#stub"],          // Soft links
    "supersedes": ["sema:OldHandle#mh:SHA-256:..."]  // [Optional] Version chain
  }
}
```

## 2. The Dependency Map Categories

Every dependency MUST belong to exactly one category.

| Category | Role | Analogy | Runtime Permission |
| --- | --- | --- | --- |
| **`accepts`** | **Input** | The arguments `func(x)` | **Read Access.** The pattern can inspect this object. |
| **`yields`** | **Output** | The return type `-> y` | **Write Access.** The pattern guarantees creation of this object. |
| **`composes_with`** | **Active Tool** | The function calls `x()` | **Execute Access.** The pattern delegates control to this tool. |
| **`references`** | **Concept** | The comments `// See also` | **None.** Metadata only. |

## 3. The Signature Syntax (`signature`)

The `signature` field declares the **Type Constructor** or **Functional Interface** satisfied by the pattern. This enables polymorphic discovery (e.g., "Find me any pattern that implements `Deep(Trace)`").

### Valid Syntax Forms

* **Single Argument:** `Intent(Target)` → `Check(Nature)`
* **Nested Arguments:** `Intent(Target(Subtarget))` → `Deep(Check(Proof))`
* **Multiple Arguments:** `Intent(Target, Modifier)` → `Transform(Input, Output)`

### The "Truth in Advertising" Rule

If a pattern claims a signature like `Act(Deploy)`, it **MUST** actively invoke the necessary tools (e.g., `composes_with: { "deploy": "..." }`) to fulfill that contract. Empty claims are invalid.

## 4. The Hashing Protocol (Merkle Tree)

Sema uses a recursive Merkle Tree to generate the `sema_id`. This ensures that every component of the definition contributes to the identity.

**The Calculation:**

1. **Leaf Nodes:** Hash individual fields (Mechanism, Gloss, Invariants).
2. **Dependency Nodes:** Hash the Dependency Map (sorted keys).
3. **Root:** `SHA-256( H(Dependencies) || H(Mechanism) || H(Signature) ... )`

**The ID Format:**
`sema:<Handle>#mh:SHA-256:<RootHash>`

* **Handle:** Human-readable name (e.g., `StateLock`).
* **RootHash:** The cryptographic proof of definition.
