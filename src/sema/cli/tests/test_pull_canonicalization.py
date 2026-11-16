"""`sema pull` keeps a workspace on one canonicalization.

An empty workspace adopts the upstream's. A workspace on an older one moves to
the upstream's inside the atomic pull, and every local identity is recomputed,
including user patterns no upstream change reached. A workspace on a newer one
refuses an older upstream instead of mixing the two.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from unittest.mock import patch

import pytest

from sema.cli.main import undo_pull, update_db
from sema.core.hashing import (
    CANONICALIZATION_V2,
    CANONICALIZATION_V3,
    generate_sema_hash,
)
from sema.core.mint import mint_pattern
from sema.taxonomy_graph.graph_store import GraphStore

INFRASTRUCTURE = {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 0}
SOCIETY = {"path": ["Society", "Economics"], "ring": 1, "tier": 1}


def _leaf(handle: str, gloss: str) -> dict:
    return {
        "handle": handle,
        "gloss": gloss,
        "mechanism": f"{gloss} against a declared condition.",
        "invariants": ["The condition is declared before use."],
        "_meta": INFRASTRUCTURE,
    }


def _composite(store: GraphStore, handle: str, role: str) -> dict:
    """A card that rates with Score under the alias ``role`` and tests with Verify."""
    score = f"sema:Score#mh:SHA-256:{store.get_pattern_hash('Score')}"
    verify = f"sema:Verify#mh:SHA-256:{store.get_pattern_hash('Verify')}"
    return {
        "handle": handle,
        "gloss": "Rate a proposal, then test it",
        "mechanism": f"Uses {{{{{role}}}}} to rate a proposal and {{{{verify}}}} to test it.",
        "invariants": ["A proposal is tested only after it is rated."],
        "dependencies": {"composes_with": {role: score, "verify": verify}},
        "_meta": SOCIETY,
    }


def _mint(store: GraphStore, pattern: dict) -> str:
    result = mint_pattern(
        pattern, store, known_handles=set(store._handle_to_id) | {pattern["handle"]}
    )
    assert result.success, result.errors
    return result.sema_id


def _database(path: Path, version: int, *, user_card: bool = False, legacy: bool = False) -> Path:
    store = GraphStore(str(path), enable_embeddings=False)
    store.set_canonicalization(version)
    _mint(store, _leaf("Score", "Rate a proposal"))
    _mint(store, _leaf("Verify", "Test a proposal"))
    _mint(store, _composite(store, "Review", "rating"))
    if user_card:
        _mint(store, _composite(store, "MyReview", "rater"))
    if legacy:
        # A database written before the setting existed carries no record.
        with sqlite3.connect(path) as conn:
            conn.execute("DROP TABLE store_settings")
    return path


def _pull(upstream: Path, workspace: Path) -> dict:
    with (
        patch("sema.cli.main.get_default_db_path", return_value=str(workspace)),
        patch("sema.cli.main.get_bundled_db_path", return_value=str(upstream)),
        patch("sema.cli.main.is_bundled_db", return_value=False),
    ):
        return update_db()


def _identity(store: GraphStore, handle: str) -> str:
    content = store._get_pattern_content(handle)
    return content["sema_id"]


@pytest.mark.parametrize("version", [CANONICALIZATION_V2, CANONICALIZATION_V3])
def test_an_empty_workspace_adopts_the_upstream_canonicalization(tmp_path, version):
    upstream = _database(tmp_path / "upstream.db", version)
    workspace = tmp_path / "workspace.db"
    GraphStore(str(workspace), enable_embeddings=False)

    assert _pull(upstream, workspace)["success"]

    store = GraphStore(str(workspace), enable_embeddings=False)
    assert store.canonicalization == version
    assert _identity(store, "Review") == _identity(GraphStore(str(upstream)), "Review")


def test_a_legacy_v2_workspace_moves_to_v3_and_recomputes_local_identities(tmp_path):
    upstream = _database(tmp_path / "upstream.db", CANONICALIZATION_V3)
    workspace = _database(
        tmp_path / "workspace.db", CANONICALIZATION_V2, user_card=True, legacy=True
    )
    before = GraphStore(str(workspace), enable_embeddings=False)
    assert before.canonicalization == CANONICALIZATION_V2
    old_user_id = _identity(before, "MyReview")

    result = _pull(upstream, workspace)

    assert result["success"]
    store = GraphStore(str(workspace), enable_embeddings=False)
    assert store.canonicalization == CANONICALIZATION_V3
    upstream_store = GraphStore(str(upstream), enable_embeddings=False)
    for handle in ("Score", "Verify", "Review"):
        assert _identity(store, handle) == _identity(upstream_store, handle)

    user = store._get_pattern_content("MyReview", include_deps=True)
    expected = generate_sema_hash(
        user, store.get_pattern_hash, canonicalization=CANONICALIZATION_V3
    )["full_id"]
    assert _identity(store, "MyReview") == expected != old_user_id
    assert "MyReview" in result["cascaded_user"]


def test_a_v3_workspace_refuses_an_older_upstream(tmp_path):
    upstream = _database(tmp_path / "upstream.db", CANONICALIZATION_V2)
    workspace = _database(tmp_path / "workspace.db", CANONICALIZATION_V3, user_card=True)
    before = workspace.read_bytes()

    result = _pull(upstream, workspace)

    assert not result["success"]
    assert "older than this workspace" in result["error"]
    assert (result["canonicalization_before"], result["canonicalization_after"]) == (3, 3)
    assert workspace.read_bytes() == before


def _child(store: GraphStore, handle: str, parent: str) -> dict:
    """A specialization pinned to the parent's current identity."""
    return {
        **_leaf(handle, f"Specialize {parent}"),
        "_meta": SOCIETY,
        "extends": _identity(store, parent),
    }


