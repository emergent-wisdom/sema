"""Library releases declare the canonicalization their identities use.

A schema-2 manifest names its canonicalization; a schema-1 manifest predates
the field and is v2. Installation verifies every identity under the declared
version, so a v3 release refuses a card whose placeholder targets were
exchanged, while a v2 release cannot see the exchange.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sqlite3
import stat
import zipfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from sema.core.hashing import (
    CANONICALIZATION_V2,
    CANONICALIZATION_V3,
    CATALOG_ROOT_SCHEME,
    SEMANTIC_ROOT_SCHEME,
    generate_sema_hash,
    pattern_hash_from_sema_id,
    vocabulary_roots,
)
from sema.core.libraries import (
    LibraryError,
    LibraryManifest,
    build_library_database,
    package_library,
    verify_installed_library,
    verify_library_package,
    verify_library_patterns,
)

INFRASTRUCTURE = {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 0}
SOCIETY = {"path": ["Society", "Economics"], "ring": 1, "tier": 1}


def _identify(pattern: dict, hashes: dict[str, str], version: int) -> dict:
    result = copy.deepcopy(pattern)
    identity = generate_sema_hash(result, hashes.get, canonicalization=version)
    result["sema_id"] = identity["full_id"]
    result["sema_ref"] = identity["reference"]
    result["sema_stub"] = identity["stub"]
    hashes[result["handle"]] = identity["hash"]
    return result


def _patterns(version: int, *, exchanged: bool = False, role: str = "score") -> dict[str, dict]:
    """Two leaves and a card that scores with one and verifies with the other.

    ``role`` is the alias bound to Score: ``score`` names its target, so the
    pairing is implied; any other name is a role name, hashed explicitly.
    """
    hashes: dict[str, str] = {}
    score = _identify(
        {
            "handle": "Score",
            "gloss": "Rate a proposal",
            "mechanism": "Assigns a proposal a rating on a declared scale.",
            "invariants": ["The rating uses the declared scale."],
            "_meta": INFRASTRUCTURE,
        },
        hashes,
        version,
    )
    verify = _identify(
        {
            "handle": "Verify",
            "gloss": "Test a proposal",
            "mechanism": "Tests a proposal against a declared condition.",
            "invariants": ["The test names the condition it checks."],
            "_meta": INFRASTRUCTURE,
        },
        hashes,
        version,
    )
    review = _identify(
        {
            "handle": "Review",
            "gloss": "Rate a proposal, then test it",
            "mechanism": f"Uses {{{{{role}}}}} to rate a proposal and {{{{verify}}}} to test it.",
            "invariants": ["A proposal is tested only after it is rated."],
            "dependencies": {
                "composes_with": {role: score["sema_id"], "verify": verify["sema_id"]}
            },
            "_meta": SOCIETY,
        },
        hashes,
        version,
    )
    if exchanged:
        bindings = review["dependencies"]["composes_with"]
        bindings[role], bindings["verify"] = bindings["verify"], bindings[role]
    return {"Score": score, "Verify": verify, "Review": review}


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _release(directory: Path, patterns: dict[str, dict], **declared) -> Path:
    """Write a release whose roots commit to the identifiers its cards claim."""
    directory.mkdir(parents=True, exist_ok=True)
    archive = directory / "patterns.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
        for handle, pattern in sorted(patterns.items()):
            info = zipfile.ZipInfo(f"patterns/{handle}.json")
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            zipped.writestr(info, _json_bytes(pattern))
    roots = vocabulary_roots(
        (handle, pattern_hash_from_sema_id(pattern["sema_id"], expected_handle=handle))
        for handle, pattern in sorted(patterns.items())
    )
    manifest_path = directory / "library.json"
    manifest = {
        **declared,
        "name": "review",
        "version": "1.0.0",
        "update_url": manifest_path.resolve().as_uri(),
        "patterns": {
            "format": "sema-patterns-zip-v1",
            "url": archive.resolve().as_uri(),
            "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
            "size_bytes": archive.stat().st_size,
        },
        "roots": {
            "semantic": {"scheme": SEMANTIC_ROOT_SCHEME, "sha256": roots["semantic_root"]},
            "catalog": {"scheme": CATALOG_ROOT_SCHEME, "sha256": roots["catalog_root"]},
        },
        "pattern_count": len(patterns),
    }
    manifest_path.write_bytes(_json_bytes(manifest))
    return manifest_path


V3 = {"manifest_schema": 2, "canonicalization": CANONICALIZATION_V3}
V1_MANIFEST = {"manifest_schema": 1}


def _verify(manifest_path: Path, patterns: dict[str, dict]):
    """Run the install-time verification of a release's cards against its manifest."""
    manifest = LibraryManifest.model_validate(json.loads(manifest_path.read_text()))
    return verify_library_patterns(copy.deepcopy(patterns), manifest)


