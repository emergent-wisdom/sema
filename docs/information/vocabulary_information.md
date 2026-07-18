# Vocabulary Information

## System Status

- **Merkle Root**: `c929ae6ef5d56f196c84cd0e5be193438b26bdc4f42b13eca35fdfe0801e395d`
- **Pattern Count**: 452
- **Verified Against Root**: `46e651aeeb832fdc…`

## Usage

### Handshake Protocol

Agents use the Merkle root for fail-closed semantic verification:

```python
# Agent A shares vocabulary root
R_context_A = "c929ae6ef5d56f196c84cd0e5be193438b26bdc4f42b13eca35fdfe0801e395d"

# Agent B computes their vocabulary root
R_context_B = compute_vocabulary_merkle_root()

if R_context_A == R_context_B:
    print("✅ PROCEED - Shared semantics verified")
else:
    print("🚫 HALT - Vocabulary mismatch")
```

## Vocabulary Statistics

Breakdown of patterns by Civilization Layer and Functional Category.

### Unclassified (452)

| Category | Count |
| :--- | :---: |
| Uncategorized | 452 |