def _pull_verified(upstream: Path, workspace: Path) -> dict:
    with (
        patch("sema.cli.main.get_default_db_path", return_value=str(workspace)),
        patch("sema.cli.main.get_bundled_db_path", return_value=str(upstream)),
        patch("sema.cli.main.is_bundled_db", return_value=False),
    ):
        return update_db(verify=True)


def test_a_migration_carries_extends_pins_of_unchanged_parents(tmp_path):
    """A pin follows its parent when the parent is only re-identified, at any depth."""
    upstream = _database(tmp_path / "upstream.db", CANONICALIZATION_V3)
    workspace = tmp_path / "workspace.db"
    store = GraphStore(str(workspace), enable_embeddings=False)
    store.set_canonicalization(CANONICALIZATION_V2)
    _mint(store, _leaf("Score", "Rate a proposal"))
    _mint(store, _leaf("Verify", "Test a proposal"))
    _mint(store, _composite(store, "Review", "rating"))
    _mint(store, _composite(store, "MyReview", "rater"))
    _mint(store, _child(store, "ReviewChild", "Review"))  # upstream parent
    _mint(store, _child(store, "MyReviewChild", "MyReview"))  # local parent
    _mint(store, _child(store, "Grandchild", "ReviewChild"))  # through a moved child
    with sqlite3.connect(workspace) as conn:
        conn.execute("DROP TABLE store_settings")
    old = {h: _identity(store, h) for h in ("ReviewChild", "MyReviewChild", "Grandchild")}

    result = _pull_verified(upstream, workspace)

    assert result["success"], result.get("error")
    assert result["verified"]
    store = GraphStore(str(workspace), enable_embeddings=False)
    assert store.canonicalization == CANONICALIZATION_V3
    for child, parent in (
        ("ReviewChild", "Review"),
        ("MyReviewChild", "MyReview"),
        ("Grandchild", "ReviewChild"),
    ):
        content = store._get_pattern_content(child, include_deps=True)
        assert content["extends"] == _identity(store, parent), child
        expected = generate_sema_hash(
            content, store.get_pattern_hash, canonicalization=CANONICALIZATION_V3
        )["full_id"]
        assert _identity(store, child) == expected != old[child], child
        assert child in result["cascaded_user"]


def test_a_pin_does_not_follow_a_parent_whose_content_changed(tmp_path):
    upstream = _database(tmp_path / "upstream.db", CANONICALIZATION_V3)
    source = GraphStore(str(upstream), enable_embeddings=False)
    changed = {**_composite(source, "Review", "rating"), "gloss": "Rate a proposal twice"}
    _mint(source, changed)
    workspace = _database(tmp_path / "workspace.db", CANONICALIZATION_V2, legacy=True)
    _mint(
        GraphStore(str(workspace), enable_embeddings=False),
        _child(GraphStore(str(workspace), enable_embeddings=False), "ReviewChild", "Review"),
    )
    before = workspace.read_bytes()

    result = _pull(upstream, workspace)

    assert not result["success"]
    assert "strand ReviewChild" in result["error"]
    assert (result["canonicalization_before"], result["canonicalization_after"]) == (2, 2)
    assert workspace.read_bytes() == before


