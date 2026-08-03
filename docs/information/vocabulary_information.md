# Vocabulary Information

## System Status

- **Semantic-set Root**: `2aaf01f6f1d084b77a8139f23f381ded6cfa0b366046921523e3dd7516bd627e`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `1d8f583987a42b3a4a536d36d0836b42ce343ecdbd8f05f303d7564a33405199`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 456
- **Unique Definition Count**: 456
- **Verified Against Semantic Root**: `2aaf01f6f1d084b7…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "2aaf01f6f1d084b77a8139f23f381ded6cfa0b366046921523e3dd7516bd627e"
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

### Physics (17)

| Category | Count |
| :--- | :---: |
| Primitives | 16 |
| Time | 1 |

### Mind (179)

| Category | Count |
| :--- | :---: |
| Strategy | 81 |
| Reasoning | 61 |
| Inference | 22 |
| Memory | 15 |

### Society (103)

| Category | Count |
| :--- | :---: |
| Protocols | 75 |
| Coordination | 12 |
| Economics | 9 |
| Governance | 7 |

### Infrastructure (157)

| Category | Count |
| :--- | :---: |
| Data Structures | 96 |
| Primitives | 52 |
| Verification | 9 |
