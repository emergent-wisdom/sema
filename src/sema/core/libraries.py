"""Verified installation of independently published Sema libraries.

The portable release is JSON: one pattern per file inside a small, bounded ZIP.
SQLite remains a locally compiled runtime format and is never accepted from an
untrusted library release.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import shutil
import sqlite3
import stat
import tempfile
import uuid
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import url2pathname

import httpx
from platformdirs import user_data_dir
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from .dependencies import (
    get_dependencies_handles,
    topological_sort,
    validate_acyclic,
    validate_layer_direction,
)
from .hashing import (
    CATALOG_ROOT_SCHEME,
    SEMANTIC_ROOT_SCHEME,
    generate_sema_hash,
    pattern_hash_from_sema_id,
    strict_json_loads,
    vocabulary_roots,
)
from .mint import mint_pattern
from .registry import get_configured_active_db, get_library, register_library, set_active_db
from .validator import clean_handle, validate_pattern

MANIFEST_SCHEMA = 1
PATTERN_ARCHIVE_FORMAT = "sema-patterns-zip-v1"

MAX_MANIFEST_BYTES = 256 * 1024
MAX_ARCHIVE_BYTES = 256 * 1024 * 1024
MAX_PATTERN_BYTES = 2 * 1024 * 1024
MAX_UNCOMPRESSED_BYTES = 512 * 1024 * 1024
MAX_PATTERN_COUNT = 100_000
MAX_COMPRESSION_RATIO = 200
MAX_REDIRECTS = 5

_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_LIBRARY_NAME_RE = re.compile(r"[a-z][a-z0-9-]{0,63}")
_VERSION_RE = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
_HANDLE_RE = re.compile(r"[A-Z][A-Za-z0-9]+")
_GITHUB_REPOSITORY_RE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
_ARCHIVE_FILENAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\.zip", re.IGNORECASE)
_FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class LibraryError(RuntimeError):
    """A library release failed validation or installation."""


class SourceUnavailableError(LibraryError):
    """A declared source could not be fetched."""


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class PatternArtifact(_StrictModel):
    format: Literal["sema-patterns-zip-v1"]
    url: str = Field(min_length=1)
    sha256: str
    size_bytes: int = Field(gt=0, le=MAX_ARCHIVE_BYTES)

    @field_validator("sha256")
    @classmethod
    def validate_sha256(cls, value: str) -> str:
        if not _SHA256_RE.fullmatch(value):
            raise ValueError("must be exactly 64 lowercase hexadecimal characters")
        return value


class RootDescriptor(_StrictModel):
    scheme: str = Field(min_length=1)
    sha256: str

    @field_validator("sha256")
    @classmethod
    def validate_sha256(cls, value: str) -> str:
        if not _SHA256_RE.fullmatch(value):
            raise ValueError("must be exactly 64 lowercase hexadecimal characters")
        return value


class LibraryRoots(_StrictModel):
    semantic: RootDescriptor
    catalog: RootDescriptor


class LibraryManifest(_StrictModel):
    manifest_schema: Literal[1]
    name: str
    version: str
    update_url: str = Field(min_length=1)
    patterns: PatternArtifact
    roots: LibraryRoots
    pattern_count: int = Field(gt=0, le=MAX_PATTERN_COUNT)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not _LIBRARY_NAME_RE.fullmatch(value):
            raise ValueError("must be a lowercase path-safe slug, such as 'defi'")
        return value

    @field_validator("version")
    @classmethod
    def validate_version(cls, value: str) -> str:
        if not _VERSION_RE.fullmatch(value):
            raise ValueError("must use MAJOR.MINOR.PATCH, such as '1.0.0'")
        return value


class VerifiedLibrary:
    """Validated, normalized pattern corpus and its computed identities."""

    def __init__(self, patterns: dict[str, dict], order: list[str], roots: dict[str, Any]):
        self.patterns = patterns
        self.order = order
        self.roots = roots


@dataclass(frozen=True)
class LibraryPackage:
    """A locally verified, upload-ready portable library release."""

    manifest_path: Path
    archive_path: Path
    semantic_root: str
    catalog_root: str
    pattern_count: int


def library_data_dir(override: str | Path | None = None) -> Path:
    """Return the root used for immutable installed-library releases."""
    if override is not None:
        return Path(override).expanduser().resolve()
    configured = os.environ.get("SEMA_LIBRARY_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path(user_data_dir("sema")) / "libraries"


def _strict_json(data: bytes, *, label: str) -> dict[str, Any]:
    try:
        value = strict_json_loads(data, label=label)
    except ValueError as exc:
        raise LibraryError(str(exc)) from exc
    if not isinstance(value, dict):
        raise LibraryError(f"{label} must contain one JSON object")
    return value


def _source_url(source: str | Path, *, base: str | None = None) -> str:
    value = str(source)
    parsed = urlparse(value)
    if not parsed.scheme:
        if base and urlparse(base).scheme:
            return urljoin(base, value)
        return Path(value).expanduser().resolve().as_uri()
    if base:
        return urljoin(base, value)
    return value


def _validate_source_url(url: str, *, manifest_scheme: str | None = None) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"file", "https"}:
        raise LibraryError(f"Unsupported URL scheme for {url!r}; use HTTPS or file")
    if parsed.username or parsed.password:
        raise LibraryError("URLs containing embedded credentials are not allowed")
    if manifest_scheme == "https" and parsed.scheme != "https":
        raise LibraryError("An HTTPS manifest may not downgrade an artifact or update URL")
    if parsed.scheme == "file" and parsed.netloc not in {"", "localhost"}:
        raise LibraryError("Remote file URLs are not allowed")


def _file_path_from_url(url: str) -> Path:
    parsed = urlparse(url)
    return Path(url2pathname(unquote(parsed.path)))


def _fetch_to_path(
    source: str,
    destination: Path,
    *,
    max_bytes: int,
    client: httpx.Client | None = None,
) -> tuple[int, str, str]:
    """Stream a file/HTTPS source and return size, SHA-256, final URL."""
    _validate_source_url(source)
    parsed = urlparse(source)
    digest = hashlib.sha256()
    total = 0

    if parsed.scheme == "file":
        path = _file_path_from_url(source)
        if not path.is_file():
            raise SourceUnavailableError(f"Source not found: {path}")
        try:
            with path.open("rb") as src, destination.open("wb") as dst:
                while chunk := src.read(1024 * 1024):
                    total += len(chunk)
                    if total > max_bytes:
                        raise LibraryError(f"Source exceeds the {max_bytes}-byte limit")
                    digest.update(chunk)
                    dst.write(chunk)
        except OSError as exc:
            raise SourceUnavailableError(f"Could not read {path}: {exc}") from exc
        return total, digest.hexdigest(), source

    owns_client = client is None
    http_client = client or httpx.Client(timeout=httpx.Timeout(30.0, connect=10.0))
    current = source
    try:
        for redirect_count in range(MAX_REDIRECTS + 1):
            _validate_source_url(current, manifest_scheme="https")
            try:
                with http_client.stream("GET", current, follow_redirects=False) as response:
                    if response.status_code in {301, 302, 303, 307, 308}:
                        location = response.headers.get("location")
                        if not location:
                            raise SourceUnavailableError(
                                f"Redirect from {current} did not include a Location header"
                            )
                        if redirect_count == MAX_REDIRECTS:
                            raise SourceUnavailableError("Too many HTTPS redirects")
                        current = urljoin(current, location)
                        continue
                    try:
                        response.raise_for_status()
                    except httpx.HTTPStatusError as exc:
                        raise SourceUnavailableError(
                            f"Could not fetch {current}: HTTP {response.status_code}"
                        ) from exc
                    with destination.open("wb") as dst:
                        for chunk in response.iter_bytes():
                            total += len(chunk)
                            if total > max_bytes:
                                raise LibraryError(f"Source exceeds the {max_bytes}-byte limit")
                            digest.update(chunk)
                            dst.write(chunk)
                    return total, digest.hexdigest(), str(response.url)
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                raise SourceUnavailableError(f"Could not fetch {current}: {exc}") from exc
    finally:
        if owns_client:
            http_client.close()
    raise SourceUnavailableError("Too many HTTPS redirects")


def _fetch_bytes(
    source: str,
    *,
    max_bytes: int,
    client: httpx.Client | None = None,
) -> tuple[bytes, str]:
    with tempfile.TemporaryDirectory(prefix="sema-fetch-") as temporary:
        path = Path(temporary) / "download"
        _, _, final_url = _fetch_to_path(source, path, max_bytes=max_bytes, client=client)
        return path.read_bytes(), final_url


def _load_manifest(
    source: str | Path, *, client: httpx.Client | None = None
) -> tuple[LibraryManifest, bytes, str, str]:
    requested_url = _source_url(source)
    _validate_source_url(requested_url)
    raw, final_url = _fetch_bytes(requested_url, max_bytes=MAX_MANIFEST_BYTES, client=client)
    manifest = _parse_manifest(raw)

    manifest_scheme = urlparse(final_url).scheme
    for candidate in (
        _source_url(manifest.patterns.url, base=final_url),
        _source_url(manifest.update_url, base=final_url),
    ):
        _validate_source_url(candidate, manifest_scheme=manifest_scheme)
    return manifest, raw, requested_url, final_url


def _parse_manifest(raw: bytes) -> LibraryManifest:
    """Parse and validate strict manifest bytes without fetching any artifacts."""
    if len(raw) > MAX_MANIFEST_BYTES:
        raise LibraryError(f"Library manifest exceeds the {MAX_MANIFEST_BYTES}-byte limit")
    try:
        manifest = LibraryManifest.model_validate(_strict_json(raw, label="library manifest"))
    except ValidationError as exc:
        raise LibraryError(f"Invalid library manifest: {exc}") from exc
    if manifest.roots.semantic.scheme != SEMANTIC_ROOT_SCHEME:
        raise LibraryError(f"Unsupported semantic root scheme: {manifest.roots.semantic.scheme}")
    if manifest.roots.catalog.scheme != CATALOG_ROOT_SCHEME:
        raise LibraryError(f"Unsupported catalog root scheme: {manifest.roots.catalog.scheme}")
    return manifest


def _is_unsafe_zip_name(name: str) -> bool:
    if not name or "\\" in name or "\x00" in name:
        return True
    if any(ord(character) < 32 for character in name):
        return True
    if name.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", name):
        return True
    parts = name.split("/")
    return any(part in {"", ".", ".."} for part in parts if part != parts[-1] or part)


def _extract_patterns(archive_path: Path, destination: Path, expected_count: int) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=False)
    extracted: list[Path] = []
    seen_paths: set[str] = set()
    seen_casefolded: set[str] = set()
    total_uncompressed = 0

    try:
        archive = zipfile.ZipFile(archive_path)
    except (OSError, zipfile.BadZipFile) as exc:
        raise LibraryError(f"Pattern artifact is not a valid ZIP: {exc}") from exc

    with archive:
        for info in archive.infolist():
            name = info.filename
            if name == "patterns/" and info.is_dir():
                continue
            if _is_unsafe_zip_name(name):
                raise LibraryError(f"Unsafe path in pattern ZIP: {name!r}")
            if info.is_dir():
                raise LibraryError(f"Unexpected directory in pattern ZIP: {name!r}")
            mode = (info.external_attr >> 16) & 0o170000
            if mode and mode != stat.S_IFREG:
                raise LibraryError(f"Non-regular file in pattern ZIP: {name!r}")
            if info.flag_bits & 0x1:
                raise LibraryError(f"Encrypted ZIP member is not allowed: {name!r}")
            if info.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}:
                raise LibraryError(f"Unsupported ZIP compression for {name!r}")
            parts = name.split("/")
            if len(parts) != 2 or parts[0] != "patterns" or not parts[1].endswith(".json"):
                raise LibraryError("The pattern ZIP may contain only patterns/<Handle>.json files")
            handle = parts[1][:-5]
            if not _HANDLE_RE.fullmatch(handle):
                raise LibraryError(f"Invalid pattern filename in ZIP: {name!r}")
            if name in seen_paths or name.casefold() in seen_casefolded:
                raise LibraryError(f"Duplicate or case-colliding path in pattern ZIP: {name!r}")
            seen_paths.add(name)
            seen_casefolded.add(name.casefold())
            if info.file_size > MAX_PATTERN_BYTES:
                raise LibraryError(f"Pattern file exceeds {MAX_PATTERN_BYTES} bytes: {name}")
            total_uncompressed += info.file_size
            if total_uncompressed > MAX_UNCOMPRESSED_BYTES:
                raise LibraryError("Pattern ZIP expands beyond the allowed size")
            if info.file_size > max(4096, info.compress_size * MAX_COMPRESSION_RATIO):
                raise LibraryError(f"Suspicious compression ratio for {name!r}")
            if len(extracted) >= MAX_PATTERN_COUNT:
                raise LibraryError("Pattern ZIP contains too many files")

            output = destination / parts[1]
            try:
                with archive.open(info, "r") as src, output.open("xb") as dst:
                    copied = 0
                    while chunk := src.read(1024 * 1024):
                        copied += len(chunk)
                        if copied > MAX_PATTERN_BYTES:
                            raise LibraryError(
                                f"Pattern file exceeds size limit while reading: {name}"
                            )
                        dst.write(chunk)
            except LibraryError:
                raise
            except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
                raise LibraryError(f"Could not safely read ZIP member {name!r}: {exc}") from exc
            if copied != info.file_size:
                raise LibraryError(f"ZIP member size mismatch for {name!r}")
            extracted.append(output)

    if len(extracted) != expected_count:
        raise LibraryError(
            f"Pattern count mismatch: manifest declares {expected_count}, ZIP contains {len(extracted)}"
        )
    return sorted(extracted)


def _load_pattern_files(paths: list[Path]) -> dict[str, dict]:
    patterns: dict[str, dict] = {}
    casefolded: set[str] = set()
    for path in paths:
        pattern = _strict_json(path.read_bytes(), label=str(path))
        handle = pattern.get("handle")
        if not isinstance(handle, str):
            raise LibraryError(f"{path.name} does not declare a string handle")
        if path.stem != handle:
            raise LibraryError(
                f"Filename/handle mismatch: {path.name!r} contains handle {handle!r}"
            )
        if handle in patterns or handle.casefold() in casefolded:
            raise LibraryError(f"Duplicate or case-colliding pattern handle: {handle}")
        patterns[handle] = pattern
        casefolded.add(handle.casefold())
    return patterns


def verify_library_patterns(
    patterns: dict[str, dict], manifest: LibraryManifest
) -> VerifiedLibrary:
    """Validate one complete, self-contained library and recompute every identity."""
    if len(patterns) != manifest.pattern_count:
        raise LibraryError(
            f"Pattern count mismatch: expected {manifest.pattern_count}, found {len(patterns)}"
        )
    handles = set(patterns)
    errors: list[str] = []
    for handle in sorted(patterns):
        valid, pattern_errors, _warnings = validate_pattern(patterns[handle], known_handles=handles)
        if not valid:
            errors.extend(f"{handle}: {error}" for error in pattern_errors)
    if errors:
        raise LibraryError("Pattern validation failed:\n" + "\n".join(errors))

    try:
        validate_acyclic(patterns)
        validate_layer_direction(patterns)
        order = topological_sort(patterns)
    except ValueError as exc:
        raise LibraryError(f"Library graph validation failed: {exc}") from exc

    normalized: dict[str, dict] = {}
    computed_hashes: dict[str, str] = {}
    for handle in order:
        pattern = copy.deepcopy(patterns[handle])
        for dependency in sorted(get_dependencies_handles(pattern)):
            if dependency not in patterns:
                raise LibraryError(
                    f"{handle} depends on {dependency}, which is absent from this release"
                )

        dependencies = pattern.get("dependencies") or {}
        for category in ("accepts", "yields", "composes_with", "references"):
            for alias, supplied_ref in (dependencies.get(category) or {}).items():
                target = clean_handle(supplied_ref)
                expected_hash = computed_hashes.get(target or "")
                if not target or expected_hash is None:
                    raise LibraryError(
                        f"{handle}.{category}.{alias} does not resolve inside this release"
                    )
                expected_ref = f"sema:{target}#mh:SHA-256:{expected_hash}"
                if supplied_ref != expected_ref:
                    raise LibraryError(
                        f"{handle}.{category}.{alias} pins {supplied_ref!r}, "
                        f"but this release contains {expected_ref!r}"
                    )

        if pattern.get("extends"):
            target = clean_handle(pattern["extends"])
            expected_hash = computed_hashes.get(target or "")
            expected_ref = (
                f"sema:{target}#mh:SHA-256:{expected_hash}" if target and expected_hash else None
            )
            if not expected_ref or pattern["extends"] != expected_ref:
                raise LibraryError(
                    f"{handle}.extends does not pin the exact parent in this release"
                )

        try:
            identity = generate_sema_hash(pattern, computed_hashes.get)
        except ValueError as exc:
            raise LibraryError(f"Could not hash {handle}: {exc}") from exc
        supplied_id = pattern.get("sema_id")
        if supplied_id != identity["full_id"]:
            raise LibraryError(
                f"Identity mismatch for {handle}: expected {identity['full_id']}, "
                f"found {supplied_id!r}"
            )
        try:
            pattern_hash_from_sema_id(supplied_id, expected_handle=handle)
        except ValueError as exc:
            raise LibraryError(f"Invalid handle binding for {handle}: {exc}") from exc
        if "sema_ref" in pattern and pattern["sema_ref"] != identity["reference"]:
            raise LibraryError(f"sema_ref mismatch for {handle}")
        if "sema_stub" in pattern and pattern["sema_stub"] != identity["stub"]:
            raise LibraryError(f"sema_stub mismatch for {handle}")

        pattern["sema_id"] = identity["full_id"]
        pattern["sema_ref"] = identity["reference"]
        pattern["sema_stub"] = identity["stub"]
        normalized[handle] = pattern
        computed_hashes[handle] = identity["hash"]

    roots = vocabulary_roots((handle, computed_hashes[handle]) for handle in sorted(patterns))
    if roots["semantic_root"] != manifest.roots.semantic.sha256:
        raise LibraryError(
            "Semantic root mismatch: "
            f"expected {manifest.roots.semantic.sha256}, computed {roots['semantic_root']}"
        )
    if roots["catalog_root"] != manifest.roots.catalog.sha256:
        raise LibraryError(
            "Catalog root mismatch: "
            f"expected {manifest.roots.catalog.sha256}, computed {roots['catalog_root']}"
        )
    return VerifiedLibrary(normalized, order, roots)


def _database_patterns(path: Path) -> dict[str, dict]:
    uri = f"{path.expanduser().resolve().as_uri()}?mode=ro"
    try:
        connection = sqlite3.connect(uri, uri=True)
    except sqlite3.Error as exc:
        raise LibraryError(f"Could not open compiled database: {exc}") from exc
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()
        if not integrity or integrity[0] != "ok":
            raise LibraryError(f"Compiled database integrity check failed: {integrity}")
        foreign_keys = connection.execute("PRAGMA foreign_key_check").fetchall()
        if foreign_keys:
            raise LibraryError("Compiled database contains broken foreign-key references")

        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        if not {"nodes", "edges"} <= tables:
            raise LibraryError("Compiled database does not use the sema-sqlite-v1 schema")
        node_columns = {row[1] for row in connection.execute("PRAGMA table_info(nodes)").fetchall()}
        edge_columns = {row[1] for row in connection.execute("PRAGMA table_info(edges)").fetchall()}
        if not {"id", "node_type", "text", "metadata", "embedding"} <= node_columns:
            raise LibraryError("Compiled database has incompatible node columns")
        if not {"id", "source_id", "target_id", "edge_type", "alias", "metadata"} <= edge_columns:
            raise LibraryError("Compiled database has incompatible edge columns")

        indexes = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='index'"
            ).fetchall()
        }
        required_indexes = {"idx_nodes_type", "idx_edges_source", "idx_edges_target"}
        missing_indexes = sorted(required_indexes - indexes)
        if missing_indexes:
            raise LibraryError(
                "Compiled database is missing required indexes: " + ", ".join(missing_indexes)
            )

        # GraphStore loads every node and edge, not just Pattern Cards. Validate
        # the complete read model so a damaged local snapshot cannot pass corpus
        # verification and then fail only after it becomes active.
        from ..taxonomy_graph.graph_store import EdgeType, NodeType

        valid_node_types = {member.value for member in NodeType}
        valid_edge_types = {member.value for member in EdgeType}
        node_ids: set[str] = set()
        for node_id, node_type, metadata_json, embedding in connection.execute(
            "SELECT id, node_type, metadata, embedding FROM nodes"
        ).fetchall():
            if not isinstance(node_id, str) or not node_id:
                raise LibraryError("Compiled database contains an invalid node ID")
            if node_id in node_ids:
                raise LibraryError(f"Compiled database contains duplicate node ID {node_id!r}")
            node_ids.add(node_id)
            if node_type not in valid_node_types:
                raise LibraryError(f"Compiled database contains unknown node type {node_type!r}")
            try:
                metadata = json.loads(metadata_json)
            except (TypeError, json.JSONDecodeError) as exc:
                raise LibraryError(f"Compiled node {node_id!r} has invalid metadata") from exc
            if not isinstance(metadata, dict):
                raise LibraryError(f"Compiled node {node_id!r} metadata must be an object")
            if embedding is not None and len(embedding) % 4:
                raise LibraryError(f"Compiled node {node_id!r} has an invalid embedding")

        for edge_id, source_id, target_id, edge_type, metadata_json in connection.execute(
            "SELECT id, source_id, target_id, edge_type, metadata FROM edges"
        ).fetchall():
            if not isinstance(edge_id, str) or not edge_id:
                raise LibraryError("Compiled database contains an invalid edge ID")
            if source_id not in node_ids or target_id not in node_ids:
                raise LibraryError(f"Compiled edge {edge_id!r} has a missing endpoint")
            if edge_type not in valid_edge_types:
                raise LibraryError(f"Compiled database contains unknown edge type {edge_type!r}")
            try:
                metadata = json.loads(metadata_json)
            except (TypeError, json.JSONDecodeError) as exc:
                raise LibraryError(f"Compiled edge {edge_id!r} has invalid metadata") from exc
            if not isinstance(metadata, dict):
                raise LibraryError(f"Compiled edge {edge_id!r} metadata must be an object")

        rows = connection.execute(
            "SELECT id, text, metadata FROM nodes WHERE node_type='PATTERN'"
        ).fetchall()
        node_handles: dict[str, str] = {}
        patterns: dict[str, dict] = {}
        for node_id, handle, metadata_json in rows:
            if handle in patterns:
                raise LibraryError(f"Compiled database contains duplicate handle {handle!r}")
            try:
                metadata = json.loads(metadata_json)
            except (TypeError, json.JSONDecodeError) as exc:
                raise LibraryError(f"Invalid metadata for compiled pattern {handle!r}") from exc
            pattern = metadata.get("pattern") if isinstance(metadata, dict) else None
            if not isinstance(pattern, dict):
                raise LibraryError(f"Compiled pattern {handle!r} has no pattern metadata")
            if pattern.get("handle") != handle:
                raise LibraryError(
                    f"Compiled pattern node {handle!r} embeds handle {pattern.get('handle')!r}"
                )
            if "dependencies" in pattern:
                raise LibraryError(
                    f"Compiled pattern {handle!r} stores dependencies outside graph edges"
                )
            pattern = copy.deepcopy(pattern)
            pattern["handle"] = handle
            patterns[handle] = pattern
            node_handles[node_id] = handle

        dependency_types = {
            "ACCEPTS": "accepts",
            "YIELDS": "yields",
            "COMPOSES_WITH": "composes_with",
            "REFERENCES": "references",
        }
        dependencies_by_handle: dict[str, dict[str, dict[str, str]]] = {}
        edge_rows = connection.execute(
            "SELECT source_id, target_id, edge_type, alias FROM edges "
            "WHERE edge_type IN ('ACCEPTS','YIELDS','COMPOSES_WITH','REFERENCES')"
        ).fetchall()
        for source_id, target_id, edge_type, alias in edge_rows:
            source_handle = node_handles.get(source_id)
            target_handle = node_handles.get(target_id)
            if not source_handle or not target_handle or not isinstance(alias, str) or not alias:
                raise LibraryError("Compiled database contains an invalid dependency edge")
            target_id_value = patterns[target_handle].get("sema_id")
            category = dependency_types[edge_type]
            bucket = dependencies_by_handle.setdefault(source_handle, {}).setdefault(category, {})
            if alias in bucket:
                raise LibraryError(
                    f"Compiled database contains duplicate dependency alias {source_handle}.{alias}"
                )
            bucket[alias] = target_id_value
        for handle, dependencies in dependencies_by_handle.items():
            patterns[handle]["dependencies"] = dependencies
        return patterns
    except sqlite3.Error as exc:
        raise LibraryError(f"Could not validate compiled database: {exc}") from exc
    finally:
        connection.close()


def _comparable_pattern(pattern: dict) -> dict:
    result = copy.deepcopy(pattern)
    result.pop("sema_layer", None)
    result.pop("sema_category", None)
    return result


def verify_library_database(
    path: Path, verified: VerifiedLibrary, manifest: LibraryManifest
) -> None:
    """Verify a compiled DB against canonical JSON, including fresh hashes."""
    db_patterns = _database_patterns(path)
    db_verified = verify_library_patterns(db_patterns, manifest)
    if set(db_verified.patterns) != set(verified.patterns):
        raise LibraryError("Compiled database pattern set differs from canonical JSON")
    for handle in verified.patterns:
        if _comparable_pattern(db_verified.patterns[handle]) != _comparable_pattern(
            verified.patterns[handle]
        ):
            raise LibraryError(
                f"Compiled database definition for {handle} differs from canonical JSON"
            )


def verify_installed_library(record: dict[str, Any]) -> dict[str, Any]:
    """Recompute a managed DB's identities before it becomes active."""
    path = Path(str(record.get("path", ""))).expanduser()
    if not path.is_file():
        raise LibraryError(f"Installed library database is missing: {path}")
    required = ("name", "version", "semantic_root", "catalog_root", "pattern_count")
    missing = [field for field in required if record.get(field) in {None, ""}]
    if missing:
        raise LibraryError(f"Installed library record is missing: {', '.join(missing)}")
    manifest = LibraryManifest(
        manifest_schema=1,
        name=str(record["name"]),
        version=str(record["version"]),
        update_url=str(record.get("update_url") or path.as_uri()),
        patterns=PatternArtifact(
            format=PATTERN_ARCHIVE_FORMAT,
            url=path.as_uri(),
            sha256=str(record.get("artifact_sha256") or "0" * 64),
            size_bytes=1,
        ),
        roots=LibraryRoots(
            semantic=RootDescriptor(
                scheme=str(record.get("semantic_root_scheme") or SEMANTIC_ROOT_SCHEME),
                sha256=str(record["semantic_root"]),
            ),
            catalog=RootDescriptor(
                scheme=str(record.get("catalog_root_scheme") or CATALOG_ROOT_SCHEME),
                sha256=str(record["catalog_root"]),
            ),
        ),
        pattern_count=int(record["pattern_count"]),
    )
    patterns = _database_patterns(path)
    verified = verify_library_patterns(patterns, manifest)
    return verified.roots


