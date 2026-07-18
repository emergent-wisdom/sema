#!/usr/bin/env python3
"""Generate `docs/manuals/vocabulary-design.md` from pattern files + design sidecar.

The manual is fully auto-generated. Everything editable lives in two places:

  - **Pattern specs** — `data/vocabulary/*.json` (mechanism, invariants,
    failure modes, dependencies, etc.).
  - **Design commentary** — `data/design_critique.json` (one entry per
    handle with `motivation`, `usage`, `design` (tensions/tradeoffs/critique),
    and `family_discussion`).

Every run of this script rewrites the manual from scratch. Do not hand-edit
the output file — hand-edit the sidecar or the pattern JSONs instead.

Usage:
    python scripts/generate_design_manual.py

Writes:
    docs/manuals/vocabulary-design.md
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = REPO_ROOT / "data" / "vocabulary"
STAGING_DIR = REPO_ROOT / "data" / "staging"
SIDECAR = REPO_ROOT / "data" / "design_critique.json"
OUTPUT = REPO_ROOT / "docs" / "manuals" / "vocabulary-design.md"

# Layer ordering reflects the civilization stack — substrate up to coordination.
LAYER_ORDER = ["Physics", "Infrastructure", "Mind", "Society"]


GOVERNING_PRINCIPLES = """\
## Governing principles

These are the rules a new pattern must pass before it enters the default library.
They are stated here forward-looking — as requirements for future mints — rather
than as history. All four are enforced or validated at mint time through
`sema apply` checks and the pattern-authoring review workflow, with the design
manual itself (this document) as the primary review surface.

### The mechanism-sufficiency test (layer placement)

A pattern's layer is determined by what its mechanism **structurally requires to
execute** — not by what the pattern is typically used for, not by what it
conceptually operates on, and not by how foundational it feels.

| Layer | Tight definition | Test question |
|---|---|---|
| **Physics** | Substrate primitives that obtain regardless of any author. Inviolable environmental realities — you cannot negotiate with Physics. | *Does this exist whether or not anyone thinks about it or designs it?* |
| **Infrastructure** | Authored structures and operations that do not require cognition to execute. Data types, composite topologies, authored foundational primitives. | *Can a program execute this without making any judgment? Was this designed?* |
| **Mind** | Mechanisms that require cognition — judgment, reasoning, inference, strategy. Single party is sufficient; cognition alone executes the mechanism. | *Does this require a knower to make a call that cannot be reduced to schema-matching? Can a single isolated agent execute it?* |
| **Society** | Mechanisms that structurally require ≥2 independent parties — parties with separate state and potentially divergent interests. Cognition alone is insufficient; external parties are part of the mechanism. | *Does the mechanism structurally require another party whose state is outside this agent's control?* |

The sharpest lines are *Physics vs Infrastructure* (substrate-given vs
author-designed) and *Mind vs Society* (single-party-sufficient vs multi-party-required).

### The two-criteria minting rule (whether to mint at all)

A concept earns a pattern only if it meets at least one of:

1. **Protocol consistency** — two or more agents must coordinate on the *exact*
   semantics of the concept. Content-addressed definition is then the mechanism
   of shared meaning (e.g. `Lock` must pin atomicity semantics because
   distributed mutex protocols break if parties disagree on reentrancy or
   stealability).

2. **Structured thinking** — the act of specifying a mechanism (what the word
   actually does, what invariants it implies, what its failure modes are)
   sharpens a concept that English uses loosely. Writing `Noise#<hash>` with an
   invariant-bearing mechanism forces the author and every downstream reader to
   confront what *noise* actually means. The pattern becomes a thinking tool.

Either criterion alone is sufficient. English suffices when neither is met —
pre-emptively minting concepts with no callers and no coordinating protocol
adds library weight without buying either form of value.

### The broad-use test (how general to make a pattern)

For each pattern, enumerate:

- the **intended** use (the canonical scenario the pattern was minted for),
- **future uses** (plausible scenarios it might reach),
- the **broad-use contexts** (the enumerated range of legitimate deployment
  contexts across which it should behave coherently),
