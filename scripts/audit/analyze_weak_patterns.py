#!/usr/bin/env python3
"""
Analyze Weak patterns to recommend Action: STRENGTHEN, REMOVE, or KEEP.
"""

import glob
import json
import os

VOCAB_DIR = "data/vocabulary"

def analyze_weak():
    weak_patterns = []
    
    # 1. Identify Weak Patterns
    for filepath in glob.glob(os.path.join(VOCAB_DIR, "*.json")):
        with open(filepath) as f:
            p = json.load(f)
            
        # Score Logic (Same as review script)
        score = 0
        if p.get('tier') == 1: score += 3
        elif p.get('tier') == 2: score += 1
        
        inv_count = len(p.get('invariants', []))
        if inv_count > 0: score += 2
        if inv_count > 2: score += 1
        if len(p.get('preconditions', [])) + len(p.get('postconditions', [])) > 0: score += 1
        
        if score < 4: # WEAK Threshold
            weak_patterns.append(p)
            
    print(f"Analyzing {len(weak_patterns)} Weak Patterns...\n")
    
    for p in sorted(weak_patterns, key=lambda x: x['handle']):
        handle = p['handle']
        mech = p.get('mechanism', '')
        gloss = p.get('gloss', '')
        
        # Heuristics
        is_primitive = any(x in mech.lower() for x in ['token', 'hash', 'cryptographic', 'buffer', 'queue', 'lock'])
        is_cognitive = any(x in mech.lower() for x in ['reasoning', 'think', 'prompt', 'bias', 'model'])
        
        action = "KEEP (Social/Soft)"
        reason = "Hard to formalize"
        
        if is_primitive:
            action = "STRENGTHEN"
            reason = "Engineering primitive - should have Invariants"
        elif len(mech) < 100:
            action = "REMOVE?"
            reason = "Vague/Short mechanism"
        elif "magic" in mech.lower() or "undefined" in mech.lower():
            action = "REMOVE"
            reason = "Undefined behavior"
            
        print(f"[{action}] {handle}\n")
        print(f"  Reason: {reason}\n")
        print(f"  Gloss: {gloss}\n")
        print(f"  Mech: {mech[:80]}...\n")
        print()

if __name__ == "__main__":
    analyze_weak()
