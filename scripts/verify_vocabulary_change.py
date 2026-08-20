#!/usr/bin/env python3
"""Run the complete post-apply verification workflow for vocabulary changes.

Check mode is non-destructive. Generator outputs and vocabulary JSON are
snapshotted before commands run and restored if a check exposes drift.

Usage:
    python scripts/verify_vocabulary_change.py
    python scripts/verify_vocabulary_change.py --refresh
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
STAGING_DIR = REPO_ROOT / "data" / "staging"
VOCAB_DIR = REPO_ROOT / "data" / "vocabulary"


class Step(NamedTuple):
    name: str
    command: tuple[str, ...]
    outputs: tuple[Path, ...] = ()


GENERATED_STEPS = (
    Step(
        "design manual",
        (sys.executable, "scripts/generate_design_manual.py"),
        (REPO_ROOT / "docs" / "manuals" / "vocabulary-design.md",),
    ),
    Step(
        "paper pattern-card appendix",
        (sys.executable, "scripts/generate_pattern_cards.py"),
        (REPO_ROOT / "paper" / "generated_pattern_cards.tex",),
    ),
    Step(
        "vocabulary information",
        (sys.executable, "scripts/vocabulary_merkle_root.py"),
        (REPO_ROOT / "docs" / "information" / "vocabulary_information.md",),
    ),
    Step(
        "vocabulary audit",
        (sys.executable, "-m", "sema.audit"),
        (REPO_ROOT / "docs" / "information" / "audit.md",),
    ),
)

DOC_REFS_CHECK = Step(
    "documentation hash references",
    (sys.executable, "scripts/update_doc_refs.py", "--check"),
)
DOC_REFS_REFRESH = Step(
    "documentation hash references",
    (sys.executable, "scripts/update_doc_refs.py"),
)
HASH_VALIDITY = Step(
    "exported hash validity",
    (sys.executable, "-m", "sema.audit.hash_validity"),
)
DETERMINISTIC_REBUILD = Step(
    "deterministic vocabulary rebuild",
    (sys.executable, "scripts/rebuild_vocabulary.py"),
)
DATABASE_EXPORT = Step(
    "database/export parity",
    (sys.executable, "scripts/export/export_sema.py"),
)

Runner = Callable[[Step], int]
Snapshot = dict[Path, bytes | None]


def workflow_environment() -> dict[str, str]:
    env = os.environ.copy()
    env["SEMA_DB_PATH"] = str(REPO_ROOT / "data" / "taxonomy.db")
    env.setdefault("SEMA_CACHE_DIR", str(Path(tempfile.gettempdir()) / "sema-cache"))
    return env


def run_step(step: Step) -> int:
    print(f"\n==> {step.name}", flush=True)
    result = subprocess.run(
        step.command,
        cwd=REPO_ROOT,
        env=workflow_environment(),
        check=False,
    )
    return result.returncode


def snapshot_files(paths: Iterable[Path]) -> Snapshot:
    return {path: path.read_bytes() if path.exists() else None for path in paths}


def changed_files(before: Snapshot) -> list[Path]:
    changed = []
    for path, old_content in before.items():
        new_content = path.read_bytes() if path.exists() else None
        if old_content != new_content:
            changed.append(path)
    return changed


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def restore_files(before: Snapshot) -> None:
    for path, content in before.items():
        if content is None:
            if path.exists():
                path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def snapshot_vocabulary() -> Snapshot:
    return snapshot_files(sorted(VOCAB_DIR.rglob("*.json")))


def changed_vocabulary_files(before: Snapshot) -> list[Path]:
    after = snapshot_vocabulary()
    return sorted(
        path for path in before.keys() | after.keys() if before.get(path) != after.get(path)
    )


def restore_vocabulary(before: Snapshot) -> None:
    known_paths = set(before)
    for path in VOCAB_DIR.rglob("*.json"):
        if path not in known_paths:
            path.unlink()
    restore_files(before)


def verify_generated_step(step: Step, runner: Runner = run_step) -> str | None:
    before = snapshot_files(step.outputs)
    try:
        return_code = runner(step)
        changed = changed_files(before)
    finally:
        restore_files(before)

    if return_code != 0:
        return f"{step.name} generator exited with status {return_code}"
    if changed:
        paths = ", ".join(display_path(path) for path in changed)
        return f"{step.name} is stale: {paths}"
    return None


def refresh_generated_step(step: Step, runner: Runner = run_step) -> str | None:
    before = snapshot_files(step.outputs)
    return_code = runner(step)
    if return_code != 0:
        return f"{step.name} generator exited with status {return_code}"

    changed = changed_files(before)
    if changed:
        paths = ", ".join(display_path(path) for path in changed)
        print(f"    refreshed: {paths}")
    return None


def verify_vocabulary_step(step: Step, runner: Runner = run_step) -> str | None:
    before = snapshot_vocabulary()
    try:
        return_code = runner(step)
        changed = changed_vocabulary_files(before)
    finally:
        if changed_vocabulary_files(before):
            restore_vocabulary(before)

    if return_code != 0:
        return f"{step.name} exited with status {return_code}"
    if changed:
        paths = ", ".join(display_path(path) for path in changed[:10])
        return f"{step.name} changed exported JSON: {paths}"
    return None


def verify_rebuild(runner: Runner = run_step) -> str | None:
    return verify_vocabulary_step(DETERMINISTIC_REBUILD, runner)


def verify_database_export(runner: Runner = run_step) -> str | None:
    return verify_vocabulary_step(DATABASE_EXPORT, runner)


def staged_patterns() -> list[Path]:
    return sorted(STAGING_DIR.glob("*.json"))


def run_workflow(refresh: bool, runner: Runner = run_step) -> list[str]:
    failures = []

    export_failure = verify_database_export(runner)
    if export_failure:
        failures.append(export_failure)

    for step in GENERATED_STEPS:
        failure = (
            refresh_generated_step(step, runner) if refresh else verify_generated_step(step, runner)
        )
        if failure:
            failures.append(failure)

    doc_refs = DOC_REFS_REFRESH if refresh else DOC_REFS_CHECK
    if runner(doc_refs) != 0:
        action = "refresh" if refresh else "check"
        failures.append(f"documentation hash reference {action} failed")

    if runner(HASH_VALIDITY) != 0:
        failures.append("exported hash validity failed")

    rebuild_failure = verify_rebuild(runner)
    if rebuild_failure:
        failures.append(rebuild_failure)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Keep regenerated manual, audit, root, and documentation references",
    )
    args = parser.parse_args()

    staged = staged_patterns()
    if staged:
        print("ERROR: staged pattern JSON remains after the apply workflow:")
        for path in staged:
            print(f"  {path.relative_to(REPO_ROOT)}")
        print("Apply or remove staging files before final verification.")
        return 1

    mode = "refresh" if args.refresh else "check"
    print(f"Running vocabulary workflow in {mode} mode...")
    failures = run_workflow(args.refresh)

    if failures:
        print("\nVocabulary workflow failed:")
        for failure in failures:
            print(f"  - {failure}")
        if not args.refresh:
            print("\nRun with --refresh, review the generated changes, then check again.")
        return 1

    print("\nVocabulary workflow passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
