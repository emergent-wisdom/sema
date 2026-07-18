#!/usr/bin/env python3
"""Verify that every pattern's stored sema_id matches the hash computed from its content.

This is the most critical audit: the paper's core claim is that
"word = Hash(canonical(definition))". If stored hashes don't match
recomputed hashes, the fail-closed handshake protocol breaks.

Exit code:
  0 — all hashes valid
  1 — at least one mismatch
"""

import json
import os
import sys
from pathlib import Path

from sema.core.hashing import generate_sema_hash

VOCAB_DIR = os.environ.get("SEMA_VOCAB_DIR", "data/vocabulary")


def extract_hash(sema_id: str) -> str | None:
    if not sema_id or "#mh:SHA-256:" not in sema_id:
        return None
    return sema_id.split("#mh:SHA-256:")[1]


def main():
    vocab = Path(VOCAB_DIR)
    if not vocab.is_dir():
        print(f"ERROR: vocabulary dir not found: {vocab}")
        sys.exit(1)

    patterns = {}
    for f in sorted(vocab.glob("*.json")):
        d = json.loads(f.read_text())
        h = d.get("handle")
        if h:
            patterns[h] = d

    print(f"Checking hash validity for {len(patterns)} patterns...\n")

    stored_hashes = {}
    for handle, p in patterns.items():
        h = extract_hash(p.get("sema_id", ""))
        if h:
            stored_hashes[handle] = h

    def hash_lookup(handle: str) -> str | None:
        return stored_hashes.get(handle)

    mismatches = []
    missing = []

    for handle, p in patterns.items():
        stored = extract_hash(p.get("sema_id", ""))
        if not stored:
            missing.append(handle)
            continue

        result = generate_sema_hash(p, hash_lookup)
        computed = result["hash"]

        if stored != computed:
            mismatches.append((handle, stored[:12], computed[:12]))

    if missing:
        print(f"Missing sema_id: {len(missing)}")
        for h in missing:
            print(f"  {h}")
        print()

    if mismatches:
        print(f"HASH MISMATCH: {len(mismatches)} patterns have stale hashes\n")
        for handle, stored, computed in mismatches:
            print(f"  {handle}: stored={stored}… computed={computed}…")
        print("\nRun 'python scripts/rebuild_vocabulary.py --replace' to fix.")
        sys.exit(1)
    else:
        print(f"All {len(patterns)} hashes valid.")
        sys.exit(0)


if __name__ == "__main__":
    main()
