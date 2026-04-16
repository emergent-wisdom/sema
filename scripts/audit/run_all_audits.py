#!/usr/bin/env python3
"""Run every audit script and write a consolidated report to docs/information/audit.md.

Runs each audit as a subprocess, captures stdout+stderr, and embeds the output
under a heading per audit. Intended to be committed to git so the history
of audit results is visible alongside vocabulary changes.

Usage:
    python scripts/audit/run_all_audits.py
"""

import datetime
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AUDIT_DIR = REPO_ROOT / "scripts" / "audit"
OUTPUT = REPO_ROOT / "docs" / "information" / "audit.md"

# Order matters: blocking/structural first, heuristic/advisory after.
AUDITS = [
    ("audit_hash_validity.py", "Hash validity (stored sema_id matches content)"),
    ("audit_missing_or_short.py", "Missing or short fields"),
    ("audit_graph.py", "Graph structure (orphans, duplicates, naked patterns)"),
    ("audit_rigor.py", "Rigor coverage (invariants / pre / post)"),
    ("audit_missing_links.py", "Potential missing dependency links"),
    ("audit_unlinked_mentions.py", "Unlinked handle mentions"),
    ("audit_similarity.py", "Semantic similarity between patterns"),
    ("audit_scenarios.py", "Scenario coverage"),
]


def run_audit(script: str) -> tuple[int, str]:
    """Run one audit script and return (exit_code, combined_output)."""
    env = os.environ.copy()
    env["SEMA_DB_PATH"] = str(REPO_ROOT / "data" / "taxonomy.db")
    # Prefer local source over any globally-installed sema. Keeps audits
    # in sync with the repo state regardless of the developer's install.
    src_path = str(REPO_ROOT / "src")
    env["PYTHONPATH"] = (
        src_path + os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else src_path
    )
    proc = subprocess.run(
        [sys.executable, str(AUDIT_DIR / script)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )
    combined = proc.stdout + (proc.stderr if proc.stderr else "")
    return proc.returncode, combined.strip()


def main():
    date = datetime.date.today().isoformat()
    sections = [f"# Vocabulary Audit Report\n\nGenerated: {date}\n"]
    sections.append(
        "All audits below are **advisory**. Heuristic audits generate false positives; "
        "use this report as a starting point for manual review, not as a correctness gate.\n"
    )

    for script, title in AUDITS:
        rc, out = run_audit(script)
        status = "ok" if rc == 0 else f"exit {rc}"
        sections.append(f"## {title}\n\nSource: `scripts/audit/{script}` ({status})\n")
        if out:
            sections.append("```text\n" + out + "\n```\n")
        else:
            sections.append("_No output._\n")

    content = "\n".join(sections)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content)
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
