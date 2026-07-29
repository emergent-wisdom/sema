# Vocabulary Information

## System Status

- **Semantic-set Root**: `62d9253829798a6ee8f51393c9154560a0a4c06d370d997a39968fda85e48d9c`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `c7ce079ec169999fe7f77dff0122e20bde7d3f22151fc0108e5d5197ea92e5af`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 453
- **Unique Definition Count**: 453
- **Verified Against Semantic Root**: `62d9253829798a6e…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "62d9253829798a6ee8f51393c9154560a0a4c06d370d997a39968fda85e48d9c"
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

### Mind (178)

| Category | Count |
| :--- | :---: |
| Strategy | 81 |
| Reasoning | 60 |
| Inference | 22 |
| Memory | 15 |

### Society (106)

| Category | Count |
| :--- | :---: |
| Protocols | 76 |
| Coordination | 12 |
| Economics | 10 |
| Governance | 8 |

### Infrastructure (152)

| Category | Count |
| :--- | :---: |
| Data Structures | 93 |
| Primitives | 50 |
| Verification | 9 |

