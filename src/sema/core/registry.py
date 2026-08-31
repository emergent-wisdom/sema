import json
import os
import re
import sqlite3
import tempfile
from pathlib import Path
from threading import Lock

import numpy as np
from pydantic import BaseModel, Field

# Try to import client for auto-discovery
try:
    from sema.client import get_default_client
except ImportError:
    get_default_client = None


# Dev paths (prefer local development over installed)
_DEV_DB = Path(__file__).parent.parent.parent.parent / "data" / "taxonomy.db"
_DEV_VOCAB = Path(__file__).parent.parent.parent.parent / "data" / "vocabulary"

# Installed package paths (data bundled inside the wheel)
_PKG_DB = Path(__file__).parent.parent / "data" / "taxonomy.db"
_PKG_VOCAB = Path(__file__).parent.parent / "data" / "vocabulary"


def _get_config_dir() -> Path:
    """Return the per-user configuration directory.

    Follow the XDG base-directory convention when the user supplies an
    override. This keeps CLI and MCP sessions isolated in containers, tests,
    and project-specific wrappers without changing the normal platform path.
    """
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg_config_home).expanduser() if xdg_config_home else Path.home() / ".config"
    return base / "sema"


def _get_active_db_config() -> str | None:
    """Read the active DB path from the per-user Sema configuration."""
    config_file = _get_config_dir() / "active_db"
    if config_file.exists():
        path = config_file.read_text().strip()
        if path and Path(path).exists():
            return path
    return None


def get_configured_active_db() -> str | None:
    """Return the configured active DB, without applying environment overrides."""
    return _get_active_db_config()


def set_active_db(path: str | None):
    """Atomically write the active DB path to the Sema configuration."""
    config_dir = _get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "active_db"
    if path is None:
        config_file.unlink(missing_ok=True)
    else:
        temp_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=config_dir,
                prefix=".active_db.",
                suffix=".tmp",
                delete=False,
            ) as temp_file:
                temp_path = Path(temp_file.name)
                temp_file.write(str(Path(path).expanduser().resolve()))
                temp_file.flush()
                os.fsync(temp_file.fileno())
            os.replace(temp_path, config_file)
        except Exception:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)
            raise


def _get_db_registry_path() -> Path:
    return _get_config_dir() / "databases.json"


def _load_db_registry() -> dict[str, object]:
    """Load the database registry, tolerating missing or legacy-invalid files."""
    registry_file = _get_db_registry_path()
    if not registry_file.exists():
        return {}
    try:
        dbs = json.loads(registry_file.read_text())
    except (json.JSONDecodeError, ValueError):
        return {}
    return dbs if isinstance(dbs, dict) else {}


def _write_db_registry(dbs: dict[str, object]) -> None:
    """Atomically replace the database registry."""
    registry_file = _get_db_registry_path()
    registry_file.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=registry_file.parent,
            prefix=f".{registry_file.name}.",
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            json.dump(dbs, temp_file, indent=2)
            temp_file.write("\n")
            temp_file.flush()
            os.fsync(temp_file.fileno())
        os.replace(temp_path, registry_file)
    except Exception:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        raise


def _record_for_path(path: str, info: object) -> dict | None:
    """Return a normalized copy of a path-keyed registry record."""
    if not isinstance(info, dict):
        return None
    resolved = str(Path(path).expanduser().resolve())
    record = dict(info)
    record["path"] = resolved
    record.setdefault("name", Path(resolved).stem)
    return record


def _is_managed_record(record: object) -> bool:
    return isinstance(record, dict) and record.get("kind") == "installed-library"


def register_db(path: str, name: str | None = None):
    """Register a DB while preserving any metadata already stored for it."""
    dbs = _load_db_registry()
    resolved = str(Path(path).expanduser().resolve())
    existing = dbs.get(resolved)
    record = dict(existing) if isinstance(existing, dict) else {}
    if name:
        record["name"] = name
    elif not record.get("name"):
        record["name"] = Path(resolved).stem
    record["path"] = resolved
    dbs[resolved] = record
    _write_db_registry(dbs)


def get_registered_db(name: str) -> dict | None:
    """Return the first registered DB whose name matches case-insensitively."""
    if not isinstance(name, str) or not name.strip():
        return None

    query = name.strip().casefold()
    matches: list[dict] = []
    for path, info in _load_db_registry().items():
        record = _record_for_path(path, info)
        if record is not None and str(record.get("name", "")).casefold() == query:
            matches.append(record)

    if not matches:
        return None
    for record in matches:
        if record.get("name") == name:
            return record
    return matches[0]


