#!/usr/bin/env python3
"""
Generate a human-readable review of the Sema vocabulary.
Grades patterns based on structural rigor and utility.
"""

import glob
import json
import os

VOCAB_DIR = "data/vocabulary"
OUTPUT_FILE = "vocabulary_review.md"

def load_patterns():
    patterns = []
    for filepath in glob.glob(os.path.join(VOCAB_DIR, "*.json")):
        with open(filepath) as f:
            patterns.append(json.load(f))
    return sorted(patterns, key=lambda x: x['handle'])

def grade_pattern(p):
    """Heuristic grading of pattern quality."""
    score = 0
    issues = []
    
    # Tier Base
    tier = p.get('tier')
    if tier == 1: score += 3
    elif tier == 2: score += 1
    else: issues.append("Experimental Tier")
    
    # Contract Rigor
    inv_count = len(p.get('invariants', []))
    pre_count = len(p.get('preconditions', []))
    post_count = len(p.get('postconditions', []))
    
    if inv_count > 0: score += 2
    if inv_count > 2: score += 1 # Bonus for rich invariants
    if pre_count + post_count > 0: score += 1
    
    if inv_count == 0: issues.append("No Invariants")
    
    # Mechanism Clarity
    mech = p.get('mechanism', '')
    if len(mech) < 50: issues.append("Short/Vague Mechanism")
    if "mechanism not defined" in mech.lower(): 
        score = 0
        issues.append("MISSING MECHANISM")
        
    # Verdict
    if score >= 6: verdict = "⭐⭐⭐ STRONG"
    elif score >= 4: verdict = "⭐⭐ SOLID"
    elif score >= 2: verdict = "⭐ WEAK"
    else: verdict = "❌ POOR"
    
    return score, verdict, issues

def generate_markdown():
    patterns = load_patterns()
    
    with open(OUTPUT_FILE, 'w') as f:
        f.write("# Sema Vocabulary Review\n\n")
        f.write(f"**Total Patterns:** {len(patterns)}\n")
        f.write("Generated via heuristic audit (Tier + Contracts + Detail).\n\n")
        
        # Stats
        strong = 0
        poor = 0
        
        sections = {
            "⭐⭐⭐ STRONG": [],
            "⭐⭐ SOLID": [],
            "⭐ WEAK": [],
            "❌ POOR": []
        }
        
        for p in patterns:
            score, verdict, issues = grade_pattern(p)
            sections[verdict].append((p, issues))
            if verdict == "⭐⭐⭐ STRONG": strong += 1
            if verdict == "❌ POOR": poor += 1

        f.write(f"**Summary:** {strong} Strong patterns, {poor} Poor patterns needing attention.\n\n")
        f.write("---\n\n")
        
        order = ["❌ POOR", "⭐ WEAK", "⭐⭐ SOLID", "⭐⭐⭐ STRONG"]
        
        for label in order:
            items = sections[label]
            if not items: continue
            
            f.write(f"## {label} ({len(items)})\n\n")
            
            for p, issues in items:
                handle = p['handle']
                gloss = p.get('gloss', 'No description')
                mech = p.get('mechanism', '')
                
                f.write(f"### {handle}\n")
                f.write(f"**Why Useful:** {gloss}\n\n")
                f.write(f"> {mech}\n\n")
                
                if issues:
                    f.write(f"**Issues:** {', '.join(issues)}\n")
                
                # Links
                links = []
                if 'links' in p:
                    for rel, targets in p['links'].items():
                        links.append(f"{rel}: {len(targets)}")
                if links:
                    f.write(f"*Connectivity: {', '.join(links)}*\n")
                    
                f.write("\n---\n\n")

    print(f"✅ Review generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_markdown()
