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
    "path": ["Society", "Governance"],    // Taxonomy path from layer to leaf
    "ring": 1,                            // Stability Ring (0=Core, 1=Extended, 2=Experimental)
    "tier": 2,                            // Rigor Tier (0=Primitive, 1=Hard, 2=Soft)
    "related": ["Pattern#stub"],          // Soft links
    "supersedes": ["sema:OldHandle#mh:SHA-256:..."],  // [Optional] Version chain
    "caution": "Brief warning..."         // [Optional] Risk notice — see below
  }
}
```

### The `caution` field

Optional one-sentence warning shown to agents and humans when a pattern carries elevated risk that isn't already self-evident from its `mechanism`, `invariants`, or `failure_modes`. It lives in `_meta` (unhashed), so it can be revised without changing the pattern's identity.

Add `caution` when the pattern:
- Enables irreversible action (data loss, financial commitment, governance changes)
- Bypasses safety checks or oversight
- Enables evasion, manipulation, or covert coordination

Skip it when:
- The risk is already explicit in the existing fields
- The pattern is purely cognitive with no external effect

The absence of a `caution` flag does not imply safety — many patterns with no flag still require careful application.

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

**The Calculation (canonicalization v2, semahash 0.3.0):**

Every node's hash input is prefixed with a single-byte type tag for domain
separation, so structurally different values can never share a hash
(`"1"` vs `1`, `["a","b"]` vs `{"a":"b"}`, `""` vs `[]` vs `{}`):

1. **Strings:** `SHA-256("s:" + NFC-normalized, whitespace-collapsed text)`
2. **Primitives** (number/bool/null): `SHA-256("p:" + canonical JSON)`
3. **Lists** (order-preserving): `SHA-256("l:" + H(item1) + H(item2) + ...)`
4. **Dicts:** `SHA-256("d:" + H(key1) + H(value1) + ...)`, entries sorted by
   the **normalized** key. Keys that collide after normalization are
   rejected (fail closed) rather than silently merged.
5. **Dependencies:** aliases are authorial, so before hashing, entries are
   re-keyed by lowercased target handle. Multiple aliases referencing the
   same handle hash as a **sorted list** of refs — multiplicity is
   semantic; alias spelling is not.
6. **Root:** the canonical dict of the eleven semantic fields, hashed by
   rule 4.

> **History:** v1 (≤ 0.2.x) hashed untagged bytes and sorted dict entries
> by raw key, so structurally different definitions could collide and the
> same canonical form could hash two ways. 0.3.0 regenerated every
> published hash; pre-0.3.0 vocabularies HALT on handshake and converge
> via `sema pull`. See CHANGELOG 0.3.0.

Reference implementations: `src/sema/core/hashing.py` (library) and
`scripts/test_hash_verification.py` (dependency-free independent verifier —
all bundled patterns must verify from their JSON files alone).

**The ID Format:**
`sema:<Handle>#mh:SHA-256:<RootHash>`

* **Handle:** Human-readable name (e.g., `StateLock`).
* **RootHash:** The cryptographic proof of definition.

### 4.1 The canonicalization-v2 rename boundary

Excluding `handle` means that renaming a pattern does not change **that
pattern's own** digest. It does not yet make the whole Merkle DAG
name-independent. Canonicalization v2 retains target handles in structured
semantic references: dependency keys and values contain them, and
`derived_from` stores a full Sema ID. Renaming a referenced target can
therefore change the hashes of both dependents and derived descendants.

Removing target handles safely is a separate, breaking canonicalization
migration. It must define how local dependency aliases remain bound to
mechanism placeholders while projecting target identities to digests, and it
must normalize `derived_from` under the same policy. The exact v3
representation is a design decision; changing only the aggregate-root
algorithm cannot repair this property.

## 5. Aggregate Vocabulary Roots

A pattern digest identifies one definition. A vocabulary snapshot has two
different identities, because these questions are not equivalent:

1. **Semantic-set root:** do both parties hold the same set of definitions?
2. **Catalog root:** do the same handles resolve to the same definitions?

Both schemes use SHA-256 and the Merkle Tree Hash (MTH) construction from
[RFC 9162 §2.1.1](https://www.rfc-editor.org/rfc/rfc9162.html#section-2.1.1):

- `MTH([]) = SHA-256("")`
- `MTH([d]) = SHA-256(0x00 || d)`
- for `n > 1`, split at the largest power of two `k < n`, then
  `MTH(D) = SHA-256(0x01 || MTH(D[0:k]) || MTH(D[k:n]))`

The recursive split is normative. It uniquely determines non-power-of-two
trees and never duplicates an unpaired final node.

### 5.1 Semantic-set scheme: `sema-semantic-set-v1`

1. Validate every pattern digest as exactly 64 lowercase hexadecimal
   characters and decode it to 32 raw bytes.
2. Deduplicate the raw digests (set semantics).
3. Sort them in ascending unsigned bytewise lexicographic order.
4. For each digest `h`, use this MTH entry:
   `ASCII("sema-semantic-set-v1") || 0x00 || h`.
5. Apply MTH to the resulting ordered entries.

The sorting rule belongs to Sema; Certificate Transparency itself commits an
already ordered log. Sorting by handle, locale text, traversal order, encoded
hex case, or post-leaf hashes is non-conforming.

### 5.2 Catalog scheme: `sema-catalog-v1`

1. Validate each binding as a unique ASCII handle matching
   `[A-Za-z][A-Za-z0-9_-]*` and one canonical 32-byte pattern digest.
2. Sort bindings by ascending raw handle bytes.
3. For handle bytes `name` and digest `h`, use this MTH entry:
   `ASCII("sema-catalog-v1") || 0x00 || uint32be(len(name)) || name || h`.
4. Apply MTH to the resulting ordered entries.

Two handles may bind to the same digest. They contribute one semantic
definition but two catalog bindings, so root payloads publish both
`definition_count` and `pattern_count`.

`sema root` and `sema_root()` expose both roots and their scheme labels.
`sema_handshake(ref="vocab")` compares the semantic-set root;
`sema_handshake(ref="catalog")` compares exact name bindings. A root digest
without its scheme is incomplete protocol state, and a comparison that omits
the scheme must not return `PROCEED`. Pattern data can converge same-scheme
drift via `sema pull`; a scheme mismatch requires a software upgrade and
cannot be repaired by pulling identical leaves.

Database- and catalog-facing aggregate-root producers fail closed if any
catalog pattern lacks a canonical full Sema ID. The low-level root functions
instead accept already-validated digest or binding inputs. Silently skipping a
malformed catalog entry could make two different catalogs produce a false
match.