def build_library_database(verified: VerifiedLibrary, destination: Path) -> None:
    """Compile verified JSON into a fresh SQLite runtime without touching source files."""
    from ..taxonomy_graph.graph_store import GraphStore

    store = GraphStore(str(destination), enable_embeddings=False)
    handles = set(verified.patterns)
    for handle in verified.order:
        candidate = copy.deepcopy(verified.patterns[handle])
        result = mint_pattern(
            candidate,
            store,
            known_handles=handles,
            skip_cascade=True,
            validated_extends_batch=True,
        )
        if not result.success:
            raise LibraryError(f"Could not compile {handle}: {'; '.join(result.errors)}")
        if result.sema_id != verified.patterns[handle]["sema_id"]:
            raise LibraryError(f"Compiler identity mismatch for {handle}")

    # A second pass links signatures whose targets were not hard dependencies;
    # exact-text matching reuses the first pass's facet nodes when embeddings are off.
    for handle in verified.order:
        candidate = copy.deepcopy(verified.patterns[handle])
        result = mint_pattern(
            candidate,
            store,
            known_handles=handles,
            skip_cascade=True,
            validated_extends_batch=True,
        )
        if not result.success or result.sema_id != verified.patterns[handle]["sema_id"]:
            raise LibraryError(f"Could not finalize compiled graph for {handle}")
    store.sweep_related_edges()
    del store
    verify_library_database(destination, verified, _manifest_for_verified(verified))


