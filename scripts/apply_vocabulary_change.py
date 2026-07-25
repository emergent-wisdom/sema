#!/usr/bin/env python3
"""Apply staged vocabulary edits in the one order that works.

    apply_vocabulary_change.py            # apply data/staging, export, rehash, export
    apply_vocabulary_change.py --check    # validate only; touch nothing
    apply_vocabulary_change.py --keep-staging

The order is load-bearing and was not obvious. `sema apply` writes the database;
`export_sema.py` writes data/vocabulary/ from the database; `rebuild_vocabulary.py`
reads data/vocabulary/ and recomputes every hash so that dependents of an edited
pattern pick up its new hash. Running the rebuild before the export therefore
rehashes the *previous* state — which once let a cycle survive a fix that had
already been applied, and cost a tranche of work to recover.

So: apply, export, rebuild, export. This script is that sequence, and it stops at
the first failure rather than carrying a broken state into the next step.

Verification is deliberately left out. Run these afterwards and read the diff:

    python scripts/verify_vocabulary_change.py --refresh
    python scripts/verify_vocabulary_change.py
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STAGING = REPO_ROOT / "data" / "staging"
VENV_PYTHON = REPO_ROOT / ".venv" / "bin" / "python"


def python_executable() -> str:
    """Prefer the project venv: a global sema install resolves a different database."""
    if VENV_PYTHON.exists():
        return str(VENV_PYTHON)
    return sys.executable


def step(label: str, cmd: list[str], allow_drift: bool = False) -> str:
    print(f"\n── {label}")
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    output = proc.stdout + proc.stderr
    drift_only = allow_drift and "HASH DRIFT" in proc.stdout
    if drift_only:
        for line in output.splitlines():
            if line.strip():
                print(f"   {line}")
        return output
    if proc.returncode != 0 or "❌" in proc.stdout:
        print(output.rstrip())
        print(f"\nFAILED at: {label}")
        print("Nothing further was run, so the state is whatever that step left.")
        sys.exit(1)
    for line in output.splitlines():
        if line.strip():
            print(f"   {line}")
    return output


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--staging", default=str(STAGING), help="directory of staged patterns")
    ap.add_argument("--check", action="store_true", help="validate only, change nothing")
    ap.add_argument(
        "--keep-staging", action="store_true", help="do not delete staged files after applying"
    )
    args = ap.parse_args()

    staging = Path(args.staging)
    staged = sorted(staging.glob("*.json")) if staging.is_dir() else []
    if not staged:
        print(f"No staged patterns in {staging}. Nothing to do.")
        return 0

    py = python_executable()
    print(f"{len(staged)} staged: {', '.join(p.stem for p in staged)}")

    sema = [py, "-m", "sema.cli.main"]

    # Validation includes the acyclic check across the batch and the committed
    # corpus, so a mutual reference is refused here rather than at rebuild time.
    step("validate", [*sema, "apply", "--add", str(staging), "--check"])

    if args.check:
        print("\n--check: validated only, nothing changed.")
        return 0

    step("apply to database", [*sema, "apply", "--add", str(staging)])
    step("export database to data/vocabulary", [py, "scripts/export/export_sema.py"])

    # Rehash so dependents of an edited pattern carry its new hash. Reads the
    # exports, which is why it must come after the export above.
    #
    # A rebuild that reports HASH DRIFT has still done its job: the stored hashes
    # were stale — usually because a dependency changed and its dependents were
    # never rehashed — and the rebuild corrected them in place. It exits non-zero so
    # the finding is visible, and under --replace it keeps the corrected database,
    # so the export below writes the corrected hashes rather than the stale ones.
    step("rehash dependents", [py, "scripts/rebuild_vocabulary.py", "--replace"], allow_drift=True)
    step("re-export after rehash", [py, "scripts/export/export_sema.py"])

    if not args.keep_staging:
        for path in staged:
            os.remove(path)
        print(f"\nCleared {len(staged)} file(s) from {staging}")

    print("\nApplied. Now verify and read the generated diff:")
    print("   python scripts/verify_vocabulary_change.py --refresh")
    print("   python scripts/verify_vocabulary_change.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
