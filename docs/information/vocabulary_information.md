# Vocabulary Information

## System Status

- **Merkle Root**: `901130d88dab244cc0d4afc149c5e6eeb9c9565e117c468a8e5326287be8fefa`
- **Pattern Count**: 453
- **Verified Against Root**: `901130d88dab244c…`

## Usage

### Handshake Protocol

Agents use the Merkle root for fail-closed semantic verification:

```python
# Agent A shares vocabulary root
R_context_A = "901130d88dab244cc0d4afc149c5e6eeb9c9565e117c468a8e5326287be8fefa"

# Agent B computes their vocabulary root
R_context_B = compute_vocabulary_merkle_root()

if R_context_A == R_context_B:
    print("✅ PROCEED - Shared semantics verified")
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

