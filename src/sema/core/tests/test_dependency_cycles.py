"""Tests for cycle detection across the batch and the committed corpus.

Regression cover for a defect that lost a tranche of vocabulary work. A mutual
`references` pair between a staged pattern and an already-committed one passed
`sema apply --check`, because `topological_sort` drops every edge whose target is
outside the batch and because it runs after --check has returned. The full rebuild
caught the cycle, but only after replacing the database.
"""

import pytest

from ..dependencies import (
    build_dependency_adjacency,
    find_cycle_through,
    get_dependencies_handles,
    topological_sort,
    validate_acyclic,
)


def pattern(handle, references=(), composes_with=()):
    """Minimal pattern carrying only what dependency extraction reads."""
    deps = {}
    if references:
        deps["references"] = {h.lower(): f"sema:{h}#mh:SHA-256:{'0' * 64}" for h in references}
    if composes_with:
        deps["composes_with"] = {
            h.lower(): f"sema:{h}#mh:SHA-256:{'0' * 64}" for h in composes_with
        }
    return {"handle": handle, "dependencies": deps}


def test_topological_sort_misses_a_cycle_that_leaves_the_batch():
    """Documents why validate_acyclic exists: the sort cannot see this case."""
    staged = {"AnalogyBridge": pattern("AnalogyBridge", references=["ConceptBlend"])}

    # No error, because ConceptBlend is not in the batch and the edge is dropped.
    assert topological_sort(staged) == ["AnalogyBridge"]


def test_validate_acyclic_catches_a_mutual_pair_with_a_committed_pattern():
    staged = {"AnalogyBridge": pattern("AnalogyBridge", references=["ConceptBlend"])}
    committed = {"ConceptBlend": pattern("ConceptBlend", references=["AnalogyBridge"])}

    with pytest.raises(ValueError) as exc:
        validate_acyclic(staged, committed)

    message = str(exc.value)
    assert "Cycle detected" in message
    assert "AnalogyBridge --> ConceptBlend --> AnalogyBridge" in message


def test_validate_acyclic_accepts_a_one_way_edge_to_a_committed_pattern():
    """Card -> Greet is legitimate precisely because Greet does not reference Card."""
    staged = {"Card": pattern("Card", references=["Greet"])}
    committed = {"Greet": pattern("Greet", references=["Agent", "Identity"])}

    validate_acyclic(staged, committed)


def test_validate_acyclic_catches_a_longer_cycle():
    staged = {"A": pattern("A", references=["B"])}
    committed = {
        "B": pattern("B", references=["C"]),
        "C": pattern("C", composes_with=["A"]),
    }

    with pytest.raises(ValueError) as exc:
        validate_acyclic(staged, committed)

    assert "A --> B --> C --> A" in str(exc.value)


def test_validate_acyclic_ignores_a_cycle_that_does_not_involve_the_batch():
    """A pre-existing cycle elsewhere must not block an unrelated change."""
    staged = {"Card": pattern("Card", references=["Greet"])}
    committed = {
        "Greet": pattern("Greet"),
        "X": pattern("X", references=["Y"]),
        "Y": pattern("Y", references=["X"]),
    }

    validate_acyclic(staged, committed)


def test_validate_acyclic_ignores_a_cycle_through_a_pattern_being_replaced():
    """The staged version of a pattern wins, so dropping its back-edge clears the cycle."""
    committed = {
        "AnalogyBridge": pattern("AnalogyBridge", references=["ConceptBlend"]),
        "ConceptBlend": pattern("ConceptBlend", references=["AnalogyBridge"]),
    }
    staged = {"AnalogyBridge": pattern("AnalogyBridge", references=["Solution"])}

    validate_acyclic(staged, committed)


def test_validate_acyclic_tolerates_edges_to_handles_outside_the_corpus():
    staged = {"A": pattern("A", references=["NotInCorpus"])}

    validate_acyclic(staged, {})


def test_validate_acyclic_rejects_self_dependency():
    staged = {"SelfRef": pattern("SelfRef", references=["SelfRef"])}

    with pytest.raises(ValueError) as exc:
        validate_acyclic(staged, {})

    assert "SelfRef --> SelfRef" in str(exc.value)


def test_build_dependency_adjacency_lets_the_batch_override_the_committed_version():
    committed = {"A": pattern("A", references=["B"]), "B": pattern("B")}
    staged = {"A": pattern("A", references=["C"])}

    adj = build_dependency_adjacency(staged, {**committed, "C": pattern("C")})

    assert adj["A"] == {"C"}


def test_legacy_derived_from_is_not_reinterpreted_as_a_dependency():
    legacy = pattern("Child")
    legacy["derived_from"] = "sema:RetiredParent"

    assert get_dependencies_handles(legacy) == set()


def test_find_cycle_through_returns_none_for_a_node_off_any_cycle():
    adj = {"A": {"B"}, "B": {"C"}, "C": set()}

    assert find_cycle_through(adj, "A") is None


def test_find_cycle_through_visits_each_node_once_on_a_dense_graph():
    """A depth-first enumeration of paths would be exponential here."""
    handles = [f"P{i}" for i in range(60)]
    adj = {h: set(handles) - {h} for h in handles}

    cycle = find_cycle_through(adj, "P0")

    assert cycle is not None
    assert cycle[0] == "P0" and cycle[-1] == "P0"