def _manifest_for_verified(verified: VerifiedLibrary) -> LibraryManifest:
    """Create an identity-only manifest used for post-build corpus verification."""
    return LibraryManifest(
        manifest_schema=1,
        name="verification",
        version="0.0.0",
        update_url=Path.cwd().as_uri(),
        patterns=PatternArtifact(
            format=PATTERN_ARCHIVE_FORMAT,
            url=Path.cwd().as_uri(),
            sha256="0" * 64,
            size_bytes=1,
        ),
        roots=LibraryRoots(
            semantic=RootDescriptor(
                scheme=SEMANTIC_ROOT_SCHEME, sha256=verified.roots["semantic_root"]
            ),
            catalog=RootDescriptor(
                scheme=CATALOG_ROOT_SCHEME, sha256=verified.roots["catalog_root"]
            ),
        ),
        pattern_count=len(verified.patterns),
    )


def github_release_urls(repository: str, name: str, version: str) -> tuple[str, str]:
    """Return the stable manifest and version-pinned artifact URLs for a GitHub release."""
    repository = repository.strip().strip("/")
    if not _GITHUB_REPOSITORY_RE.fullmatch(repository):
        raise LibraryError("GitHub repository must use OWNER/REPOSITORY form")
    if any(part in {".", ".."} for part in repository.split("/")):
        raise LibraryError("GitHub repository contains an unsafe path segment")
    if not _LIBRARY_NAME_RE.fullmatch(name):
        raise LibraryError("Library name must be a lowercase path-safe slug, such as 'defi'")
    if not _VERSION_RE.fullmatch(version):
        raise LibraryError("Library version must use MAJOR.MINOR.PATCH, such as '1.0.0'")

    archive_name = f"{name}-patterns-{version}.zip"
    base = f"https://github.com/{repository}/releases"
    return (
        f"{base}/latest/download/library.json",
        f"{base}/download/v{version}/{archive_name}",
    )


