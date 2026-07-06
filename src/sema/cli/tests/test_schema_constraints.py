"""Schema-level integrity constraints (issue #29).

Python write paths (`sema apply`, mint, pull) validate these invariants,
but the schema is the backstop for writes that bypass them — direct SQL,
migration bugs, crashed half-writes. These tests corrupt the DB the way
`apply()` never would, and expect SQLite itself to refuse.
"""

import json
import os
import shutil
import sqlite3
import tempfile
import unittest
import uuid

import pytest

from sema.taxonomy_graph.graph_store import GraphStore


class TestSchemaConstraints(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "constraints.db")
        self.store = GraphStore(self.db_path)
        result = self.store.add_pattern(
            {
                "handle": "Anchor",
                "mechanism": "anchor mechanism",
                "gloss": "Anchor",
                "_meta": {"layer": "Infrastructure", "category": "Primitives", "tier": 1},
            }
        )
        assert result.get("success"), result.get("error")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def _raw_conn(self):
        return sqlite3.connect(self.db_path)

    def test_duplicate_pattern_handle_rejected_by_schema(self):
        """A second PATTERN row with the same handle must fail at the DB."""
        with self._raw_conn() as conn:
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO nodes (id, node_type, text, metadata) VALUES (?, ?, ?, ?)",
                    (str(uuid.uuid4()), "PATTERN", "Anchor", "{}"),
                )

    def test_duplicate_sema_id_rejected_by_schema(self):
        """A second PATTERN row with the same sema_id must fail at the DB."""
        with self._raw_conn() as conn:
            sema_id = conn.execute(
                "SELECT sema_id FROM nodes WHERE node_type='PATTERN' AND text='Anchor'"
            ).fetchone()[0]
            assert sema_id, "Anchor should have a sema_id after mint"

            metadata = json.dumps({"pattern": {"handle": "Other", "sema_id": sema_id}})
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO nodes (id, node_type, text, metadata) VALUES (?, ?, ?, ?)",
                    (str(uuid.uuid4()), "PATTERN", "Other", metadata),
                )

    def test_non_pattern_nodes_exempt_from_uniqueness(self):
        """Two INVARIANT nodes may share text — only PATTERN rows are constrained."""
        with self._raw_conn() as conn:
            for _ in range(2):
                conn.execute(
                    "INSERT INTO nodes (id, node_type, text, metadata) VALUES (?, ?, ?, ?)",
                    (str(uuid.uuid4()), "INVARIANT", "same invariant text", "{}"),
                )

    def test_dangling_edge_rejected_through_store_connection(self):
        """Edges referencing missing nodes must fail on store connections.

        FK enforcement is per-connection, so this exercises the store's own
        connection helper — the path every real write uses.
        """
        anchor_id = self.store._find_pattern_id("Anchor")
        conn = self.store._connect()
        try:
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO edges (id, source_id, target_id, edge_type) "
                    "VALUES (?, ?, ?, ?)",
                    (str(uuid.uuid4()), anchor_id, "no-such-node-id", "REFERENCES"),
                )
        finally:
            conn.close()

    def test_legacy_db_with_duplicates_still_opens(self):
        """A pre-constraint DB that already violates uniqueness must load
        (with a warning), not crash — constraints are a backstop, not a
        migration blocker."""
        legacy_path = os.path.join(self.temp_dir, "legacy.db")
        conn = sqlite3.connect(legacy_path)
        conn.execute(
            "CREATE TABLE nodes (id TEXT PRIMARY KEY, node_type TEXT NOT NULL, "
            "text TEXT NOT NULL, metadata TEXT DEFAULT '{}', embedding BLOB)"
        )
        conn.execute(
            "CREATE TABLE edges (id TEXT PRIMARY KEY, source_id TEXT NOT NULL, "
            "target_id TEXT NOT NULL, edge_type TEXT NOT NULL, "
            "metadata TEXT DEFAULT '{}', "
            "FOREIGN KEY (source_id) REFERENCES nodes(id), "
            "FOREIGN KEY (target_id) REFERENCES nodes(id))"
        )
        for _ in range(2):
            conn.execute(
                "INSERT INTO nodes (id, node_type, text) VALUES (?, 'PATTERN', 'Dupe')",
                (str(uuid.uuid4()),),
            )
        conn.commit()
        conn.close()

        store = GraphStore(legacy_path)  # must not raise
        self.assertIn("Dupe", store._handle_to_id)


if __name__ == "__main__":
    unittest.main()
