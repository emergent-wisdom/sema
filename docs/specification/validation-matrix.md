# Validation Matrix

This document maps the validation rules currently enforced by Sema's schema,
GraphStore, apply, and pull paths. It is a maintained coverage map rather than a
formal proof that no validator exists outside the table.

---

## 1. Structure & Format Validators

| # | Rule | Description | Implemented |
|---|------|-------------|-------------|
| 1.1 | **JSON Validity** | File must be valid JSON | YES |
| 1.2 | **Required Fields** | Must contain: `handle`, `mechanism`, `_meta` | YES |
| 1.3 | **Handle Format** | Must be CamelCase: `^[A-Z][a-zA-Z0-9]+$` | YES |
| 1.4 | **Path Root Enum** | `_meta.path[0]` ∈ {Physics, Mind, Society, Infrastructure} | YES |
| 1.5 | **Tier Enum** | `_meta.tier` ∈ {0, 1, 2, 3} | YES |
| 1.6 | **Ring Enum** | `_meta.ring` ∈ {0, 1, 2} | YES |
| 1.7 | **Taxonomy Path Valid** | `_meta.path` must be one of the valid taxonomy paths | YES |
| 1.8 | **No Empty Fields** | Empty arrays `[]` or objects `{}` must be omitted, not present | YES |
| 1.9 | **No Null Values** | Null values forbidden in hashed fields | YES |

---

## 2. Dependency Validators (The "Wiring" Checks)

| # | Rule | Description | Implemented |
|---|------|-------------|-------------|
| 2.1 | **Valid Categories (Rule A)** | `dependencies` may only contain keys: `accepts`, `yields`, `composes_with`, `references` | YES |
| 2.2 | **No Empty Categories** | Dependency categories must not be empty `{}` | YES |
| 2.3 | **Uniqueness (Rule A)** | A dependency key must appear in exactly one category (no duplicates across categories) | YES |
| 2.4 | **Full Hash Standard (Rule D)** | Every dependency value must match: `^sema:[A-Z][a-zA-Z0-9]+#mh:SHA-256:[a-f0-9]{64}$` | YES |
| 2.5 | **Snake Case Keys** | Dependency keys must be `snake_case` (e.g., `my_tool`, not `MyTool`) | YES |
| 2.6 | **Reference Existence** | Referenced patterns must exist in the database (when `known_handles` provided) | YES |

---

## 3. Text-Code Consistency (Rule B / Prime Directive)

| # | Rule | Description | Implemented |
|---|------|-------------|-------------|
| 3.1 | **Forward Weld** | Every `{{key}}` in text fields must exist in `dependencies` | YES |
| 3.2 | **Inverse Weld** | Every key in `dependencies` must appear as `{{key}}` in text fields | YES |
| 3.3 | **Text Fields Scanned** | Scan: `mechanism`, `gloss`, `invariants`, `preconditions`, `postconditions`, `failure_modes` | YES |

---

## 4. Parameter Validators (Rule C)

| # | Rule | Description | Implemented |
|---|------|-------------|-------------|
| 4.1 | **Field Name** | Field is named `parameters` | YES |
| 4.2 | **Structure** | Must be a list of objects | YES |
| 4.3 | **Required Subfields** | Each object must have: `name`, `type`, `range`, `description` | YES |
| 4.4 | **Optional Default** | The `default` field is allowed but not required | YES |
| 4.5 | **Hash Inclusion** | If `default` exists, it is included in identity hash | YES |

---

## 5. Noun Schema Validators (Rule K)

| # | Rule | Description | Implemented |
|---|------|-------------|-------------|
| 5.1 | **Data Structures Require Schema** | If `_meta.path` ends in `"Data Structures"`, `data_schema` MUST exist | YES |
| 5.2 | **Valid JSON Schema** | `data_schema` must be a valid JSON Schema object | YES |
| 5.3 | **Non-Empty Schema** | `data_schema` must not be empty `{}` | YES |

---

## 6. Signature Validators (Rule F)

| # | Rule | Description | Implemented |
|---|------|-------------|-------------|
| 6.1 | **Syntax** | Each signature must match: `^[A-Z][A-Za-z]*\(.+\)$` | YES |
| 6.2 | **No Bare Names** | Signatures cannot be bare names (e.g., `"Check"` invalid, `"Check(Proof)"` valid) | YES |
| 6.3 | **Explicit Wiring** | Signature types must appear in dependencies (enforces implementation) | YES |

