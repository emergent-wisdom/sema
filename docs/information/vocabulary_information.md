# Vocabulary Information

## System Status

- **Semantic-set Root**: `3f6cfecffa0eb0d38e9ddcc8cc3c5019af3902455b75d41046e8dcc006f26c59`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `3965ab805187928054af321c959fe09587eaaf2e648a74f2c217614bf33e3b76`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 606
- **Unique Definition Count**: 606
- **Verified Against Semantic Root**: `3f6cfecffa0eb0d3…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "3f6cfecffa0eb0d38e9ddcc8cc3c5019af3902455b75d41046e8dcc006f26c59"
scheme_A = "sema-semantic-set-v1"

# Agent B independently reads its local versioned roots
local = json.loads(sema_root())
semantic_root_B = local["semantic_root"]
scheme_B = local["semantic_root_scheme"]

if scheme_A == scheme_B and semantic_root_A == semantic_root_B:
    print("✅ PROCEED - Definition sets match")
else:
    print("🚫 HALT - Vocabulary mismatch")
```

## Vocabulary Statistics

Breakdown of patterns by Civilization Layer and Functional Category.

### Physics (22)

| Category | Count |
| :--- | :---: |
| Primitives | 15 |
| Dynamics | 6 |
| Time | 1 |

### Mind (261)

| Category | Count |
| :--- | :---: |
| Strategy | 104 |
| Reasoning | 98 |
| Inference | 28 |
| Memory | 18 |
| Dynamics | 13 |

### Society (156)

| Category | Count |
| :--- | :---: |
| Protocols | 91 |
| Governance | 24 |
| Dynamics | 20 |
| Coordination | 12 |
| Economics | 9 |

### Infrastructure (167)

| Category | Count |
| :--- | :---: |
| Data Structures | 101 |
| Primitives | 53 |
| Verification | 10 |
| Dynamics | 3 |
