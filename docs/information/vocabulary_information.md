# Vocabulary Information

## System Status

- **Merkle Root**: `eb8d07b90d27146b3ac58dc08c5f90ab55b574de0f74468d9346c8dce52681cc`
- **Pattern Count**: 450
- **Last Verified**: 2025-12-29

## Usage

### Handshake Protocol

Agents use the Merkle root for fail-closed semantic verification:

```python
# Agent A shares vocabulary root
R_context_A = "eb8d07b90d27146b3ac58dc08c5f90ab55b574de0f74468d9346c8dce52681cc"

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

### Mind (147)

| Category | Count |
| :--- | :---: |
| Strategy | 72 |
| Reasoning | 45 |
| Inference | 18 |
| Memory | 12 |

### Society (164)

| Category | Count |
| :--- | :---: |
| Protocols | 120 |
| Economics | 23 |
| Governance | 20 |
| Coordination | 1 |

### Infrastructure (112)

| Category | Count |
| :--- | :---: |
| Data Structures | 80 |
| Primitives | 23 |
| Verification | 9 |

