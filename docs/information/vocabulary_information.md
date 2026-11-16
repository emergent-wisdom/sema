# Vocabulary Information

## System Status

- **Semantic-set Root**: `a6a3d1ff0f982ee30430c5b42f3784c8ec901fd68482cfc1bc30899c1e5e48c5`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `bd1e476a176f94e0b6c2fad2eb058782e3f0798ba1aedec8822383b187bbd99b`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 617
- **Unique Definition Count**: 617
- **Verified Against Semantic Root**: `a6a3d1ff0f982ee3…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "a6a3d1ff0f982ee30430c5b42f3784c8ec901fd68482cfc1bc30899c1e5e48c5"
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
