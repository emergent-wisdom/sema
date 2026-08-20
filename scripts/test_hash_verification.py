#!/usr/bin/env python3
"""
Test to verify exactly what gets hashed in Sema patterns.
Manually hashes a pattern and compares with the stored sema_id.
"""

import hashlib
import json
import unicodedata
from typing import Any

# Independent copy of the canonicalization-v2 logic from
# src/sema/core/hashing.py. Kept as a standalone reimplementation on
# purpose: this script exists so a third party can verify hashes without
# importing semahash. Must stay in sync with the library (v2: type-tagged
# domain separation, dict entries sorted by normalized key).
HASH_ALGO = "SHA-256"

_TAG_STR = b"s:"
_TAG_PRIMITIVE = b"p:"
_TAG_LIST = b"l:"
_TAG_DICT = b"d:"

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

def merkle_hash(obj: Any) -> tuple[str, Any]:
    """
    Recursively hash an object, returning (hash, canonical_obj).
    Canonicalization v2 (type-tagged; see src/sema/core/hashing.py).
    """
    if isinstance(obj, str):
        norm = normalize_string(obj)
        return _sha256(_TAG_STR + norm.encode('utf-8')), norm

    elif isinstance(obj, int | float | bool | type(None)):
        canon = canonical_json(obj)
        return _sha256(_TAG_PRIMITIVE + canon), obj

    elif isinstance(obj, list):
        hashed_items = [merkle_hash(item) for item in obj]
        concatenated = _TAG_LIST + "".join(h for h, _ in hashed_items).encode('utf-8')
        return _sha256(concatenated), [val for _, val in hashed_items]

    elif isinstance(obj, dict):
        entries = []
        canon_dict = {}

        for k, v in obj.items():
            k_hash, k_canon = merkle_hash(str(k))
            if k_canon in canon_dict:
                raise ValueError(f"Dict keys collide after normalization: {k_canon!r}")
            v_hash, v_canon = merkle_hash(v)
            entries.append((k_canon, k_hash, v_hash))
            canon_dict[k_canon] = v_canon

        entries.sort(key=lambda entry: entry[0])
        concatenated = _TAG_DICT + b"".join(
            k_hash.encode('utf-8') + v_hash.encode('utf-8') for _, k_hash, v_hash in entries
        )
        canon_dict = {k_canon: canon_dict[k_canon] for k_canon, _, _ in entries}

        return _sha256(concatenated), canon_dict

    else:
        raise ValueError(f"Unsupported type for hashing: {type(obj)}")


def extract_handle_from_ref(ref: str) -> str:
    if not ref:
        return ref
    if ref.startswith('sema:'):
        ref = ref[5:]
    return ref.split('#')[0]


def canonicalize_dependency_keys(deps: Any) -> Any:
    """Part of the hash spec: dependency aliases are authorial, so the hash
    input keys entries by lowercased target handle. Multiple aliases to the
    same handle keep a sorted list of refs."""
    if not isinstance(deps, dict):
        return deps
    normalized = {}
    for dep_type, items in deps.items():
        if isinstance(items, dict):
            grouped = {}
            passthrough = {}
            for key, val in items.items():
                if isinstance(val, str):
                    grouped.setdefault(extract_handle_from_ref(val).lower(), []).append(val)
                else:
                    passthrough[key] = val
            normalized[dep_type] = {
                k: (refs[0] if len(refs) == 1 else sorted(refs)) for k, refs in grouped.items()
            }
            normalized[dep_type].update(passthrough)
        else:
            normalized[dep_type] = items
    return normalized


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
        "parameters", "failure_modes", "extends"
    ]

    if "extends" in pattern and "derived_from" in pattern:
        print("ERROR: Pattern contains both extends and legacy derived_from")
        return False

    # Extract only semantic content
    content = {k: pattern[k] for k in semantic_fields if k in pattern}
    # Preserve the pre-0.4 key verbatim so historical card identities remain
    # independently verifiable after the field was renamed to `extends`.
    if "derived_from" in pattern:
        content["derived_from"] = pattern["derived_from"]

    # Dependency aliases are canonicalized before hashing (see hash spec).
    # The JSON stores resolved dep refs, so no registry lookup is needed —
    # this script stays independently runnable from the files alone.
    if 'dependencies' in content:
        content = dict(content)
        content['dependencies'] = canonicalize_dependency_keys(content['dependencies'])

    print(f"\n{'='*60}")
    print(f"Pattern: {handle}")
    print(f"{'='*60}")
    print(f"\nStored sema_id: {stored_sema_id}")
    print(f"\nSemantic fields present: {list(content.keys())}")
    print("\nCanonical content to hash:")
    print(json.dumps(content, indent=2, ensure_ascii=False))

    # Compute hash
    computed_hash, canonical_content = merkle_hash(content)

    print("\n--- Hash Comparison ---")
    print(f"Stored hash:   {stored_hash}")
    print(f"Computed hash: {computed_hash}")

    if stored_hash == computed_hash:
        print(f"\n✅ MATCH! Hash verified for {handle}")
        return True
    else:
        print(f"\n❌ MISMATCH! Hashes don't match for {handle}")
        print("\nCanonical form after normalization:")
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
