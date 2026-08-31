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
import os
import re
import sqlite3
from pathlib import Path

REF_RE = re.compile(r"\b([A-Z][A-Za-z0-9]*)#([0-9a-f]{4})\b")

CHECK_SCHEMA_VERSION = 1

EXIT_CLEAN = 0
EXIT_ERROR = 1
EXIT_STALE = 3


class RegistryUnavailableError(RuntimeError):
    """The reference registry could not be located or read."""


class RefRegistry:
    """Minimal registry surface needed by :func:`check_text`."""

    def __init__(self, patterns: dict[str, dict], db_path: Path):
        self.registry = patterns
        self.db_path = str(db_path)

    def get_pattern(self, handle: str) -> dict | None:
        return self.registry.get(handle)

    def count(self) -> int:
        return len(self.registry)


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
    """Verdict every ref in ``text`` against a registry with ``get_pattern``.

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


def _default_db_path() -> Path:
    """Resolve the active DB without importing optional Sema dependencies."""
    if "SEMA_DB_PATH" in os.environ:
        return Path(os.environ["SEMA_DB_PATH"]).expanduser()

    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    config_home = Path(xdg_config_home).expanduser() if xdg_config_home else Path.home() / ".config"
    active_file = config_home / "sema" / "active_db"
    if active_file.exists():
        try:
            configured = active_file.read_text().strip()
        except OSError as e:
            raise RegistryUnavailableError(f"cannot read active DB config: {e}") from e
        if configured:
            return Path(configured).expanduser()

    module_path = Path(__file__).resolve()
    candidates = (
        module_path.parents[3] / "data" / "taxonomy.db",  # source checkout/plugin
        module_path.parents[1] / "data" / "taxonomy.db",  # installed wheel
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate

    raise RegistryUnavailableError("no active or bundled registry database found")


def _load_patterns(db_path: Path) -> dict[str, dict]:
    """Read just the canonical pattern records needed for ref verdicts."""
    try:
        connection = sqlite3.connect(f"{db_path.resolve().as_uri()}?mode=ro", uri=True)
        try:
            rows = connection.execute(
                "SELECT text, metadata FROM nodes WHERE node_type='PATTERN'"
            ).fetchall()
        finally:
            connection.close()
    except sqlite3.Error as e:
        raise RegistryUnavailableError(f"cannot read registry database {db_path}: {e}") from e

    patterns = {}
    for handle, metadata_json in rows:
        try:
            metadata = json.loads(metadata_json)
            pattern = metadata.get("pattern", metadata)
        except (AttributeError, TypeError, json.JSONDecodeError) as e:
            raise RegistryUnavailableError(
                f"invalid metadata for pattern {handle!r} in {db_path}: {e}"
            ) from e

        if not isinstance(handle, str) or not handle or not isinstance(pattern, dict):
            raise RegistryUnavailableError(f"invalid pattern row in {db_path}")
        if handle in patterns:
            raise RegistryUnavailableError(f"duplicate pattern handle {handle!r} in {db_path}")

        stub = pattern.get("sema_stub")
        if not isinstance(stub, str) or re.fullmatch(r"[0-9a-f]{4}", stub) is None:
            raise RegistryUnavailableError(
                f"pattern {handle!r} in {db_path} has no valid canonical stub"
            )
        patterns[handle] = pattern

    return patterns


def load_registry(db_path: str | None = None) -> RefRegistry:
    """Load a ref-check registry from ``db_path`` or the active default DB.

    The loader is deliberately standard-library-only so plugin hooks can use
    the checked-out source without a separate package installation.
    """
    path = Path(db_path).expanduser() if db_path is not None else _default_db_path()
    if not path.is_file():
        raise RegistryUnavailableError(f"registry database does not exist: {path}")
    return RefRegistry(_load_patterns(path), path.resolve())
