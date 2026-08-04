#!/usr/bin/env python3
"""Measure the bundled vocabulary against the lettered rules in
docs/specification/validation.md.

Rules A–K are stated there. Not all are mechanical: J (Semantic Meaningfulness)
and the Truth-in-Advertising half of F need a reader, and this script says so
rather than scoring them. What it does check, it checks against every pattern in
data/vocabulary/, including rules the apply-time validator does not reach.

That last point is the reason this script exists. `validate_layer_direction`
(Rule G) skips any dependency it cannot resolve, and at apply time it resolves
only the staged batch — pattern nodes store the handle in `data["text"]` rather
than `data["handle"]`, so the committed corpus arrives as an empty dict. A
staged pattern's edges into the existing library are therefore all "unknown" and
all skipped. Rule G has consequently never been enforced against the corpus, and
the same is true of any rule that needs cross-pattern resolution.

    python scripts/audit/rule_adherence.py           # summary
    python scripts/audit/rule_adherence.py --detail  # every violation
"""

from __future__ import annotations

import argparse
import glob
import json
import re
from collections import defaultdict

LAYER_ORDER = {"Infrastructure": 0, "Physics": 1, "Mind": 2, "Society": 3}
HASHED_TEXT = ("mechanism", "gloss", "invariants", "preconditions", "postconditions",
               "failure_modes", "parameters", "signature", "data_schema")
BUCKETS = ("accepts", "yields", "composes_with", "references")
LAYER_CHECKED = ("accepts", "composes_with")  # Rule G exempts yields and references


def load() -> dict[str, dict]:
    out = {}
    for path in sorted(glob.glob("data/vocabulary/*.json")):
        d = json.loads(open(path).read())
        out[d["handle"]] = d
    return out


def text_blob(d: dict) -> str:
    return json.dumps({k: d.get(k) for k in HASHED_TEXT}, ensure_ascii=False)


def placeholders(d: dict) -> set[str]:
    return set(re.findall(r"\{\{(\w+)\}\}", text_blob(d)))


def declared(d: dict) -> dict[str, str]:
    """placeholder key -> bucket"""
    out = {}
    for b, v in (d.get("dependencies") or {}).items():
        for k in (v or {}):
            out[k] = b
    return out


def layer(d: dict) -> str | None:
    path = (d.get("_meta") or {}).get("path") or []
    return path[0] if path else (d.get("_meta") or {}).get("layer")


def resolve(name: str, pats: dict[str, dict]) -> str | None:
    lowered = {h.lower(): h for h in pats}
    return lowered.get(name.replace("_", "").lower())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--detail", action="store_true")
    args = ap.parse_args()
    pats = load()
    v: dict[str, list[str]] = defaultdict(list)

    for h, d in pats.items():
        ph, dec = placeholders(d), declared(d)

        # Rule A — forward and inverse
        for miss in sorted(ph - set(dec)):
            v["A forward: placeholder with no dependency"].append(f"{h}: {{{{{miss}}}}}")
        for unused in sorted(set(dec) - ph):
            v["A inverse: dependency never used in text"].append(f"{h}: {unused}")

        # Rule B — exactly one category
        seen: dict[str, list[str]] = defaultdict(list)
        for b, vv in (d.get("dependencies") or {}).items():
            for k in (vv or {}):
                seen[k].append(b)
        for k, bs in seen.items():
            if len(bs) > 1:
                v["B: dependency in more than one category"].append(f"{h}: {k} in {bs}")

        # Rule D — no empty containers, no nulls where the field is present
        for f in ("invariants", "preconditions", "postconditions", "failure_modes",
                  "parameters", "signature", "dependencies", "data_schema"):
            if f in d and d[f] in ([], {}, None):
                v["D: empty or null field present instead of omitted"].append(f"{h}: {f}")

        # Rule F — every signature entry needs an argument
        for s in (d.get("signature") or []):
            if "(" not in s or not s.rstrip().endswith(")"):
                v["F: signature entry with no argument"].append(f"{h}: {s!r}")

        # Rule G — accepts/composes_with may not point at a more abstract layer
        my_layer = layer(d)
        if my_layer in LAYER_ORDER:
            for b in LAYER_CHECKED:
                for k in ((d.get("dependencies") or {}).get(b) or {}):
                    tgt = resolve(k, pats)
                    if not tgt:
                        continue
                    tl = layer(pats[tgt])
                    if tl in LAYER_ORDER and LAYER_ORDER[tl] > LAYER_ORDER[my_layer]:
                        v["G: hard dependency on a more abstract layer"].append(
                            f"{h} ({my_layer}) {b} -> {tgt} ({tl})")

        # Rule I — a split compound is only a violation when the two halves name a
        # real handle. "The {{problem}} Statement" for ProblemStatement is the rule's
        # own example. "{{sandbox}} Escape" is a failure mode's NAME, not a split
        # handle, and there is no SandboxEscape pattern to split — flagging those
        # inflated an early run of this script from 3 to 55.
        for m in re.finditer(r"\{\{(\w+)\}\}\s+([A-Z][a-z]+)", text_blob(d)):
            key, word = m.group(1), m.group(2)
            joined = resolve(key.replace("_", "") + word, pats)
            if joined and joined != h:
                v["I: half-concept — split compound names a real pattern"].append(
                    f"{h}: {{{{{key}}}}} {word}  ->  {joined}")
            else:
                v["(not a rule) placeholder used as a label word"].append(
                    f"{h}: {{{{{key}}}}} {word}")

        # Rule E / K — nouns and state-bearing primitives need a non-vacuous schema
        ds = d.get("data_schema")
        path = (d.get("_meta") or {}).get("path") or []
        if path and path[-1] == "Data Structures":
            if not ds:
                v["E/K: Data Structures category with no data_schema"].append(h)
            elif not (ds.get("properties") or {}):
                v["E non-vacuous: schema defines no property"].append(h)

    # Rule E's wider clause: anything used as accepts/yields is a Noun
    used_as_noun: set[str] = set()
    for h, d in pats.items():
        for b in ("accepts", "yields"):
            for k in ((d.get("dependencies") or {}).get(b) or {}):
                tgt = resolve(k, pats)
                if tgt:
                    used_as_noun.add(tgt)
    for tgt in sorted(used_as_noun):
        if not (pats[tgt].get("data_schema") or {}).get("properties"):
            v["E wider: used in accepts/yields but no schema properties"].append(tgt)

    print(f"{len(pats)} patterns audited against docs/specification/validation.md\n")
    order = sorted(v, key=lambda k: -len(v[k]))
    width = max((len(k) for k in v), default=0)
    for k in order:
        print(f"  {len(v[k]):4d}  {k}")
        if args.detail:
            for line in v[k]:
                print(f"        {line}")
    if not v:
        print("  no violations of the mechanical rules")
    print("\nNot mechanically checkable, and therefore not scored here:")
    print("  C  cycle-freedom is enforced at apply time; the Noun/Verb tie-break is judgment")
    print("  F  the Truth-in-Advertising half — whether a claimed signature is fulfilled")
    print("  H  Concept Suspicion — see scripts/audit/dangling_handles.py and its docstring")
    print("  J  Semantic Meaningfulness — no tautologies, no vacuous definitions")


if __name__ == "__main__":
    main()
