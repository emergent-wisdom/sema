"""Tests for `sema build` — project DB creation from presets and pattern files."""

import sqlite3
from pathlib import Path

import pytest

from sema.cli.main import _get_presets_dir, _read_patterns_file, build_db
from sema.core.registry import RegistryManager, get_default_db_path

# Skip entire module if no source DB is available
SOURCE_DB = get_default_db_path()
pytestmark = pytest.mark.skipif(
    not SOURCE_DB or not Path(SOURCE_DB).exists(),
    reason="No source taxonomy.db available",
)


@pytest.fixture
def dest(tmp_path):
    """Return a non-existent path for the destination DB."""
    return str(tmp_path / "project.db")


# ── Preset: full ──────────────────────────────────────────────────────────────


def test_build_full_copies_all_patterns(dest):
    assert build_db(dest, preset="full")
    source_count = RegistryManager(db_path=SOURCE_DB).count()
    dest_count = RegistryManager(db_path=dest).count()
    assert dest_count == source_count


def test_build_full_is_byte_copy(dest):
    """Full preset should produce a file identical to the source."""
    build_db(dest, preset="full")
    source_size = Path(SOURCE_DB).stat().st_size
    dest_size = Path(dest).stat().st_size
    assert dest_size == source_size


# ── Preset: empty ─────────────────────────────────────────────────────────────


def test_build_empty_has_schema_but_no_data(dest):
    assert build_db(dest, preset="empty")
    conn = sqlite3.connect(dest)
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert "nodes" in tables
    assert "edges" in tables
    assert conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0] == 0
    conn.close()


# ── Preset: standard ─────────────────────────────────────────────────────────


def test_build_standard_is_subset_of_full(dest, tmp_path):
    build_db(dest, preset="standard")
    full_dest = str(tmp_path / "full.db")
    build_db(full_dest, preset="full")

    standard = RegistryManager(db_path=dest)
    full = RegistryManager(db_path=full_dest)

    assert standard.count() > 0
    assert standard.count() < full.count()
    # Every pattern in standard must exist in full
    for handle in standard.registry:
        assert handle in full.registry, f"{handle} in standard but not in full"


def test_build_standard_includes_promotions(dest):
    """Key tier-2 patterns should be in standard via promotion."""
    build_db(dest, preset="standard")
    r = RegistryManager(db_path=dest)
    for handle in ["ChainOfThought", "Vote", "OODA", "Mutex", "Context"]:
        assert handle in r.registry, f"Expected {handle} in standard"


def test_build_standard_excludes_exotic(dest):
    """Exotic patterns should not be in standard."""
    build_db(dest, preset="standard")
    r = RegistryManager(db_path=dest)
    for handle in ["Jazz", "Jester", "AnalogicalMask"]:
        assert handle not in r.registry, f"Expected {handle} excluded from standard"


# ── Custom patterns file ─────────────────────────────────────────────────────


def test_build_from_file_resolves_dependencies(dest, tmp_path):
    patterns_file = tmp_path / "patterns.txt"
    patterns_file.write_text("ChainOfThought\n")

    assert build_db(dest, patterns_file=str(patterns_file))
    r = RegistryManager(db_path=dest)

    # ChainOfThought itself
    assert "ChainOfThought" in r.registry

    # Must have at least some transitive deps
    assert r.count() > 1, "Expected transitive dependencies to be included"


def test_build_from_file_with_comments(dest, tmp_path):
    patterns_file = tmp_path / "patterns.txt"
    patterns_file.write_text("# My project patterns\nVote\n\n# Governance\nConsensus\n")

    assert build_db(dest, patterns_file=str(patterns_file))
    r = RegistryManager(db_path=dest)
    assert "Vote" in r.registry
    assert "Consensus" in r.registry


def test_build_missing_handle_warns_but_succeeds(dest, tmp_path, capsys):
    patterns_file = tmp_path / "patterns.txt"
    patterns_file.write_text("Vote\nNonExistentPattern123\n")

    assert build_db(dest, patterns_file=str(patterns_file))
    out = capsys.readouterr().out
    assert "NonExistentPattern123" in out  # warning printed
    r = RegistryManager(db_path=dest)
    assert "Vote" in r.registry


# ── Destination already exists ────────────────────────────────────────────────


def test_build_refuses_if_dest_exists(dest):
    build_db(dest, preset="empty")
    assert not build_db(dest, preset="empty")  # should fail


# ── DB integrity ──────────────────────────────────────────────────────────────


def test_built_db_has_layer_and_category_nodes(dest, tmp_path):
    patterns_file = tmp_path / "patterns.txt"
    patterns_file.write_text("Vote\n")

    build_db(dest, patterns_file=str(patterns_file))
    conn = sqlite3.connect(dest)
    node_types = {r[0] for r in conn.execute("SELECT DISTINCT node_type FROM nodes")}
    conn.close()

    assert "PATTERN" in node_types
    assert "LAYER" in node_types or "CATEGORY" in node_types


def test_built_db_has_edges(dest, tmp_path):
    patterns_file = tmp_path / "patterns.txt"
    patterns_file.write_text("Vote\n")

    build_db(dest, patterns_file=str(patterns_file))
    conn = sqlite3.connect(dest)
    edge_count = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
    conn.close()

    assert edge_count > 0, "Expected edges in the built DB"


def test_built_db_search_works(dest):
    build_db(dest, preset="standard")
    r = RegistryManager(db_path=dest)
    results = r.search("consensus")
    assert len(results) > 0
    handles = [res["handle"].split("#")[0] for res in results]
    assert "Consensus" in handles


def test_built_db_resolve_works(dest):
    build_db(dest, preset="standard")
    r = RegistryManager(db_path=dest)
    subgraph = r.resolve("ChainOfThought")
    assert subgraph is not None
    assert "ChainOfThought" in subgraph


# ── Presets infrastructure ────────────────────────────────────────────────────


def test_presets_dir_exists():
    d = _get_presets_dir()
    assert d.exists(), f"Presets directory not found: {d}"


def test_presets_have_expected_files():
    d = _get_presets_dir()
    names = {f.stem for f in d.glob("*.txt")}
    assert "full" in names
    assert "standard" in names
    assert "empty" in names


def test_full_preset_covers_entire_vocabulary():
    d = _get_presets_dir()
    full_handles = _read_patterns_file(d / "full.txt")
    source = RegistryManager(db_path=SOURCE_DB)
    assert len(full_handles) == source.count()


def test_standard_preset_is_nonempty():
    d = _get_presets_dir()
    handles = _read_patterns_file(d / "standard.txt")
    assert len(handles) > 100
