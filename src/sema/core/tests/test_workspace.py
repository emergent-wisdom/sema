import hashlib

from sema.core.workspace import GraphWorkspace, WorkspaceSession, WorkspaceSource


class StubRegistry:
    source = "stub"
    db_path = "/tmp/workspace.db"
    vocab_dir = "/tmp/vocabulary"

    def __init__(self):
        self.registry = {
            "Alpha": {
                "handle": "Alpha",
                "gloss": "Alpha gloss",
                "mechanism": "Alpha mechanism",
                "sema_id": "sema:Alpha#mh:SHA-256:" + ("a" * 64),
                "sema_ref": "Alpha#aaaa",
                "sema_stub": "aaaa",
                "sema_layer": "Mind",
                "sema_category": "Reasoning",
            },
            "Task": {
                "handle": "Task",
                "gloss": "Task gloss",
                "mechanism": "Task mechanism",
                "sema_id": "sema:Task#mh:SHA-256:" + ("b" * 64),
                "sema_ref": "Task#bbbb",
                "sema_stub": "bbbb",
                "sema_layer": "Infrastructure",
                "sema_category": "Data Structures",
            },
        }

    def refresh(self):
        pass

    def search(self, query, use_semantic=True):
        return [
            {
                "handle": "Alpha",
                "sema_ref": "Alpha#aaaa",
                "gloss": "Alpha gloss",
                "mechanism": "Alpha mechanism",
                "score": 1.0,
            }
        ]

    def get_context(self, handle):
        return {"dependencies": [], "used_by": []}

    def resolve(self, handle, depth=1):
        if handle == "Alpha":
            return {"Alpha": self.registry["Alpha"], "Task": self.registry["Task"]}
        return None

    def get_pattern(self, handle):
        return self.registry.get(handle)

    def get_graph_skeleton(self):
        return "stub skeleton"


def make_workspace():
    return GraphWorkspace(
        WorkspaceSource(workspace_id="team-a", label="Team A", db_path="/tmp/workspace.db"),
        registry_manager=StubRegistry(),
    )


def test_search_session_cache_is_per_session():
    workspace = make_workspace()
    first_session = WorkspaceSession()
    second_session = WorkspaceSession()

    first_seen = workspace.search("alpha", session=first_session)
    first_compact = workspace.search("alpha", session=first_session)
    second_seen = workspace.search("alpha", session=second_session)

    assert "_seen" not in first_seen[0]
    assert first_compact[0]["_seen"] is True
    assert "_seen" not in second_seen[0]


def test_resolve_marks_only_the_supplied_session():
    workspace = make_workspace()
    session = WorkspaceSession()

    result = workspace.resolve("Alpha", session=session)

    assert result["count"] == 2
    assert "Alpha" in session.served_patterns
    assert "Task" in session.served_patterns


def test_validate_uses_workspace_known_handles():
    workspace = make_workspace()
    task_id = "sema:Task#mh:SHA-256:" + ("b" * 64)
    pattern = {
        "handle": "Consumer",
        "mechanism": "Consumes {{task}}.",
        "gloss": "Consumes task",
        "_meta": {"path": ["Mind", "Reasoning"], "ring": 1, "tier": 2},
        "dependencies": {"references": {"task": task_id}},
    }

    result = workspace.validate_pattern(pattern)

    assert result["valid"] is True
    assert result["errors"] == []


def test_validate_reports_missing_workspace_dependency():
    workspace = make_workspace()
    missing_id = "sema:Missing#mh:SHA-256:" + ("c" * 64)
    pattern = {
        "handle": "Consumer",
        "mechanism": "Consumes {{missing}}.",
        "gloss": "Consumes missing thing",
        "_meta": {"path": ["Mind", "Reasoning"], "ring": 1, "tier": 2},
        "dependencies": {"references": {"missing": missing_id}},
    }

    result = workspace.validate_pattern(pattern)

    assert result["valid"] is False
    assert any("Missing" in error for error in result["errors"])


def test_vocabulary_root_sorts_by_handle():
    workspace = make_workspace()
    expected = hashlib.sha256((("a" * 64) + ("b" * 64)).encode()).hexdigest()

    root = workspace.vocabulary_root()

    assert root["hash"] == expected
    assert root["stub"] == expected[:16]
    assert root["pattern_count"] == 2


def test_handshake_is_scoped_to_workspace():
    workspace = make_workspace()

    provide = workspace.handshake("Alpha")
    proceed = workspace.handshake("Alpha", your_hash="aaaa")
    halt = workspace.handshake("Alpha", your_hash="zzzz")

    assert provide["verdict"] == "PROVIDE_HASH"
    assert proceed["verdict"] == "PROCEED"
    assert halt["verdict"] == "HALT"
    assert halt["canonical_hash"] == "aaaa"


def test_handshake_pattern_accepts_full_hash():
    """An agent holding the full 64-char hash must not get a false HALT."""
    workspace = make_workspace()

    proceed = workspace.handshake("Alpha", your_hash="a" * 64)

    assert proceed["verdict"] == "PROCEED"


def test_handshake_pattern_normalizes_case_and_whitespace():
    workspace = make_workspace()

    proceed_stub = workspace.handshake("Alpha", your_hash="  AAAA  ")
    proceed_full = workspace.handshake("Alpha", your_hash=("A" * 64))

    assert proceed_stub["verdict"] == "PROCEED"
    assert proceed_full["verdict"] == "PROCEED"


def test_handshake_pattern_blank_hash_asks_for_hash():
    workspace = make_workspace()

    result = workspace.handshake("Alpha", your_hash="   ")

    assert result["verdict"] == "PROVIDE_HASH"


def test_handshake_pattern_full_hash_drift_still_halts():
    workspace = make_workspace()

    halt = workspace.handshake("Alpha", your_hash="f" * 64)

    assert halt["verdict"] == "HALT"


def test_workspace_description_exposes_hosted_identity_fields():
    workspace = make_workspace()

    description = workspace.describe()

    assert description["workspace_id"] == "team-a"
    assert description["label"] == "Team A"
    assert description["pattern_count"] == 2
    assert description["db_path"] == "/tmp/workspace.db"
    assert description["data_source"] == "stub"