- **what every context needs** (a review hypothesis about the intersection;
  each candidate must still pass the constraint-placement test before it
  enters the pattern's mechanism or contracts),
- **what varies** (context-specific features that belong in descendants, not
  the parent pattern),
- the **extension shape** (specific `derived_from` descendants that specialize
  along the varying axes).

The discipline prevents two failure modes simultaneously: a mechanism overfit
to the author's first use case (too specific, breaks legitimate variants) and
a mechanism so generic it has no teeth (too vague, underconstrains the concept).

### The constraint-placement test (what belongs in the hash)

Breadth is required of the reusable ancestry spine, not of every leaf. A
specific leaf pattern can and should pin a concrete strategy when that
specificity is what gives the pattern value. A short, general parent handle has
a different obligation: its hashed definition must admit every legitimate
broad-use context named in its commentary.

Before adding a mechanism clause, invariant, precondition, postcondition, or
failure mode to a parent, ask:

1. **Identity test** — if an implementation omits this requirement, does it
   cease to be the pattern in every broad-use context? If not, the requirement
   is not universal enough for the parent hash.
2. **Placement test** — is this an intrinsic quantitative axis, a qualitatively
   different strategy, deployment policy, or reviewer diagnostic? Put intrinsic
   quantitative axes in parameters, different strategies in descendants,
   deployment policy in callers, and contextual guidance in the sidecar.
3. **Testability test** — can independent agents determine whether the
   requirement holds without importing unstated domain policy? Aspirational or
   context-relative claims belong in commentary until a caller supplies the
   missing standard.

Failure modes belong in the hash when they arise structurally from the named
mechanism. Risks that depend on a particular deployment, threat model, or
quality threshold belong in the sidecar or a specialized descendant.

An absent contract is therefore not automatically a defect. Thin primitives,
abstract nouns, and extension points may intentionally omit contracts that
would merely restate the mechanism or narrow legitimate composition. Audit the
reason for the omission; do not optimize for the number of populated fields.

### Reading the design commentary

The sidecar is review evidence, not a normative extension of the pattern. Its
broad-use intersection is a hypothesis to test against the canonical
definition, and its critique identifies questions and risks for reviewers. A
listed diagnostic does not imply that a matching invariant or failure mode
belongs in the parent hash.

Useful commentary names the likely placement of a concern: parent identity,
parameter, descendant strategy, caller policy, or reviewer diagnostic. Counts
such as "only two invariants" are not evidence of a design defect by
themselves; rewrite them around the semantic risk and run the placement test.
"""


# ──────────────────────────────────────────────────────────────────────────
# Loaders
# ──────────────────────────────────────────────────────────────────────────


def load_patterns(vocab_dir: Path, staging_dir: Path | None = None) -> dict[str, dict]:
    """Load pattern specs, preferring staging/<Handle>.json when present.

    Staging contains in-progress edits not yet applied to taxonomy.db /
    data/vocabulary/. The manual reflects current work-in-progress by
    preferring staging entries over vocabulary for any handle that has both.
    """
    staged_count = 0
    out: dict[str, dict] = {}
    for fp in sorted(vocab_dir.glob("*.json")):
        try:
            pat = json.loads(fp.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"warning: failed to parse {fp.name}: {e}", file=sys.stderr)
            continue
        handle = pat.get("handle") or fp.stem
        # If staging has a copy, prefer it.
        if staging_dir and staging_dir.exists():
            staged_fp = staging_dir / f"{handle}.json"
            if staged_fp.exists():
                try:
                    staged_pat = json.loads(staged_fp.read_text(encoding="utf-8"))
                    # Preserve the vocabulary's sema_id/ref/stub if staging lacks them
                    for k in ("sema_id", "sema_ref", "sema_stub"):
                        if k not in staged_pat and k in pat:
                            staged_pat[k] = pat[k]
                    pat = staged_pat
                    staged_count += 1
                except Exception as e:  # noqa: BLE001
                    print(
                        f"warning: failed to parse staging {staged_fp.name}: {e}", file=sys.stderr
                    )
        out[handle] = pat
    if staged_count:
        print(f"info: rendering {staged_count} staged pattern(s) (prefer staging over vocabulary)")
    return out


def load_sidecar(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"error: sidecar unparseable: {e}", file=sys.stderr)
        return {}


# ──────────────────────────────────────────────────────────────────────────
# Rendering
# ──────────────────────────────────────────────────────────────────────────


def _short_ref(pattern: dict) -> str:
    sema_id = pattern.get("sema_id", "")
    stub = pattern.get("sema_stub") or (
        sema_id.split(":SHA-256:")[-1][:4] if ":SHA-256:" in sema_id else ""
    )
    return f"{pattern.get('handle', '?')}#{stub}" if stub else pattern.get("handle", "?")


def _safe_list(xs) -> list[str]:
    if not xs:
        return []
    if isinstance(xs, str):
        return [xs]
    return [str(x) for x in xs]


def render_pattern_entry(pattern: dict, commentary: dict | None) -> str:
    meta = pattern.get("_meta") or {}
    layer = meta.get("layer") or pattern.get("sema_layer") or "?"
    category = meta.get("category") or pattern.get("sema_category") or ""
    tier = meta.get("tier")
    ring = meta.get("ring")
    gloss = (pattern.get("gloss") or "").strip()
    mechanism = (pattern.get("mechanism") or "").strip()
    invariants = _safe_list(pattern.get("invariants"))
    preconditions = _safe_list(pattern.get("preconditions"))
    postconditions = _safe_list(pattern.get("postconditions"))
    failure_modes = _safe_list(pattern.get("failure_modes"))
    signature = _safe_list(pattern.get("signature"))
    supersedes = _safe_list((pattern.get("_meta") or {}).get("supersedes"))
    derived_from = pattern.get("derived_from") or ""

    motivation = (commentary or {}).get("motivation") or {}
    usage = (commentary or {}).get("usage") or {}
    design = (commentary or {}).get("design") or {}
    family = (commentary or {}).get("family_discussion") or ""

    head_bits = [f"`{layer}`"]
    if category:
        head_bits.append(f"`{category}`")
    if ring is not None:
        head_bits.append(f"R{ring}")
    if tier is not None:
        head_bits.append(f"T{tier}")

    lines: list[str] = []
    lines.append(f"### {_short_ref(pattern)}")
    lines.append("")
    lines.append(" · ".join(head_bits))
    lines.append("")
    if gloss:
        lines.append(f"**Gloss.** {gloss}")
        lines.append("")
    if signature:
        lines.append(f"**Signature.** `{', '.join(signature)}`")
        lines.append("")
    if mechanism:
        lines.append("**Mechanism.**")
        lines.append("")
        lines.append("> " + mechanism.replace("\n", "\n> "))
        lines.append("")
    if invariants:
        lines.append("**Invariants.**")
        for inv in invariants:
            lines.append(f"- {inv}")
        lines.append("")
    if preconditions:
        lines.append("**Preconditions.**")
        for pc in preconditions:
            lines.append(f"- {pc}")
        lines.append("")
    if postconditions:
        lines.append("**Postconditions.**")
        for pc in postconditions:
            lines.append(f"- {pc}")
        lines.append("")
    if failure_modes:
        lines.append("**Failure modes.**")
        for fm in failure_modes:
            lines.append(f"- {fm}")
        lines.append("")

    # Design commentary — everything below comes from the sidecar.
    has_any_commentary = any(
        [
            motivation.get("why_this_layer"),
            motivation.get("why_it_exists"),
            motivation.get("removability"),
            usage.get("intended"),
            usage.get("future"),
            usage.get("broad_contexts"),
            usage.get("every_context_needs"),
            usage.get("varies"),
            usage.get("extensions"),
            design.get("tensions"),
            design.get("tradeoffs"),
            design.get("critique"),
            family,
        ]
    )
    if has_any_commentary:
        lines.append("#### Design")
        lines.append("")

    if motivation.get("why_it_exists"):
        lines.append(f"**Why it exists.** {motivation['why_it_exists']}")
        lines.append("")
    if motivation.get("why_this_layer"):
        lines.append(f"**Why {layer}.** {motivation['why_this_layer']}")
        lines.append("")
    if motivation.get("removability"):
        lines.append(f"**Can it be removed?** {motivation['removability']}")
        lines.append("")

    if usage.get("intended"):
        lines.append(f"**Intended use.** {usage['intended']}")
        lines.append("")
    if usage.get("future"):
        lines.append(f"**Future uses.** {usage['future']}")
        lines.append("")
    if usage.get("broad_contexts"):
        lines.append(f"**Broad-use contexts.** {usage['broad_contexts']}")
        lines.append("")
    if usage.get("every_context_needs"):
        lines.append(
            f"**Broad-use intersection (review hypothesis).** {usage['every_context_needs']}"
        )
        lines.append("")
    if usage.get("varies"):
        lines.append(f"**Varies (descendant territory).** {usage['varies']}")
        lines.append("")
    if usage.get("extensions"):
        lines.append(f"**Extension shape.** {usage['extensions']}")
        lines.append("")
    for n in usage.get("notes") or []:
        lines.append(f"_Note: {n}_")
        lines.append("")

    if design.get("tensions"):
        lines.append("**Design tensions.**")
        for t in design["tensions"]:
            lines.append(f"- {t}")
        lines.append("")
    if design.get("tradeoffs"):
        lines.append("**Tradeoffs.**")
        for t in design["tradeoffs"]:
            lines.append(f"- {t}")
        lines.append("")
    if design.get("critique"):
        lines.append("**Critique (diagnostic, not contract requirements).**")
        for c in design["critique"]:
            lines.append(f"- {c}")
        lines.append("")

    if family:
        lines.append(f"**In the family.** {family}")
        lines.append("")

    # Lineage.
    if derived_from:
        parent_handle = derived_from.split("sema:")[-1].split("#")[0]
        lines.append(f"**Derived from.** `{parent_handle}`")
        lines.append("")
    if supersedes:
        lines.append("**Supersedes (prior versions).**")
        for s in supersedes:
            old_handle = s.split("sema:")[-1].split("#")[0] if "sema:" in s else s
            short = s.split(":SHA-256:")[-1][:4] if ":SHA-256:" in s else ""
            lines.append(f"- `{old_handle}{'#' + short if short else ''}`")
        lines.append("")

    lines.append("---")
    return "\n".join(lines)


def render_manual(patterns: dict[str, dict], sidecar: dict[str, dict]) -> str:
    header = [
        "# Sema Vocabulary Design Manual",
        "",
        "<!-- AUTOGENERATED — do not hand-edit. Regenerate with:",
        "     `python scripts/generate_design_manual.py`. Edit pattern specs",
        "     in `data/vocabulary/*.json` and design commentary in",
        "     `data/design_critique.json`. -->",
        "",
        f"_Generated: {date.today().isoformat()}_",
        f"_Patterns covered: {len(patterns)} (from `data/vocabulary/`)_",
        f"_Commentary entries in sidecar: {len(sidecar)} (from `data/design_critique.json`)_",
        "",
        "This manual is the design reference for the Sema Bootstrap Library. "
        "For each pattern, it shows the machine-checkable spec (mechanism, "
        "invariants, pre/postconditions, failure modes) alongside the design "
        "commentary: why it exists, why it sits where it does, whether it could "
        "be removed, how it's used across contexts, its design tensions and "
        "tradeoffs, critique, and where it sits in its family.",
        "",
        "See also: `docs/core/philosophy.md` for the protocol-level principles, "
        "`docs/guides/lifecycle.md` for pull / refinement / distribution workflows.",
        "",
        "---",
        "",
        GOVERNING_PRINCIPLES,
        "---",
        "",
        "## Patterns",
        "",
    ]

    body: list[str] = []
    by_layer: dict[str, dict[str, list[str]]] = {layer: {} for layer in LAYER_ORDER}
    unknown: list[str] = []
    for handle, pat in patterns.items():
        meta = pat.get("_meta") or {}
        layer = meta.get("layer") or pat.get("sema_layer") or ""
        category = meta.get("category") or pat.get("sema_category") or "(uncategorized)"
        if layer not in by_layer:
            unknown.append(handle)
            continue
        by_layer[layer].setdefault(category, []).append(handle)

    for layer in LAYER_ORDER:
        categories = by_layer[layer]
        total = sum(len(v) for v in categories.values())
        if total == 0:
            continue
        body.append(f"## {layer} ({total})")
        body.append("")
        for category in sorted(categories):
            handles = sorted(categories[category])
            body.append(f"### {layer}/{category} ({len(handles)})")
            body.append("")
            for handle in handles:
                body.append(render_pattern_entry(patterns[handle], sidecar.get(handle)))
                body.append("")

    if unknown:
        body.append("## Uncategorized")
        body.append("")
        for handle in sorted(unknown):
            body.append(f"- `{handle}`")
        body.append("")

    return "\n".join(header) + "\n".join(body) + "\n"


def main() -> int:
    if not VOCAB_DIR.exists():
        print(f"error: {VOCAB_DIR} not found", file=sys.stderr)
        return 1
    patterns = load_patterns(VOCAB_DIR, STAGING_DIR)
    sidecar = load_sidecar(SIDECAR)

    content = render_manual(patterns, sidecar)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content, encoding="utf-8")

    def _fill_stat(attr_path: tuple) -> int:
        n = 0
        for entry in sidecar.values():
            cursor = entry
            for key in attr_path:
                cursor = (cursor or {}).get(key) if isinstance(cursor, dict) else None
            if cursor:
                n += 1
        return n

    print(f"✓ Wrote {OUTPUT.relative_to(REPO_ROOT)}")
    print(f"  Patterns: {len(patterns)}")
    print(f"  Sidecar entries: {len(sidecar)}")
    print("  Fill stats:")
    print(f"    motivation.why_this_layer: {_fill_stat(('motivation', 'why_this_layer'))}")
    print(f"    motivation.why_it_exists:  {_fill_stat(('motivation', 'why_it_exists'))}")
    print(f"    motivation.removability:   {_fill_stat(('motivation', 'removability'))}")
    print(f"    usage.intended:            {_fill_stat(('usage', 'intended'))}")
    print(f"    design.tensions:           {_fill_stat(('design', 'tensions'))}")
    print(f"    design.tradeoffs:          {_fill_stat(('design', 'tradeoffs'))}")
    print(f"    design.critique:           {_fill_stat(('design', 'critique'))}")
    print(f"    family_discussion:         {_fill_stat(('family_discussion',))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
