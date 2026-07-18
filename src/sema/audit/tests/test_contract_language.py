"""Contract coverage must remain advisory rather than a quality score."""

import networkx as nx

from sema.audit import graph, rigor
from sema.taxonomy_graph.graph_store import EdgeType, NodeType


class ContractFreeStore:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.graph.add_node(
            "pattern",
            node_type=NodeType.PATTERN,
            text="BroadPrimitive",
            metadata={"layer": "Infrastructure", "category": "Primitives"},
        )
        self.graph.add_node(
            "path",
            node_type=NodeType.TAXONOMY_PATH,
            text="Infrastructure/Primitives",
            metadata={},
        )
        self.graph.add_edge("pattern", "path", key="path-edge", edge_type=EdgeType.IN_PATH)

    def get_nodes_by_type(self, node_type):
        return [
            (node_id, data)
            for node_id, data in self.graph.nodes(data=True)
            if data.get("node_type") == node_type
        ]


def test_graph_audit_does_not_treat_contract_coverage_as_a_problem(monkeypatch, capsys):
    store = ContractFreeStore()
    monkeypatch.setattr(graph, "GraphStore", lambda _path: store)

    graph.audit_graph()

    output = capsys.readouterr().out
    assert "0 structural problems" in output
    assert "No structural problems found." in output
    assert "[NO_CONTRACTS]" not in output
    assert "CONTRACT_REVIEW" not in output


def test_rigor_audit_uses_neutral_contract_coverage_language(monkeypatch, capsys):
    store = ContractFreeStore()
    monkeypatch.setattr(rigor, "GraphStore", lambda _path: store)

    rigor.audit_rigor()

    output = capsys.readouterr().out
    assert '"without_explicit_contracts": 1' in output
    assert "review only; omission may be intentional" in output
    assert "Naked" not in output
