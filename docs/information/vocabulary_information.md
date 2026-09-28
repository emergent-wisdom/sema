# Vocabulary Information

## System Status

- **Semantic-set Root**: `c46b779f2c062f150413aa38768836162e5ee0d1f5e4b595f92139166e4d7c7e`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `f1f1ceaf61b715f35343b288e95dabbe45b8195e1279a4cd25adbabd371d78d4`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 457
- **Unique Definition Count**: 457
- **Verified Against Semantic Root**: `c46b779f2c062f15…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "c46b779f2c062f150413aa38768836162e5ee0d1f5e4b595f92139166e4d7c7e"
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

### Mind (181)

| Category | Count |
| :--- | :---: |
| Strategy | 81 |
| Reasoning | 63 |
| Inference | 22 |
| Memory | 15 |

### Society (102)

| Category | Count |
| :--- | :---: |
| Protocols | 74 |
| Coordination | 12 |
| Economics | 9 |
| Governance | 7 |

### Infrastructure (158)

| Category | Count |
| :--- | :---: |
| Data Structures | 96 |
| Primitives | 53 |
| Verification | 9 |
