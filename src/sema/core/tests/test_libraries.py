"""Focused install/update coverage for manifest-driven vocabulary libraries."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sqlite3
import stat
import zipfile
from dataclasses import dataclass
from pathlib import Path

import httpx
import pytest
from pydantic import ValidationError

from sema.cli.main import install_remote_library, undo_pull, update_remote_library, use_db
from sema.core.hashing import (
    CATALOG_ROOT_SCHEME,
    SEMANTIC_ROOT_SCHEME,
    generate_sema_hash,
    pattern_hash_from_sema_id,
    vocabulary_roots,
)
from sema.core.libraries import (
    DATABASE_FORMAT,
    DATABASE_SCHEMA_VERSION,
    LibraryError,
    LibraryManifest,
    install_library,
    update_library,
    verify_installed_library,
    verify_library_patterns,
)
from sema.core.registry import get_configured_active_db, get_library, set_active_db


@dataclass(frozen=True)
class Release:
    manifest_path: Path
    archive_path: Path
    patterns: dict[str, dict]
    pattern_bytes: dict[str, bytes]
    roots: dict[str, object]


def _with_identity(pattern: dict, known_hashes: dict[str, str]) -> tuple[dict, str]:
    result = copy.deepcopy(pattern)
    identity = generate_sema_hash(result, known_hashes.get)
    result["sema_id"] = identity["full_id"]
    result["sema_ref"] = identity["reference"]
    result["sema_stub"] = identity["stub"]
    return result, identity["hash"]


def _defi_patterns(*, guard_revision: str = "") -> dict[str, dict]:
    hashes: dict[str, str] = {}
    asset_price, hashes["AssetPrice"] = _with_identity(
        {
            "handle": "AssetPrice",
            "gloss": "A quoted value for one asset",
            "mechanism": "Carries a quoted monetary value for an identified asset.",
            "invariants": ["The quote identifies both its asset and valuation unit."],
            "_meta": {
                "path": ["Infrastructure", "Primitives"],
                "ring": 0,
                "tier": 0,
            },
        },
        hashes,
    )
    liquidation_guard, hashes["LiquidationGuard"] = _with_identity(
        {
            "handle": "LiquidationGuard",
            "gloss": "Reject unsafe liquidation decisions",
            "mechanism": (
                "Checks a position against the exact {{asset_price}} before liquidation"
                f"{guard_revision}."
            ),
            "invariants": ["A liquidation decision uses the pinned asset-price definition."],
            "dependencies": {
                "accepts": {"asset_price": ("sema:AssetPrice#mh:SHA-256:" + hashes["AssetPrice"])}
            },
            "_meta": {
                "path": ["Society", "Economics"],
                "ring": 1,
                "tier": 1,
            },
        },
        hashes,
    )
    return {
        "AssetPrice": asset_price,
        "LiquidationGuard": liquidation_guard,
    }


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _write_zip(
    archive_path: Path,
    pattern_bytes: dict[str, bytes],
    *,
    extra_members: dict[str, bytes] | None = None,
) -> None:
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for handle, raw in sorted(pattern_bytes.items()):
            info = zipfile.ZipInfo(f"patterns/{handle}.json")
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, raw)
        for name, raw in (extra_members or {}).items():
            archive.writestr(name, raw)


def _write_release(
    directory: Path,
    *,
    version: str = "1.0.0",
    patterns: dict[str, dict] | None = None,
    update_path: Path | None = None,
    database: dict | None = None,
    extra_members: dict[str, bytes] | None = None,
) -> Release:
    directory.mkdir(parents=True, exist_ok=True)
    patterns = copy.deepcopy(patterns or _defi_patterns())
    pattern_bytes = {handle: _json_bytes(pattern) for handle, pattern in patterns.items()}
    archive_path = directory / "patterns.zip"
    _write_zip(archive_path, pattern_bytes, extra_members=extra_members)

    bindings = [
        (
            handle,
            pattern_hash_from_sema_id(pattern["sema_id"], expected_handle=handle),
        )
        for handle, pattern in sorted(patterns.items())
    ]
    roots = vocabulary_roots(bindings)
    manifest_path = directory / "library.json"
    manifest = {
        "manifest_schema": 1,
        "name": "defi",
        "version": version,
        "update_url": (update_path or manifest_path).resolve().as_uri(),
        "patterns": {
            "format": "sema-patterns-zip-v1",
            "url": archive_path.resolve().as_uri(),
            "sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
            "size_bytes": archive_path.stat().st_size,
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
    if database is not None:
        manifest["database"] = database
    manifest_path.write_bytes(_json_bytes(manifest))
    return Release(manifest_path, archive_path, patterns, pattern_bytes, roots)


@pytest.fixture
def library_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    home = tmp_path / "home"
    home.mkdir()
    data_dir = tmp_path / "library-data"
    original_db = tmp_path / "original.db"
    original_db.write_bytes(b"active-before-library-install")

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("SEMA_LIBRARY_DIR", str(data_dir))
    monkeypatch.delenv("SEMA_DB_PATH", raising=False)
    set_active_db(str(original_db))
    return {
        "home": home,
        "data_dir": data_dir,
        "original_db": original_db,
        "active_file": home / ".config" / "sema" / "active_db",
        "registry_file": home / ".config" / "sema" / "databases.json",
    }


def _bytes_if_present(path: Path) -> bytes | None:
    return path.read_bytes() if path.exists() else None


def test_file_install_preserves_source_and_active_and_can_use_by_name(
    tmp_path: Path, library_environment: dict[str, Path]
) -> None:
    release = _write_release(tmp_path / "release")
    active_before = library_environment["active_file"].read_bytes()

    manifest = LibraryManifest.model_validate(json.loads(release.manifest_path.read_text()))
    verified_source = verify_library_patterns(release.patterns, manifest)
    assert verified_source.roots["semantic_root"] == release.roots["semantic_root"]
    assert verified_source.roots["catalog_root"] == release.roots["catalog_root"]

    assert install_remote_library(str(release.manifest_path))
    assert library_environment["active_file"].read_bytes() == active_before

    record = get_library("defi")
    assert record is not None
    assert record["version"] == "1.0.0"
    assert record["database_source"] == "generated"
    assert record["semantic_root"] == release.roots["semantic_root"]
    assert record["catalog_root"] == release.roots["catalog_root"]

    installed_patterns = Path(record["path"]).parent / "patterns"
    for filename, original in release.pattern_bytes.items():
        assert (installed_patterns / f"{filename}.json").read_bytes() == original

    verified_db = verify_installed_library(record)
    assert verified_db["semantic_root"] == release.roots["semantic_root"]
    assert verified_db["catalog_root"] == release.roots["catalog_root"]

    assert use_db("defi")
    assert get_configured_active_db() == record["path"]


def test_https_latest_release_redirect_installs_relative_artifact(
    tmp_path: Path, library_environment: dict[str, Path]
) -> None:
    release = _write_release(tmp_path / "https-release")
    manifest = json.loads(release.manifest_path.read_text())
    manifest["update_url"] = "https://github.test/releases/latest/download/library.json"
    manifest["patterns"]["url"] = "patterns.zip"
    manifest_bytes = _json_bytes(manifest)
    archive_bytes = release.archive_path.read_bytes()

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/releases/latest/download/library.json":
            return httpx.Response(
                302,
                headers={"location": "/releases/download/v1.0.0/library.json"},
                request=request,
            )
        if request.url.path == "/releases/download/v1.0.0/library.json":
            return httpx.Response(200, content=manifest_bytes, request=request)
        if request.url.path == "/releases/download/v1.0.0/patterns.zip":
            return httpx.Response(200, content=archive_bytes, request=request)
        return httpx.Response(404, request=request)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        record = install_library(
            "https://github.test/releases/latest/download/library.json",
            data_dir=library_environment["data_dir"],
            http_client=client,
        )

    assert record["manifest_url"] == ("https://github.test/releases/download/v1.0.0/library.json")
    assert record["update_url"] == ("https://github.test/releases/latest/download/library.json")
    assert verify_installed_library(record)["catalog_root"] == release.roots["catalog_root"]


@pytest.mark.parametrize(
    ("field_path", "invalid_value"),
    [(("pattern_count",), True), (("patterns", "size_bytes"), "123")],
)
def test_manifest_does_not_coerce_types(
    tmp_path: Path,
    field_path: tuple[str, ...],
    invalid_value: object,
) -> None:
    release = _write_release(tmp_path / "strict-manifest")
    manifest = json.loads(release.manifest_path.read_text())
    target = manifest
    for field in field_path[:-1]:
        target = target[field]
    target[field_path[-1]] = invalid_value

    with pytest.raises(ValidationError):
        LibraryManifest.model_validate(manifest)


def test_tampered_zip_fails_without_registry_or_active_change(
    tmp_path: Path, library_environment: dict[str, Path]
) -> None:
    release = _write_release(tmp_path / "tampered")
    release.archive_path.write_bytes(release.archive_path.read_bytes() + b"tamper")
    registry_before = _bytes_if_present(library_environment["registry_file"])
    active_before = library_environment["active_file"].read_bytes()

    with pytest.raises(LibraryError, match="exceeds|SHA-256 mismatch"):
        install_library(release.manifest_path, data_dir=library_environment["data_dir"])

    assert _bytes_if_present(library_environment["registry_file"]) == registry_before
    assert library_environment["active_file"].read_bytes() == active_before
    assert get_library("defi") is None


@pytest.mark.parametrize("defect", ["missing-dependency", "stale-id"])
def test_invalid_dependency_or_identity_fails_closed(
    tmp_path: Path, library_environment: dict[str, Path], defect: str
) -> None:
    patterns = _defi_patterns()
    if defect == "missing-dependency":
        del patterns["AssetPrice"]
        expected_error = "MISSING DEPENDENCY"
    else:
        patterns["LiquidationGuard"]["sema_id"] = "sema:LiquidationGuard#mh:SHA-256:" + ("0" * 64)
        expected_error = "Identity mismatch"
    release = _write_release(tmp_path / defect, patterns=patterns)
    registry_before = _bytes_if_present(library_environment["registry_file"])
    active_before = library_environment["active_file"].read_bytes()

    with pytest.raises(LibraryError, match=expected_error):
        install_library(release.manifest_path, data_dir=library_environment["data_dir"])

    assert _bytes_if_present(library_environment["registry_file"]) == registry_before
    assert library_environment["active_file"].read_bytes() == active_before


def test_update_repoints_an_active_library(
    tmp_path: Path, library_environment: dict[str, Path]
) -> None:
    update_pointer = tmp_path / "current-library.json"
    release_v1 = _write_release(
        tmp_path / "release-v1", version="1.0.0", update_path=update_pointer
    )
    update_pointer.write_bytes(release_v1.manifest_path.read_bytes())
    assert install_remote_library(str(release_v1.manifest_path))
    assert use_db("defi")
    old_record = get_library("defi")
    assert old_record is not None
    old_path = old_record["path"]
    assert get_configured_active_db() == old_path

    release_v11 = _write_release(
        tmp_path / "release-v1-1",
        version="1.1.0",
        patterns=_defi_patterns(guard_revision=" under the revised threshold policy"),
        update_path=update_pointer,
    )
    update_pointer.write_bytes(release_v11.manifest_path.read_bytes())

    assert update_remote_library("defi")
    new_record = get_library("defi")
    assert new_record is not None
    assert new_record["version"] == "1.1.0"
    assert new_record["path"] != old_path
    assert Path(old_path).exists()
    assert get_configured_active_db() == new_record["path"]
    assert new_record["catalog_root"] == release_v11.roots["catalog_root"]


def test_failed_active_repoint_restores_previous_registry_record(
    tmp_path: Path,
    library_environment: dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    update_pointer = tmp_path / "atomic-current-library.json"
    release_v1 = _write_release(
        tmp_path / "atomic-release-v1", version="1.0.0", update_path=update_pointer
    )
    update_pointer.write_bytes(release_v1.manifest_path.read_bytes())
    old_record = install_library(release_v1.manifest_path, data_dir=library_environment["data_dir"])
    set_active_db(old_record["path"])

    release_v11 = _write_release(
        tmp_path / "atomic-release-v1-1",
        version="1.1.0",
        patterns=_defi_patterns(guard_revision=" after an atomic update"),
        update_path=update_pointer,
    )
    update_pointer.write_bytes(release_v11.manifest_path.read_bytes())

    def fail_active_write(_path: str) -> None:
        raise OSError("simulated active-pointer failure")

    monkeypatch.setattr("sema.core.libraries.set_active_db", fail_active_write)
    with pytest.raises(OSError, match="simulated active-pointer failure"):
        update_library("defi", data_dir=library_environment["data_dir"])

    assert get_library("defi")["path"] == old_record["path"]
    assert get_configured_active_db() == old_record["path"]


def test_same_version_republication_is_rejected(
    tmp_path: Path, library_environment: dict[str, Path]
) -> None:
    update_pointer = tmp_path / "current-library.json"
    original = _write_release(tmp_path / "original", version="1.0.0", update_path=update_pointer)
    update_pointer.write_bytes(original.manifest_path.read_bytes())
    record = install_library(original.manifest_path, data_dir=library_environment["data_dir"])
    registry_before = library_environment["registry_file"].read_bytes()
    active_before = library_environment["active_file"].read_bytes()

    republished_patterns = _defi_patterns()
    # `_meta` is deliberately outside pattern identity; release immutability must
    # still catch changed canonical source bytes under the same version.
    republished_patterns["AssetPrice"]["_meta"]["caution"] = "Same identity, new metadata"
    republished = _write_release(
        tmp_path / "republished",
        version="1.0.0",
        patterns=republished_patterns,
        update_path=update_pointer,
    )
    update_pointer.write_bytes(republished.manifest_path.read_bytes())

    with pytest.raises(LibraryError, match="republished"):
        update_library("defi", data_dir=library_environment["data_dir"])

    assert get_library("defi")["path"] == record["path"]
    assert library_environment["registry_file"].read_bytes() == registry_before
    assert library_environment["active_file"].read_bytes() == active_before


@pytest.mark.parametrize("database_state", ["missing", "incompatible"])
def test_optional_database_falls_back_to_json(
    tmp_path: Path,
    library_environment: dict[str, Path],
    database_state: str,
) -> None:
    missing_database = tmp_path / database_state / "missing-taxonomy.db"
    database = {
        "format": DATABASE_FORMAT,
        "schema_version": (
            DATABASE_SCHEMA_VERSION if database_state == "missing" else DATABASE_SCHEMA_VERSION + 1
        ),
        "url": missing_database.resolve().as_uri(),
        "sha256": "0" * 64,
        "size_bytes": 1,
    }
    release = _write_release(tmp_path / database_state, database=database)

    record = install_library(release.manifest_path, data_dir=library_environment["data_dir"])

    assert record["database_source"] == "generated"
    assert Path(record["path"]).is_file()
    assert verify_installed_library(record)["catalog_root"] == release.roots["catalog_root"]


def test_zip_traversal_is_rejected_before_activation(
    tmp_path: Path, library_environment: dict[str, Path]
) -> None:
    release = _write_release(
        tmp_path / "traversal",
        extra_members={"patterns/../Escape.json": b"{}"},
    )
    registry_before = _bytes_if_present(library_environment["registry_file"])
    active_before = library_environment["active_file"].read_bytes()

    with pytest.raises(LibraryError, match="Unsafe path"):
        install_library(release.manifest_path, data_dir=library_environment["data_dir"])

    assert _bytes_if_present(library_environment["registry_file"]) == registry_before
    assert library_environment["active_file"].read_bytes() == active_before
    assert not list(library_environment["data_dir"].glob("**/Escape.json"))


def test_managed_path_is_verified_and_bare_name_wins_over_cwd_file(
    tmp_path: Path,
    library_environment: dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    release = _write_release(tmp_path / "managed-path")
    record = install_library(release.manifest_path, data_dir=library_environment["data_dir"])

    shadow = tmp_path / "defi"
    shadow.write_bytes(b"not sqlite")
    monkeypatch.chdir(tmp_path)
    assert use_db("defi")
    assert get_configured_active_db() == record["path"]

    set_active_db(str(library_environment["original_db"]))
    Path(record["path"]).chmod(0o644)
    with sqlite3.connect(record["path"]) as connection:
        connection.execute("DELETE FROM nodes WHERE node_type='PATTERN'")
    assert not use_db(record["path"])
    assert get_configured_active_db() == str(library_environment["original_db"].resolve())


def test_invalid_file_and_pull_undo_cannot_replace_active_managed_library(
    tmp_path: Path, library_environment: dict[str, Path]
) -> None:
    invalid = tmp_path / "not-a-database"
    invalid.write_bytes(b"plain text")
    active_before = library_environment["active_file"].read_bytes()
    assert not use_db(str(invalid))
    assert library_environment["active_file"].read_bytes() == active_before

    release = _write_release(tmp_path / "undo-managed")
    record = install_library(release.manifest_path, data_dir=library_environment["data_dir"])
    set_active_db(record["path"])
    db_before = Path(record["path"]).read_bytes()
    Path(record["path"] + ".pull_previous").write_bytes(b"not a valid snapshot")
    assert not undo_pull()
    assert Path(record["path"]).read_bytes() == db_before


def test_prebuilt_database_rejects_embedded_handle_mismatch(
    tmp_path: Path, library_environment: dict[str, Path]
) -> None:
    source_release = _write_release(tmp_path / "prebuilt-source")
    source_record = install_library(
        source_release.manifest_path, data_dir=library_environment["data_dir"]
    )
    prebuilt = tmp_path / "tampered-prebuilt.db"
    shutil.copy2(source_record["path"], prebuilt)
    prebuilt.chmod(0o644)
    with sqlite3.connect(prebuilt) as connection:
        metadata_json = connection.execute(
            "SELECT metadata FROM nodes WHERE node_type='PATTERN' AND text='AssetPrice'"
        ).fetchone()[0]
        metadata = json.loads(metadata_json)
        metadata["pattern"]["handle"] = "WrongHandle"
        connection.execute(
            "UPDATE nodes SET metadata=? WHERE node_type='PATTERN' AND text='AssetPrice'",
            (json.dumps(metadata),),
        )

    library_environment["registry_file"].unlink()
    database = {
        "format": DATABASE_FORMAT,
        "schema_version": DATABASE_SCHEMA_VERSION,
        "url": prebuilt.resolve().as_uri(),
        "sha256": hashlib.sha256(prebuilt.read_bytes()).hexdigest(),
        "size_bytes": prebuilt.stat().st_size,
    }
    release = _write_release(tmp_path / "prebuilt-release", database=database)

    with pytest.raises(LibraryError, match="embeds handle"):
        install_library(release.manifest_path, data_dir=tmp_path / "prebuilt-install")


def test_compatible_prebuilt_database_is_used(
    tmp_path: Path, library_environment: dict[str, Path]
) -> None:
    source_release = _write_release(tmp_path / "valid-prebuilt-source")
    source_record = install_library(
        source_release.manifest_path, data_dir=library_environment["data_dir"]
    )
    prebuilt = tmp_path / "valid-prebuilt.db"
    shutil.copy2(source_record["path"], prebuilt)
    library_environment["registry_file"].unlink()
    database = {
        "format": DATABASE_FORMAT,
        "schema_version": DATABASE_SCHEMA_VERSION,
        "url": prebuilt.resolve().as_uri(),
        "sha256": hashlib.sha256(prebuilt.read_bytes()).hexdigest(),
        "size_bytes": prebuilt.stat().st_size,
    }
    release = _write_release(tmp_path / "valid-prebuilt-release", database=database)

    record = install_library(release.manifest_path, data_dir=tmp_path / "valid-prebuilt-install")

    assert record["database_source"] == "prebuilt"
    assert verify_installed_library(record)["catalog_root"] == release.roots["catalog_root"]