def _publication_archive_name(update_url: str, artifact_url: str) -> str:
    """Validate publication URLs and return the artifact's local filename."""
    parsed_update = urlparse(update_url)
    if parsed_update.scheme != "https" or not parsed_update.hostname:
        raise LibraryError("Publication update URL must be an absolute HTTPS URL")
    _validate_source_url(update_url)
    parsed_artifact = urlparse(artifact_url)
    if parsed_artifact.scheme != "https" or not parsed_artifact.hostname:
        raise LibraryError("Publication artifact URL must be an absolute HTTPS URL")
    _validate_source_url(artifact_url, manifest_scheme=parsed_update.scheme)
    archive_name = Path(unquote(parsed_artifact.path)).name
    if not _ARCHIVE_FILENAME_RE.fullmatch(archive_name):
        raise LibraryError(
            "Pattern artifact URL must end in a path-safe .zip filename, "
            "such as 'defi-patterns-1.0.0.zip'"
        )
    return archive_name


def _release_json_bytes(value: dict[str, Any]) -> bytes:
    """Serialize portable release JSON deterministically."""
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def _write_pattern_archive(path: Path, pattern_bytes: dict[str, bytes]) -> None:
    """Write one deterministic, portable ZIP member per pattern."""
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as archive:
        for handle, raw in sorted(pattern_bytes.items()):
            info = zipfile.ZipInfo(f"patterns/{handle}.json", date_time=_FIXED_ZIP_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, raw)


