"""Run every vocabulary audit and write a consolidated report.

Each audit is launched through its package module so subprocesses resolve the
same editable ``sema`` installation as this runner. This avoids manipulating
``PYTHONPATH`` and makes a missing development install fail explicitly.

The checkout is ``SEMA_REPO_ROOT`` when set, as ``scripts/verify_vocabulary_change.py``
does, and otherwise the checkout this module sits in. Run from an installed,
non-editable package, that second root is not a checkout, so ``main`` refuses
to run rather than write the report into the installation.
"""

import os
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    override = os.environ.get("SEMA_REPO_ROOT")
    return Path(override).resolve() if override else Path(__file__).resolve().parents[3]


REPO_ROOT = _repo_root()
OUTPUT = REPO_ROOT / "docs" / "information" / "audit.md"


def checkout_problem(root: Path) -> str | None:
    """Say why ``root`` is not a Sema checkout the audit can read and write, or None."""
    missing = [
        part for part in ("data/vocabulary", "data/taxonomy.db") if not (root / part).exists()
    ]
    if not missing:
        return None
    return (
        f"{root} is not a Sema checkout (missing {', '.join(missing)}). Run the audit from a "
        "checkout with an editable install or PYTHONPATH=src, or set SEMA_REPO_ROOT."
    )


# Order matters: blocking/structural first, heuristic/advisory after.
AUDITS = [
    ("sema.audit.hash_validity", "Hash validity (stored sema_id matches content)"),
    ("sema.audit.missing_or_short", "Missing or short fields"),
    ("sema.audit.graph", "Graph structure (orphans, cycles, metadata, duplicates)"),
    ("sema.audit.rigor", "Contract-field coverage (invariants / pre / post)"),
    ("sema.audit.missing_links", "Potential missing dependency links"),
    ("sema.audit.unlinked_mentions", "Unlinked handle mentions"),
    ("sema.audit.similarity", "Semantic similarity between patterns"),
    ("sema.audit.scenarios", "Scenario coverage"),
]


def run_audit(module: str) -> tuple[int, str]:
    """Run one audit module and return its exit code and combined output."""
    env = os.environ.copy()
    env["SEMA_DB_PATH"] = str(REPO_ROOT / "data" / "taxonomy.db")
    proc = subprocess.run(
        [sys.executable, "-m", module],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )
    combined = proc.stdout + (proc.stderr if proc.stderr else "")
    return proc.returncode, combined.strip()


def main() -> None:
    """Run all audits and write ``docs/information/audit.md``."""
    problem = checkout_problem(REPO_ROOT)
    if problem:
        raise SystemExit(f"sema.audit: {problem}")
    sections = ["# Vocabulary Audit Report\n"]
    sections.append(
        "All audits below are **advisory**. Heuristic audits generate false positives; "
        "use this report as a starting point for manual review, not as a correctness gate.\n"
    )

    for module, title in AUDITS:
        rc, out = run_audit(module)
        status = "ok" if rc == 0 else f"exit {rc}"
        sections.append(f"## {title}\n\nSource: `{module}` ({status})\n")
        if out:
            sections.append("```text\n" + out + "\n```\n")
        else:
            sections.append("_No output._\n")

    content = "\n".join(sections)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content)
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}")
