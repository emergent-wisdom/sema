"""The handshake says which canonicalization a workspace's digests use.

A digest does not say how its definition was canonicalized, and v2 does not bind
placeholders to their targets. A v2 and a v3 workspace can therefore agree on a
digest while the v2 one holds a card whose targets were exchanged. Every answer
about a known identity carries the workspace's canonicalization. When the peer's
differs, strict mode halts and cooperative mode warns; a strict comparison that
declares none is read as v2, the version of every release before the declaration.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from sema.core.hashing import CANONICALIZATION_V2, CANONICALIZATION_V3
from sema.core.mint import mint_pattern
from sema.core.workspace import GraphWorkspace, WorkspaceSource
from sema.taxonomy_graph.graph_store import GraphStore

INFRASTRUCTURE = {"path": ["Infrastructure", "Primitives"], "ring": 0, "tier": 0}
SOCIETY = {"path": ["Society", "Economics"], "ring": 1, "tier": 1}
OTHER = {CANONICALIZATION_V2: CANONICALIZATION_V3, CANONICALIZATION_V3: CANONICALIZATION_V2}


def _leaf(handle: str, gloss: str) -> dict:
    return {
        "handle": handle,
        "gloss": gloss,
        "mechanism": f"{gloss} against a declared condition.",
        "invariants": ["The condition is declared before use."],
        "_meta": INFRASTRUCTURE,
    }


def _workspace(path, version: int, *, exchanged: bool = False, legacy: bool = False):
    """A workspace holding Score, Verify and Review, which uses both by name.

    ``exchanged`` binds each of Review's placeholders to the other's target.
    """
    store = GraphStore(str(path), enable_embeddings=False)
    store.set_canonicalization(version)
    ids = {}
    for card in (_leaf("Score", "Rate a proposal"), _leaf("Verify", "Test a proposal")):
        result = mint_pattern(card, store, known_handles={"Score", "Verify", "Review"})
        assert result.success, result.errors
        ids[card["handle"]] = result.sema_id
    score, verify = ("Verify", "Score") if exchanged else ("Score", "Verify")
    review = {
        "handle": "Review",
        "gloss": "Rate a proposal, then test it",
        "mechanism": "Uses {{score}} to rate a proposal and {{verify}} to test it.",
        "invariants": ["A proposal is tested only after it is rated."],
        "dependencies": {"composes_with": {"score": ids[score], "verify": ids[verify]}},
        "_meta": SOCIETY,
    }
    result = mint_pattern(review, store, known_handles={"Score", "Verify", "Review"})
    assert result.success, result.errors
    if legacy:
        with sqlite3.connect(path) as conn:
            conn.execute("DROP TABLE store_settings")
    return GraphWorkspace(WorkspaceSource(db_path=str(path)))


def _digest(workspace: GraphWorkspace, handle: str) -> str:
    return workspace.registry[handle]["sema_id"].split("SHA-256:")[1]


@pytest.fixture(params=[CANONICALIZATION_V2, CANONICALIZATION_V3], ids=["v2", "v3"])
def workspace(request, tmp_path):
    return _workspace(tmp_path / "workspace.db", request.param)


def test_every_answer_about_a_known_identity_carries_the_canonicalization(workspace):
    version = workspace.canonicalization
    digest = _digest(workspace, "Review")
    root = workspace.root_payload()
    assert root["canonicalization"] == version
    answers = [
        workspace.handshake("Review"),
        workspace.handshake("Review", digest[:4]),
        workspace.handshake("Review", digest[:4], strict=True, your_canonicalization=version),
        workspace.handshake("Review", digest, strict=True, your_canonicalization=version),
        workspace.handshake("Review", "0" * 64),
        workspace.handshake("vocab"),
        workspace.handshake(
            "catalog", root["catalog_root"], your_scheme=root["catalog_root_scheme"]
        ),
        workspace.handshake("catalog", root["catalog_root"]),
    ]
    assert [a["verdict"] for a in answers] == [
        "PROVIDE_HASH",
        "PROCEED",
        "REQUIRE_FULL_HASH",
        "PROCEED",
        "HALT",
        "PROVIDE_HASH",
        "PROCEED",
        "HALT",
    ]
    assert all(a["canonicalization"] == version for a in answers)


def test_a_database_without_the_record_answers_as_v2(tmp_path):
    workspace = _workspace(tmp_path / "legacy.db", CANONICALIZATION_V2, legacy=True)
    assert workspace.canonicalization == CANONICALIZATION_V2
    assert workspace.handshake("Review")["canonicalization"] == CANONICALIZATION_V2


def test_strict_mode_halts_on_a_declared_difference(workspace):
    digest = _digest(workspace, "Review")
    answer = workspace.handshake(
        "Review", digest, strict=True, your_canonicalization=OTHER[workspace.canonicalization]
    )
    assert answer["verdict"] == "HALT"
    assert answer["reason"] == "CANONICALIZATION MISMATCH"
    assert answer["handle"] == "Review"
    assert answer["canonicalization"] == workspace.canonicalization
    assert answer["your_canonicalization"] == OTHER[workspace.canonicalization]
    assert "verified_ref" not in answer and "assurance" not in answer


def test_strict_mode_proceeds_when_the_declared_version_agrees(workspace):
    digest = _digest(workspace, "Review")
    answer = workspace.handshake(
        "Review", digest, strict=True, your_canonicalization=workspace.canonicalization
    )
    assert answer["verdict"] == "PROCEED"
    assert answer["assurance"] == "full_hash"


def test_strict_mode_reads_an_undeclared_version_as_v2(workspace):
    """A peer that declares nothing is on a release that hashes under v2.

    A v2 workspace compares as it always did. A v3 workspace does not take an
    undeclared digest as proof, since the peer never checked the bindings.
    """
    digest = _digest(workspace, "Review")
    for presented in (digest, digest[:4]):
        answer = workspace.handshake("Review", presented, strict=True)
        if workspace.canonicalization == CANONICALIZATION_V2:
            assert answer["verdict"] == ("PROCEED" if presented == digest else "REQUIRE_FULL_HASH")
        else:
            assert answer["verdict"] == "HALT"
            assert answer["reason"] == "CANONICALIZATION REQUIRED"
            assert answer["canonicalization"] == CANONICALIZATION_V3
            assert answer["your_canonicalization"] is None
            assert "your_canonicalization" in answer["action"]


def test_an_undeclared_version_changes_nothing_outside_a_strict_comparison(workspace):
    digest = _digest(workspace, "Review")
    assert workspace.handshake("Review", digest[:4])["verdict"] == "PROCEED"
    assert workspace.handshake("Review", digest)["verdict"] == "PROCEED"
    assert "warning" not in workspace.handshake("Review", digest)
    # Asking for the canonical hash is not a comparison, in either mode.
    assert workspace.handshake("Review", strict=True)["verdict"] == "PROVIDE_HASH"
    assert workspace.handshake("vocab", strict=True)["verdict"] == "PROVIDE_HASH"


def test_strict_roots_read_an_undeclared_version_as_v2(workspace):
    root = workspace.root_payload()
    answer = workspace.handshake(
        "catalog", root["catalog_root"], strict=True, your_scheme=root["catalog_root_scheme"]
    )
    if workspace.canonicalization == CANONICALIZATION_V2:
        assert answer["verdict"] == "PROCEED"
    else:
        assert answer["verdict"] == "HALT"
        assert answer["reason"] == "CANONICALIZATION REQUIRED"


def test_a_legacy_workspace_compares_strictly_as_before(tmp_path):
    workspace = _workspace(tmp_path / "legacy.db", CANONICALIZATION_V2, legacy=True)
    answer = workspace.handshake("Review", _digest(workspace, "Review"), strict=True)
    assert answer["verdict"] == "PROCEED" and answer["assurance"] == "full_hash"


def test_cooperative_mode_keeps_its_verdict_and_warns(workspace):
    digest = _digest(workspace, "Review")
    other = OTHER[workspace.canonicalization]
    answer = workspace.handshake("Review", digest[:4], your_canonicalization=other)
    assert answer["verdict"] == "PROCEED"
    assert answer["your_canonicalization"] == other
    assert f"v{other}" in answer["warning"]
    drift = workspace.handshake("Review", "0" * 64, your_canonicalization=other)
    assert drift["verdict"] == "HALT" and "warning" in drift


@pytest.mark.parametrize("declared", [1, 4, "3", 3.0, True], ids=repr)
def test_an_unsupported_declaration_never_proceeds_in_strict_mode(workspace, declared):
    digest = _digest(workspace, "Review")
    answer = workspace.handshake("Review", digest, strict=True, your_canonicalization=declared)
    assert answer["verdict"] == "HALT"
    assert answer["reason"] == "CANONICALIZATION MISMATCH"


def test_an_unknown_pattern_halts_as_before(workspace):
    answer = workspace.handshake("Missing", "abcd", strict=True, your_canonicalization=3)
    assert answer["verdict"] == "HALT"
    assert "not found" in answer["reason"]


def test_roots_follow_the_same_rule(workspace):
    root = workspace.root_payload()
    for scope, digest, scheme in (
        ("vocab", root["semantic_root"], root["semantic_root_scheme"]),
        ("catalog", root["catalog_root"], root["catalog_root_scheme"]),
    ):
        same = workspace.handshake(
            scope,
            digest,
            strict=True,
            your_scheme=scheme,
            your_canonicalization=workspace.canonicalization,
        )
        assert same["verdict"] == "PROCEED"
        other = workspace.handshake(
            scope,
            digest,
            strict=True,
            your_scheme=scheme,
            your_canonicalization=OTHER[workspace.canonicalization],
        )
        assert other["verdict"] == "HALT"
        assert other["reason"] == "CANONICALIZATION MISMATCH"
        assert other["scope"] == scope


def test_a_workspace_without_a_recorded_version_cannot_match_a_declared_one():
    class Registry:
        registry = {"Solo": {"sema_id": f"sema:Solo#mh:SHA-256:{'a' * 64}", "sema_stub": "aaaa"}}

        def refresh(self):
            pass

    workspace = GraphWorkspace(registry_manager=Registry())
    assert workspace.canonicalization is None
    # Nothing recorded and nothing declared: there is no version to hold it to.
    assert workspace.handshake("Solo", "a" * 64, strict=True)["verdict"] == "PROCEED"
    answer = workspace.handshake("Solo", "a" * 64, strict=True, your_canonicalization=3)
    assert answer["verdict"] == "HALT"
    assert "does not record" in answer["action"]


def test_the_case_the_declaration_exists_for(tmp_path):
    """A v2 peer holds Review with its targets exchanged; the digest is the same.

    Every pairing of the honest card is implied, so its v2 and v3 digests are
    equal, and v2 cannot see the exchange. A strict comparison halts whether the
    v2 peer declares its version or, like every release before the declaration,
    sends none. Only the cooperative check, which is not proof, goes through.
    """
    honest = _workspace(tmp_path / "honest.db", CANONICALIZATION_V3)
    miswired = _workspace(tmp_path / "miswired.db", CANONICALIZATION_V2, exchanged=True)
    peer_digest = _digest(miswired, "Review")
    assert peer_digest == _digest(honest, "Review")

    undeclared = honest.handshake("Review", peer_digest, strict=True)
    assert undeclared["verdict"] == "HALT"
    assert undeclared["reason"] == "CANONICALIZATION REQUIRED"
    declared = honest.handshake(
        "Review", peer_digest, strict=True, your_canonicalization=miswired.canonicalization
    )
    assert declared["verdict"] == "HALT"
    assert declared["reason"] == "CANONICALIZATION MISMATCH"
    assert honest.handshake("Review", peer_digest)["verdict"] == "PROCEED"


def test_the_mcp_tool_passes_the_declaration_through(tmp_path, monkeypatch):
    from sema.mcp import server

    workspace = _workspace(tmp_path / "workspace.db", CANONICALIZATION_V3)
    monkeypatch.setattr(server, "_active_workspace", lambda: workspace)
    digest = _digest(workspace, "Review")

    assert json.loads(server.sema_root())["canonicalization"] == CANONICALIZATION_V3
    proceed = json.loads(
        server.sema_handshake("Review", digest, strict=True, your_canonicalization=3)
    )
    assert proceed["verdict"] == "PROCEED" and proceed["canonicalization"] == 3
    halt = json.loads(server.sema_handshake("Review", digest, strict=True, your_canonicalization=2))
    assert halt["verdict"] == "HALT" and halt["reason"] == "CANONICALIZATION MISMATCH"
