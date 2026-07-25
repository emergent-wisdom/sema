#!/usr/bin/env python3
"""Report CapitalisedNames in pattern text that resolve to no pattern.

    dangling_handles.py                 # report over data/vocabulary/
    dangling_handles.py --sidecar       # also read data/design_critique.json
    dangling_handles.py --strict        # exit 1 if anything is found

A card that contrasts itself against `Broad` when no Broad pattern exists leaves a
reader with a reference that goes nowhere, and leaves the card as half of a pair
whose other half was never minted. Nine such names were found by reading the
corpus one pattern at a time: Broad (in Deep and DeepResearch), Trinary (TriGate),
History (Trace, Reason, SunkCostIgnore, Context), Amplify, Recall, Nominate and
Appoint (all in commentary).

This resolves names; it does not decide what to do about them. The response is a
judgment and belongs to a human: mint the missing pattern, redirect to an existing
one that already covers it, or lowercase the word because it was never a handle.
The instance count matters for that decision, so it is reported — MintWhenFriction
asks for three instances of explanation overhead before a mint is justified.

What this CANNOT find, measured rather than assumed
---------------------------------------------------
A single capitalised word outside backticks is undetectable here. This corpus
capitalises ordinary nouns mid-sentence, so scanning for them yields 769
candidates against 4 true positives — about 1:200 — even after stripping the
`Label: description` prefixes that invariants and failure modes use. Stripping
labels removed only 205 of 974; the rest are words like Threshold, Cost, Time,
Input, Source and Target.

That matters because it is exactly where the real findings were. `Broad` (in Deep
and DeepResearch), `Trinary` (TriGate) and `History` (Trace, Reason,
SunkCostIgnore, Context) are all single bare words, each at one or two sites, and
each was found by reading the pattern rather than by any scan. Do not re-attempt
the single-word case expecting a better filter; the limit is the corpus's prose
style, not the regex.

So: run this for the two classes it does resolve, and keep reading for the rest.

Deliberately NOT a review aid. It cannot tell you whether a pattern is sound, and
it must not be used to choose which patterns to read.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VOCAB_DIR = REPO_ROOT / "data" / "vocabulary"
SIDECAR = REPO_ROOT / "data" / "design_critique.json"

# Hashed text fields plus the sidecar's prose. Placeholders ({{foo}}) are excluded
# separately, since the Forward rule already guarantees those resolve.
TEXT_FIELDS = (
    "mechanism",
    "gloss",
    "invariants",
    "preconditions",
    "postconditions",
    "failure_modes",
)

# A single capitalised word inside backticks is an explicit reference claim.
# Outside backticks, only CamelCase of two or more capitalised parts counts —
# a bare capitalised word is far too noisy, since every sentence starts with one.
BACKTICKED = re.compile(r"`([A-Z][A-Za-z0-9]*)`")
CAMEL = re.compile(r"\b((?:[A-Z][a-z0-9]+){2,})\b")

# ALL-CAPS tokens are protocol message and phase names by convention in this
# corpus — NOMINATE, VOTE, GREET, CLOSE, DEBT, ENLIST — not handle references.
ALL_CAPS = re.compile(r"^[A-Z0-9]+[a-z]?$")


def collect_text(obj) -> list[str]:
    """Flatten strings out of a field value."""
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, list):
        return [s for item in obj for s in collect_text(item)]
    if isinstance(obj, dict):
        return [s for value in obj.values() for s in collect_text(value)]
    return []


def candidate_names(text: str) -> set[tuple[str, bool]]:
    """(name, was_backticked) pairs a reader would take for pattern references."""
    stripped = re.sub(r"\{\{[^}]*\}\}", " ", text)
    names = {(n, True) for n in BACKTICKED.findall(stripped)}
    backticked = {n for n, _ in names}
    names |= {(n, False) for n in CAMEL.findall(stripped) if n not in backticked}
    return names


def resolves(name: str, known_lower: set[str]) -> bool:
    """True if the name is a known handle, or an inflection of one.

    `CARDs`, `AcceptSpecs` and `SOLVERs` are plurals of real patterns, not missing
    ones. Folding them is what makes the remaining list worth reading.
    """
    candidates = {name.lower()}
    for suffix in ("'s", "s", "es"):
        if name.lower().endswith(suffix):
            candidates.add(name.lower()[: -len(suffix)])
    return bool(candidates & known_lower)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--sidecar", action="store_true", help="also scan data/design_critique.json prose"
    )
    ap.add_argument("--strict", action="store_true", help="exit 1 if any dangling name is found")
    args = ap.parse_args()

    patterns = {}
    for path in sorted(VOCAB_DIR.glob("*.json")):
        data = json.loads(path.read_text())
        handle = data.get("handle")
        if handle:
            patterns[handle] = data
    if not patterns:
        print(f"No patterns found in {VOCAB_DIR}", file=sys.stderr)
        return 2

    known_lower = {h.lower() for h in patterns}
    sites: dict[str, set[str]] = defaultdict(set)
    explicit: set[str] = set()

    def record(name, was_backticked, owner, where):
        if name == owner or resolves(name, known_lower):
            return
        if ALL_CAPS.match(name):
            return
        sites[name].add(where)
        if was_backticked:
            explicit.add(name)

    for handle, data in patterns.items():
        for field in TEXT_FIELDS:
            for text in collect_text(data.get(field)):
                for name, ticked in candidate_names(text):
                    record(name, ticked, handle, f"{handle}.{field}")

    if args.sidecar and SIDECAR.exists():
        sidecar = json.loads(SIDECAR.read_text())
        for handle, entry in sidecar.items():
            for text in collect_text(entry):
                for name, ticked in candidate_names(text):
                    record(name, ticked, handle, f"{handle} (sidecar)")

    if not sites:
        print(f"No unresolved names across {len(patterns)} patterns.")
        return 0

    print(f"{len(sites)} unresolved name(s) across {len(patterns)} patterns.")
    print("Resolving a name is mechanical; deciding what to do about it is not.")
    print("Backticked names are explicit reference claims and are listed first.\n")

    def group(names, title):
        if not names:
            return
        print(f"{title}\n")
        for name in sorted(names, key=lambda n: (-len(sites[n]), n)):
            where = sites[name]
            bar = "clears" if len(where) >= 3 else "below"
            print(f"  {name:26s} {len(where):2d} site(s)  [{bar} the 3-instance mint bar]")
            for site in sorted(where):
                print(f"       {site}")
        print()

    group(explicit, "── Backticked: written as a handle, resolves to nothing")
    group(set(sites) - explicit, "── Bare CamelCase: may be a concept, a quantity, or prose")

    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
