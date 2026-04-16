# Vocabulary Information

## System Status

- **Merkle Root**: `d9f373d87bcb2620bd410a3ad747f168c0b1736fca0568a4844ed9d4175fb422`
- **Pattern Count**: 427
- **Last Verified**: 2026-04-16

## Usage

### Handshake Protocol

Agents use the Merkle root for fail-closed semantic verification:

```python
# Agent A shares vocabulary root
R_context_A = "d9f373d87bcb2620bd410a3ad747f168c0b1736fca0568a4844ed9d4175fb422"

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

