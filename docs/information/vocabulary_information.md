# Vocabulary Information

## System Status

- **Merkle Root**: `72f1c59a00c58aba8d811fdf4ad22751b5ab4ef52013d9165545be7985c499ed`
- **Pattern Count**: 427
- **Last Verified**: 2026-04-16

## Usage

### Handshake Protocol

Agents use the Merkle root for fail-closed semantic verification:

```python
# Agent A shares vocabulary root
R_context_A = "72f1c59a00c58aba8d811fdf4ad22751b5ab4ef52013d9165545be7985c499ed"

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

### Mind (139)

| Category | Count |
| :--- | :---: |
| Strategy | 66 |
| Reasoning | 44 |
| Inference | 18 |
| Memory | 11 |

### Society (149)

| Category | Count |
| :--- | :---: |
| Protocols | 114 |
| Governance | 17 |
| Economics | 17 |
| Coordination | 1 |

### Infrastructure (112)

| Category | Count |
| :--- | :---: |
| Data Structures | 80 |
| Primitives | 23 |
| Verification | 9 |

