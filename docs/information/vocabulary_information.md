# Vocabulary Information

## System Status

- **Merkle Root**: `9b882acfa657dcbc1082aad30c784a07bf0bcd0cc1a0feaf7ddc04dc87620e3b`
- **Pattern Count**: 453
- **Last Verified**: 2026-04-08

## Usage

### Handshake Protocol

Agents use the Merkle root for fail-closed semantic verification:

```python
# Agent A shares vocabulary root
R_context_A = "9b882acfa657dcbc1082aad30c784a07bf0bcd0cc1a0feaf7ddc04dc87620e3b"

# Agent B computes their vocabulary root
R_context_B = compute_vocabulary_merkle_root()

if R_context_A == R_context_B:
    print("✅ PROCEED - Shared semantics verified")
else:
    print("🚫 HALT - Vocabulary mismatch")
```

## Vocabulary Statistics

Breakdown of patterns by Civilization Layer and Functional Category.

### Physics (27)

| Category | Count |
| :--- | :---: |
| Primitives | 20 |
| Time | 7 |

### Mind (146)

| Category | Count |
| :--- | :---: |
| Strategy | 72 |
| Reasoning | 45 |
| Inference | 18 |
| Memory | 11 |

### Society (166)

| Category | Count |
| :--- | :---: |
| Protocols | 122 |
| Economics | 23 |
| Governance | 20 |
| Coordination | 1 |

### Infrastructure (114)

| Category | Count |
| :--- | :---: |
| Data Structures | 80 |
| Primitives | 24 |
| Verification | 10 |

