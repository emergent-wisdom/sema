#!/usr/bin/env python3
"""
Generate a Situational Review of the Sema vocabulary.
Infers usage context from Category and value from Tier/Gloss.
"""

import glob
import json
import os

VOCAB_DIR = "data/vocabulary"
OUTPUT_FILE = "vocabulary_situational_review.md"

# Map Categories to Situational Contexts
CATEGORY_CONTEXTS = {
    # Physics
    "Synchronization": "situations involving multiple agents contending for shared, rivalrous resources",
    "State Management": "situations requiring durability, history, or rollback of agent state",
    "Sharding & Distribution": "situations where a single agent is resource-constrained or the dataset is too large",
    "Primitives": "foundational operations required for higher-order logic",
    
    # Mind
    "Reasoning & Inference": "complex tasks where immediate intuition is insufficient and step-by-step logic is required",
    "Decision Making": "situations requiring a choice between multiple valid options with competing trade-offs",
    "Calibration": "situations where the agent must assess its own confidence or error rates before acting",
    "Perspective & Reframing": "situations where the initial problem formulation is stuck or unsolvable",
    "Decomposition": "situations where a task is too large to solve in a single context window",
    "Meta-Cognition": "situations where the agent must reason about its own thinking process",
    
    # Society
    "Trust & Verification": "interactions with untrusted, anonymous, or potentially adversarial peers",
    "Governance": "situations requiring binding group decisions or constitution updates",
    "Communication": "situations involving information exchange between distinct entities",
    "Economic Coordination": "situations involving resource allocation, pricing, or value exchange",
    "Emergence & Self-Organization": "situations where group behavior arises without central command",
    "Negotiation": "situations where agents have conflicting goals but seek a cooperative outcome",
    
    # Infrastructure
    "Safety & Alignment": "high-stakes environments where failure has significant negative externalities",
    "Flow Control": "situations needing to manage rate, concurrency, or signal propagation",
    "Resource Management": "situations where compute, bandwidth, or tokens are scarce constraints",
    "Resilience": "situations where partial system failure is expected and must be survived",
    "Data Structures": "situations requiring standardized formats for interoperability"
}

# Map Tiers to Value Propositions
TIER_VALUE = {
    1: "CRITICAL. Provides fail-closed safety or fundamental capability. Absence risks failure.",
    2: "HIGH. Optimizes efficiency or clarity. Provides robust handling of standard edge cases.",
    3: "EXPERIMENTAL. Potential for novel capabilities, but utility is unproven."
}

def load_patterns():
    patterns = []
    for filepath in glob.glob(os.path.join(VOCAB_DIR, "*.json")):
        with open(filepath) as f:
            patterns.append(json.load(f))
    # Sort by Category then Handle
    return sorted(patterns, key=lambda x: (x.get('sema_category', 'Unknown'), x['handle']))

def generate_review():
    patterns = load_patterns()
    
    with open(OUTPUT_FILE, 'w') as f:
        f.write("# Sema Situational Review\n\n")
        f.write("Analysis of utility and value for each pattern.\n\n")
        
        current_cat = None
        
        for p in patterns:
            # Metadata
            handle = p['handle']
            category = p.get('sema_category', 'Uncategorized')
            tier = p.get('tier', 2)
            gloss = p.get('gloss', 'No description.')
            
            # Headers
            if category != current_cat:
                f.write(f"## Category: {category}\n")
                context = CATEGORY_CONTEXTS.get(category, "General agent operations.")
                f.write(f"*Context: Primarily useful in {context}.*\n\n")
                current_cat = category
            
            # Situational Analysis
            value_prop = TIER_VALUE.get(tier, "Unknown Value.")
            
            f.write(f"### {handle}\n")
            f.write(f"**Situation:** Used when {gloss.lower()}\n")
            f.write(f"**Value:** {value_prop}\n")
            
            # Mechanism highlight
            mech = p.get('mechanism', '')
            if len(mech) > 150:
                mech = mech[:147] + "..."
            f.write(f"> *Mechanism: {mech}*\n\n")
            
            f.write("---\n\n")

    print(f"✅ Situational Review generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_review()