def get_registered_db_by_path(path: str | os.PathLike) -> dict | None:
    """Return a registered DB record by its resolved filesystem path."""
    resolved = str(Path(path).expanduser().resolve())
    return _record_for_path(resolved, _load_db_registry().get(resolved))


def validate_registry_db(path: str | os.PathLike) -> None:
    """Reject non-files and malformed SQLite files before activating them."""
    resolved = Path(path).expanduser().resolve()
    if not resolved.is_file():
        raise ValueError(f"Database is not a regular file: {resolved}")
    uri = f"{resolved.as_uri()}?mode=ro"
    try:
        connection = sqlite3.connect(uri, uri=True)
        try:
            quick_check = connection.execute("PRAGMA quick_check").fetchone()
            if not quick_check or quick_check[0] != "ok":
                raise ValueError(f"Database integrity check failed: {quick_check}")
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            }
            if not {"nodes", "edges"} <= tables:
                raise ValueError("Database does not contain the Sema nodes and edges tables")
        finally:
            connection.close()
    except sqlite3.Error as exc:
        raise ValueError(f"Not a valid Sema SQLite database: {exc}") from exc


def register_library(record: dict) -> dict:
    """Validate and atomically register an installed, read-only library."""
    if not isinstance(record, dict):
        raise TypeError("library record must be a dictionary")

    normalized = dict(record)
    for field in ("name", "version", "catalog_root"):
        value = normalized.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"library record requires a non-empty {field}")

    path = normalized.get("path")
    if not isinstance(path, str | os.PathLike) or not str(path).strip():
        raise ValueError("library record requires a non-empty path")
    if normalized.get("kind", "installed-library") != "installed-library":
        raise ValueError("library record kind must be 'installed-library'")
    if "read_only" in normalized and normalized["read_only"] is not True:
        raise ValueError("installed-library records must be read-only")

    normalized["name"] = normalized["name"].strip()
    normalized["version"] = normalized["version"].strip()
    normalized["catalog_root"] = normalized["catalog_root"].strip()
    normalized["path"] = str(Path(path).expanduser().resolve())
    normalized["kind"] = "installed-library"
    normalized["read_only"] = True

    dbs = _load_db_registry()
    old_keys: list[str] = []
    for old_path, old_info in dbs.items():
        if not isinstance(old_info, dict):
            continue
        old_name = old_info.get("name")
        if not isinstance(old_name, str) or old_name.casefold() != normalized["name"].casefold():
            continue
        if not _is_managed_record(old_info):
            raise ValueError(
                f"a local database is already registered with the name {normalized['name']!r}"
            )
        if (
            old_info.get("version") == normalized["version"]
            and old_info.get("catalog_root") != normalized["catalog_root"]
        ):
            raise ValueError(
                "an installed library with this name and version has a different catalog_root"
            )
        old_keys.append(old_path)

    for old_path in old_keys:
        del dbs[old_path]
    dbs[normalized["path"]] = normalized
    _write_db_registry(dbs)
    return dict(normalized)


def get_library(name: str) -> dict | None:
    """Return an installed-library record by case-insensitive name."""
    if not isinstance(name, str) or not name.strip():
        return None
    query = name.strip().casefold()
    for path, info in _load_db_registry().items():
        if not _is_managed_record(info):
            continue
        record = _record_for_path(path, info)
        if record is not None and str(record.get("name", "")).casefold() == query:
            return record
    return None


def is_managed_db(path: str | None) -> bool:
    """Return whether path is registered as an installed library."""
    if not path:
        return False
    resolved = str(Path(path).expanduser().resolve())
    info = _load_db_registry().get(resolved)
    return _is_managed_record(info)


