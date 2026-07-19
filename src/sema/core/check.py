"""Ref checking: extract content-addressed refs from text and verdict them.

This is the single home for the scan/verdict logic that harness shims
(Claude Code hook, and equivalents for other harnesses) build on. Shims
must never reimplement extraction: harness payloads are typically JSON,
where ``\\n``-escaping at line starts destroys regex word boundaries —
scanning must happen on decoded string values, once, here.

Verdicts per ref:

  KNOWN    handle exists in the registry, stub matches the canonical stub
  STALE    handle exists, stub differs — the definition drifted
  UNKNOWN  handle not in the registry (the ref syntax can match non-sema
           text like "PR#12ab", so UNKNOWN is informational, never fatal)

The verdict document (see :func:`check_text`) is a versioned schema; the
``sema check`` CLI emits it as JSON and communicates via exit codes:

  0  no stale refs (clean, or only KNOWN/UNKNOWN)
  3  at least one STALE ref
  1  infrastructure error (registry unavailable) — callers should fail open
"""

import json
import re

REF_RE = re.compile(r"\b([A-Z][A-Za-z0-9]*)#([0-9a-f]{4})\b")

CHECK_SCHEMA_VERSION = 1

EXIT_CLEAN = 0
EXIT_ERROR = 1
EXIT_STALE = 3


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


def extract_refs(text: str) -> list[tuple[str, str]]:
    """Extract (handle, stub) refs from text, decoding JSON payloads first.

    If ``text`` parses as JSON, refs are scanned in its decoded string
    values (wire-escaped ``\\n`` would otherwise fuse with a following
    handle and defeat the word boundary). Otherwise the raw text is
    scanned as-is. Returns sorted unique refs.
    """
    texts = [text]
    try:
        texts = list(_string_values(json.loads(text))) or [text]
    except json.JSONDecodeError:
        pass
    return sorted({ref for chunk in texts for ref in REF_RE.findall(chunk)})


def repair_message(stale: list[dict]) -> str:
    """Model-facing repair instruction for a set of STALE ref verdicts."""
    lines = [f"  {item['ref']} -> canonical stub is #{item['canonical'] or '?'}" for item in stale]
    return (
        "STALE sema ref(s) detected — definition drift.\n"
        + "\n".join(lines)
        + "\nDo not proceed on the drifted definition. Run sema_handshake on each "
        "ref to confirm, then sema_resolve for the canonical definition (or "
        "sema_pull if upstream moved). Re-issue the action with correct refs."
    )


def check_text(text: str, registry) -> dict:
    """Verdict every ref in ``text`` against ``registry`` (a RegistryManager).

    Returns the versioned verdict document:

    ``{"schema": 1, "refs": [{"ref", "handle", "stub", "verdict", "canonical"}],
    "stale": [...], "unknown": [...], "repair": str | None}``

    where ``stale``/``unknown`` are the subsets of ``refs`` with those
    verdicts, and ``repair`` is the ready-to-deliver model-facing message
    (None when nothing is stale).
    """
    refs = []
    for handle, stub in extract_refs(text):
        pattern = registry.get_pattern(handle)
        if pattern is None:
            verdict, canonical = "UNKNOWN", None
        else:
            canonical = pattern.get("sema_stub")
            verdict = "KNOWN" if canonical == stub else "STALE"
        refs.append(
            {
                "ref": f"{handle}#{stub}",
                "handle": handle,
                "stub": stub,
                "verdict": verdict,
                "canonical": canonical,
            }
        )

    stale = [r for r in refs if r["verdict"] == "STALE"]
    unknown = [r for r in refs if r["verdict"] == "UNKNOWN"]
    return {
        "schema": CHECK_SCHEMA_VERSION,
        "refs": refs,
        "stale": stale,
        "unknown": unknown,
        "repair": repair_message(stale) if stale else None,
    }


def load_registry(db_path: str | None = None):
    """RegistryManager for ``db_path``, or the active default registry."""
    from sema.core.registry import RegistryManager, get_default_db_path, get_default_vocab_dir

    if db_path:
        return RegistryManager(db_path=db_path)
    return RegistryManager(get_default_vocab_dir(), db_path=get_default_db_path())
