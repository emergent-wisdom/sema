#!/usr/bin/env python3
"""Check the exact wheel and sdist before publishing, without extracting them.

The positive input mappings below deliberately mirror pyproject.toml. Changes to
package scope must update this gate as well. Tracked source files and the complete
fresh frontend build define the payload; generated packaging metadata has a small
separate allowlist. Byte equality preserves the vocabulary/DB parity checked by
verify_vocabulary_change.py rather than reimplementing its export semantics.
"""

from __future__ import annotations

import argparse
import re
import stat
import subprocess
import tarfile
import zipfile
from email.parser import BytesParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO_ROOT = Path(__file__).resolve().parents[1]
STATIC = "src/sema/server/static/"
FORCE_INCLUDE = {
    "data/vocabulary": "sema/data/vocabulary",
    "data/taxonomy.db": "sema/data/taxonomy.db",
    "data/graph.json": "sema/data/graph.json",
    "data/presets": "sema/data/presets",
    ".claude-plugin": "sema/.claude-plugin",
    "skills": "sema/skills",
    "docs/specification/canonicalization-v2-test-vectors.json": "sema/specification/canonicalization-v2-test-vectors.json",
}
LICENSES = ("LICENSE", "LICENSE-CONTENT", "THIRD_PARTY_NOTICES.md")
SDIST_ONLY = (
    ".gitignore",
    "README.md",
    "pyproject.toml",
    "scripts/test_hash_verification.py",
    *LICENSES,
)
VIEWER_FILES = {"index.html", "__spa-fallback.html", "favicon.svg", "sema_logo.svg", "llms.txt"}
ASSET_SUFFIXES = {
    ".js",
    ".css",
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def safe_path(name: str) -> str:
    """Reject aliases and traversal before normalizing any archive path."""
    require(
        bool(name) and "\\" not in name and not any(ord(c) < 32 for c in name),
        "Invalid archive path",
    )
    require(
        all(part not in {"", ".", ".."} for part in name.split("/")),
        "Non-relative or non-canonical archive path",
    )
    require(
        name == ".gitignore"
        or not any(
            part.startswith(".") and part not in {".claude-plugin", ".gitkeep"}
            for part in name.split("/")
        ),
        "Hidden working artifact in package",
    )
    return name


def read_archives(wheel: Path, sdist: Path, stem: str) -> tuple[dict[str, bytes], dict[str, bytes]]:
    wheel_files: dict[str, bytes] = {}
    with zipfile.ZipFile(wheel) as archive:
        for entry in archive.infolist():
            name = safe_path(entry.filename)
            mode = stat.S_IFMT(entry.external_attr >> 16)
            require(mode in {0, stat.S_IFREG} and not entry.is_dir(), "Non-file wheel entry")
            require(name not in wheel_files, "Duplicate wheel entry")
            wheel_files[name] = archive.read(entry)
    sdist_files: dict[str, bytes] = {}
    with tarfile.open(sdist, "r:gz") as archive:
        for entry in archive:
            require(entry.isfile(), "Non-file sdist entry")
            require(entry.name.startswith(stem + "/"), "Unexpected sdist root")
            name = safe_path(entry.name[len(stem) + 1 :])
            require(name not in sdist_files, "Duplicate sdist entry")
            stream = archive.extractfile(entry)
            require(stream is not None, "Unreadable sdist entry")
            sdist_files[name] = stream.read()
    return wheel_files, sdist_files


def source_bytes(root: Path, name: str) -> bytes:
    safe_path(name)
    path = root / name
    require(path.resolve().is_relative_to(root.resolve()), "Source input leaves checkout")
    require(path.is_file() and not path.is_symlink(), "Missing or non-file source input")
    return path.read_bytes()


def expected_payloads(root: Path, tracked: set[str]) -> tuple[dict[str, bytes], dict[str, bytes]]:
    wheel: dict[str, bytes] = {}
    sdist: dict[str, bytes] = {}
    for name in sorted(tracked):
        if name.startswith("src/sema/"):
            if name.startswith(STATIC) and name != STATIC + ".gitkeep":
                continue  # Fresh frontend output supersedes tracked viewer snapshots.
            data = source_bytes(root, name)
            sdist[name] = data
            wheel[name.removeprefix("src/")] = data
        for source, destination in FORCE_INCLUDE.items():
            if name == source or name.startswith(source + "/"):
                data = source_bytes(root, name)
                sdist[name] = data
                wheel[destination + name[len(source) :]] = data
    for name in SDIST_ONLY:
        require(name in tracked, "Required source input is not tracked")
        sdist[name] = source_bytes(root, name)
    for source in FORCE_INCLUDE:
        require(
            any(name == source or name.startswith(source + "/") for name in sdist),
            "Required package input is missing",
        )
    require(
        any(name.startswith("data/vocabulary/") and name.endswith(".json") for name in sdist),
        "Vocabulary is empty",
    )
    require("sema/__init__.py" in wheel, "Python package is missing")

    frontend = root / "web/build/client"
    require(frontend.is_dir() and not frontend.is_symlink(), "Fresh frontend build is missing")
    generated: dict[str, bytes] = {}
    for path in sorted(frontend.rglob("*")):
        require(not path.is_symlink(), "Symlink in frontend build")
        if path.is_dir():
            continue
        name = safe_path(path.relative_to(frontend).as_posix())
        require(
            name in VIEWER_FILES or (name.startswith("assets/") and path.suffix in ASSET_SUFFIXES),
            "Unexpected frontend output",
        )
        require(path.is_file(), "Non-file frontend output")
        generated[name] = path.read_bytes()
    require(VIEWER_FILES <= generated.keys(), "Frontend pages or public assets are missing")
    require(any(name.startswith("assets/") for name in generated), "Frontend bundle is missing")
    for name, data in generated.items():
        sdist[STATIC + name] = data
        wheel[STATIC.removeprefix("src/") + name] = data
    return wheel, sdist


def check_payload(
    actual: dict[str, bytes], expected: dict[str, bytes], metadata: set[str], label: str
) -> None:
    require(
        actual.keys() == expected.keys() | metadata,
        f"{label}: unexpected or missing files (extra={len(actual.keys() - expected.keys() - metadata)}, "
        f"missing={len((expected.keys() | metadata) - actual.keys())})",
    )
    for name, data in expected.items():
        require(actual[name] == data, f"{label}: payload differs from approved input: {name}")


def check_viewer(files: dict[str, bytes], prefix: str) -> None:
    for page in ("index.html", "__spa-fallback.html"):
        references = re.findall(r"/assets/[^\"'<>\\\s]+", files[prefix + page].decode("utf-8"))
        require(bool(references), "Viewer page has no bundled asset references")
        for reference in references:
            name = safe_path(unquote(urlsplit(reference).path).removeprefix("/"))
            require(
                name.startswith("assets/") and prefix + name in files,
                "Viewer refers to a missing or unsafe bundled asset",
            )


def verify(root: Path, dist: Path) -> None:
    project = (root / "pyproject.toml").read_text()
    section = re.search(r"(?ms)^\[project\]\s*$(.*?)(?=^\[|\Z)", project)
    require(section is not None, "Project metadata is missing")
    version = re.search(r'^version\s*=\s*"([0-9]+\.[0-9]+\.[0-9]+)"\s*$', section[1], re.M)
    require(version is not None, "Expected a stable release version")
    stem = f"semahash-{version[1]}"
    wheel_name, sdist_name = stem + "-py3-none-any.whl", stem + ".tar.gz"
    require(
        dist.is_dir() and {path.name for path in dist.iterdir()} == {wheel_name, sdist_name},
        "Distribution directory must contain exactly the expected wheel and sdist",
    )
    require(
        all(not (dist / name).is_symlink() for name in (wheel_name, sdist_name)),
        "Distribution artifacts must not be symlinks",
    )
    tracked = set(
        subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    ) - {""}
    expected_wheel, expected_sdist = expected_payloads(root, tracked)
    wheel, sdist = read_archives(dist / wheel_name, dist / sdist_name, stem)
    info = stem + ".dist-info/"
    for name in LICENSES:
        expected_wheel[info + "licenses/" + name] = source_bytes(root, name)
    check_payload(
        wheel,
        expected_wheel,
        {info + name for name in ("METADATA", "WHEEL", "entry_points.txt", "RECORD")},
        "wheel",
    )
    check_payload(sdist, expected_sdist, {"PKG-INFO"}, "sdist")
    require(wheel[info + "METADATA"] == sdist["PKG-INFO"], "Wheel/sdist metadata differs")
    metadata = BytesParser().parsebytes(sdist["PKG-INFO"])
    require(
        metadata["Name"] == "semahash" and metadata["Version"] == version[1],
        "Incorrect release metadata",
    )
    check_viewer(wheel, STATIC.removeprefix("src/"))
    check_viewer(sdist, STATIC)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist-dir", type=Path, default=REPO_ROOT / "dist")
    args = parser.parse_args()
    try:
        verify(REPO_ROOT, args.dist_dir)
    except (
        ValueError,
        OSError,
        subprocess.CalledProcessError,
        tarfile.TarError,
        zipfile.BadZipFile,
    ) as error:
        parser.exit(1, f"Release artifact verification failed: {error}\n")
    print(
        "Release artifacts match approved inputs; vocabulary, database and viewer assets are complete."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
