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
    4. Report whether any JSON files changed (git diff)
    5. Restore the original DB (or keep the new one with --replace)

This is the canonical way to prove the hash pipeline is deterministic:
if the JSON files don't change, every hash is stable.
"""

import argparse
import os
import shutil
import subprocess
import sys
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(REPO_ROOT, "data", "taxonomy.db")
VOCAB_DIR = os.path.join(REPO_ROOT, "data", "vocabulary")


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

    json_count = len([f for f in os.listdir(VOCAB_DIR) if f.endswith(".json")])
    print(f"Rebuilding {json_count} patterns from {VOCAB_DIR}")

    # 1. Back up
    backup_path = DB_PATH + ".rebuild_bak"
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backed up DB to {backup_path}")

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
        rc, out, err = run([sys.executable, "-m", "sema.cli.main", "init", DB_PATH])
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

        if args.check:
            print("\n--check mode: no JSON files were modified")
            return

        # 4. Check git diff on JSON files
        rc, diff_out, _ = run(["git", "diff", "--stat", "data/vocabulary/"])
        if diff_out.strip():
            print(f"\n❌ HASH DRIFT DETECTED — {diff_out.count('|')} files changed:")
            print(diff_out)
            rc2, diff_detail, _ = run(["git", "diff", "--name-only", "data/vocabulary/"])
            for line in diff_detail.strip().split("\n")[:10]:
                if line:
                    print(f"  {line}")
            sys.exit(1)
        else:
            print("\n✅ All hashes stable — zero diff on vocabulary JSON files")

    finally:
        # 5. Restore DB
        if args.replace:
            os.remove(backup_path)
            print("Kept rebuilt DB (--replace)")
        else:
            shutil.move(backup_path, DB_PATH)
            print("Restored original DB")

        # Restore embedding cache
        if embed_cache_backup and os.path.exists(embed_cache_backup):
            shutil.move(embed_cache_backup, embed_cache_path)
            print("Restored embedding cache")


if __name__ == "__main__":
    main()
