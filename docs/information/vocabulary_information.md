# Vocabulary Information

## System Status

- **Semantic-set Root**: `4101c57961420ba1caf092caeb8090ad87200c309a4eaa9901aca68bf21303cb`
- **Semantic-set Scheme**: `sema-semantic-set-v1`
- **Catalog Root**: `af272c2f1821b5e5773c6d936769de2929d5266941fa8cdb5a0ca31c63cca3f2`
- **Catalog Scheme**: `sema-catalog-v1`
- **Pattern Count**: 606
- **Unique Definition Count**: 606
- **Verified Against Semantic Root**: `4101c57961420ba1…`

## Usage

### Handshake Protocol

Agents use the semantic-set root to compare canonical-v2 definition sets and
the catalog root when exact handle-to-definition bindings must also agree.
Because canonicalization v2 hashes target handles in structured references,
a target rename can also change dependent definition digests:

```python
import json

# Agent A shares semantic-set root + scheme
semantic_root_A = "4101c57961420ba1caf092caeb8090ad87200c309a4eaa9901aca68bf21303cb"
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
| Primitives | 20 |
| Time | 2 |

### Mind (261)

| Category | Count |
| :--- | :---: |
| Strategy | 113 |
| Reasoning | 101 |
| Inference | 28 |
| Memory | 19 |

### Society (156)

| Category | Count |
| :--- | :---: |
| Protocols | 100 |
| Governance | 27 |
| Economics | 15 |
| Coordination | 14 |

### Infrastructure (167)

| Category | Count |
| :--- | :---: |
| Data Structures | 101 |
| Primitives | 56 |
| Verification | 10 |
