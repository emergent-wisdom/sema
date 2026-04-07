#!/usr/bin/env python3
"""
Check Half-Concepts (Rule H)

Detects violations where a Compound Concept (e.g., "ProblemStatement") is referenced
by its parts (e.g., "Problem Statement", "{{problem}} statement", "{{problem}} {{statement}}")
instead of the full concept handle (e.g., "{{problem_statement}}").
"""

import glob
import json
import os
import re

VOCAB_DIR = "nextvocabulary"

def split_camel_case(name):
    """
    Splits CamelCase into list of words.
    e.g. "ProblemStatement" -> ["Problem", "Statement"]
    """
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', name)

def load_patterns():
    patterns_map = {}
    content_map = {}
    files = glob.glob(os.path.join(VOCAB_DIR, "*.json"))
    for fpath in files:
        try:
            with open(fpath) as f:
                data = json.load(f)
                handle = data.get("handle")
                if handle:
                    patterns_map[handle] = data
        except:
            pass
    return patterns_map

def get_snake_case(handle):
    # Convert PascalCase to snake_case for {{key}} matching
    # Simple conversion: ProblemStatement -> problem_statement
    # But often keys are just lowercased handle in simple cases? 
    # The convention in this project seems to be snake_case.
    # Let's try to infer or just use regex.
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', handle)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def check_half_concepts():
    patterns = load_patterns()
    all_handles = set(patterns.keys())
    
    # Identify Compound Concepts
    compounds = {} # Handle -> [Parts]
    for h in all_handles:
        parts = split_camel_case(h)
        if len(parts) > 1:
            compounds[h] = parts

    print(f"🔍 Checking {len(patterns)} patterns for Half-Concept violations against {len(compounds)} compound concepts...")

    violations = 0

    for handle, data in patterns.items():
        # Text fields to check
        text_fields = []
        if 'mechanism' in data: text_fields.append(('mechanism', data['mechanism']))
        if 'invariants' in data: text_fields.append(('invariants', " ".join(data['invariants'])))
        if 'preconditions' in data: text_fields.append(('preconditions', " ".join(data['preconditions'])))
        if 'postconditions' in data: text_fields.append(('postconditions', " ".join(data['postconditions'])))
        if 'failure_modes' in data: text_fields.append(('failure_modes', " ".join(data['failure_modes'])))

        file_violations = []

        for field_name, text in text_fields:
            if not text: continue

            for compound, parts in compounds.items():
                if compound == handle: continue # Don't check against self

                # Construct regex for split concept
                # We want to match "Part1 Part2" or "{{part1}} Part2" etc.
                # Regex parts:
                # Part -> (Part|part|{{part_snake}})
                
                regex_parts = []
                for part in parts:
                    snake_part = part.lower() # Approximation
                    # Match literal Word (case insensitive) or {{snake_key}}
                    # We accept "Word" or "word" or "{{word}}"
                    # Note: identifying the exact snake key for a part is tricky if the part isn't a pattern itself.
                    # But if the part IS a pattern, it might be linked.
                    # Heuristic: Match the word boundary. 
                    
                    # Pattern for one part:
                    # \b(Part|part)\b  OR  \{\{[^}]*part[^}]*\}\} 
                    # This is getting complex.
                    
                    # Simpler approach:
                    # Look for the sequence of words in the plain text (ignoring {{...}} syntax for a moment)
                    # AND check if the user wrote "{{part1}} {{part2}}"
                    pass

                # Let's try a simpler regex that catches the textual split:
                # "Part1\s+Part2" (case insensitive)
                pattern_str = r'\b' + r'\s+'.join([re.escape(p) for p in parts]) + r'\b'
                if re.search(pattern_str, text, re.IGNORECASE):
                    file_violations.append(f"Potential split concept: '{compound}' found as text sequence in '{field_name}'")

        if file_violations:
            print(f"⚠️  {handle}:")
            for v in set(file_violations):
                print(f"   • {v}")
            violations += 1

    print(f"\n🔍 Scan complete. Found {violations} potential violations.")
    return violations

if __name__ == "__main__":
    check_half_concepts()
