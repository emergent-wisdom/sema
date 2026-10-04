# Vocabulary Information

## System Status

- **Semantic-set Root**: `ac323cb0f3a2f17928ca079e20e25e426ca7cf2144031252ebd32d1009aef9f8`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `ee2e46f7684046ca9d4cae7fa05e348b0fc271af96994ea7f2f70c950932346c`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 457
- **Unique Definition Count**: 457
- **Verified Against Semantic Root**: `ac323cb0f3a2f179…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "ac323cb0f3a2f17928ca079e20e25e426ca7cf2144031252ebd32d1009aef9f8"
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
