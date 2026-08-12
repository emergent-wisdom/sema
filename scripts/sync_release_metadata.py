#!/usr/bin/env python3
"""Keep release-surface files in sync with pyproject.toml and the active DB.

Sources of truth:
  - Version:       pyproject.toml  (the `version = "X.Y.Z"` line under [project])
  - Pattern count: data/taxonomy.db (patterns in the active vocabulary)

Targets kept in sync:
  - src/sema/__init__.py          — `__version__`
  - src/sema/mcp/__init__.py      — `__version__`
  - .claude-plugin/plugin.json   — `version`
  - server.json                  — `version`, `packages[].version`, and the
                                   pattern-count number embedded in the
                                   `description` string
  - uv.lock                      — editable `semahash` package version

Usage:
  scripts/sync_release_metadata.py          # fix drift in place
  scripts/sync_release_metadata.py --check  # exit 1 if anything is out of sync

The `--check` form is the CI/pre-commit gate; the no-arg form is the fixer
you run locally. Both are idempotent — run twice, second run is a no-op.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = REPO_ROOT / "pyproject.toml"
PLUGIN_JSON = REPO_ROOT / ".claude-plugin" / "plugin.json"
SERVER_JSON = REPO_ROOT / "server.json"
PYTHON_INIT = REPO_ROOT / "src" / "sema" / "__init__.py"
MCP_INIT = REPO_ROOT / "src" / "sema" / "mcp" / "__init__.py"
UV_LOCK = REPO_ROOT / "uv.lock"
TAXONOMY_DB = REPO_ROOT / "data" / "taxonomy.db"


def read_pyproject_version() -> str:
    text = PYPROJECT.read_text()
    # Match `version = "X.Y.Z"` at the start of a line (inside [project]).
    m = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not m:
        sys.exit(f"sync_release_metadata: could not find version in {PYPROJECT}")
    return m.group(1)


def read_pattern_count(db_path: Path) -> int:
    if not db_path.is_file():
        sys.exit(f"sync_release_metadata: {db_path} missing — can't read pattern count")
    with sqlite3.connect(db_path) as con:
        (n,) = con.execute("SELECT COUNT(*) FROM nodes WHERE node_type='PATTERN'").fetchone()
    return int(n)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def _dump_json(path: Path, data: dict) -> None:
    # 2-space indent + trailing newline matches what the repo's existing
    # tooling produces. Don't reorder keys — readers expect the file to
    # stay stable.
    path.write_text(json.dumps(data, indent=2) + "\n")


def sync_python_init(path: Path, version: str) -> bool:
    text = path.read_text()
    updated, count = re.subn(
        r'^__version__\s*=\s*"[^"]+"',
        f'__version__ = "{version}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        sys.exit(f"sync_release_metadata: could not find __version__ in {path}")
    if updated == text:
        return False
    path.write_text(updated)
    return True


def sync_uv_lock(version: str) -> bool:
    text = UV_LOCK.read_text()
    updated, count = re.subn(
        r'(\[\[package\]\]\nname = "semahash"\nversion = ")[^"]+("\n)',
        rf"\g<1>{version}\g<2>",
        text,
        count=1,
    )
    if count != 1:
        sys.exit(f"sync_release_metadata: could not find editable semahash entry in {UV_LOCK}")
    if updated == text:
        return False
    UV_LOCK.write_text(updated)
    return True


def sync_plugin_json(version: str) -> bool:
    data = _load_json(PLUGIN_JSON)
    if data.get("version") == version:
        return False
    data["version"] = version
    _dump_json(PLUGIN_JSON, data)
    return True


def sync_server_json(version: str, pattern_count: int) -> bool:
    data = _load_json(SERVER_JSON)
    changed = False

    if data.get("version") != version:
        data["version"] = version
        changed = True

    for pkg in data.get("packages", []):
        if pkg.get("version") != version:
            pkg["version"] = version
            changed = True

    # Description carries the live pattern count via the phrase
    # "over <N> cognitive patterns". If that phrasing changes, update the
    # regex too — the test is whether the sentinel still matches after an
    # edit.
    desc = data.get("description", "")
    new_desc, subs = re.subn(
        r"over\s+\d+\s+cognitive\s+patterns",
        f"over {pattern_count} cognitive patterns",
        desc,
    )
    if subs == 0 and "cognitive patterns" in desc:
        # Phrase exists but didn't match the regex — phrasing drifted. Fail
        # loudly rather than silently leaving a stale count in place.
        sys.exit(
            "sync_release_metadata: server.json description mentions "
            "'cognitive patterns' but doesn't match the expected "
            "'over <N> cognitive patterns' phrasing. Edit the regex in "
            "sync_release_metadata.py or the description to realign."
        )
    if new_desc != desc:
        data["description"] = new_desc
        changed = True

    if changed:
        _dump_json(SERVER_JSON, data)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if any target file is out of sync (CI / pre-commit mode)",
    )
    args = parser.parse_args()

    version = read_pyproject_version()
    pattern_count = read_pattern_count(TAXONOMY_DB)

    changes: list[str] = []
    if sync_python_init(PYTHON_INIT, version):
        changes.append(f"  src/sema/__init__.py → version={version}")
    if sync_python_init(MCP_INIT, version):
        changes.append(f"  src/sema/mcp/__init__.py → version={version}")
    if sync_plugin_json(version):
        changes.append(f"  .claude-plugin/plugin.json → version={version}")
    if sync_server_json(version, pattern_count):
        changes.append(f"  server.json → version={version}, pattern_count={pattern_count}")
    if sync_uv_lock(version):
        changes.append(f"  uv.lock → version={version}")

    if args.check and changes:
        print("sync_release_metadata: drift detected", file=sys.stderr)
        for line in changes:
            print(line, file=sys.stderr)
        print(
            "\nRun `python3 scripts/sync_release_metadata.py` to fix, then re-stage.",
            file=sys.stderr,
        )
        return 1

    if changes:
        print(f"Synced to version={version}, pattern_count={pattern_count}:")
        for line in changes:
            print(line)
    else:
        print(f"Already in sync (version={version}, pattern_count={pattern_count}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
