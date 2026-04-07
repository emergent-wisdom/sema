#!/usr/bin/env python3
"""
Test to verify exactly what gets hashed in Sema patterns.
Manually hashes a pattern and compares with the stored sema_id.
"""

import json
import hashlib
import unicodedata
from typing import Any, Tuple

# Copy of hashing logic from src/sema/core/hashing.py
HASH_ALGO = "SHA-256"

def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def normalize_string(s: str) -> str:
    """NFC normalize and strip whitespace."""
    s = unicodedata.normalize('NFC', s.strip())
    return ' '.join(s.split())

def canonical_json(obj: Any) -> bytes:
    """Produce deterministic JSON bytes."""
    return json.dumps(
        obj, sort_keys=True, ensure_ascii=False, separators=(',', ':')
    ).encode('utf-8')

def merkle_hash(obj: Any) -> Tuple[str, Any]:
    """
    Recursively hash an object, returning (hash, canonical_obj).
    """
    if isinstance(obj, str):
        norm = normalize_string(obj)
        return _sha256(norm.encode('utf-8')), norm

    elif isinstance(obj, (int, float, bool, type(None))):
        canon = canonical_json(obj)
        return _sha256(canon), obj

    elif isinstance(obj, list):
        hashed_items = [merkle_hash(item) for item in obj]
        concatenated = "".join(h for h, _ in hashed_items).encode('utf-8')
        return _sha256(concatenated), [val for _, val in hashed_items]

    elif isinstance(obj, dict):
        sorted_items = sorted(obj.items(), key=lambda x: x[0])

        concatenated = b""
        canon_dict = {}

        for k, v in sorted_items:
            k_hash, k_canon = merkle_hash(str(k))
            v_hash, v_canon = merkle_hash(v)

            concatenated += k_hash.encode('utf-8') + v_hash.encode('utf-8')
            canon_dict[k_canon] = v_canon

        return _sha256(concatenated), canon_dict

    else:
        raise ValueError(f"Unsupported type for hashing: {type(obj)}")


def test_pattern_hash(pattern_path: str):
    """Test that we can reproduce the hash from a pattern file."""

    with open(pattern_path) as f:
        pattern = json.load(f)

    handle = pattern.get('handle', 'Unknown')
    stored_sema_id = pattern.get('sema_id', '')

    # Extract stored hash
    if 'SHA-256:' in stored_sema_id:
        stored_hash = stored_sema_id.split('SHA-256:')[1]
    else:
        print(f"ERROR: No valid sema_id found in {pattern_path}")
        return False

    # These are the semantic fields that get hashed
    semantic_fields = [
        "dependencies", "signature", "data_schema", "mechanism",
        "gloss", "invariants", "preconditions", "postconditions",
        "parameters", "failure_modes", "derived_from"
    ]

    # Extract only semantic content
    content = {k: pattern[k] for k in semantic_fields if k in pattern}

    print(f"\n{'='*60}")
    print(f"Pattern: {handle}")
    print(f"{'='*60}")
    print(f"\nStored sema_id: {stored_sema_id}")
    print(f"\nSemantic fields present: {list(content.keys())}")
    print(f"\nCanonical content to hash:")
    print(json.dumps(content, indent=2, ensure_ascii=False))

    # Compute hash
    computed_hash, canonical_content = merkle_hash(content)

    print(f"\n--- Hash Comparison ---")
    print(f"Stored hash:   {stored_hash}")
    print(f"Computed hash: {computed_hash}")

    if stored_hash == computed_hash:
        print(f"\n✅ MATCH! Hash verified for {handle}")
        return True
    else:
        print(f"\n❌ MISMATCH! Hashes don't match for {handle}")
        print(f"\nCanonical form after normalization:")
        print(json.dumps(canonical_content, indent=2, ensure_ascii=False))
        return False


def main():
    import os

    vocab_dir = 'data/vocabulary'

    # Test a few patterns
    test_patterns = [
        'StateLock.json',
        'FractalIntelligence.json',
        'SpectralTune.json',
        'SteelmanCheck.json',
    ]

    results = []
    for filename in test_patterns:
        path = os.path.join(vocab_dir, filename)
        if os.path.exists(path):
            result = test_pattern_hash(path)
            results.append((filename, result))
        else:
            print(f"WARNING: {path} not found")
            results.append((filename, None))

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for filename, result in results:
        status = "✅ PASS" if result else "❌ FAIL" if result is False else "⚠️ SKIP"
        print(f"  {filename}: {status}")


if __name__ == "__main__":
    main()
