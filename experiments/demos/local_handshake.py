"""Local handshake demo with cooperative and strict trust modes.

No external APIs are required.
Run from the repository root: ``python experiments/demos/local_handshake.py``.
"""

import os
import sys

# Ensure src is importable when running from a checkout without installation.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from sema.core.registry import RegistryManager
from sema.core.workspace import GraphWorkspace


def main():
    workspace = GraphWorkspace(registry_manager=RegistryManager())

    print("Sema Local Handshake Demo")
    print("=" * 60)

    print("\nRound 0: Look up StateLock's canonical identity")
    print("-" * 60)
    lookup = workspace.handshake("StateLock")
    canonical_stub = lookup["canonical_stub"]
    full_sema_id = lookup["full_sema_id"]
    canonical_full = full_sema_id.split("#mh:SHA-256:", 1)[1]
    print(f"  Stub:     {canonical_stub}")
    print(f"  Full ID:  {full_sema_id}")

    print("\nRound 1: Cooperative prefix check")
    print("-" * 60)
    cooperative = workspace.handshake("StateLock", your_hash=canonical_stub)
    print(f"  Verdict:   {cooperative['verdict']}")
    print(f"  Assurance: {cooperative['assurance']}")
    assert cooperative["verdict"] == "PROCEED"
    assert cooperative["assurance"] == "prefix"

    print("\nRound 2: Strict mode rejects prefix-only evidence")
    print("-" * 60)
    strict_prefix = workspace.handshake("StateLock", your_hash=canonical_stub, strict=True)
    print(f"  Verdict: {strict_prefix['verdict']}")
    assert strict_prefix["verdict"] == "REQUIRE_FULL_HASH"

    print("\nRound 3: Strict full-hash verification")
    print("-" * 60)
    strict_full = workspace.handshake("StateLock", your_hash=canonical_full, strict=True)
    print(f"  Verdict:   {strict_full['verdict']}")
    print(f"  Assurance: {strict_full['assurance']}")
    assert strict_full["verdict"] == "PROCEED"
    assert strict_full["assurance"] == "full_hash"

    print("\nRound 4: Mismatched full hash")
    print("-" * 60)
    mismatch = workspace.handshake("StateLock", your_hash="0" * 64, strict=True)
    print(f"  Verdict: {mismatch['verdict']}")
    assert mismatch["verdict"] == "HALT"

    print("\nRound 5: Unknown pattern")
    print("-" * 60)
    unknown = workspace.handshake("NonExistentPattern", your_hash="0" * 64, strict=True)
    print(f"  Verdict: {unknown['verdict']}")
    assert unknown["verdict"] == "HALT"

    print("\n" + "=" * 60)
    print("All rounds passed.")


if __name__ == "__main__":
    main()