def verify_library_package(
    manifest_path: str | Path,
    archive_path: str | Path | None = None,
) -> VerifiedLibrary:
    """Verify local release files through the same corpus/compiler path as install.

    A publisher normally declares an HTTPS artifact URL that is not live until
    after upload. ``archive_path`` lets the producer verify those exact local
    bytes before publication without weakening or rewriting the manifest.
    """
    manifest_file = Path(manifest_path).expanduser().resolve()
    if not manifest_file.is_file():
        raise LibraryError(f"Library manifest not found: {manifest_file}")
    manifest = _parse_manifest(manifest_file.read_bytes())
    _publication_archive_name(manifest.update_url, manifest.patterns.url)

    if archive_path is None:
        declared = _source_url(manifest.patterns.url, base=manifest_file.as_uri())
        if urlparse(declared).scheme != "file":
            raise LibraryError("archive_path is required when the manifest declares a remote URL")
        archive_file = _file_path_from_url(declared)
    else:
        archive_file = Path(archive_path).expanduser().resolve()
    if not archive_file.is_file():
        raise LibraryError(f"Pattern artifact not found: {archive_file}")

    size = archive_file.stat().st_size
    if size > MAX_ARCHIVE_BYTES:
        raise LibraryError(f"Pattern artifact exceeds the {MAX_ARCHIVE_BYTES}-byte limit")
    if size != manifest.patterns.size_bytes:
        raise LibraryError(
            f"Pattern artifact size mismatch: expected {manifest.patterns.size_bytes}, got {size}"
        )
    digest = hashlib.sha256(archive_file.read_bytes()).hexdigest()
    if digest != manifest.patterns.sha256:
        raise LibraryError(
            f"Pattern artifact SHA-256 mismatch: expected {manifest.patterns.sha256}, got {digest}"
        )

    with tempfile.TemporaryDirectory(prefix="sema-verify-package-") as temporary:
        root = Path(temporary)
        pattern_dir = root / "patterns"
        paths = _extract_patterns(archive_file, pattern_dir, manifest.pattern_count)
        source_bytes = {path.name: path.read_bytes() for path in paths}
        patterns = _load_pattern_files(paths)
        verified = verify_library_patterns(patterns, manifest)
        database = root / "taxonomy.db"
        build_library_database(verified, database)
        verify_library_database(database, verified, manifest)
        for path in paths:
            if path.read_bytes() != source_bytes[path.name]:
                raise LibraryError(f"Compiler modified canonical source file {path.name}")
    return verified


