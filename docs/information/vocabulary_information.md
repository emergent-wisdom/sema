# Vocabulary Information

## System Status

- **Semantic-set Root**: `bc0698d0afac84a656a63634d2d1858aaf3b54243b5d7443cfa7a2528cadc768`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `cacadc5bf58f54d6d3eb774032c969523b7e371e4373553c84d4e9fe59fc4bf3`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 456
- **Unique Definition Count**: 456
- **Verified Against Semantic Root**: `bc0698d0afac84a6…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "bc0698d0afac84a656a63634d2d1858aaf3b54243b5d7443cfa7a2528cadc768"
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

### Physics (16)

| Category | Count |
| :--- | :---: |
| Primitives | 15 |
| Time | 1 |

### Mind (180)

| Category | Count |
| :--- | :---: |
| Strategy | 81 |
| Reasoning | 62 |
| Inference | 22 |
| Memory | 15 |

### Society (103)

| Category | Count |
| :--- | :---: |
| Protocols | 74 |
| Coordination | 13 |
| Economics | 9 |
| Governance | 7 |

### Infrastructure (157)

| Category | Count |
| :--- | :---: |
| Data Structures | 96 |
| Primitives | 52 |
| Verification | 9 |
