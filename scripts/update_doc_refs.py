#!/usr/bin/env python3
"""Rewrite stale `Handle#stub` references in docs to current pattern stubs.

A hash drift in the vocabulary (cascade or content update) changes
`sema_ref` values. Any doc that cited those refs becomes stale. This
script walks a scoped set of docs, finds every `Handle#stub` mention,
looks up the current stub from data/vocabulary/*.json, and rewrites
any mismatch.

Scope: README.md, install.md, docs/**/*.md, skills/**/*.md.
Out of scope: paper/, experiments/, tests/, source code — they may
cite specific historical refs or use intentionally-invalid stubs.
The generated vocabulary manual's "Supersedes (prior versions)" blocks
are also preserved because those refs are deliberately historical.

Usage:
    python scripts/update_doc_refs.py          # rewrite in place
    python scripts/update_doc_refs.py --check  # exit 1 if stale

Exit code:
    0 — no stale refs (or all rewritten)
    1 — with --check, stale refs found; run without --check to fix
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_DIR = REPO_ROOT / "data" / "vocabulary"

SCOPED_PATHS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "install.md",
    REPO_ROOT / "docs",
    REPO_ROOT / "skills",
]

# Specific source files with user-facing refs in docstrings/comments.
# Excluded: tests/ (fixtures use intentional invalid stubs like #dead),
# experiments/ (historical run data), scripts/viz/ (dynamic computation).
SCOPED_SOURCE_FILES = [
    REPO_ROOT / "src" / "sema" / "core" / "stdlib.py",
    REPO_ROOT / "src" / "sema" / "mcp" / "server.py",
]

HASH_REF = re.compile(r"(?P<handle>[A-Z][A-Za-z0-9]+)#(?P<stub>[a-f0-9]{4,8})\b")
GENERATED_MANUAL = REPO_ROOT / "docs" / "manuals" / "vocabulary-design.md"
HISTORICAL_MANUAL_HEADINGS = {"**Supersedes (prior versions).**"}


def load_current_stubs() -> dict[str, str]:
    stubs = {}
    for f in sorted(VOCAB_DIR.glob("*.json")):
        d = json.loads(f.read_text())
        h = d.get("handle")
        stub = d.get("sema_stub", "")
        if h and stub:
            stubs[h] = stub
    return stubs


def iter_doc_files():
    for path in SCOPED_PATHS:
        if path.is_file() and path.suffix == ".md":
            yield path
        elif path.is_dir():
            yield from path.rglob("*.md")
    for path in SCOPED_SOURCE_FILES:
        if path.is_file():
            yield path


def rewrite(text: str, current: dict[str, str]) -> tuple[str, list[tuple[str, str, str]]]:
    """Return (new_text, list of (handle, old_stub, new_stub))."""
    changes = []

    def repl(m):
        handle = m.group("handle")
        old_stub = m.group("stub")
        if handle not in current:
            return m.group(0)
        new_stub = current[handle]
        if old_stub[:4] == new_stub[:4]:
            return m.group(0)
        changes.append((handle, old_stub, new_stub))
        return f"{handle}#{new_stub}"

    return HASH_REF.sub(repl, text), changes


def rewrite_doc(
    path: Path, text: str, current: dict[str, str]
) -> tuple[str, list[tuple[str, str, str]]]:
    """Rewrite current refs while preserving historical refs in the generated manual."""
    if path != GENERATED_MANUAL:
        return rewrite(text, current)

    chunks = []
    all_changes = []
    in_historical_block = False

    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped in HISTORICAL_MANUAL_HEADINGS:
            in_historical_block = True
            chunks.append(line)
            continue
        if in_historical_block:
            chunks.append(line)
            if not stripped:
                in_historical_block = False
            continue

        new_line, changes = rewrite(line, current)
        chunks.append(new_line)
        all_changes.extend(changes)

    return "".join(chunks), all_changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if stale refs exist")
    args = parser.parse_args()

    current = load_current_stubs()
    total_changes = 0
    files_changed = []

    for path in iter_doc_files():
        text = path.read_text()
        new_text, changes = rewrite_doc(path, text, current)
        if changes:
            total_changes += len(changes)
            files_changed.append((path.relative_to(REPO_ROOT), changes))
            if not args.check:
                path.write_text(new_text)

    if not total_changes:
        print("All doc refs up-to-date.")
        return 0

    verb = "would update" if args.check else "updated"
    print(f"{verb} {total_changes} stale refs across {len(files_changed)} files:\n")
    for rel, changes in files_changed:
        print(f"  {rel}")
        for handle, old, new in changes:
            print(f"    {handle}#{old} → {handle}#{new}")

    if args.check:
        print("\n::error::Doc refs are stale. Run 'python scripts/update_doc_refs.py' and commit.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
