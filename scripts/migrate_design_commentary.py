#!/usr/bin/env python3
"""One-time migration: audit .md files → `data/design_critique.json`.

Extracts per-pattern layer reasoning from `audits/2026-04-17/layer-assignment.md`
and broad-use analysis from `audits/2026-04-17/2026-04-broad-use-analysis.md`
into a single sidecar keyed by handle. After this runs, the sidecar is the
editable source of design commentary — the audit .md files become historical
snapshots and are no longer read by the manual generator.

Schema (per handle):

    {
        "motivation": {
            "why_this_layer": str,         # from layer-assignment.md
            "why_it_exists":  str,         # to be filled in iteratively
            "removability":   str          # to be filled in iteratively
        },
        "usage": {
            "intended":            str,    # from broad-use.md
            "future":              str,
            "broad_contexts":      str,
            "every_context_needs": str,
            "varies":              str,
            "extensions":          str,
            "notes":               [str]
        },
        "design": {
            "tensions":  [str],            # to be filled in iteratively
            "tradeoffs": [str],            # to be filled in iteratively
            "critique":  [str]             # to be filled in iteratively
        },
        "family_discussion": str           # to be filled in iteratively
    }

Unknown/empty keys are allowed — the manual generator renders whatever is
present. Running this script again is safe: it preserves any fields already
populated (motivation.why_it_exists, design.*, etc.) and only refreshes the
fields sourced from the audit docs.

Usage:
    python scripts/migrate_design_commentary.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = REPO_ROOT / "data" / "vocabulary"
LAYER_ASSIGNMENT = REPO_ROOT / "audits" / "2026-04-17" / "layer-assignment.md"
BROAD_USE = REPO_ROOT / "audits" / "2026-04-17" / "2026-04-broad-use-analysis.md"
SIDECAR = REPO_ROOT / "data" / "design_critique.json"


# ──────────────────────────────────────────────────────────────────────────
# Parsers (shared with generate_design_manual.py — duplicated here to keep
# the migration script standalone)
# ──────────────────────────────────────────────────────────────────────────


ENTRY_RE = re.compile(
    r"^-\s+"
    r"(?:`~`\s*\*\*(?P<handle_moved>\w+)\*\*\s*\*\(was [^)]+\)\*\s*|)"
    r"(?P<handle_plain>\w+)?"
    r"\s*(?:—|–|-)\s+(?P<reason>.+)$"
)


def parse_layer_assignment(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ENTRY_RE.match(line.strip())
        if not m:
            continue
        handle = m.group("handle_moved") or m.group("handle_plain")
        if not handle:
            continue
        out[handle] = m.group("reason").strip()
    return out


SECTION_RE = re.compile(r"^## \d+\.\s+`(?P<handle>\w+)`")
FIELD_RE = re.compile(r"^\*\*(?P<label>[^*:]+)\*\*\s*:\s*(?P<value>.*)$")

FIELD_MAP = {
    "Intended": "intended",
    "Future": "future",
    "Broad-use contexts": "broad_contexts",
    "Every context needs": "every_context_needs",
    "Varies": "varies",
    "Extension": "extensions",
}


def parse_broad_use(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    out: dict[str, dict] = {}
    current: dict | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        m_section = SECTION_RE.match(line)
        if m_section:
            current = {"notes": []}
            out[m_section.group("handle")] = current
            continue
        if current is None:
            continue
        m_field = FIELD_RE.match(line)
        if not m_field:
            continue
        label = m_field.group("label").strip()
        value = m_field.group("value").strip()
        attr = FIELD_MAP.get(label)
        if attr:
            current[attr] = value
        elif label in ("Note", "Notes"):
            current["notes"].append(value)
    return out


def load_handles(vocab_dir: Path) -> list[str]:
    """Return sorted list of handles from the vocabulary directory."""
    return sorted(p.stem for p in vocab_dir.glob("*.json"))


# ──────────────────────────────────────────────────────────────────────────
# Migration
# ──────────────────────────────────────────────────────────────────────────


def default_entry() -> dict:
    """An empty but structurally-complete entry. Keeps the shape explicit
    even for patterns the audit docs don't cover yet."""
    return {
        "motivation": {
            "why_this_layer": "",
            "why_it_exists": "",
            "removability": "",
        },
        "usage": {
            "intended": "",
            "future": "",
            "broad_contexts": "",
            "every_context_needs": "",
            "varies": "",
            "extensions": "",
            "notes": [],
        },
        "design": {
            "tensions": [],
            "tradeoffs": [],
            "critique": [],
        },
        "family_discussion": "",
    }


def migrate() -> dict:
    handles = load_handles(VOCAB_DIR)
    layer_reasons = parse_layer_assignment(LAYER_ASSIGNMENT)
    broad_use = parse_broad_use(BROAD_USE)

    # Load existing sidecar to preserve hand-edited / analytical fields.
    existing: dict = {}
    if SIDECAR.exists():
        try:
            existing = json.loads(SIDECAR.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"⚠ existing sidecar unparseable ({e}) — overwriting", file=sys.stderr)
            existing = {}

    out: dict[str, dict] = {}
    for handle in handles:
        entry = existing.get(handle) or default_entry()
        # Ensure shape — migrate older partial entries forward.
        for top_key, default_val in default_entry().items():
            if top_key not in entry:
                entry[top_key] = default_val
            elif isinstance(default_val, dict):
                for sub_key, sub_default in default_val.items():
                    if sub_key not in entry[top_key]:
                        entry[top_key][sub_key] = sub_default

        # Overwrite ONLY the audit-sourced fields. Preserve anything else the
        # user (or a prior authoring pass) has populated.
        if handle in layer_reasons:
            entry["motivation"]["why_this_layer"] = layer_reasons[handle]
        if handle in broad_use:
            bu = broad_use[handle]
            for field in (
                "intended",
                "future",
                "broad_contexts",
                "every_context_needs",
                "varies",
                "extensions",
            ):
                if field in bu:
                    entry["usage"][field] = bu[field]
            if bu.get("notes"):
                entry["usage"]["notes"] = bu["notes"]

        out[handle] = entry

    SIDECAR.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    covered_layer = sum(1 for h in handles if layer_reasons.get(h))
    covered_broad = sum(1 for h in handles if h in broad_use)
    print(f"✓ Wrote {SIDECAR.relative_to(REPO_ROOT)}")
    print(f"  Handles: {len(handles)}")
    print(f"  Layer reasoning populated:      {covered_layer}")
    print(f"  Broad-use usage block populated: {covered_broad}")
    print("  Motivation/tensions/tradeoffs/critique: empty, to be filled iteratively.")
    return out


if __name__ == "__main__":
    migrate()