---

## 7. Graph Constraints

| # | Rule | Description | Implemented |
|---|------|-------------|-------------|
| 7.1 | **Acyclicity (DAG)** | New pattern must not create circular dependency chain | YES |
| 7.2 | **Self-Reference Ban** | Pattern cannot depend on itself (A → A) | YES |
| 7.3 | **Transitive Cycle Detection** | Detects A → B → C → A cycles with path reporting | YES |
| 7.4 | **Dangling Reference Prevention** | Cannot remove pattern if ordinary dependents or exact `extends` children would be stranded | YES |
| 7.5 | **Topological Sort** | Patterns added in dependency order (leaf → root) | YES |
| 7.6 | **Dependency Direction (Rule G)** | Dependencies flow specific → general (lower layers don't depend on higher) | YES |

---

## 8. Transaction & Atomicity Validators

| # | Rule | Description | Implemented |
|---|------|-------------|-------------|
| 8.1 | **Apply Preflight** | `sema apply` validates the projected batch before any changes | YES |
| 8.2 | **File Existence** | Pattern files must exist and be readable | YES |
| 8.3 | **Directory Support** | Can add all `*.json` files from a directory | YES |
| 8.4 | **Round-Trip Preservation** | Export → Remove → Add preserves all metadata and hashes | YES |
| 8.5 | **Combined Remove+Add Preflight** | A replacement's removals and additions are validated as one projected batch | YES |
| 8.6 | **Pull Rollback** | Pull restores its pre-write SQLite backup on mutation or verification failure | YES |

---

## 9. Additional Validators (From Code Analysis)

| # | Rule | Description | Implemented |
|---|------|-------------|-------------|
| 9.1 | **Dependency/Related Separation** | Patterns in `dependencies` must not also appear in `_meta.related` | YES |
| 9.2 | **Forbidden Extra Fields** | Only allowed top-level fields permitted (extra='forbid' in Pydantic) | YES |
| 9.3 | **Whitespace Normalization** | Strings are NFC normalized and whitespace-collapsed before hashing | YES |
| 9.4 | **Novelty Check** | Mechanism similarity > 0.92 triggers duplicate warning | YES |
| 9.5 | **Merkle DAG Cascade** | Updating a pattern cascades hash updates through ordinary dependency edges; exact specialization pins do not move implicitly | YES |
| 9.6 | **Handle Extraction** | Correctly extracts handle from `sema:Handle#mh:SHA-256:...` format | YES |

---

## 10. Specialization and Legacy Compatibility

| # | Rule | Description | Implemented |
|---|------|-------------|-------------|
| 10.1 | **Exclusive Keys** | A card cannot contain both `extends` and legacy `derived_from`, even when one value is null | YES |
| 10.2 | **Exact Format** | `extends` must contain a full Sema ID | YES |
| 10.3 | **Active Resolution** | The exact parent definition named by `extends` must be active in the current single-version workspace | YES |
| 10.4 | **Graph Projection** | `extends` emits `IS_A` and participates in ordering and cycle checks | YES |
| 10.5 | **No Silent Retarget** | Parent edits that would strand a child fail before mutation | YES |
| 10.6 | **Reviewed Retarget** | `--retarget-extends` changes staged cards only | YES |
| 10.7 | **Legacy Dual Read** | `derived_from` remains hash-verifiable under its authored key but gains no `IS_A`, ordering, or active-parent semantics | YES |

Every rule listed above has an implemented enforcement point. The executable
tests and source remain authoritative when this coverage map drifts.

---

## Code Locations

| File | Purpose |
|------|---------|
| `src/sema/core/schema.py` | Pydantic models, main validation logic |
| `src/sema/core/validator.py` | Wrapper functions, legacy validation |
| `src/sema/core/hashing.py` | Merkle tree hashing, SEMANTIC_FIELDS list |
| `src/sema/core/dependencies.py` | Topological sort, cycle detection |
| `src/sema/cli/main.py` | Apply command, graph-level checks |
| `src/sema/taxonomy_graph/graph_store.py` | Graph operations, Merkle DAG cascade |