class TestReleases:
    def test_a_v3_release_installs_and_records_its_canonicalization(self, tmp_path):
        patterns = _patterns(CANONICALIZATION_V3, role="rating")
        verified = _verify(_release(tmp_path / "release", patterns, **V3), patterns)
        assert verified.canonicalization == CANONICALIZATION_V3

        database = tmp_path / "library.db"
        build_library_database(verified, database)
        with sqlite3.connect(database) as conn:
            recorded = conn.execute(
                "SELECT value FROM store_settings WHERE key = 'pattern_canonicalization'"
            ).fetchone()
        assert recorded == ("3",)

    def test_a_v3_release_refuses_an_exchanged_card(self, tmp_path):
        tampered = _patterns(CANONICALIZATION_V3, exchanged=True)
        manifest = _release(tmp_path / "release", tampered, **V3)
        with pytest.raises(LibraryError, match="Identity mismatch for Review"):
            _verify(manifest, tampered)

    def test_a_schema_1_release_is_v2_and_cannot_see_the_exchange(self, tmp_path):
        """The released behaviour, kept so that published v2 libraries still install."""
        tampered = _patterns(CANONICALIZATION_V2, exchanged=True)
        manifest = _release(tmp_path / "release", tampered, **V1_MANIFEST)
        verified = _verify(manifest, tampered)
        assert verified.canonicalization == CANONICALIZATION_V2
        bindings = verified.patterns["Review"]["dependencies"]["composes_with"]
        assert bindings["score"].startswith("sema:Verify#")

    def test_a_v2_identity_is_not_a_v3_identity_for_an_exchanged_card(self, tmp_path):
        """A v2 release relabelled as v3 is refused: the declaration is checked."""
        patterns = _patterns(CANONICALIZATION_V2, exchanged=True)
        manifest = _release(tmp_path / "release", patterns, **V3)
        with pytest.raises(LibraryError, match="Identity mismatch"):
            _verify(manifest, patterns)


class TestManifestDeclaration:
    BASE = {
        "name": "review",
        "version": "1.0.0",
        "update_url": "https://example.org/library.json",
        "patterns": {
            "format": "sema-patterns-zip-v1",
            "url": "https://example.org/patterns.zip",
            "sha256": "0" * 64,
            "size_bytes": 1,
        },
        "roots": {
            "semantic": {"scheme": SEMANTIC_ROOT_SCHEME, "sha256": "0" * 64},
            "catalog": {"scheme": CATALOG_ROOT_SCHEME, "sha256": "0" * 64},
        },
        "pattern_count": 1,
    }

    def test_schema_1_means_v2(self):
        manifest = LibraryManifest.model_validate({**self.BASE, "manifest_schema": 1})
        assert manifest.pattern_canonicalization == CANONICALIZATION_V2

    @pytest.mark.parametrize(
        "fields",
        [
            {"manifest_schema": 1, "canonicalization": 3},
            {"manifest_schema": 2},
            {"manifest_schema": 2, "canonicalization": 4},
            {"manifest_schema": 3, "canonicalization": 3},
        ],
        ids=["schema-1-declares", "schema-2-silent", "unknown-version", "unknown-schema"],
    )
    def test_invalid_declarations_fail_closed(self, fields):
        with pytest.raises(ValidationError):
            LibraryManifest.model_validate({**self.BASE, **fields})


class TestInstalledRecordsAndPackages:
    def _database(self, tmp_path: Path, version: int) -> tuple[Path, dict]:
        patterns = _patterns(version, role="rating")
        declared = V3 if version == CANONICALIZATION_V3 else V1_MANIFEST
        manifest = LibraryManifest.model_validate(
            json.loads(_release(tmp_path / f"source-{version}", patterns, **declared).read_text())
        )
        verified = verify_library_patterns(patterns, manifest)
        database = tmp_path / f"library-{version}.db"
        build_library_database(verified, database)
        return database, verified.roots

    def _record(self, database: Path, roots: dict, **extra) -> dict:
        return {
            "name": "review",
            "version": "1.0.0",
            "path": str(database),
            "semantic_root": roots["semantic_root"],
            "catalog_root": roots["catalog_root"],
            "pattern_count": 3,
            **extra,
        }

    def test_a_record_without_a_version_is_verified_as_v2(self, tmp_path):
        database, roots = self._database(tmp_path, CANONICALIZATION_V2)
        assert verify_installed_library(self._record(database, roots)) == roots

    def test_a_record_with_its_version_is_verified_under_it(self, tmp_path):
        database, roots = self._database(tmp_path, CANONICALIZATION_V3)
        record = self._record(database, roots, canonicalization=CANONICALIZATION_V3)
        assert verify_installed_library(record) == roots
        with pytest.raises(LibraryError):
            verify_installed_library(self._record(database, roots))

    @pytest.mark.parametrize("version", [CANONICALIZATION_V2, CANONICALIZATION_V3])
    def test_a_package_declares_its_database_canonicalization(self, tmp_path, version):
        database, _roots = self._database(tmp_path, version)
        package = package_library(
            database,
            tmp_path / "package",
            name="review",
            version="1.0.0",
            update_url="https://github.com/acme/review/releases/latest/download/library.json",
            artifact_url=(
                "https://github.com/acme/review/releases/download/v1.0.0/review-patterns-1.0.0.zip"
            ),
        )
        manifest = json.loads(package.manifest_path.read_text())
        if version == CANONICALIZATION_V2:
            # Nothing schema 2 adds is needed, so earlier releases can still install it.
            assert manifest["manifest_schema"] == 1
            assert "canonicalization" not in manifest
        else:
            assert manifest["manifest_schema"] == 2
            assert manifest["canonicalization"] == version
        verified = verify_library_package(package.manifest_path, package.archive_path)
        assert verified.canonicalization == version
