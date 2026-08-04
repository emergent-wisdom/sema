# Vocabulary Information

## System Status

- **Semantic-set Root**: `502d7f981a29a4a134e3080cdc4f361049a30f30ece026224a668bda80a83661`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `146db4c0b6172432a0694baa74263a2e33edfce2c5ba7756c33622f7bc69e324`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 457
- **Unique Definition Count**: 457
- **Verified Against Semantic Root**: `502d7f981a29a4a1…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "502d7f981a29a4a134e3080cdc4f361049a30f30ece026224a668bda80a83661"
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