def package_library(
    source_db: str | Path,
    output_dir: str | Path,
    *,
    name: str,
    version: str,
    update_url: str,
    artifact_url: str,
) -> LibraryPackage:
    """Export a project DB as a deterministic, locally verified library release."""
    source = Path(source_db).expanduser().resolve()
    if not source.is_file():
        raise LibraryError(f"Source database not found: {source}")
    archive_name = _publication_archive_name(update_url, artifact_url)
    patterns = _database_patterns(source)
    if not patterns:
        raise LibraryError("Cannot package an empty vocabulary")

    pattern_bytes = {
        handle: _release_json_bytes(pattern) for handle, pattern in sorted(patterns.items())
    }
    try:
        bindings = [
            (
                handle,
                pattern_hash_from_sema_id(pattern["sema_id"], expected_handle=handle),
            )
            for handle, pattern in sorted(patterns.items())
        ]
    except (KeyError, TypeError, ValueError) as exc:
        raise LibraryError(f"Source database contains an invalid pattern identity: {exc}") from exc
    roots = vocabulary_roots(bindings)

    destination = Path(output_dir).expanduser().resolve()
    if destination.exists():
        raise LibraryError(f"Refusing to overwrite existing output directory: {destination}")
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise LibraryError(f"Could not create output parent {destination.parent}: {exc}") from exc

    lock_path = destination.parent / f".{destination.name}.sema-package.lock"
    try:
        lock_path.mkdir()
    except FileExistsError as exc:
        raise LibraryError(
            f"Another package operation is using {destination}, or a stale lock remains at "
            f"{lock_path}"
        ) from exc
    except OSError as exc:
        raise LibraryError(f"Could not reserve output directory {destination}: {exc}") from exc

    final_manifest = destination / "library.json"
    final_archive = destination / archive_name
    staging: Path | None = None
    try:
        # Recheck after taking the reservation so concurrent package commands
        # cannot both proceed from the same initial absence check.
        if destination.exists():
            raise LibraryError(f"Refusing to overwrite existing output directory: {destination}")
        staging = Path(
            tempfile.mkdtemp(
                prefix=f".{destination.name}.sema-package-",
                dir=destination.parent,
            )
        )
        staged_archive = staging / archive_name
        _write_pattern_archive(staged_archive, pattern_bytes)
        archive_bytes = staged_archive.read_bytes()
        manifest_data = {
            "manifest_schema": MANIFEST_SCHEMA,
            "name": name,
            "version": version,
            "update_url": update_url,
            "patterns": {
                "format": PATTERN_ARCHIVE_FORMAT,
                "url": artifact_url,
                "sha256": hashlib.sha256(archive_bytes).hexdigest(),
                "size_bytes": len(archive_bytes),
            },
            "roots": {
                "semantic": {
                    "scheme": SEMANTIC_ROOT_SCHEME,
                    "sha256": roots["semantic_root"],
                },
                "catalog": {
                    "scheme": CATALOG_ROOT_SCHEME,
                    "sha256": roots["catalog_root"],
                },
            },
            "pattern_count": len(patterns),
        }
        staged_manifest = staging / "library.json"
        staged_manifest.write_bytes(_release_json_bytes(manifest_data))

        # This re-reads the ZIP, recomputes identities/roots, compiles a fresh
        # SQLite read model, and verifies that model exactly as installation does.
        verified = verify_library_package(staged_manifest, staged_archive)
        try:
            # The complete directory becomes visible in one same-filesystem
            # rename, so readers never observe a mismatched manifest/ZIP pair.
            os.rename(staging, destination)
        except OSError as exc:
            raise LibraryError(
                f"Could not finalize package directory {destination}: {exc}"
            ) from exc
        staging = None
    finally:
        if staging is not None:
            shutil.rmtree(staging, ignore_errors=True)
        try:
            lock_path.rmdir()
        except FileNotFoundError:
            pass
        except OSError:
            # A stale reservation is safer than allowing a concurrent writer to
            # interleave another release with an uncertain finalization state.
            pass

    return LibraryPackage(
        manifest_path=final_manifest,
        archive_path=final_archive,
        semantic_root=verified.roots["semantic_root"],
        catalog_root=verified.roots["catalog_root"],
        pattern_count=len(verified.patterns),
    )


