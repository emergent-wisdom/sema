"""Exercise the release gate against archives with representative packaging failures."""

import importlib.util
import io
import tarfile
import zipfile
from pathlib import Path

import pytest


@pytest.fixture
def verifier():
    script = Path(__file__).resolve().parents[4] / "scripts" / "verify_release_artifacts.py"
    spec = importlib.util.spec_from_file_location("verify_release_artifacts", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_archives(dist, wheel, sdist):
    with zipfile.ZipFile(dist / "semahash-1.2.3-py3-none-any.whl", "w") as archive:
        for name, content in wheel.items():
            archive.writestr(name, content)
    with tarfile.open(dist / "semahash-1.2.3.tar.gz", "w:gz") as archive:
        for name, content in sdist.items():
            entry = tarfile.TarInfo("semahash-1.2.3/" + name)
            entry.size = len(content)
            archive.addfile(entry, io.BytesIO(content))


@pytest.fixture
def release(tmp_path, monkeypatch, verifier):
    sources = {
        ".gitignore": b"build/\ndist/\n",
        "pyproject.toml": b'[project]\nname = "semahash"\nversion = "1.2.3"\n',
        "README.md": b"Public readme",
        "LICENSE": b"Code license",
        "LICENSE-CONTENT": b"Content license",
        "THIRD_PARTY_NOTICES.md": b"Notices",
        "scripts/test_hash_verification.py": b"# hash verification",
        "src/sema/__init__.py": b'__version__ = "1.2.3"',
        "src/sema/server/static/.gitkeep": b"",
        "src/sema/server/static/index.html": b"Old tracked viewer snapshot",
        "data/vocabulary/Example.json": b'{"handle": "Example"}',
        "data/taxonomy.db": b"Database bytes",
        "data/graph.json": b"{}",
        "data/presets/full.txt": b"Example",
        ".claude-plugin/plugin.json": b"{}",
        "skills/sema-usage/SKILL.md": b"Public instructions",
        "docs/specification/canonicalization-v2-test-vectors.json": b"[]",
    }
    frontend = {
        "index.html": b'<script src="/assets/viewer.js"></script>',
        "__spa-fallback.html": b'<link href="/assets/viewer.css?version=1">',
        "favicon.svg": b"<svg/>",
        "sema_logo.svg": b"<svg/>",
        "llms.txt": b"Public context",
        "assets/viewer.js": b"export const ready = true;",
        "assets/viewer.css": b"body {}",
    }
    for name, content in sources.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    for name, content in frontend.items():
        path = tmp_path / "web/build/client" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    monkeypatch.setattr(
        verifier.subprocess, "check_output", lambda *a, **kw: "\0".join(sources).encode()
    )

    wheel = {
        "sema/__init__.py": sources["src/sema/__init__.py"],
        "sema/server/static/.gitkeep": b"",
        "sema/data/vocabulary/Example.json": sources["data/vocabulary/Example.json"],
        "sema/data/taxonomy.db": sources["data/taxonomy.db"],
        "sema/data/graph.json": b"{}",
        "sema/data/presets/full.txt": b"Example",
        "sema/.claude-plugin/plugin.json": b"{}",
        "sema/skills/sema-usage/SKILL.md": b"Public instructions",
        "sema/specification/canonicalization-v2-test-vectors.json": b"[]",
    }
    sdist = dict(sources)
    for name, content in frontend.items():
        wheel["sema/server/static/" + name] = content
        sdist["src/sema/server/static/" + name] = content
    info = "semahash-1.2.3.dist-info/"
    for name in ("LICENSE", "LICENSE-CONTENT", "THIRD_PARTY_NOTICES.md"):
        wheel[info + "licenses/" + name] = sources[name]
    metadata = b"Metadata-Version: 2.4\nName: semahash\nVersion: 1.2.3\n"
    wheel.update(
        {
            info + "METADATA": metadata,
            info + "WHEEL": b"",
            info + "RECORD": b"",
            info + "entry_points.txt": b"",
        }
    )
    sdist["PKG-INFO"] = metadata
    dist = tmp_path / "dist"
    dist.mkdir()
    write_archives(dist, wheel, sdist)
    return tmp_path, dist, wheel, sdist


def test_complete_matching_release_passes(verifier, release):
    root, dist, _, _ = release
    verifier.verify(root, dist)


@pytest.mark.parametrize("target,prefix", [("wheel", "sema/"), ("sdist", "")])
@pytest.mark.parametrize("mutation", ["extra", "missing_card", "altered_card", "altered_db"])
def test_rejects_unapproved_or_incomplete_payload(verifier, release, target, prefix, mutation):
    root, dist, wheel, sdist = release
    files = wheel if target == "wheel" else sdist
    card = prefix + "data/vocabulary/Example.json"
    if mutation == "extra":
        files[prefix + "data/notes.txt"] = b"Unexpected notes"
    elif mutation == "missing_card":
        del files[card]
    elif mutation == "altered_card":
        files[card] = b"{}"
    else:
        files[prefix + "data/taxonomy.db"] = b"Other database"
    write_archives(dist, wheel, sdist)
    with pytest.raises(ValueError, match="unexpected or missing files|payload differs"):
        verifier.verify(root, dist)


@pytest.mark.parametrize("target,prefix", [("wheel", "sema/"), ("sdist", "src/sema/")])
def test_requires_every_built_asset_in_both_archives(verifier, release, target, prefix):
    root, dist, wheel, sdist = release
    files = wheel if target == "wheel" else sdist
    del files[prefix + "server/static/assets/viewer.css"]
    write_archives(dist, wheel, sdist)
    with pytest.raises(ValueError, match="unexpected or missing files"):
        verifier.verify(root, dist)


@pytest.mark.parametrize("reference", ["/assets/absent.js", "/assets/%2e%2e/hidden.js"])
def test_rejects_invalid_references_even_when_pages_match_build(verifier, release, reference):
    root, dist, wheel, sdist = release
    page = f'<script src="{reference}"></script>'.encode()
    (root / "web/build/client/index.html").write_bytes(page)
    wheel["sema/server/static/index.html"] = page
    sdist["src/sema/server/static/index.html"] = page
    write_archives(dist, wheel, sdist)
    with pytest.raises(ValueError, match="missing or unsafe|non-canonical"):
        verifier.verify(root, dist)


def test_rejects_stale_frontend_snapshot(verifier, release):
    root, dist, wheel, sdist = release
    wheel["sema/server/static/index.html"] = b"Old tracked viewer snapshot"
    write_archives(dist, wheel, sdist)
    with pytest.raises(ValueError, match="payload differs"):
        verifier.verify(root, dist)


@pytest.mark.parametrize(
    "name", ["../outside.py", "/absolute.py", "sema/.local-work/notes.txt", "sema//extra.py"]
)
def test_rejects_unsafe_archive_paths(verifier, release, name):
    root, dist, wheel, sdist = release
    wheel[name] = b"Unexpected"
    write_archives(dist, wheel, sdist)
    with pytest.raises(ValueError, match="archive path|working artifact"):
        verifier.verify(root, dist)


def test_rejects_duplicate_wheel_entries(verifier, release):
    root, dist, _, _ = release
    with zipfile.ZipFile(dist / "semahash-1.2.3-py3-none-any.whl", "a") as archive:
        with pytest.warns(UserWarning, match="Duplicate name"):
            archive.writestr("sema/__init__.py", b"Shadowed source")
    with pytest.raises(ValueError, match="Duplicate wheel entry"):
        verifier.verify(root, dist)


def test_rejects_sdist_symlinks(verifier, release):
    root, dist, _, _ = release
    with tarfile.open(dist / "semahash-1.2.3.tar.gz", "w:gz") as archive:
        entry = tarfile.TarInfo("semahash-1.2.3/link")
        entry.type = tarfile.SYMTYPE
        entry.linkname = "../outside"
        archive.addfile(entry)
    with pytest.raises(ValueError, match="Non-file sdist entry"):
        verifier.verify(root, dist)


def test_rejects_extra_distribution(verifier, release):
    root, dist, _, _ = release
    (dist / "old-release.whl").write_bytes(b"Old archive")
    with pytest.raises(ValueError, match="exactly the expected"):
        verifier.verify(root, dist)


def test_rejects_unexpected_frontend_output(verifier, release):
    root, dist, _, _ = release
    (root / "web/build/client/notes.txt").write_text("Working notes")
    with pytest.raises(ValueError, match="Unexpected frontend output"):
        verifier.verify(root, dist)