def list_dbs() -> list[dict]:
    """List all known databases with their status."""
    active = _get_active_db_config()
    bundled = get_bundled_db_path()

    env_db = os.environ.get("SEMA_DB_PATH")
    if env_db:
        env_db = str(Path(env_db).expanduser().resolve())

    results = []

    # Bundled DB always listed first
    if bundled:
        results.append(
            {
                "name": "default",
                "path": bundled,
                "active": env_db == bundled or (active is None and not env_db),
                "bundled": True,
                "kind": "bundled",
                "read_only": is_bundled_db(bundled),
                "exists": Path(bundled).exists(),
            }
        )

    for path, info in _load_db_registry().items():
        record = _record_for_path(path, info)
        if record is None:
            continue
        record.update(
            {
                "active": (env_db == record["path"] if env_db else active == record["path"]),
                "bundled": False,
                "exists": Path(record["path"]).exists(),
            }
        )
        if _is_managed_record(record):
            record["read_only"] = True
        else:
            record.setdefault("read_only", False)
        results.append(record)

    known_paths = {record["path"] for record in results}
    if env_db and env_db not in known_paths:
        results.append(
            {
                "name": Path(env_db).stem or "environment",
                "path": env_db,
                "active": True,
                "bundled": False,
                "kind": "environment",
                "read_only": is_read_only_db(env_db),
                "exists": Path(env_db).exists(),
            }
        )

    return results


def get_bundled_db_path() -> str | None:
    """Find the bundled catalog DB, ignoring user config and SEMA_DB_PATH."""
    if _DEV_DB.exists():
        return str(_DEV_DB)
    if _PKG_DB.exists():
        return str(_PKG_DB)
    return None


def is_bundled_db(path: str | None) -> bool:
    """Check if a DB path points to the installed package's read-only catalog.

    The dev DB (repo data/) is NOT considered bundled — maintainers
    need to mint into it. Only the pip-installed copy is read-only.
    """
    if not path:
        return False
    resolved = Path(path).resolve()
    if _PKG_DB.exists() and resolved.exists():
        try:
            return resolved.samefile(_PKG_DB)
        except OSError:
            pass
    return str(resolved) == str(_PKG_DB.resolve())


def is_read_only_db(path: str | None) -> bool:
    """Return whether path is bundled or registered as read-only."""
    if not path:
        return False
    if is_bundled_db(path):
        return True
    resolved = str(Path(path).expanduser().resolve())
    info = _load_db_registry().get(resolved)
    if _is_managed_record(info):
        return True
    return isinstance(info, dict) and info.get("read_only") is True


def get_default_db_path() -> str | None:
    """Get default DB path.

    Priority:
      1. SEMA_DB_PATH env var (explicit override)
      2. Active DB from the per-user Sema configuration (set via `sema use`)
      3. Dev DB (repo data/ — for local development)
      4. Bundled package DB (read-only catalog)
      5. Client fallback (download)
    """
    if os.environ.get("SEMA_DB_PATH"):
        return str(Path(os.environ["SEMA_DB_PATH"]).expanduser().resolve())
    active = _get_active_db_config()
    if active:
        return active
    if _DEV_DB.exists():
        return str(_DEV_DB)
    if _PKG_DB.exists():
        return str(_PKG_DB)
    if get_default_client:
        try:
            client = get_default_client()
            return str(client.get_db_path())
        except Exception:
            pass
    return None


def get_default_vocab_dir() -> str | None:
    """Get default vocab dir. Priority: env var > dev vocab > client vocab."""
    if os.environ.get("SEMA_VOCAB_DIR"):
        return os.environ["SEMA_VOCAB_DIR"]
    if _DEV_VOCAB.exists():
        return str(_DEV_VOCAB)
    # Check if data is bundled inside the installed package
    if _PKG_VOCAB.exists():
        return str(_PKG_VOCAB)
    if get_default_client:
        try:
            client = get_default_client()
            return str(client.data_dir / "vocabulary")
        except Exception:
            pass
    return None


class SearchResult(BaseModel):
    """Structured result from a registry search."""

    handle: str
    gloss: str
    mechanism: str
    category: str
    layer: str
    sema_ref: str
    score: float = Field(default=0.0)