def _version_tuple(version: str) -> tuple[int, int, int]:
    return tuple(int(part) for part in version.split("."))  # type: ignore[return-value]


def _same_version_release_changed(existing: dict[str, Any], manifest: LibraryManifest) -> bool:
    """Detect immutable-release changes, including unhashed metadata/package bytes."""
    expected = {
        "semantic_root": manifest.roots.semantic.sha256,
        "catalog_root": manifest.roots.catalog.sha256,
        "artifact_sha256": manifest.patterns.sha256,
        "pattern_count": manifest.pattern_count,
    }
    return any(existing.get(field) != value for field, value in expected.items())


def _install_loaded_manifest(
    manifest: LibraryManifest,
    manifest_bytes: bytes,
    requested_url: str,
    final_manifest_url: str,
    *,
    data_dir: str | Path | None,
    client: httpx.Client | None,
    allow_update: bool,
    register_release: bool = True,
) -> dict[str, Any]:
    existing = get_library(manifest.name)
    expected_catalog = manifest.roots.catalog.sha256
    if existing:
        if existing.get("version") == manifest.version:
            if _same_version_release_changed(existing, manifest):
                raise LibraryError(
                    f"{manifest.name} {manifest.version} was republished with different content"
                )
            if Path(existing.get("path", "")).is_file():
                verify_installed_library(existing)
                return existing
        elif not allow_update:
            raise LibraryError(
                f"Library {manifest.name!r} is already installed; use `sema update {manifest.name}`"
            )

    root = library_data_dir(data_dir)
    releases_dir = root / manifest.name / "releases"
    releases_dir.mkdir(parents=True, exist_ok=True)
    final_dir = releases_dir / f"{manifest.version}-{expected_catalog[:16]}"
    staging_dir = Path(
        tempfile.mkdtemp(prefix=f".install-{uuid.uuid4().hex[:8]}-", dir=releases_dir)
    )
    try:
        (staging_dir / "library.json").write_bytes(manifest_bytes)
        archive_path = staging_dir / "patterns.zip"
        archive_url = _source_url(manifest.patterns.url, base=final_manifest_url)
        size, digest, _ = _fetch_to_path(
            archive_url,
            archive_path,
            max_bytes=min(MAX_ARCHIVE_BYTES, manifest.patterns.size_bytes),
            client=client,
        )
        if size != manifest.patterns.size_bytes:
            raise LibraryError(
                f"Pattern artifact size mismatch: expected {manifest.patterns.size_bytes}, got {size}"
            )
        if digest != manifest.patterns.sha256:
            raise LibraryError(
                f"Pattern artifact SHA-256 mismatch: expected {manifest.patterns.sha256}, got {digest}"
            )

        pattern_dir = staging_dir / "patterns"
        paths = _extract_patterns(archive_path, pattern_dir, manifest.pattern_count)
        source_bytes = {path.name: path.read_bytes() for path in paths}
        patterns = _load_pattern_files(paths)
        verified = verify_library_patterns(patterns, manifest)

        db_path = staging_dir / "taxonomy.db"
        build_library_database(verified, db_path)
        verify_library_database(db_path, verified, manifest)
        for path in paths:
            if path.read_bytes() != source_bytes[path.name]:
                raise LibraryError(f"Compiler modified canonical source file {path.name}")

        update_url = _source_url(manifest.update_url, base=final_manifest_url)
        record: dict[str, Any] = {
            "name": manifest.name,
            "path": str(final_dir / "taxonomy.db"),
            "kind": "installed-library",
            "read_only": True,
            "version": manifest.version,
            "manifest_url": final_manifest_url,
            "requested_manifest_url": requested_url,
            "update_url": update_url,
            "artifact_sha256": manifest.patterns.sha256,
            "semantic_root": verified.roots["semantic_root"],
            "semantic_root_scheme": verified.roots["semantic_root_scheme"],
            "catalog_root": verified.roots["catalog_root"],
            "catalog_root_scheme": verified.roots["catalog_root_scheme"],
            "pattern_count": len(verified.patterns),
            "database_source": "generated",
        }
        (staging_dir / "install.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

        if final_dir.exists():
            verify_library_database(final_dir / "taxonomy.db", verified, manifest)
            shutil.rmtree(staging_dir)
        else:
            os.replace(staging_dir, final_dir)
        final_db = final_dir / "taxonomy.db"
        try:
            final_db.chmod(0o444)
        except OSError:
            pass
        record["path"] = str(final_db)
        if register_release:
            register_library(record)
        return record
    except Exception:
        if staging_dir.exists():
            shutil.rmtree(staging_dir, ignore_errors=True)
        raise


def install_library(
    manifest_source: str | Path,
    *,
    data_dir: str | Path | None = None,
    http_client: httpx.Client | None = None,
) -> dict[str, Any]:
    """Install and register a verified release without changing the active library."""
    manifest, raw, requested_url, final_url = _load_manifest(manifest_source, client=http_client)
    return _install_loaded_manifest(
        manifest,
        raw,
        requested_url,
        final_url,
        data_dir=data_dir,
        client=http_client,
        allow_update=False,
    )


def update_library(
    name: str,
    *,
    data_dir: str | Path | None = None,
    http_client: httpx.Client | None = None,
) -> tuple[dict[str, Any], bool]:
    """Fetch a library's recorded update pointer and atomically install a newer release."""
    existing = get_library(name)
    if not existing:
        raise LibraryError(f"Library {name!r} is not installed")
    update_url = existing.get("update_url")
    if not update_url:
        raise LibraryError(f"Library {name!r} has no update URL")
    manifest, raw, requested_url, final_url = _load_manifest(update_url, client=http_client)
    if manifest.name.casefold() != name.casefold():
        raise LibraryError(
            f"Update pointer for {name!r} returned a different library: {manifest.name!r}"
        )
    old_version = str(existing.get("version", "0.0.0"))
    if _version_tuple(manifest.version) < _version_tuple(old_version):
        raise LibraryError(
            f"Update pointer attempts to downgrade {name} from {old_version} to {manifest.version}"
        )
    if manifest.version == old_version:
        if _same_version_release_changed(existing, manifest):
            raise LibraryError(f"{name} {old_version} was republished with different content")
        verify_installed_library(existing)
        return existing, False

    old_path = str(existing.get("path", ""))
    configured_active = get_configured_active_db()
    record = _install_loaded_manifest(
        manifest,
        raw,
        requested_url,
        final_url,
        data_dir=data_dir,
        client=http_client,
        allow_update=True,
        register_release=False,
    )
    try:
        register_library(record)
        if configured_active == old_path:
            set_active_db(record["path"])
    except Exception as exc:
        try:
            register_library(existing)
        except Exception as rollback_exc:
            raise LibraryError(
                "Update failed and the previous registry record could not be restored: "
                f"{rollback_exc}"
            ) from exc
        raise
    return record, True
