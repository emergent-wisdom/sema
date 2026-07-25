#!/usr/bin/env python3
"""Rebuild the vocabulary DB from JSON source files and verify hash stability.

Usage:
    python scripts/rebuild_vocabulary.py              # rebuild + verify (no git diff = pass)
    python scripts/rebuild_vocabulary.py --check      # dry-run: only report if hashes would change
    python scripts/rebuild_vocabulary.py --verbose     # print every pattern's ref
    python scripts/rebuild_vocabulary.py --cold        # also nuke embedding cache (full cold rebuild)

What it does:
    1. Back up the current taxonomy.db
    2. Create a fresh empty DB
    3. Feed all data/vocabulary/*.json through sema apply (topo-sorted, one-by-one via mint_pattern)
    4. Compare the rebuilt JSON files with a pre-rebuild byte snapshot
    5. Restore the original DB (or keep the new one with --replace)

This is the canonical way to prove the hash pipeline is deterministic:
if the JSON files don't change, every hash is stable.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(REPO_ROOT, "data", "taxonomy.db")
VOCAB_DIR = os.path.join(REPO_ROOT, "data", "vocabulary")


def snapshot_vocabulary(vocab_dir=VOCAB_DIR) -> dict[str, bytes]:
    """Capture root vocabulary JSON bytes for deterministic rebuild checks."""
    return {path.name: path.read_bytes() for path in sorted(Path(vocab_dir).glob("*.json"))}


def changed_vocabulary_files(before: dict[str, bytes], vocab_dir=VOCAB_DIR) -> list[str]:
    """Return added, removed, or byte-changed vocabulary files."""
    after = snapshot_vocabulary(vocab_dir)
    return sorted(
        name for name in before.keys() | after.keys() if before.get(name) != after.get(name)
    )


def backup_path_for(db_path: str, stamp: str | None = None) -> str:
    """Timestamped backup name.

    A fixed name meant a second rebuild overwrote the backup taken by the first,
    so running the verify script after a failed rebuild destroyed the only copy of
    the good database.
    """
    return f"{db_path}.rebuild_bak.{stamp or time.strftime('%Y%m%d-%H%M%S')}"


def restore_plan(
    *, replace: bool, rebuild_succeeded: bool, check_only_run: bool, db_valid: bool = False
) -> tuple[bool, str]:
    """Decide whether to keep the rebuilt DB, and what to say about it.

    --replace means "keep the rebuilt DB". A failed rebuild produced no rebuilt DB
    to keep — only a fresh empty one, or a partially applied one — and a --check
    run applies nothing at all. Honouring --replace in either case discarded the
    vocabulary outright: the kept database was empty, the backup was deleted in
    the same branch, and the next export wrote zero patterns over
    data/vocabulary/.
    """
    if replace and rebuild_succeeded and not check_only_run:
        return True, "Kept rebuilt DB (--replace)"
    # Hash drift is the one failure where the rebuilt database is still the better
    # copy: the apply completed, and the corrected hashes are the right ones.
    # Restoring here discards the correction, and a caller that re-exports
    # afterwards writes the stale hashes back — which loops forever.
    if replace and db_valid and not check_only_run:
        return True, "Kept rebuilt DB (--replace) — hashes were corrected, not lost"
    if not replace:
        return False, "Restored original DB"
    if check_only_run:
        return False, "Restored original DB — --check applies nothing, so there was nothing to keep"
    return False, "Restored original DB — rebuild failed, so there was nothing to keep"


def run(cmd, **kwargs):
    """Run a command, return (returncode, stdout, stderr).

    Forces SEMA_DB_PATH so the sema CLI subprocess targets the repo DB
    regardless of ~/.config/sema/active_db on the host.
    """
    env = kwargs.pop("env", None) or os.environ.copy()
    env["SEMA_DB_PATH"] = DB_PATH
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT, env=env, **kwargs)
    return result.returncode, result.stdout, result.stderr


def get_embedding_cache_path():
    """Find the embedding cache DB path (same logic as EmbeddingService)."""
    try:
        from platformdirs import user_cache_dir

        return os.path.join(user_cache_dir("sema"), "embedding_cache.db")
    except ImportError:
        return None


def isolated_registry_environment(home: str) -> dict[str, str]:
    """Return an environment that keeps ``sema init`` out of user config."""
    env = os.environ.copy()
    env["HOME"] = home
    return env


def main():
    parser = argparse.ArgumentParser(description="Rebuild vocabulary DB and verify hash stability.")
    parser.add_argument("--check", action="store_true", help="Dry-run: report without modifying DB")
    parser.add_argument(
        "--replace", action="store_true", help="Keep the rebuilt DB instead of restoring"
    )
    parser.add_argument("--verbose", action="store_true", help="Print each pattern ref")
    parser.add_argument(
        "--cold",
        action="store_true",
        help="Nuke embedding cache too (full cold rebuild, much slower)",
    )
    args = parser.parse_args()

    if not os.path.exists(DB_PATH):
        print(f"ERROR: Database not found: {DB_PATH}")
        sys.exit(1)

    if not os.path.isdir(VOCAB_DIR):
        print(f"ERROR: Vocabulary dir not found: {VOCAB_DIR}")
        sys.exit(1)

    vocabulary_before = snapshot_vocabulary()
    json_count = len(vocabulary_before)
    print(f"Rebuilding {json_count} patterns from {VOCAB_DIR}")

    # 1. Back up
    backup_path = backup_path_for(DB_PATH)
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backed up DB to {backup_path}")
    rebuild_succeeded = False
    check_only_run = False
    db_valid = False

    # Cold mode: nuke embedding cache
    embed_cache_path = get_embedding_cache_path()
    embed_cache_backup = None
    if args.cold and embed_cache_path and os.path.exists(embed_cache_path):
        embed_cache_backup = embed_cache_path + ".rebuild_bak"
        shutil.copy2(embed_cache_path, embed_cache_backup)
        os.remove(embed_cache_path)
        print(f"Nuked embedding cache: {embed_cache_path}")
    elif args.cold:
        print("Embedding cache not found (already cold)")

    try:
        # 2. Fresh DB
        os.remove(DB_PATH)
        with tempfile.TemporaryDirectory(prefix="sema-rebuild-home-") as isolated_home:
            rc, out, err = run(
                [sys.executable, "-m", "sema.cli.main", "init", DB_PATH],
                env=isolated_registry_environment(isolated_home),
            )
        if rc != 0:
            print(f"ERROR: sema init failed:\n{err}")
            sys.exit(1)
        print("Created fresh DB")

        # 3. Feed all vocab through apply
        cmd = [sys.executable, "-m", "sema.cli.main", "apply", "--add", VOCAB_DIR]
        if args.check:
            cmd.append("--check")

        t0 = time.time()
        rc, out, err = run(cmd)
        elapsed = time.time() - t0

        if args.verbose:
            print(out)

        if rc != 0 or "Failed" in out or "❌" in out:
            print(f"ERROR: sema apply failed:\n{out}\n{err}")
            sys.exit(1)

        # Count added
        added = out.count("✓ Added")
        print(f"Added {added}/{json_count} patterns in {elapsed:.1f}s")
        # The rebuild produced a complete database from the JSON. Hash drift below
        # is a finding about the *inputs*, not a failure of this rebuild, so the
        # database it just built is valid and is the better copy.
        db_valid = True

        if args.check:
            print("\n--check mode: no JSON files were modified")
            # A check run applies with --check, so the fresh DB holds nothing.
            # Never keep it, whatever --replace says.
            check_only_run = True
            return

        # 4. Compare against the exact inputs to this rebuild. Using `git
        # diff` here produces false failures whenever an author is verifying
        # an intentional, not-yet-committed vocabulary edit.
        changed_files = changed_vocabulary_files(vocabulary_before)
        if changed_files:
            print(f"\n❌ HASH DRIFT DETECTED — {len(changed_files)} files changed:")
            for name in changed_files[:10]:
                print(f"  data/vocabulary/{name}")
            print(
                "\nThe rebuilt hashes are the correct ones — the stored ones were stale, "
                "usually\nbecause a dependency changed and its dependents were never rehashed. "
                "The JSON\nfiles above have been corrected in place."
            )
            sys.exit(1)
        else:
            print("\n✅ All hashes stable — zero diff on vocabulary JSON files")

        rebuild_succeeded = True

    finally:
        # 5. Keep the rebuilt DB or restore the backup — see restore_plan.
        keep, message = restore_plan(
            replace=args.replace,
            rebuild_succeeded=rebuild_succeeded,
            check_only_run=check_only_run,
            db_valid=db_valid,
        )
        if keep:
            os.remove(backup_path)
        else:
            shutil.move(backup_path, DB_PATH)
        print(message)

        # Restore embedding cache
        if embed_cache_backup and os.path.exists(embed_cache_backup):
            shutil.move(embed_cache_backup, embed_cache_path)
            print("Restored embedding cache")


if __name__ == "__main__":
    main()