class RegistryManager:
    def __init__(self, vocab_dir=None, db_path=None):
        self.vocab_dir = vocab_dir or get_default_vocab_dir()
        self.db_path = db_path or get_default_db_path()
        self._semantic_lock = Lock()
        self._embedding_service = None
        self._semantic_candidates = None

        self.source = "unknown"
        self.registry = self._load_registry()

    def _load_registry(self):
        registry = {}

        # Priority 1: Load from DB (Fast)
        if self.db_path and os.path.exists(self.db_path):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                # Load patterns
                cursor.execute("SELECT id, text, metadata FROM nodes WHERE node_type='PATTERN'")
                node_id_to_handle = {}
                for node_id, handle, meta_json in cursor.fetchall():
                    try:
                        meta = json.loads(meta_json)
                        # Extract the full pattern data
                        # Structure is {"pattern": {...}} in DB
                        data = meta.get("pattern", {}) if "pattern" in meta else meta

                        if data and handle:
                            registry[handle] = data
                            node_id_to_handle[node_id] = handle
                    except Exception:
                        continue

                # Load dependencies from graph edges (database is source of truth)
                edge_type_map = {
                    "REFERENCES": "references",
                    "COMPOSES_WITH": "composes_with",
                    "ACCEPTS": "accepts",
                    "YIELDS": "yields",
                }

                # The alias column preserves the key the author minted with
                # (e.g. {"references": {"my_gate": ...}}). Dropping it and
                # substituting snake_case(handle) would rename dependency
                # keys, so {{my_gate}} templates could never resolve and the
                # registry view would disagree with the graph-store view
                # (get_dependencies_from_edges reads the same column).
                try:
                    cursor.execute(
                        "SELECT source_id, target_id, edge_type, alias FROM edges "
                        "WHERE edge_type IN ('REFERENCES', 'COMPOSES_WITH', 'ACCEPTS', 'YIELDS')"
                    )
                    edge_rows = cursor.fetchall()
                except sqlite3.OperationalError:
                    # Legacy DB without the alias column (pre-migration,
                    # never opened via GraphStore). Fall back gracefully.
                    cursor.execute(
                        "SELECT source_id, target_id, edge_type, NULL FROM edges "
                        "WHERE edge_type IN ('REFERENCES', 'COMPOSES_WITH', 'ACCEPTS', 'YIELDS')"
                    )
                    edge_rows = cursor.fetchall()

                for source_id, target_id, edge_type, alias in edge_rows:
                    source_handle = node_id_to_handle.get(source_id)
                    target_handle = node_id_to_handle.get(target_id)

                    if source_handle and target_handle and source_handle in registry:
                        dep_category = edge_type_map.get(edge_type)
                        if dep_category:
                            if "dependencies" not in registry[source_handle]:
                                registry[source_handle]["dependencies"] = {}
                            if dep_category not in registry[source_handle]["dependencies"]:
                                registry[source_handle]["dependencies"][dep_category] = {}

                            # Get target's sema_id for full reference
                            target_sema_id = registry.get(target_handle, {}).get(
                                "sema_id", target_handle
                            )

                            key = alias
                            if not key:
                                # Legacy edges that pre-date alias storage:
                                # fall back to snake_case of the handle.
                                s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", target_handle)
                                key = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

                            registry[source_handle]["dependencies"][dep_category][key] = (
                                target_sema_id
                            )

                conn.close()
                if registry:
                    self.source = "database"
                    return registry
            except Exception:
                # Fallback to file system if DB read fails
                pass

        return registry

    def refresh(self):
        refreshed_registry = self._load_registry()
        with self._semantic_lock:
            self.registry = refreshed_registry
            self._semantic_candidates = None

    def count(self) -> int:
        return len(self.registry)

    def _get_ref(self, data, default=None):
        """Helper to get the canonical reference (Handle#stub) from pattern data."""
        if not data:
            return default

        # 1. Prefer explicit sema_ref
        if "sema_ref" in data:
            return data["sema_ref"]

        # 2. Construct from Handle + Stub
        handle = data.get("handle")
        stub = data.get("stub") or data.get("sema_stub")
        if handle and stub:
            return f"{handle}#{stub}"

        # 3. Fallback to Handle or default
        return handle if handle else default

    def resolve_templates(self, text, context=None):
        """Replace {{Handle}} with Pattern#Hash (sema_ref), checking local context first."""
        if not isinstance(text, str):
            return text

        # Lazy build lower map if missing or the handle set changed.
        # Key is lowercase with underscores removed for flexible matching.
        # (A pure len() check misses same-size swaps — e.g. a supersession
        # pull replacing one handle with another — leaving a stale map that
        # points at handles no longer in the registry.)
        registry_keys = set(self.registry.keys())
        if (
            not hasattr(self, "_lower_map")
            or getattr(self, "_lower_map_keys", None) != registry_keys
        ):
            self._lower_map = {k.lower().replace("_", ""): k for k in registry_keys}
            self._lower_map_keys = registry_keys

        def replacer(match):
            content = match.group(1)
            # Handle is the part before any # if present in the template link
            handle = content.split("#")[0]

            # 1. Check Local Context (e.g. dependencies like 'source_content' -> 'Datum')
            if context:
                # Try exact match in context
                if handle in context:
                    return context[handle]

                # Normalize for context check
                normalized_ctx = handle.lower().replace("_", "")
                # We need to scan context keys if we want normalized matching there too.
                # But typically dependency keys are exact.
                # Let's assume exact or simple lower for now.
                # If strict normalization is needed for context keys:
                for ctx_key, ctx_val in context.items():
                    if ctx_key.lower().replace("_", "") == normalized_ctx:
                        return ctx_val

            # 2. Check Global Registry
            # Try exact match
            if handle in self.registry:
                return self._get_ref(self.registry[handle], default=content)

            # Normalize: lowercase and remove underscores for flexible matching
            # e.g., "confidence_calibrate" -> "confidencecalibrate" matches "ConfidenceCalibrate"
            normalized = handle.lower().replace("_", "")
            if normalized in self._lower_map:
                real_handle = self._lower_map[normalized]
                return self._get_ref(self.registry[real_handle], default=content)

            return match.group(0)  # Keep original if not found

        # Matches {{Handle}} or {{Handle#Hash}}
        return re.sub(r"\{\{\s*([A-Za-z0-9_#]+)\s*\}\}", replacer, text)

    def get_pattern(self, handle):
        data = self.registry.get(handle)
        if not data:
            return None

        # Build local context from dependencies for template resolution
        local_context = {}
        raw_deps = data.get("dependencies", {})
        if isinstance(raw_deps, dict):
            for _category, items in raw_deps.items():
                if isinstance(items, dict):
                    for key, ref in items.items():
                        # Resolve the ref to its full sema_ref if possible
                        if isinstance(ref, str):
                            target_handle = (
                                ref.split(":")[1].split("#")[0]
                                if "sema:" in ref
                                else ref.split("#")[0]
                            )

                            if target_handle in self.registry:
                                local_context[key] = self._get_ref(
                                    self.registry[target_handle], default=ref
                                )
                            elif (
                                hasattr(self, "_lower_map")
                                and target_handle.lower() in self._lower_map
                            ):
                                real = self._lower_map[target_handle.lower()]
                                local_context[key] = self._get_ref(self.registry[real], default=ref)
                            else:
                                local_context[key] = ref
                        else:
                            local_context[key] = str(ref)

        # Return a copy with resolved templates
        resolved = data.copy()
        fields_to_resolve = [
            "gloss",
            "mechanism",
            "invariants",
            "usage_examples",
            "preconditions",
            "postconditions",
            "failure_modes",
        ]
        for field in fields_to_resolve:
            if field in resolved:
                val = resolved[field]
                if isinstance(val, str):
                    resolved[field] = self.resolve_templates(val, context=local_context)
                elif isinstance(val, list):
                    resolved[field] = [
                        self.resolve_templates(v, context=local_context) for v in val
                    ]

        # Ensure top-level handle is overlaid
        resolved["handle"] = resolved.get("sema_ref", resolved.get("handle"))

        # Resolve dependencies to Overlay format
        if "dependencies" in resolved and isinstance(resolved["dependencies"], dict):
            new_deps = {}
            for rel_type, targets in resolved["dependencies"].items():
                if isinstance(targets, dict):
                    new_targets = {}
                    for key, ref in targets.items():
                        # Extract handle from sema:Handle#... or Handle
                        if isinstance(ref, str):
                            target_handle = (
                                ref.split(":")[1].split("#")[0]
                                if "sema:" in ref
                                else ref.split("#")[0]
                            )

                            # Lookup overlay
                            if target_handle in self.registry:
                                new_targets[key] = self._get_ref(
                                    self.registry[target_handle], default=ref
                                )
                            elif (
                                hasattr(self, "_lower_map")
                                and target_handle.lower() in self._lower_map
                            ):
                                real = self._lower_map[target_handle.lower()]
                                new_targets[key] = self._get_ref(self.registry[real], default=ref)
                            else:
                                new_targets[key] = ref  # Keep original if unknown
                        else:
                            new_targets[key] = ref
                    new_deps[rel_type] = new_targets
            resolved["dependencies"] = new_deps

        # Resolve 'related' list in _meta
        if "_meta" in resolved and isinstance(resolved["_meta"], dict):
            related_source = resolved["_meta"].get("related")
            if isinstance(related_source, list):
                new_related = []
                for item in related_source:
                    if isinstance(item, str):
                        h = item.split("#")[0]
                        if h in self.registry:
                            new_related.append(self._get_ref(self.registry[h], default=item))
                        elif hasattr(self, "_lower_map") and h.lower() in self._lower_map:
                            real = self._lower_map[h.lower()]
                            new_related.append(self._get_ref(self.registry[real], default=item))
                        else:
                            new_related.append(item)
                    else:
                        new_related.append(item)
                # data.copy() above is shallow — writing into the original
                # _meta would mutate the shared registry entry in place.
                resolved["_meta"] = {**resolved["_meta"], "related": new_related}

        return resolved

    def search(self, query: str, use_semantic: bool = True) -> list[dict]:
        """Search the registry. Returns a list of dicts (compatible with SearchResult)."""
        import re

        # 1. Keyword Search with tiered scoring
        #
        # Every keyword hit used to get a flat 1.0 regardless of where it
        # matched, which meant a handle-match and a substring-buried-in-
        # a-400-word-mechanism came back indistinguishable. Now each field
        # has a weight, exact-word hits beat substring hits, and repeated
        # hits accumulate so "consensus consensus consensus" beats a single
        # off-hand mention.
        keyword_results = []
        query_lower = query.lower()

        # Build a word-boundary regex for exact token matching.
        # re.escape handles punctuation; \b gives us word boundaries.
        try:
            word_re = re.compile(rf"\b{re.escape(query_lower)}\b")
        except re.error:
            word_re = None

        # Field weights (max attainable per field if the match is clean).
        # Handle > signature > gloss > mechanism matches the cognitive
        # hierarchy of what a term "means" in a pattern.
        FIELD_WEIGHTS = {
            "handle": 1.00,
            "signature": 0.75,
            "gloss": 0.70,
            "mechanism": 0.55,
        }

        def _field_score(text: str, weight: float) -> float:
            """Score a field: word-boundary hit gets full weight, substring
            hit gets 60% of weight, and additional occurrences add a small
            log bonus (so frequency matters but doesn't dominate)."""
            if not text:
                return 0.0
            text_lower = text.lower()
            if query_lower not in text_lower:
                return 0.0
            # Exact word hit beats substring hit
            has_word = bool(word_re and word_re.search(text_lower))
            base = weight if has_word else weight * 0.6
            # Frequency bonus (capped)
            n = text_lower.count(query_lower)
            if n > 1:
                import math

                base = min(1.0, base + 0.05 * math.log2(n))
            return base

        for handle, data in self.registry.items():
            gloss = data.get("gloss", "")
            mechanism = data.get("mechanism", "")
            signatures = " ".join(data.get("signature") or [])

            # Per-field sub-scores
            scores = {
                "handle": _field_score(handle, FIELD_WEIGHTS["handle"]),
                "signature": _field_score(signatures, FIELD_WEIGHTS["signature"]),
                "gloss": _field_score(gloss, FIELD_WEIGHTS["gloss"]),
                "mechanism": _field_score(mechanism, FIELD_WEIGHTS["mechanism"]),
            }
            total_score = max(scores.values())
            if total_score == 0.0:
                continue

            # Resolve templates for the result snippet
            resolved_gloss = self.resolve_templates(gloss)
            resolved_mechanism = self.resolve_templates(mechanism)

            # Record which field the top score came from (debug aid)
            matched_fields = [f for f, s in scores.items() if s > 0]

            result = {
                "handle": handle,
                "gloss": resolved_gloss,
                "mechanism": resolved_mechanism,
                "category": data.get("sema_category") or data.get("category", "Unknown"),
                "layer": data.get("sema_layer") or data.get("layer", "Unknown"),
                "sema_ref": data.get("sema_ref", f"{handle}#????"),
                "score": round(total_score, 3),
                "source": "keyword",
                "matched_fields": matched_fields,
            }
            keyword_results.append(result)

        # 2. Semantic Search (Optional)
        semantic_results = []
        if use_semantic and self.db_path and os.path.exists(self.db_path):
            try:
                from sema.taxonomy_graph.embedding_service import EmbeddingService

                with self._semantic_lock:
                    if self._embedding_service is None:
                        self._embedding_service = EmbeddingService(self.db_path)
                    service = self._embedding_service
                    query_vec = service.get_embedding(query)

                    if self._semantic_candidates is None:
                        conn = sqlite3.connect(self.db_path)
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT id, text, embedding FROM nodes "
                            "WHERE node_type='PATTERN' AND embedding IS NOT NULL"
                        )

                        candidates = []
                        handle_map = {}  # ID -> Handle

                        for node_id, text, blob in cursor.fetchall():
                            if blob:
                                vec = np.frombuffer(blob, dtype=np.float32)
                                candidates.append((node_id, vec))
                                handle_map[node_id] = text  # text column is the Handle
                        conn.close()
                        self._semantic_candidates = (candidates, handle_map)

                    candidates, handle_map = self._semantic_candidates
                    sim_results = (
                        service.find_similar(query_vec, candidates, top_k=20, threshold=0.2)
                        if candidates
                        else []
                    )

                for node_id, score in sim_results:
                    handle_name = handle_map.get(node_id)
                    if handle_name and handle_name in self.registry:
                        data = self.registry[handle_name]

                        resolved_gloss = self.resolve_templates(data.get("gloss", ""))
                        resolved_mechanism = self.resolve_templates(data.get("mechanism", ""))

                        semantic_results.append(
                            {
                                "handle": handle_name,
                                "gloss": resolved_gloss,
                                "mechanism": resolved_mechanism,
                                "category": data.get("sema_category")
                                or data.get("category", "Unknown"),
                                "layer": data.get("sema_layer") or data.get("layer", "Unknown"),
                                "sema_ref": data.get("sema_ref", f"{handle_name}#????"),
                                "score": float(score),
                                "source": "semantic",
                            }
                        )
            except (ImportError, Exception):
                pass

        # 3. Merge and Deduplicate
        merged = {}

        # Add keyword results (high priority)
        for r in keyword_results:
            h = r["handle"]
            merged[h] = r

        # Add semantic results
        for r in semantic_results:
            h = r["handle"]
            if h not in merged:
                merged[h] = r
            else:
                # Boost score if found in both
                merged[h]["score"] = max(merged[h]["score"], r["score"])
                merged[h]["source"] = "hybrid"

        # Sort by score
        final_results = list(merged.values())
        final_results.sort(key=lambda x: x.get("score", 0), reverse=True)

        return final_results

    def resolve(self, handle, depth=1):
        # 1. Check for Polymorphic Signature: "Intent(Target)"
        if "(" in handle and ")" in handle:
            # Search for a pattern that claims this signature
            target_pattern = None
            query_sig = handle.strip()
            for p_handle, p_data in self.registry.items():
                signatures = p_data.get("signature", [])
                if query_sig in signatures:
                    target_pattern = p_handle
                    break

            if target_pattern:
                # Redirect resolution to the concrete pattern
                handle = target_pattern
            else:
                return None

        if handle not in self.registry:
            return None

        root = self.registry[handle]
        subgraph = {handle: root}
        to_expand = [handle]

        for _ in range(depth):
            next_expand = []
            for current in to_expand:
                pattern = self.registry.get(current, {})

                # Traverse 'dependencies' which contains categories like 'accepts', 'yields', etc.
                deps = pattern.get("dependencies", {})
                for _category, items in deps.items():
                    # items is a dict of {key: sema_id}
                    for _key, ref in items.items():
                        if isinstance(ref, str):
                            # Extract handle from "sema:Handle#mh:SHA..." or "Handle#stub"
                            # Handle is the part between "sema:" (optional) and "#"
                            if ref.startswith("sema:"):
                                ref_handle = ref.split(":")[1].split("#")[0]
                            else:
                                ref_handle = ref.split("#")[0]

                            if ref_handle in self.registry and ref_handle not in subgraph:
                                subgraph[ref_handle] = self.registry[ref_handle]
                                next_expand.append(ref_handle)
            to_expand = next_expand

        return subgraph

    def get_graph_skeleton(self) -> str:
        """Generate a minimal graph skeleton (regions, hubs) for orientation."""
        if not self.db_path or not os.path.exists(self.db_path):
            return "No database found."

        try:
            # Lazy import to avoid heavy dependencies
            # Ensure root is in path if needed, though usually resolved by package structure

            from networkx.algorithms import community

            from sema.taxonomy_graph.graph_store import GraphStore

            store = GraphStore(self.db_path)
            graph = store.graph

            if graph.number_of_nodes() == 0:
                return "Empty graph."

            # Calculate degrees
            degree = dict(graph.degree())

            # Detect communities
            undirected = graph.to_undirected()
            try:
                communities = community.louvain_communities(undirected)
            except Exception:
                try:
                    communities = community.greedy_modularity_communities(undirected)
                except Exception:
                    communities = []

            # Build region summaries
            region_summaries = []
            for i, comm in enumerate(communities):
                nodes_in_comm = list(comm)
                sorted_nodes = sorted(
                    [(n, degree[n], graph.nodes[n].get("text", "")) for n in nodes_in_comm],
                    key=lambda x: x[1],
                    reverse=True,
                )
                if not sorted_nodes:
                    continue

                label = sorted_nodes[0][2]
                label = " ".join(label.split(" ")[:3])
                region_summaries.append({"label": label, "count": len(nodes_in_comm), "id": i})

            region_summaries.sort(key=lambda x: x["count"], reverse=True)

            # Get hubs
            hubs = sorted(
                [(n, d, graph.nodes[n].get("text", "")) for n, d in degree.items()],
                key=lambda x: x[1],
                reverse=True,
            )[:5]

            # Build output
            out = [f"{graph.number_of_nodes()}n {graph.number_of_edges()}e", ""]

            out.append("Regions:")
            main_regions = region_summaries[:7]
            small_count = len(region_summaries) - 7

            for r in main_regions:
                out.append(f"  {r['label']} ({r['count']}) [R{r['id']}]")

            if small_count > 0:
                out.append(f"  +{small_count} smaller")

            out.append("")
            out.append("Hubs: " + " · ".join([h[2] for h in hubs]))
            out.append("")
            out.append("→ sema_tree() or sema_search() for details")

            return "\n".join(out)

        except Exception as e:
            return f"Error generating skeleton: {str(e)}"

    def get_context(self, handle: str, include_content: bool = True) -> dict:
        """Get graph context: dependencies and prominent consumers (reverse deps).

        Args:
            handle: Pattern handle to get context for
            include_content: If True, include gloss for each neighbor pattern
        """
        context = {"dependencies": [], "used_by": []}

        if not self.db_path or not os.path.exists(self.db_path):
            return context

        try:
            # Lazy import

            from sema.taxonomy_graph.graph_store import GraphStore, NodeType

            # Init store (lightweight if DB exists)
            store = GraphStore(self.db_path)
            graph = store.graph

            # Find node ID for handle
            node_id = None
            # Fast lookup if text matches handle directly (most cases)
            # We iterate because ID is UUID, text is Handle
            for nid, data in graph.nodes(data=True):
                if data.get("text") == handle and data.get("node_type") == NodeType.PATTERN:
                    node_id = nid
                    break

            if not node_id:
                return context

            def _enrich(h: str) -> dict:
                """Return the compact identity and gloss for a neighbor."""
                if not include_content:
                    return {"handle": h}
                pattern = self.registry.get(h, {})
                if pattern:
                    neighbor = {"handle": h}
                    for field in ("sema_ref", "gloss"):
                        value = pattern.get(field)
                        if isinstance(value, str) and value:
                            neighbor[field] = value
                    return neighbor
                return {"handle": h}

            # 1. Dependencies (Successors)
            deps = []
            for succ in graph.successors(node_id):
                succ_node = graph.nodes[succ]
                if succ_node.get("node_type") == NodeType.PATTERN:
                    deps.append(succ_node.get("text"))
            context["dependencies"] = [_enrich(h) for h in sorted(deps)]

            # 2. Used By (Predecessors) - Prominent ones
            # Sort by degree (importance)
            consumers = []
            degree = dict(graph.degree())

            for pred in graph.predecessors(node_id):
                pred_node = graph.nodes[pred]
                if pred_node.get("node_type") == NodeType.PATTERN:
                    consumers.append(
                        {"handle": pred_node.get("text"), "degree": degree.get(pred, 0)}
                    )

            # Sort by degree desc, take top 5
            consumers.sort(key=lambda x: x["degree"], reverse=True)
            context["used_by"] = [_enrich(c["handle"]) for c in consumers[:5]]

        except Exception:
            pass

        return context
