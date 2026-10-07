# Vocabulary Information

## System Status

- **Semantic-set Root**: `a7db6b927834c9370271a608d8872b7aff457ebe93c6972806d6457b3df38971`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `7eec1a26a7b1454e48507a26c382aa804ac93e8a08d290d452b0448c49e74aa8`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 590
- **Unique Definition Count**: 590
- **Verified Against Semantic Root**: `a7db6b927834c937…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "a7db6b927834c9370271a608d8872b7aff457ebe93c6972806d6457b3df38971"
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

### Physics (20)

| Category | Count |
| :--- | :---: |
| Primitives | 18 |
| Time | 2 |

### Mind (261)

| Category | Count |
| :--- | :---: |
| Strategy | 113 |
| Reasoning | 101 |
| Inference | 28 |
| Memory | 19 |

### Society (142)

| Category | Count |
| :--- | :---: |
| Protocols | 97 |
| Governance | 24 |
| Coordination | 12 |
| Economics | 9 |

### Infrastructure (167)

| Category | Count |
| :--- | :---: |
| Data Structures | 101 |
| Primitives | 56 |
| Verification | 10 |
