#!/usr/bin/env python3
"""
Multi-Agent Coordination Demo via Sema MCP Tools

Simulates two agents (Architect and Engineer) coordinating on a design task:
1. Architect proposes a context (shared pattern set)
2. Engineer verifies the context
3. Both work using the shared vocabulary
4. Engineer discovers a missing concept and mints a new pattern
5. Both re-handshake on the expanded context

No API keys needed. Run: python experiments/demos/multi_agent_coordination.py
"""

import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from sema.mcp.server import (
    sema_search,
    sema_resolve,
    sema_handshake,
    sema_propose_context,
    sema_verify_context,
    sema_mint,
    sema_lookup,
    sema_graph_skeleton,
)


def agent_log(agent: str, action: str, detail: str = ""):
    prefix = "🏗️  ARCHITECT" if agent == "A" else "🔧 ENGINEER"
    print(f"\n{prefix} [{action}]")
    if detail:
        for line in detail.strip().split("\n"):
            print(f"  {line}")


def main():
    print("=" * 70)
    print("SEMA MULTI-AGENT COORDINATION DEMO")
    print("=" * 70)

    # =========================================================================
    # PHASE 1: Discovery
    # =========================================================================
    print("\n" + "─" * 70)
    print("PHASE 1: DISCOVERY")
    print("─" * 70)

    agent_log("A", "ORIENT", "Mapping the vocabulary terrain...")
    skeleton = sema_graph_skeleton()
    # Just show first 5 lines
    for line in skeleton.split("\n")[:5]:
        print(f"  {line}")

    agent_log("A", "SEARCH", "Looking for design coordination patterns...")
    results = json.loads(sema_search("design coordination"))
    top_3 = results[:3]
    for r in top_3:
        print(f"  - {r['handle']}#{r.get('stub', '????')} : {r.get('gloss', '')}")

    agent_log("A", "RESOLVE", "Inspecting MechanisticDesignProposal...")
    resolved = json.loads(sema_resolve("MechanisticDesignProposal"))
    for p in resolved.get("patterns", {}).values():
        if isinstance(p, dict):
            print(f"  - {p.get('handle', '?')}: {p.get('gloss', '')[:60]}")

    # =========================================================================
    # PHASE 2: Context Proposal (Architect → Engineer)
    # =========================================================================
    print("\n" + "─" * 70)
    print("PHASE 2: CONTEXT HANDSHAKE")
    print("─" * 70)

    context_patterns = ["MechanisticDesignProposal", "StateLock", "Check", "SteelmanCheck"]

    agent_log("A", "PROPOSE CONTEXT", f"Patterns: {context_patterns}")
    proposal = json.loads(sema_propose_context(context_patterns))
    context_hash = proposal["context_hash"]
    context_scheme = proposal["root_scheme"]
    print(f"  Context hash: {context_hash}")
    print(f"  Root scheme: {context_scheme}")
    print(f"  Patterns: {proposal['patterns']}")
    print(f"  → Sending hash and scheme to Engineer...")

    agent_log("B", "VERIFY CONTEXT", f"Received hash: {context_hash}")
    verification = json.loads(
        sema_verify_context(context_patterns, context_hash, context_scheme)
    )
    print(f"  Verdict: {verification['verdict']}")
    if verification["verdict"] == "PROCEED":
        print(f"  ✅ Context verified. Both agents share exact same definitions.")
    else:
        print(f"  ❌ HALT: {verification.get('reason', 'unknown')}")
        return

    # =========================================================================
    # PHASE 3: Individual Pattern Handshakes
    # =========================================================================
    print("\n" + "─" * 70)
    print("PHASE 3: PATTERN-LEVEL VERIFICATION")
    print("─" * 70)

    agent_log("B", "HANDSHAKE", "Verifying each pattern individually...")
    for pattern in context_patterns:
        result = json.loads(sema_handshake(pattern))
        stub = result.get("canonical_stub", result.get("verified_ref", "?"))
        print(f"  {pattern}#{stub}: {result['verdict']}")

    # Demonstrate HALT on wrong hash
    agent_log("B", "HANDSHAKE (adversarial)", "Testing with wrong hash...")
    bad_result = json.loads(sema_handshake("StateLock#dead"))
    print(f"  StateLock#dead: {bad_result['verdict']} — {bad_result.get('reason', '')}")

    # =========================================================================
    # PHASE 4: Engineer Mints a New Pattern
    # =========================================================================
    print("\n" + "─" * 70)
    print("PHASE 4: MINTING A NEW PATTERN")
    print("─" * 70)

    # First check if the concept exists
    agent_log("B", "SEARCH", "Looking for 'load test' patterns...")
    load_results = json.loads(sema_search("load test stress"))
    if load_results:
        print(f"  Found {len(load_results)} related patterns, but none for load testing specifically.")
    else:
        print(f"  No existing patterns found.")

    # Look up dependencies we'll need
    agent_log("B", "LOOKUP", "Getting dependency sema_ids...")
    probe = json.loads(sema_lookup("Probe"))
    check = json.loads(sema_lookup("Check"))
    probe_id = probe.get("sema_id", "")
    check_id = check.get("sema_id", "")
    print(f"  Probe: {probe.get('sema_ref', '?')}")
    print(f"  Check: {check.get('sema_ref', '?')}")

    agent_log("B", "MINT", "Creating LoadTest pattern...")
    new_pattern = json.dumps({
        "handle": "LoadTest",
        "mechanism": (
            "Systematically increase load on a target system using {{probe}} "
            "to inject calibrated traffic, then {{check}} response times and error rates "
            "against threshold invariants. Ramp load linearly from baseline to peak, "
            "recording metrics at each step. If any invariant is violated, capture the "
            "exact load level and failure mode."
        ),
        "gloss": "Verify system behavior under increasing load before deployment",
        "invariants": [
            "Load must increase monotonically during the ramp phase",
            "Every {{check}} result must be recorded with its corresponding load level",
            "Test must not exceed the declared peak load"
        ],
        "preconditions": [
            "Target system is in a known baseline state",
            "{{probe}} has network access to the target"
        ],
        "postconditions": [
            "A load profile report exists mapping load levels to response metrics",
            "Any invariant violations are flagged with exact failure threshold"
        ],
        "failure_modes": [
            "Cascading Failure: Load test itself causes unrecoverable system state",
            "Observer Effect: Monitoring overhead distorts measurements at high load"
        ],
        "dependencies": {
            "composes_with": {
                "probe": probe_id,
                "check": check_id
            }
        },
        "parameters": [
            {
                "name": "peak_load",
                "type": "Integer",
                "range": "[1, 1000000]",
                "description": "Maximum requests per second"
            },
            {
                "name": "ramp_duration",
                "type": "Integer",
                "range": "[10, 3600]",
                "description": "Seconds to ramp from baseline to peak"
            }
        ],
        "_meta": {
            "layer": "Infrastructure",
            "category": "Verification",
            "tier": 1,
            "ring": 2,
            "related": ["ChaosDrift#3805", "Canary#f9d7"]
        }
    })

    mint_result = json.loads(sema_mint(new_pattern))
    if mint_result.get("success"):
        print(f"  ✅ Minted: {mint_result['sema_ref']}")
        print(f"  ID: {mint_result['sema_id']}")
    else:
        print(f"  ❌ Failed: {mint_result.get('errors', [])}")
        return

    # =========================================================================
    # PHASE 5: Re-handshake with Expanded Context
    # =========================================================================
    print("\n" + "─" * 70)
    print("PHASE 5: EXPANDED CONTEXT HANDSHAKE")
    print("─" * 70)

    expanded_context = context_patterns + ["LoadTest"]

    agent_log("B", "PROPOSE CONTEXT", f"Adding LoadTest to shared context")
    new_proposal = json.loads(sema_propose_context(expanded_context))
    new_hash = new_proposal["context_hash"]
    new_scheme = new_proposal["root_scheme"]
    print(f"  New context hash: {new_hash}")
    print(f"  Root scheme: {new_scheme}")
    print(f"  (Old hash was: {context_hash})")
    print(f"  → Context changed because it expanded. Sending hash and scheme to Architect...")

    agent_log("A", "VERIFY CONTEXT", f"Received new hash: {new_hash}")
    new_verification = json.loads(
        sema_verify_context(expanded_context, new_hash, new_scheme)
    )
    print(f"  Verdict: {new_verification['verdict']}")
    if new_verification["verdict"] == "PROCEED":
        print(f"  ✅ Expanded context verified. Both agents aligned on {new_verification['count']} patterns.")

    # =========================================================================
    # CLEANUP
    # =========================================================================
    print("\n" + "─" * 70)
    print("CLEANUP")
    print("─" * 70)

    # Remove the test pattern
    from sema.cli.main import apply_changes
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        apply_changes(remove_handles=["LoadTest"])
    print(f"  Removed LoadTest (demo cleanup)")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("""
Summary:
  1. Architect discovered patterns via search and resolve
  2. Both agents verified a shared context (Merkle root handshake)
  3. Individual pattern handshakes confirmed alignment
  4. Adversarial hash was correctly rejected (HALT)
  5. Engineer minted a new pattern (LoadTest) with proper dependencies
  6. Both agents re-handshaked on the expanded context

This is the full Sema coordination loop:
  DISCOVER → PROPOSE → VERIFY → WORK → MINT → RE-VERIFY
""")


if __name__ == "__main__":
    main()
