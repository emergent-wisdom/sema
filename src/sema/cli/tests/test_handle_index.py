"""Index consistency tests for GraphStore._handle_to_id.

The index must match a full graph scan across every mutation path
(create_node via add_pattern, delete_node_cascade, merge_nodes)
and survive a reload (_load_graph).
"""

import os
import tempfile
import unittest

from sema.taxonomy_graph.graph_store import EdgeType, GraphStore, NodeType


def _scan_patterns(store: GraphStore) -> dict[str, str]:
    """Ground-truth handle→id map via full graph scan."""
    return {
        data["text"]: nid
        for nid, data in store.graph.nodes(data=True)
        if data.get("node_type") == NodeType.PATTERN
    }


class TestHandleIndex(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "idx.db")
        self.store = GraphStore(self.db_path)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir)

    def _add(self, handle: str, mechanism: str = "noop", **extra) -> str:
        pattern = {
            "handle": handle,
            "mechanism": mechanism,
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
            **extra,
        }
        result = self.store.add_pattern(pattern)
        self.assertTrue(result.get("success"), result.get("error"))
        return result["solution_id"]

    def test_add_pattern_populates_index(self):
        pid = self._add("FooPattern")
        self.assertIn("FooPattern", self.store._handle_to_id)
        self.assertEqual(self.store._handle_to_id["FooPattern"], pid)

    def test_delete_node_cascade_evicts_index(self):
        pid = self._add("BarPattern")
        self.assertIn("BarPattern", self.store._handle_to_id)
        self.store.delete_node_cascade(pid)
        self.assertNotIn("BarPattern", self.store._handle_to_id)

    def test_merge_nodes_evicts_removed_handle(self):
        keep_id = self._add("KeepPattern")
        remove_id = self._add("RemovePattern")
        self.assertIn("RemovePattern", self.store._handle_to_id)

        ok = self.store.merge_nodes(keep_id, remove_id)
        self.assertTrue(ok)
        self.assertNotIn("RemovePattern", self.store._handle_to_id)
        # The kept pattern stays
        self.assertEqual(self.store._handle_to_id["KeepPattern"], keep_id)

    def test_load_graph_reconstructs_index(self):
        self._add("AlphaPattern")
        self._add("BetaPattern")
        before = dict(self.store._handle_to_id)

        # Drop and reload the store from the same on-disk DB
        reopened = GraphStore(self.db_path)
        self.assertEqual(before, reopened._handle_to_id)

    def test_index_matches_scan_after_churn(self):
        """Bulk add/remove/merge — index parity must survive."""
        handles = [f"Pat{i}" for i in range(5)]
        ids = [self._add(h) for h in handles]

        # Remove two
        self.store.delete_node_cascade(ids[0])
        self.store.delete_node_cascade(ids[2])

        # Merge one into another
        self.store.merge_nodes(ids[1], ids[3])

        self.assertEqual(self.store._handle_to_id, _scan_patterns(self.store))

    def test_add_pattern_with_dependency_uses_index(self):
        """Dependency wiring should resolve target via the index."""
        self._add("Base")
        self._add(
            "Child",
            mechanism="Uses {{base}}",
            dependencies={"references": {"base": "Base#stub"}},
        )

        child_id = self.store._handle_to_id["Child"]
        base_id = self.store._handle_to_id["Base"]
        # Verify the REFERENCES edge exists from Child → Base
        self.assertTrue(
            self.store.has_edge_of_type(child_id, base_id, EdgeType.REFERENCES),
            "REFERENCES edge missing — dependency wiring may be broken",
        )


if __name__ == "__main__":
    unittest.main()
