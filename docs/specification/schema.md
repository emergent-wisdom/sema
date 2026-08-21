# Schema Spec

## 1. The Pattern Card Schema

Every Sema pattern is a JSON object adhering to this strict schema. This structure ensures that every definition is machine-verifiable, content-addressable, and type-safe.

```json
{
  "handle": "PascalCaseName",

  // --- HASHED FIELDS (The Definition) ---
  // These fields constitute the Identity. Changing their canonical content changes
  // the Pattern ID; raw spelling differences normalized by §4 do not.
  // There are exactly eleven, enumerated in §5.

  // 0. Specialisation: the pattern this one is a kind of.
  // HASHED, and it emits an IS_A edge — see §5. Renamed from `derived_from`;
  // version lineage is a different relation and lives unhashed in _meta.supersedes.
  "extends": "sema:AncestorHandle#mh:SHA-256:...", // [Optional]

  // 1. Dependencies: The "Imports" list.
  // CRITICAL, and enforced in BOTH directions:
  //   - every {{key}} in the text MUST map to a full hash here, and
  //   - every entry here MUST be referenced by a {{key}} somewhere in the
  //     hashed text. An unused declaration is rejected as an
  //     "Inverse dependency violation: declared but never used in text".
  // A consequence worth knowing: deleting the last {{placeholder}} that uses a
  // dependency deletes the dependency. Placeholders sitting decoratively in an
  // invariant's label prefix are therefore load-bearing.
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

  // 6. Data Schema: REQUIRED when the taxonomy path ends in "Data Structures".
  // The validator keys on the path, not on the ring — the two do not coincide.
  // Of 455 bundled patterns, 158 are ring 0 and 94 end in "Data Structures",
  // overlapping on 55. A pattern outside that category may still define one.
  "data_schema": {
    "type": "object",
    "properties": { ... } // JSON Schema or Zod definition
  },

  // 7. Parameters: Identity Configuration (Control Plane)
  // Variables that change the Hash/Identity of the pattern.
  // Defaults are OPTIONAL — the base pattern represents the abstract capability.
  //
  // NOT for per-instance data. A value that differs between two invocations of
  // the same pattern is instance data and belongs in `data_schema`. Putting it
  // here asserts that each value is a DIFFERENT PATTERN. The test: would a
  // descendant that fixes this value be a pattern worth naming? If yes it is a
  // parameter; if it just varies per call, it is a schema property.
  // Modes and thresholds are usually parameters; measurements and readings are not.
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

## 4. The Hashing Protocol (Normative Merkle Encoding)

Sema uses a recursive Merkle Tree to generate the `sema_id`. This ensures that every component of the definition contributes to the identity.

**The calculation (canonicalization v2, semahash 0.3.0):**

The input is strict UTF-8 JSON without a byte-order mark, duplicate object
members, non-finite or overflowing real numbers, or lone Unicode surrogates.
JSON object keys are strings. Direct in-memory callers must supply the same
JSON value domain; tuples, byte strings, and non-string object keys are rejected.

Every node preimage starts with a two-byte ASCII domain tag. This separates
structurally different values (`"1"` vs `1`, `["a","b"]` vs `{"a":"b"}`,
and `""` vs `[]` vs `{}`):

1. **Strings:** `SHA-256("s:" + normalized UTF-8 text)`. Apply Unicode NFC,
   then remove leading and trailing runs of the following exact whitespace set
   and replace every remaining non-empty run with U+0020: U+0009-U+000D,
   U+001C-U+001F, U+0020, U+0085, U+00A0, U+1680, U+2000-U+200A,
   U+2028-U+2029, U+202F, U+205F, and U+3000. The whitespace repertoire is a
   protocol constant, not a property inherited from the host language.

   **V2 compatibility boundary:** semahash v2 did not commit the Unicode data
   version used by NFC. Changing that retroactively would alter some previously
   valid external IDs. Deployments that require reproducibility across runtimes
   must pin their runtime and Unicode normalization version. The golden vectors
   cover stable interoperability cases, not every version-sensitive Unicode
   string. Fully version-independent normalization requires a future hash
   version with an explicit migration rule.
2. **Primitives** (number/bool/null): `SHA-256("p:" + v2 primitive spelling)`.
   Null and booleans are `null`, `true`, and `false`. Integer tokens remain
   signed base-10 integers. Real tokens are finite IEEE 754 binary64 values and use
   the compact finite number spelling produced by the compatibility expression
   `json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)`.
   V2 deliberately distinguishes `1` from `1.0` and preserves `-0.0`. The real
   spelling uses Python's shortest-roundtrip significant digits, with fixed
   notation for decimal exponents from -4 through 15 and scientific notation otherwise;
   scientific notation uses lowercase `e`, an explicit exponent sign, and at
   least two exponent digits. An integral real in fixed notation retains `.0`.
   This is not RFC 8785/JCS; non-Python implementations must match the golden
   vectors below.

   **V2 integer boundary:** semahash v2 did not commit a maximum integer size;
   parsing and decimal conversion limits therefore follow the implementation
   runtime. Deployments requiring reproducibility for unusually large integers
   must pin that runtime. A portable size bound requires a future hash version
   and migration rule.
3. **Lists** (order-preserving): `SHA-256("l:" + H(item1) + H(item2) + ...)`.
   Each child digest is the 64-character lowercase ASCII hexadecimal digest,
   not its raw 32 bytes.
4. **Dicts:** `SHA-256("d:" + H(key1) + H(value1) + ...)`, using the same
   lowercase ASCII hexadecimal digests. Entries are sorted lexicographically by
   the sequence of Unicode scalar values in the **normalized** key. This is
   code-point order, not UTF-16 code-unit order. Keys that collide after
   normalization are rejected rather than silently merged.
5. **Dependencies:** aliases are authorial, so before hashing, entries are
   re-keyed by lowercased target handle. Multiple aliases referencing the
   same handle hash as a **sorted list** of refs — multiplicity is
   semantic; alias spelling is not.
6. **Root:** the canonical dict of the eleven semantic fields (§5), hashed by
   rule 4.

> **History:** v1 (≤ 0.2.x) hashed untagged bytes and sorted dict entries
> by raw key, so structurally different definitions could collide and the
> same canonical form could hash two ways. 0.3.0 regenerated every
> published hash; pre-0.3.0 vocabularies HALT on handshake and converge
> via `sema pull`. See CHANGELOG 0.3.0.

Normative interoperability cases, including exact preimages and rejection
cases, are published in
[`canonicalization-v2-test-vectors.json`](canonicalization-v2-test-vectors.json).
The `input_json` field is intentionally a string so integer and real tokens
remain distinguishable across host-language parsers.

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
semantic references: dependency keys and values contain them, and `extends`
stores a full Sema ID. Renaming a referenced target can therefore change the
hashes of both dependents and descendants.

Removing target handles safely is a separate, breaking canonicalization
migration. It must define how local dependency aliases remain bound to
mechanism placeholders while projecting target identities to digests, and it
must normalize `extends` under the same policy. The exact v3 representation is
a design decision; changing only the aggregate-root algorithm cannot repair
this property.

## 5. The Eleven Semantic Fields

These are the fields that constitute identity. The canonical list is
`SEMANTIC_FIELDS` in `src/sema/core/hashing.py`; this table is the
documentation of it, in declaration order.

| # | Field | Note |
| --- | --- | --- |
| 1 | `dependencies` | Re-keyed by target handle before hashing — aliases are authorial (§4 rule 5) |
| 2 | `signature` | Subject to Truth in Advertising (§3) |
| 3 | `data_schema` | Required when the path ends in `Data Structures` |
| 4 | `mechanism` | |
| 5 | `gloss` | |
| 6 | `invariants` | |
| 7 | `preconditions` | |
| 8 | `postconditions` | |
| 9 | `parameters` | Identity configuration, not instance data (§1) |
| 10 | `failure_modes` | |
| 11 | `extends` | Hashed specialisation claim; emits `IS_A` — see below |

Everything else is metadata. `_meta.supersedes`, `_meta.caution`,
`_meta.related`, the `sema_*` fields, and the design sidecar are all outside
the hash, so they can be revised without minting a new identity.

### Specialisation is not version history

`extends` says **"this pattern is a kind of that exact parent definition."** It
is part of the definition, so it is hashed, stores a full Sema ID, and emits an
`IS_A` graph edge. It participates in dependency ordering and cycle validation.
The referenced parent version is immutable: publishing a newer version of the
parent does not make the child's existing claim false or silently change its
meaning.

`_meta.supersedes` says **"this version replaces those earlier versions."** It
records provenance rather than meaning, so it is unhashed and may contain
more than one prior Sema ID. Keeping it outside the hash preserves the rule
that identity is a function of content and permits history to be recorded
without recursively minting another identity.

These relations confer no implicit contract inheritance. A child must state
the contracts needed to substantiate its `extends` claim. An author may
explicitly retarget a child to a newer parent, preferably as part of the parent
change, but that retargeting is a semantic edit and must not be inferred from a
matching handle. If a child remains pinned, its exact parent definition must
remain resolvable by hash. Conformance to an abstract surface belongs in
`signature` and emits `HAS_SIGNATURE`, not `IS_A`.

The protocol permits a registry to retain multiple immutable versions per
handle. The current GraphStore does not: it indexes one active definition per
handle. Its apply preflight therefore rejects a parent change that would
strand an existing child. The author must stage reviewed children and request
their retargeting explicitly; historical version storage remains future work.

For compatibility, 0.4 clients can still read and verify a pre-0.4 card whose
Merkle input used the field name `derived_from`. That legacy key remains part
of that card's historical hash; it is not silently normalized to `extends`,
validated as a specialization claim, or projected to an `IS_A` edge. A card
carrying both fields is rejected. Migrating a legacy card to `extends` is an
explicit semantic edit and mints a new identity.

## 6. Aggregate Vocabulary Roots

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

### 6.1 Semantic-set scheme: `sema-semantic-set-v1`

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

### 6.2 Catalog scheme: `sema-catalog-v1`

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
