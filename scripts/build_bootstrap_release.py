#!/usr/bin/env python3
"""Build the official bootstrap library's portable release artifacts.

The repository keeps one maintained vocabulary under ``data/vocabulary``.
This script packages those exact exported bytes into a deterministic ZIP,
writes the small ``library.json`` index consumed by ``sema install``, and
proves that the portable release has the same identities and roots as the
bundled runtime database.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_SRC = REPO_ROOT / "src"
if str(REPO_SRC) not in sys.path:
    sys.path.insert(0, str(REPO_SRC))

from sema.core.hashing import (  # noqa: E402
    CATALOG_ROOT_SCHEME,
    SEMANTIC_ROOT_SCHEME,
    pattern_hash_from_sema_id,
    vocabulary_roots,
)
from sema.core.libraries import (  # noqa: E402
    LibraryManifest,
    _strict_json,
    verify_library_database,
    verify_library_patterns,
)

DEFAULT_PATTERN_DIR = REPO_ROOT / "data" / "vocabulary"
DEFAULT_DATABASE = REPO_ROOT / "data" / "taxonomy.db"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "dist" / "bootstrap"
DEFAULT_UPDATE_URL = "https://github.com/emergent-wisdom/sema/releases/latest/download/library.json"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


@dataclass(frozen=True)
class BootstrapRelease:
    manifest_path: Path
    archive_path: Path
    semantic_root: str
    catalog_root: str
    pattern_count: int


def read_project_version(pyproject: Path = REPO_ROOT / "pyproject.toml") -> str:
    """Read the project version without adding a TOML dependency on Python 3.10."""
    match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject.read_text(), re.MULTILINE)
    if not match:
        raise ValueError(f"Could not find the project version in {pyproject}")
    return match.group(1)


def _pattern_sources(pattern_dir: Path) -> tuple[dict[str, dict], dict[str, bytes]]:
    paths = sorted(pattern_dir.glob("*.json"))
    if not paths:
        raise ValueError(f"No pattern JSON files found in {pattern_dir}")

    patterns: dict[str, dict] = {}
    source_bytes: dict[str, bytes] = {}
    for path in paths:
        raw = path.read_bytes()
        pattern = _strict_json(raw, label=str(path))
        handle = pattern.get("handle")
        if not isinstance(handle, str) or path.stem != handle:
            raise ValueError(f"Filename/handle mismatch in {path}")
        if handle in patterns:
            raise ValueError(f"Duplicate pattern handle {handle!r}")
        patterns[handle] = pattern
        source_bytes[handle] = raw
    return patterns, source_bytes


def _write_deterministic_zip(archive_path: Path, source_bytes: dict[str, bytes]) -> None:
    archive_path.unlink(missing_ok=True)
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_STORED) as archive:
        for handle, raw in sorted(source_bytes.items()):
            info = zipfile.ZipInfo(f"patterns/{handle}.json", date_time=FIXED_ZIP_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, raw)


def build_bootstrap_release(
    output_dir: Path,
    *,
    version: str,
    pattern_dir: Path = DEFAULT_PATTERN_DIR,
    database_path: Path = DEFAULT_DATABASE,
    update_url: str = DEFAULT_UPDATE_URL,
) -> BootstrapRelease:
    """Build and verify ``library.json`` plus the deterministic pattern ZIP."""
    output_dir.mkdir(parents=True, exist_ok=True)
    patterns, source_bytes = _pattern_sources(pattern_dir)
    archive_path = output_dir / f"sema-bootstrap-{version}.zip"
    _write_deterministic_zip(archive_path, source_bytes)

    bindings = [
        (
            handle,
            pattern_hash_from_sema_id(pattern["sema_id"], expected_handle=handle),
        )
        for handle, pattern in sorted(patterns.items())
    ]
    roots = vocabulary_roots(bindings)
    archive_bytes = archive_path.read_bytes()
    manifest_data = {
        "manifest_schema": 1,
        "name": "bootstrap",
        "version": version,
        "update_url": update_url,
        "patterns": {
            "format": "sema-patterns-zip-v1",
            "url": archive_path.name,
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
    manifest = LibraryManifest.model_validate(manifest_data)
    verified = verify_library_patterns(patterns, manifest)
    verify_library_database(database_path, verified, manifest)

    manifest_path = output_dir / "library.json"
    manifest_path.write_text(
        json.dumps(manifest_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return BootstrapRelease(
        manifest_path=manifest_path,
        archive_path=archive_path,
        semantic_root=roots["semantic_root"],
        catalog_root=roots["catalog_root"],
        pattern_count=len(patterns),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for library.json and the pattern ZIP",
    )
    parser.add_argument(
        "--version",
        default=read_project_version(),
        help="Library release version (defaults to the tool version)",
    )
    args = parser.parse_args()

    release = build_bootstrap_release(args.output_dir, version=args.version)
    print(f"Built bootstrap library {args.version} with {release.pattern_count} patterns")
    print(f"  Manifest:      {release.manifest_path}")
    print(f"  Pattern ZIP:   {release.archive_path}")
    print(f"  Semantic root: {release.semantic_root}")
    print(f"  Catalog root:  {release.catalog_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
