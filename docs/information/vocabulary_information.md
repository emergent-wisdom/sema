# Vocabulary Information

## System Status

- **Semantic-set Root**: `22655282cfb9d7dd78a8307ac4fcc21aedd2b3498311e32b097aa38a0ea7f906`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `4aaa820f4443be9e43ed3c1a6e496e901c662d3b848882f706b28563b649f219`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 616
- **Unique Definition Count**: 616
- **Verified Against Semantic Root**: `22655282cfb9d7dd…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "22655282cfb9d7dd78a8307ac4fcc21aedd2b3498311e32b097aa38a0ea7f906"
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

### Mind (265)

| Category | Count |
| :--- | :---: |
| Strategy | 105 |
| Reasoning | 101 |
| Inference | 27 |
| Memory | 18 |
| Dynamics | 14 |

### Society (156)

| Category | Count |
| :--- | :---: |
| Protocols | 91 |
| Governance | 24 |
| Dynamics | 20 |
| Coordination | 12 |
| Economics | 9 |

### Infrastructure (173)

| Category | Count |
| :--- | :---: |
| Data Structures | 101 |
| Primitives | 54 |
| Verification | 14 |
| Dynamics | 3 |
| Safety | 1 |
