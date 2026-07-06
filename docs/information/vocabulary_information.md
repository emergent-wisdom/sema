# Vocabulary Information

## System Status

- **Merkle Root**: `46e651aeeb832fdc654d6e48ba2b9c9049f8585a5423371624426c1ab6d3f15b`
- **Pattern Count**: 452
- **Last Verified**: 2026-07-06

## Usage

### Handshake Protocol

Agents use the Merkle root for fail-closed semantic verification:

```python
# Agent A shares vocabulary root
R_context_A = "46e651aeeb832fdc654d6e48ba2b9c9049f8585a5423371624426c1ab6d3f15b"

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

