"""
Local Handshake Demo — no external APIs required.

Simulates two agents verifying semantic alignment via Sema hashes.
Run: python experiments/demos/local_handshake.py
"""

import json
import sys
import os

# Ensure src is importable when running from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from sema.core.actions import sema_handshake


def main():
    print("Sema Local Handshake Demo")
    print("=" * 50)

    # --- Round 0: Look up the canonical hash ---
    print("\nRound 0: Agent A looks up StateLock's canonical hash")
    print("-" * 50)

    lookup = json.loads(sema_handshake("StateLock"))
    canonical_stub = lookup.get("canonical_stub")
    print(f"  Handle:         StateLock")
    print(f"  Canonical stub: {canonical_stub}")
    print(f"  -> Agent A now knows the correct ref: StateLock#{canonical_stub}")

    # --- Round 1: Matching hashes (happy path) ---
    print(f"\nRound 1: Agent A proposes StateLock#{canonical_stub}")
    print("-" * 50)

    result = json.loads(sema_handshake(f"StateLock#{canonical_stub}"))
    print(f"  Ref:     {result.get('ref')}")
    print(f"  Verdict: {result.get('verdict')}")

    if result["verdict"] == "PROCEED":
        print("  -> Agents are semantically aligned. Coordination can proceed.")
    else:
        print(f"  -> Unexpected verdict: {result.get('verdict')}")

    # --- Round 2: Mismatched hash (attack/drift) ---
    print("\nRound 2: Agent A proposes StateLock with wrong hash")
    print("-" * 50)

    result = json.loads(sema_handshake("StateLock#deadbeef"))
    print(f"  Ref:      {result.get('ref')}")
    print(f"  Verdict:  {result.get('verdict')}")
    print(f"  Expected: {result.get('expected_hash', 'N/A')}")
    print(f"  Got:      {result.get('your_hash', 'N/A')}")

    if result["verdict"] == "HALT":
        print("  -> Drift detected. Coordination halted. Fail-closed.")
    else:
        print("  -> ERROR: Expected HALT on mismatched hash.")

    # --- Round 3: Session-scoped handshake (multiple patterns) ---
    print("\nRound 3: Session handshake over multiple patterns")
    print("-" * 50)

    # Step 1: Agent A computes context hash for a set of patterns
    patterns = ["StateLock", "Abduction", "ChainOfThought"]
    result = json.loads(sema_handshake(patterns))
    context_hash = result.get("context_hash")
    print(f"  Patterns:     {patterns}")
    print(f"  Context hash: {context_hash}")

    # Step 2: Agent B verifies with the same context hash
    print(f"\n  Agent B verifies with context hash: {context_hash}")
    result2 = json.loads(sema_handshake(patterns, your_hash=context_hash))
    print(f"  Verdict:      {result2.get('verdict')}")

    if result2["verdict"] == "PROCEED":
        print(f"  -> All three patterns verified. Session is semantically aligned.")
        print(f"     Any agent with context hash {context_hash} shares the exact same contracts.")

    # --- Round 4: Unknown pattern ---
    print("\nRound 4: Agent A proposes a pattern that doesn't exist")
    print("-" * 50)

    result = json.loads(sema_handshake("NonExistentPattern#abcd"))
    print(f"  Ref:     {result.get('ref')}")
    print(f"  Verdict: {result.get('verdict')}")

    if result["verdict"] == "HALT":
        print("  -> Unknown pattern. Coordination halted.")

    print("\n" + "=" * 50)
    print("All rounds complete. The protocol is working.")


if __name__ == "__main__":
    main()
