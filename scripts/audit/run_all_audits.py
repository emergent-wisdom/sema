#!/usr/bin/env python3
"""Compatibility entry point for the importable Sema audit runner.

Usage:
    python scripts/audit/run_all_audits.py
"""

import sys

try:
    from sema.audit.runner import main
except ModuleNotFoundError as exc:
    if exc.name != "sema":
        raise
    print(
        "Sema is not installed. Run `python -m pip install -e .` from the repository root, "
        "then retry the audit.",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
