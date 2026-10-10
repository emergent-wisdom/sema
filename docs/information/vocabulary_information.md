# Vocabulary Information

## System Status

- **Semantic-set Root**: `8f9c8b8446e185bf94650ce0f3f351d8f66bde6f084d93ef6d2c0300bd362190`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `40c2100ab60726f8ce39a993645efc80e2c9c3cdd6bdf89e0abc35e146418913`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 617
- **Unique Definition Count**: 617
- **Verified Against Semantic Root**: `8f9c8b8446e185bf…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "8f9c8b8446e185bf94650ce0f3f351d8f66bde6f084d93ef6d2c0300bd362190"
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

### Mind (266)

| Category | Count |
| :--- | :---: |
| Strategy | 105 |
| Reasoning | 102 |
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
