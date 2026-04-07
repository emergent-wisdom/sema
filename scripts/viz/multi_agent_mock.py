import hashlib
import json
import time

# Simulation Constants
AGENT_A = "Agent_Alpha (Standard)"
AGENT_B = "Agent_Beta (Drifting)"

# --- The Sema Protocols (Simulated Registry) ---

# The "True" Definition (Standard)
DEF_STATELOCK_STD = {
    "handle": "StateLock",
    "gloss": "Atomic coordination via temporary state fusion",
    "parameters": {"timeout": "Duration"},
    "invariants": ["Sign(A) + Sign(B) required"]
}

# The "Drifted" Definition (Beta has a buggy version)
DEF_STATELOCK_DRIFT = {
    "handle": "StateLock",
    "gloss": "Atomic coordination via temporary state fusion",
    "parameters": {"timeout": "Integer"}, # <--- TYPE MISMATCH
    "invariants": ["Sign(A) + Sign(B) required"]
}

def get_hash(definition):
    """Canonicalize and hash."""
    canonical = json.dumps(definition, sort_keys=True).encode('utf-8')
    return hashlib.sha256(canonical).hexdigest()[:8]

def print_trace(agent, pattern, mechanism, thought):
    """Render a Cognitive Trace."""
    print(f"\n🧠 [{agent}] <trace>")
    print(f"   └── 🪜 {pattern}: {mechanism}")
    print(f"       └── 💭 \"{thought}\"")

def print_msg(sender, receiver, payload):
    """Render a Network Message."""
    print(f"\n📨 {sender} -> {receiver}:")
    print(json.dumps(payload, indent=2))

def run_experiment(simulate_drift=False):
    print(f"\n{'='*60}")
    print(f"🧪 EXPERIMENT: {'Semantic Drift / Babel Test' if simulate_drift else 'Baseline / Perfect Alignment'}")
    print(f"{'='*60}")

    # 1. Setup
    hash_a = get_hash(DEF_STATELOCK_STD)
    hash_b = get_hash(DEF_STATELOCK_DRIFT if simulate_drift else DEF_STATELOCK_STD)

    print(f"📋 {AGENT_A} loaded StateLock#{hash_a}")
    print(f"📋 {AGENT_B} loaded StateLock#{hash_b}")

    # 2. Agent A Initiates
    print_trace(AGENT_A, "StateLock", "Initiating atomic transaction", 
                "I need to write to the shared log. Initiating Lock protocol.")
    
    msg_1 = {
        "protocol": "Sema/1.0",
        "type": "INTENT",
        "verb": f"sema:StateLock#{hash_a}",
        "params": {"timeout": "5s"}
    }
    print_msg(AGENT_A, AGENT_B, msg_1)

    # 3. Agent B Receives and Verifies
    print_trace(AGENT_B, "SpectralTune", "Verifying ontology alignment", 
                f"Received request for {msg_1['verb']}. Checking local registry...")

    incoming_hash = msg_1['verb'].split('#')[1]
    
    if incoming_hash == hash_b:
        # Success Case
        print_trace(AGENT_B, "Resonate", "Alignment confirmed", 
                    "Hashes match. Our definitions are identical. Proceeding.")
        
        msg_2 = {
            "type": "ACK",
            "status": "PROCEED",
            "signature": "sig_beta_99x"
        }
        print_msg(AGENT_B, AGENT_A, msg_2)
        print("\n✅ RESULT: SUCCESS. Coordination established.")
        
    else:
        # Failure Case (Fail-Closed)
        print_trace(AGENT_B, "SomaticMarker", "Anomaly detected", 
                    f"HASH MISMATCH! Remote: {incoming_hash}, Local: {hash_b}. Stopping.")
        
        msg_2 = {
            "type": "NACK",
            "status": "HALT",
            "error": "SemanticDivergence",
            "details": f"I know StateLock#{hash_b}, you asked for #{incoming_hash}"
        }
        print_msg(AGENT_B, AGENT_A, msg_2)
        print("\n🛑 RESULT: FAIL-CLOSED. Misalignment caught before execution.")

if __name__ == "__main__":
    # Run Control
    run_experiment(simulate_drift=False)
    time.sleep(1)
    # Run Experiment
    run_experiment(simulate_drift=True)
