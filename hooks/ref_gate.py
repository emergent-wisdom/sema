#!/usr/bin/env python3
"""Sema ref gate — Claude Code hook that blocks stale sema refs.

Thin shim over ``sema.core.check``: reads the hook event JSON from stdin,
extracts content-addressed refs (Handle#stub), and verdicts each against the
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
"""

import json
import os
import sys
from pathlib import Path

# A git-installed plugin contains the package source but does not install it
# into the system ``python3`` used by command hooks. Prefer this plugin's source
# over any unrelated globally installed Sema version.
PLUGIN_SRC = Path(__file__).resolve().parent.parent / "src"
if PLUGIN_SRC.is_dir():
    sys.path.insert(0, str(PLUGIN_SRC))

try:
    from sema.core.check import REF_RE  # noqa: F401
except ImportError:  # sema not importable: main() fails open, so must import too
    REF_RE = None

MODE = os.environ.get("SEMA_REF_GATE", "warn")
VALID_MODES = {"off", "warn", "enforce"}


def _normalized_mode(value: str) -> str:
    mode = value.strip().lower()
    return mode if mode in VALID_MODES else "warn"


def _hook_event_name(raw: str) -> str | None:
    try:
        event = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(event, dict):
        return None
    event_name = event.get("hook_event_name")
    return event_name if isinstance(event_name, str) else None


def _emit_context(event_name: str | None, message: str) -> None:
    """Emit context in the format Claude Code expects for this event."""
    if event_name in {"UserPromptSubmit", "PreToolUse"}:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": event_name,
                        "additionalContext": message,
                    }
                }
            )
        )
    else:
        print(message)


def main() -> int:
    mode = _normalized_mode(MODE)
    if mode == "off":
        return 0

    raw = sys.stdin.read()
    event_name = _hook_event_name(raw)

    try:
        from sema.core.check import check_text, extract_refs, load_registry

        refs = extract_refs(raw)
        if not refs:
            return 0
        registry = load_registry(os.environ.get("SEMA_REF_GATE_DB"))
        doc = check_text(raw, registry)
    except Exception as e:  # registry unavailable: fail open, but say so
        print(f"sema-ref-gate: registry unavailable, gate skipped ({e})", file=sys.stderr)
        return 0

    log_path = os.environ.get("SEMA_REF_GATE_LOG")
    if log_path:
        try:
            with open(log_path, "a") as f:
                f.write(
                    json.dumps(
                        {
                            "mode": mode,
                            "refs": [f"{h}#{s}" for h, s in refs],
                            "stale": [r["ref"] for r in doc["stale"]],
                            "unknown": [r["ref"] for r in doc["unknown"]],
                            "blocked": bool(doc["stale"]) and mode == "enforce",
                        }
                    )
                    + "\n"
                )
        except OSError:
            pass

    context_messages = []
    unknown_ref_strings = [r["ref"] for r in doc["unknown"]]
    if unknown_ref_strings:
        context_messages.append(
            "sema-ref-gate: unrecognized refs (not in the active vocabulary): "
            + ", ".join(unknown_ref_strings)
            + ". If these are sema refs, verify with sema_handshake before relying on them."
        )

    if doc["stale"]:
        message = "sema-ref-gate: " + doc["repair"]
        if mode == "enforce":
            print(message, file=sys.stderr)
            return 2
        context_messages.append(message)

    if context_messages:
        _emit_context(event_name, "\n".join(context_messages))

    return 0


if __name__ == "__main__":
    sys.exit(main())