def test_a_read_only_empty_database_opens(tmp_path):
    path = tmp_path / "empty.db"
    GraphStore(str(path), enable_embeddings=False)
    with sqlite3.connect(path) as conn:
        conn.execute("DROP TABLE store_settings")
    path.chmod(0o444)
    try:
        store = GraphStore(str(path), enable_embeddings=False)
        assert store.canonicalization == CANONICALIZATION_V3
    finally:
        path.chmod(0o644)


def test_a_failed_migration_restores_the_old_canonicalization(tmp_path):
    """The recorded version is written inside the atomic pull and rolls back with it."""
    upstream = _database(tmp_path / "upstream.db", CANONICALIZATION_V3)
    workspace = _database(
        tmp_path / "workspace.db", CANONICALIZATION_V2, user_card=True, legacy=True
    )
    before = GraphStore(str(workspace), enable_embeddings=False)
    old = {h: _identity(before, h) for h in ("Score", "Verify", "Review", "MyReview")}

    with patch.object(GraphStore, "rehash_all", side_effect=RuntimeError("interrupted")):
        result = _pull(upstream, workspace)

    assert not result["success"]
    assert (result["canonicalization_before"], result["canonicalization_after"]) == (2, 2)
    store = GraphStore(str(workspace), enable_embeddings=False)
    assert store.canonicalization == CANONICALIZATION_V2
    assert {h: _identity(store, h) for h in old} == old
    with sqlite3.connect(workspace) as conn:
        assert not conn.execute(
            "SELECT 1 FROM sqlite_master WHERE name = 'store_settings'"
        ).fetchone()


def test_a_migration_that_changes_no_identity_can_still_be_undone(tmp_path):
    """Every pairing is implied, so no identity moves; the recorded version does."""
    upstream = tmp_path / "upstream.db"
    workspace = tmp_path / "workspace.db"
    for path, version in ((upstream, CANONICALIZATION_V3), (workspace, CANONICALIZATION_V2)):
        store = GraphStore(str(path), enable_embeddings=False)
        store.set_canonicalization(version)
        _mint(store, _leaf("Score", "Rate a proposal"))
        _mint(store, _leaf("Verify", "Test a proposal"))
        _mint(store, _composite(store, "Review", "score"))
    with sqlite3.connect(workspace) as conn:
        conn.execute("DROP TABLE store_settings")
    before = {
        h: _identity(GraphStore(str(workspace), enable_embeddings=False), h)
        for h in ("Score", "Verify", "Review")
    }

    result = _pull(upstream, workspace)

    assert result["success"]
    assert not result["added"] and not result["updated"] and not result["cascaded_user"]
    assert (result["canonicalization_before"], result["canonicalization_after"]) == (2, 3)
    moved = GraphStore(str(workspace), enable_embeddings=False)
    assert moved.canonicalization == CANONICALIZATION_V3
    assert {h: _identity(moved, h) for h in before} == before
    assert Path(str(workspace) + ".pull_previous").exists()

    with (
        patch("sema.cli.main.get_default_db_path", return_value=str(workspace)),
        patch("sema.cli.main.is_bundled_db", return_value=False),
        patch("sema.cli.main.is_read_only_db", return_value=False),
    ):
        assert undo_pull()
    restored = GraphStore(str(workspace), enable_embeddings=False)
    assert restored.canonicalization == CANONICALIZATION_V2
    assert {h: _identity(restored, h) for h in before} == before


def test_a_pull_that_changes_nothing_keeps_no_snapshot(tmp_path):
    upstream = _database(tmp_path / "upstream.db", CANONICALIZATION_V3)
    workspace = _database(tmp_path / "workspace.db", CANONICALIZATION_V3)

    result = _pull(upstream, workspace)

    assert result["success"]
    assert (result["canonicalization_before"], result["canonicalization_after"]) == (3, 3)
    assert not Path(str(workspace) + ".pull_previous").exists()


def test_a_dry_run_reports_the_version_the_pull_would_record(tmp_path):
    upstream = _database(tmp_path / "upstream.db", CANONICALIZATION_V3)
    workspace = _database(tmp_path / "workspace.db", CANONICALIZATION_V2, legacy=True)
    with (
        patch("sema.cli.main.get_default_db_path", return_value=str(workspace)),
        patch("sema.cli.main.get_bundled_db_path", return_value=str(upstream)),
        patch("sema.cli.main.is_bundled_db", return_value=False),
    ):
        result = update_db(dry_run=True)
    assert result["success"]
    assert (result["canonicalization_before"], result["canonicalization_after"]) == (2, 3)
    assert GraphStore(str(workspace), enable_embeddings=False).canonicalization == 2
