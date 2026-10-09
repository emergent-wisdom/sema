# Vocabulary Information

## System Status

- **Semantic-set Root**: `3a10ccf481dbd54d33f81eda13858a8a3e8df2b2e5e92de5348d1fa464f416b4`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `adaca5ba4d6bbb789d941fee288db4e593cfee1d4a3c33da2dc6241a9ae883c0`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 616
- **Unique Definition Count**: 616
- **Verified Against Semantic Root**: `3a10ccf481dbd54d…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "3a10ccf481dbd54d33f81eda13858a8a3e8df2b2e5e92de5348d1fa464f416b4"
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
