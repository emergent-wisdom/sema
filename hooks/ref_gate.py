#!/usr/bin/env python3
"""Sema ref gate — Claude Code hook that blocks stale sema refs.

Reads the hook event JSON from stdin, scans the raw payload for
content-addressed refs (Handle#stub), and verdicts each against the
active sema registry:

  KNOWN   handle exists, stub matches      -> pass
  STALE   handle exists, stub differs      -> BLOCK (exit 2)
  UNKNOWN handle not in registry           -> pass with a context note
          (not blocked: the regex can match non-sema text like "PR#12ab")

Exit 2 makes Claude Code block the action and feed stderr back to the
model, so the block always carries the repair instruction (canonical
stub + handshake/pull guidance).

Modes (SEMA_REF_GATE):
  off      disable entirely
  warn     detect and report as model-visible context, never block (default)
  enforce  block STALE refs (exit 2) with the repair message

This is prototype glue. The scan/verdict logic belongs upstream as
`sema check`; when that lands this file becomes a thin wrapper around it.
"""

import json
import os
import re
import sys

REF_RE = re.compile(r"\b([A-Z][A-Za-z0-9]*)#([0-9a-f]{4})\b")

MODE = os.environ.get("SEMA_REF_GATE", "warn").lower()


def _string_values(node):
    """Yield every string value in a decoded JSON structure."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from _string_values(value)
    elif isinstance(node, list):
        for value in node:
            yield from _string_values(value)


def main() -> int:
    if MODE == "off":
        return 0

    raw = sys.stdin.read()
    # The hook payload is JSON: newlines inside strings arrive escaped as
    # literal \n, which destroys the \b word boundary for refs at line starts.
    # Scan the decoded strings, not the encoded wire bytes.
    texts = [raw]
    try:
        texts = list(_string_values(json.loads(raw))) or [raw]
    except json.JSONDecodeError:
        pass
    refs = sorted({ref for text in texts for ref in REF_RE.findall(text)})
    if not refs:
        return 0

    try:
        from sema.core.registry import (
            RegistryManager,
            get_default_db_path,
            get_default_vocab_dir,
        )

        db_override = os.environ.get("SEMA_REF_GATE_DB")
        if db_override:
            registry = RegistryManager(db_path=db_override)
        else:
            registry = RegistryManager(get_default_vocab_dir(), db_path=get_default_db_path())
    except Exception as e:  # registry unavailable: fail open, but say so
        print(f"sema-ref-gate: registry unavailable, gate skipped ({e})", file=sys.stderr)
        return 0

    stale, unknown = [], []
    for handle, stub in refs:
        pattern = registry.get_pattern(handle)
        if pattern is None:
            unknown.append(f"{handle}#{stub}")
        elif pattern.get("sema_stub") != stub:
            stale.append((f"{handle}#{stub}", pattern.get("sema_stub", "?")))

    log_path = os.environ.get("SEMA_REF_GATE_LOG")
    if log_path:
        try:
            with open(log_path, "a") as f:
                f.write(
                    json.dumps(
                        {
                            "mode": MODE,
                            "refs": [f"{h}#{s}" for h, s in refs],
                            "stale": [r for r, _ in stale],
                            "unknown": unknown,
                            "blocked": bool(stale) and MODE == "enforce",
                        }
                    )
                    + "\n"
                )
        except OSError:
            pass

    if unknown:
        # stdout on exit 0 becomes model-visible context on UserPromptSubmit
        print(
            "sema-ref-gate: unrecognized refs (not in the active vocabulary): "
            + ", ".join(unknown)
            + ". If these are sema refs, verify with sema_handshake before relying on them."
        )

    if stale:
        lines = [f"  {ref} -> canonical stub is #{canonical}" for ref, canonical in stale]
        message = (
            "sema-ref-gate: STALE sema ref(s) detected — definition drift.\n"
            + "\n".join(lines)
            + "\nDo not proceed on the drifted definition. Run sema_handshake on each "
            "ref to confirm, then sema_resolve for the canonical definition (or "
            "sema_pull if upstream moved). Re-issue the action with correct refs."
        )
        if MODE == "warn":
            print(message)
            return 0
        print(message, file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
