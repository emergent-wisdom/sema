"""Graph store for SolutionTaxonomy using SQLite + NetworkX."""

import json
import re
import sqlite3
import uuid
from enum import Enum
from typing import Any

import networkx as nx
import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from .embedding_service import EmbeddingService


class NodeType(str, Enum):
    PATTERN = "PATTERN"
    SOLUTION = "SOLUTION"  # Deprecated: use PATTERN
    MECHANISM = "MECHANISM"  # core_mechanism
    OUTCOME = "OUTCOME"  # long_term_vision
    PRINCIPLE = "PRINCIPLE"  # design_principles
    CRITICISM = "CRITICISM"  # why_it_fails
    JUSTIFICATION = "JUSTIFICATION"  # why_it_works
    NOVELTY = "NOVELTY"  # what_is_new
    SCENARIO = "SCENARIO"  # when_to_use / context
    COUNTERFACTUAL = "COUNTERFACTUAL"  # what happens WITHOUT this pattern (baseline comparison)
    # Contract types (formal specification)
    INVARIANT = "INVARIANT"  # strict logical rules that must hold
    PRECONDITION = "PRECONDITION"  # required state before pattern execution
    POSTCONDITION = "POSTCONDITION"  # guaranteed state after pattern execution
    INPUT = "INPUT"  # typed input parameters
    OUTPUT = "OUTPUT"  # typed output values
    PARAMETER = "PARAMETER"  # configuration slots with range contracts
    BASELINE = "BASELINE"  # baseline comparison (deprecated: use COUNTERFACTUAL)
    # Taxonomy hierarchy (hypergraph structure)
    LAYER = "LAYER"  # Physics, Mind, Society, Infrastructure
    CATEGORY = "CATEGORY"  # 19 pattern categories


class EdgeType(Enum):
    # Core Relationships
    IS_A = "IS_A"
    PART_OF = "PART_OF"
    HAS_PROPERTY = "HAS_PROPERTY"
    RELATED_TO = "RELATED_TO"

    # Structural/Taxonomic
    IN_CATEGORY = "IN_CATEGORY"
    USES_MECHANISM = "USES_MECHANISM"
    MACRO_FOR = "MACRO_FOR"  # Alias/Wrapper relationship

    # Contracts & Safety
    HAS_INVARIANT = "HAS_INVARIANT"
    HAS_PRECONDITION = "HAS_PRECONDITION"
    HAS_POSTCONDITION = "HAS_POSTCONDITION"
    HAS_INPUT = "HAS_INPUT"
    HAS_OUTPUT = "HAS_OUTPUT"
    HAS_PARAMETER = "HAS_PARAMETER"

    # Functionality
    SOLVES_PROBLEM = "SOLVES_PROBLEM"
    PRODUCES_OUTCOME = "PRODUCES_OUTCOME"
    REQUIRES_INPUT = "REQUIRES_INPUT"
    FOLLOWS_PRINCIPLE = "FOLLOWS_PRINCIPLE"
    HAS_FAILURE_MODE = "HAS_FAILURE_MODE"
    HAS_CRITICISM = "HAS_CRITICISM"
    HAS_JUSTIFICATION = "HAS_JUSTIFICATION"
    CLAIMS_NOVELTY = "CLAIMS_NOVELTY"
    SOLVES_SCENARIO = "SOLVES_SCENARIO"
    COMPARED_TO_BASELINE = "COMPARED_TO_BASELINE"

    # New Interface Standard (from "links" field)
    ACCEPTS = "ACCEPTS"  # Input dependencies
    YIELDS = "YIELDS"  # Output dependencies
    COMPOSES_WITH = "COMPOSES_WITH"  # Patterns actively invoked
    REFERENCES = "REFERENCES"  # Conceptual references (not invoked)
    IMPLEMENTS = "IMPLEMENTS"  # Abstract interfaces (deprecated)
    HAS_SIGNATURE = "HAS_SIGNATURE"  # Replaces IMPLEMENTS
    DEPENDS_ON = "DEPENDS_ON"  # Deprecated: use specific link types instead

    # Other
    IN_LAYER = "IN_LAYER"
    TRIGGERED_BY = "TRIGGERED_BY"
    SIMILAR_TO = "SIMILAR_TO"
    OPPOSITE_TO = "OPPOSITE_TO"
    ENABLES = "ENABLES"
    OPERATES_ON = "OPERATES_ON"
    ACCEPTS_PAYLOAD = "ACCEPTS_PAYLOAD"
    PRODUCES = "PRODUCES"
    CONFIGURES = "CONFIGURES"
    ESCALATES_TO = "ESCALATES_TO"
    HAS_MECHANISM = "HAS_MECHANISM"
    AVOIDS = "AVOIDS"
    HAS_PRINCIPLE = "HAS_PRINCIPLE"
    PARENT_OF = "PARENT_OF"
    IS_VERSION_OF = "IS_VERSION_OF"


class Node(BaseModel):
    id: str
    node_type: NodeType
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    embedding: np.ndarray | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Edge(BaseModel):
    id: str
    source_id: str
    target_id: str
    edge_type: EdgeType
    metadata: dict[str, Any] = Field(default_factory=dict)


class GraphStore:
    """Persistent graph store with semantic search capabilities."""

    SIMILARITY_THRESHOLD = 0.75  # For auto-linking (novelty rejection uses 0.92)

    def __init__(self, db_path: str = "taxonomy.db"):
        self.db_path = db_path
        self.embedding_service = EmbeddingService(db_path)
        # MultiDiGraph: a pattern can have multiple typed edges to the same
        # target (e.g. `accepts: Task` AND `yields: Task`). DiGraph would
        # silently collapse them to one edge.
        self.graph = nx.MultiDiGraph()
        self._init_tables()
        self._migrate_schema()
        self._load_graph()

    def _init_tables(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        # CRITICAL: Enable foreign key enforcement to prevent dangling edges
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                node_type TEXT NOT NULL,
                text TEXT NOT NULL,
                metadata TEXT DEFAULT '{}',
                embedding BLOB
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS edges (
                id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                edge_type TEXT NOT NULL,
                alias TEXT,
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (source_id) REFERENCES nodes(id),
                FOREIGN KEY (target_id) REFERENCES nodes(id)
            )
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(node_type)
        """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id)
        """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id)
        """
        )

        conn.commit()
        conn.close()

    def _migrate_schema(self):
        """Add columns to existing DBs that pre-date them. Idempotent."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(edges)")
        cols = {row[1] for row in cursor.fetchall()}
        if "alias" not in cols:
            cursor.execute("ALTER TABLE edges ADD COLUMN alias TEXT")
        conn.commit()
        conn.close()

    def _load_graph(self):
        """Load graph from database into memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, node_type, text, metadata, embedding FROM nodes")
        for row in cursor.fetchall():
            node_id, node_type, text, metadata_json, embedding_blob = row
            embedding = np.frombuffer(embedding_blob, dtype=np.float32) if embedding_blob else None
            self.graph.add_node(
                node_id,
                node_type=NodeType(node_type),
                text=text,
                metadata=json.loads(metadata_json),
                embedding=embedding,
            )

        cursor.execute("SELECT id, source_id, target_id, edge_type, alias, metadata FROM edges")
        for row in cursor.fetchall():
            edge_id, source_id, target_id, edge_type, alias, metadata_json = row
            self.graph.add_edge(
                source_id,
                target_id,
                key=edge_id,
                id=edge_id,
                edge_type=EdgeType(edge_type),
                alias=alias,
                metadata=json.loads(metadata_json),
            )

        conn.close()

    def create_node(
        self,
        node_type: NodeType,
        text: str,
        metadata: dict[str, Any] | None = None,
        compute_embedding: bool = True,
        embedding_text: str | None = None,
    ) -> str:
        """Create a new node in the graph."""
        node_id = str(uuid.uuid4())
        metadata = metadata or {}

        embedding = None
        embedding_blob = None
        if compute_embedding:
            # Use specific embedding text if provided, else label text
            content = embedding_text or text
            embedding = self.embedding_service.get_embedding(content)
            embedding_blob = embedding.tobytes()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO nodes (id, node_type, text, metadata, embedding) VALUES (?, ?, ?, ?, ?)",
            (node_id, node_type.value, text, json.dumps(metadata), embedding_blob),
        )
        conn.commit()
        conn.close()

        self.graph.add_node(
            node_id, node_type=node_type, text=text, metadata=metadata, embedding=embedding
        )

        return node_id

    def create_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: EdgeType,
        metadata: dict[str, Any] | None = None,
        alias: str | None = None,
    ) -> str:
        """Create a new edge in the graph.

        For dependency edges, `alias` preserves the original key from the
        pattern's dependencies dict (e.g. "my_alias" → Target). Without it,
        we'd have to regenerate keys from target handles, dropping author
        intent and breaking patterns that use multiple aliases for one type.
        """
        edge_id = str(uuid.uuid4())
        metadata = metadata or {}

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO edges (id, source_id, target_id, edge_type, alias, metadata) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (edge_id, source_id, target_id, edge_type.value, alias, json.dumps(metadata)),
        )
        conn.commit()
        conn.close()

        self.graph.add_edge(
            source_id,
            target_id,
            key=edge_id,
            id=edge_id,
            edge_type=edge_type,
            alias=alias,
            metadata=metadata,
        )

        return edge_id

    # ── MultiDiGraph helpers ────────────────────────────────────────────────
    # Multi-graphs allow many parallel edges between the same (src, tgt).
    # NetworkX returns these as `{key: attrs}` from get_edge_data; these
    # helpers wrap that so callers can filter by edge_type cleanly.

    def _edges_between(self, src: str, tgt: str) -> list[dict]:
        """All edge attribute dicts between src and tgt (empty if none)."""
        edges = self.graph.get_edge_data(src, tgt) or {}
        return list(edges.values())

    def _edge_keys_between(self, src: str, tgt: str) -> list[tuple[str, dict]]:
        """List of (key, attrs) for all parallel edges between src and tgt."""
        edges = self.graph.get_edge_data(src, tgt) or {}
        return list(edges.items())

    def has_edge_of_type(self, src: str, tgt: str, edge_type: EdgeType) -> bool:
        """True if at least one edge of given type exists between src and tgt."""
        return any(e.get("edge_type") == edge_type for e in self._edges_between(src, tgt))

    def remove_edges_of_type(self, src: str, tgt: str, edge_type: EdgeType) -> list[str]:
        """Remove all parallel edges of `edge_type` between src and tgt.
        Returns list of edge_ids removed (for DB cleanup by caller)."""
        removed_ids = []
        for key, attrs in self._edge_keys_between(src, tgt):
            if attrs.get("edge_type") == edge_type:
                removed_ids.append(attrs.get("id"))
                self.graph.remove_edge(src, tgt, key=key)
        return removed_ids

    def get_nodes_by_type(self, node_type: NodeType) -> list[tuple[str, dict]]:
        """Get all nodes of a specific type."""
        return [
            (node_id, data)
            for node_id, data in self.graph.nodes(data=True)
            if data.get("node_type") == node_type
        ]

    def validate_links(self, links: dict[str, list[str]]) -> list[str]:
        """
        Pre-flight validation: Check all link targets exist in the graph.

        Args:
            links: Dict mapping relation type to list of target handles
                   e.g., {"COMPOSES_WITH": ["Foo#1234", "Bar#5678"]}

        Returns:
            List of missing target handles (empty if all exist)
        """
        missing = []
        solutions = self.get_nodes_by_type(NodeType.SOLUTION)
        existing_handles = {data.get("text") for _, data in solutions}

        for _rel_type, targets in links.items():
            for target in targets:
                # Handle format: "Handle#hash" or just "Handle"
                target_handle = target.split("#")[0]
                if target_handle not in existing_handles:
                    missing.append(target)

        return missing

    def handle_exists(self, handle: str) -> bool:
        """Check if a pattern handle exists in the graph."""
        solutions = self.get_nodes_by_type(NodeType.SOLUTION)
        return any(data.get("text") == handle for _, data in solutions)

    def find_similar_node(
        self, node_type: NodeType, text: str, threshold: float | None = None
    ) -> tuple[str, float] | None:
        """Find existing node semantically similar to text.

        Returns:
            (node_id, similarity) if found above threshold, else None
        """
        threshold = threshold or self.SIMILARITY_THRESHOLD
        query_embedding = self.embedding_service.get_embedding(text)

        candidates = []
        for node_id, data in self.get_nodes_by_type(node_type):
            if data.get("embedding") is not None:
                candidates.append((node_id, data["embedding"]))

        if not candidates:
            return None

        results = self.embedding_service.find_similar(
            query_embedding, candidates, threshold, top_k=1
        )

        if results:
            return results[0]
        return None

    def find_or_create_node(
        self,
        node_type: NodeType,
        text: str,
        metadata: dict[str, Any] | None = None,
        threshold: float | None = None,
    ) -> tuple[str, bool]:
        """Find existing similar node or create new one.

        Returns:
            (node_id, is_new) - node_id and whether it was newly created
        """
        similar = self.find_similar_node(node_type, text, threshold)

        if similar:
            node_id, _ = similar
            return node_id, False

        node_id = self.create_node(node_type, text, metadata)
        return node_id, True

    # Required schema: field_name -> (NodeType, EdgeType)
    REQUIRED_SCHEMA = {
        "core_mechanism": (NodeType.MECHANISM, EdgeType.USES_MECHANISM),
        "long_term_vision": (NodeType.OUTCOME, EdgeType.PRODUCES_OUTCOME),
        "design_principles": (NodeType.PRINCIPLE, EdgeType.FOLLOWS_PRINCIPLE),
        "why_it_fails": (NodeType.CRITICISM, EdgeType.HAS_CRITICISM),
        "why_it_works": (NodeType.JUSTIFICATION, EdgeType.HAS_JUSTIFICATION),
        "what_is_new": (NodeType.NOVELTY, EdgeType.CLAIMS_NOVELTY),
        "scenario": (NodeType.SCENARIO, EdgeType.SOLVES_SCENARIO),
        "without_this": (NodeType.COUNTERFACTUAL, EdgeType.COMPARED_TO_BASELINE),
        # Formal Contract Fields
        "invariants": (NodeType.INVARIANT, EdgeType.HAS_INVARIANT),
        "preconditions": (NodeType.PRECONDITION, EdgeType.HAS_PRECONDITION),
        "postconditions": (NodeType.POSTCONDITION, EdgeType.HAS_POSTCONDITION),
        "inputs": (NodeType.INPUT, EdgeType.HAS_INPUT),
        "outputs": (NodeType.OUTPUT, EdgeType.HAS_OUTPUT),
        "parameters": (NodeType.PARAMETER, EdgeType.HAS_PARAMETER),
    }

    def add_pattern(
        self,
        solution: dict[str, Any],
        field_mappings: dict[str, str] | None = None,
        skip_cascade: bool = False,
    ) -> dict[str, Any]:
        """Add a pattern with strict enforcement that EVERY schema field is mapped.

        ALL fields are required (unless they are optional lists like invariants).
        For each field, agent explicitly decides:
        - 'NEW' or None → Create a new node with the text content
        - '<existing_node_id>' → Link to that existing node

        SAFE MERGE: If a solution with the same label exists, it updates/merges
        instead of creating a duplicate.

        MERKLE DAG: Dependencies are stored as handles only (no hashes).
        Hashes are computed fresh using the cascade system.

        Args:
            solution: Solution dict with 'label' and required field texts.
                      Fields can be strings or lists of strings.
            field_mappings: Dict mapping field_name -> 'NEW' or existing node_id.
                           For list fields, this applies to ALL items (usually 'NEW').

        Returns:
            Dict with solution_id, created nodes, linked nodes
            On failure: {"success": False, "error": "..."}
        """
        from ..core.hashing import extract_handle_from_ref

        field_mappings = field_mappings or {}

        # 1. Validate 'handle' is present (patterns use 'handle', not 'label')
        handle = solution.get("handle") or solution.get("label")
        if not handle:
            return {"success": False, "error": "Missing required field: handle or label"}

        # 2. Extract dependencies for edge creation
        #    Dependencies are stored as graph edges, NOT in pattern JSON content
        #    Note: We use .get() not .pop() to preserve the original dict for callers
        input_deps = solution.get("dependencies", {})

        # 3. Validate all dependency references exist before creating edges
        if isinstance(input_deps, dict):
            existing_handles = {
                data["text"] for _, data in self.get_nodes_by_type(NodeType.PATTERN)
            }
            for _, items in input_deps.items():
                if isinstance(items, dict):
                    for _, ref in items.items():
                        if isinstance(ref, str):
                            dep_handle = extract_handle_from_ref(ref)
                            if dep_handle not in existing_handles and dep_handle != handle:
                                return {
                                    "success": False,
                                    "error": f"Missing dependency target: {dep_handle}",
                                }

        # 4. Validate all explicit link IDs exist and have correct type
        for field_name, link_id in field_mappings.items():
            if field_name not in self.REQUIRED_SCHEMA:
                return {"success": False, "error": f"Unknown field in mapping: {field_name}"}

            if link_id and link_id.upper() != "NEW":
                # Agent wants to link to existing node
                if link_id not in self.graph:
                    return {
                        "success": False,
                        "error": f"Cannot link {field_name}: node {link_id} does not exist",
                    }
                expected_type, _ = self.REQUIRED_SCHEMA[field_name]
                actual_type = self.graph.nodes[link_id].get("node_type")
                if actual_type != expected_type:
                    return {
                        "success": False,
                        "error": (
                            f"Type mismatch for {field_name}: expected {expected_type.name}, "
                            f"got {actual_type.name if actual_type else 'None'}"
                        ),
                    }

        # Find/Create the container Pattern node
        pattern_id = None

        # Create a copy of solution WITHOUT dependencies for storage
        # Dependencies are stored as edges only (Merkle DAG design)
        stored_pattern = {k: v for k, v in solution.items() if k != "dependencies"}

        # Check for existing pattern with same handle
        for nid, data in self.get_nodes_by_type(NodeType.PATTERN):
            if data["text"] == handle:
                pattern_id = nid
                # Update metadata - store as 'pattern' (without dependencies)
                if "metadata" in data:
                    data["metadata"]["pattern"] = stored_pattern

                    # Also promote layer/category to root metadata for easy access/indexing
                    meta_block = solution.get("_meta", {})
                    data["metadata"]["layer"] = (
                        meta_block.get("layer") or solution.get("sema_layer") or "Unknown"
                    )
                    data["metadata"]["category"] = (
                        meta_block.get("category")
                        or solution.get("sema_category")
                        or "Uncategorized"
                    )

                    # Persist metadata update
                    conn = sqlite3.connect(self.db_path)
                    conn.execute(
                        "UPDATE nodes SET metadata = ? WHERE id = ?",
                        (json.dumps(data["metadata"]), nid),
                    )
                    conn.commit()
                    conn.close()
                break

        if not pattern_id:
            # Construct rich text for embedding: "Handle: Gloss"
            rich_text = f"{handle}: {solution.get('gloss', '')} {solution.get('mechanism', '')}"

            # Prepare metadata with root-level layer/category
            # Note: stored_pattern already excludes dependencies (created above)
            meta_block = solution.get("_meta", {})
            node_meta = {
                "pattern": stored_pattern,
                "layer": meta_block.get("layer") or solution.get("sema_layer") or "Unknown",
                "category": meta_block.get("category")
                or solution.get("sema_category")
                or "Uncategorized",
            }

            pattern_id = self.create_node(
                NodeType.PATTERN,
                handle,
                metadata=node_meta,
                compute_embedding=True,
                embedding_text=rich_text,
            )

        # =====================================================================
        # 4a. AUTO-LINKING: Layers, Categories, Dependencies, Signatures
        # =====================================================================

        # A. Layer & Category
        meta = solution.get("_meta", {})
        layer_name = meta.get("layer") or solution.get("sema_layer") or "Unknown"
        category_name = meta.get("category") or solution.get("sema_category") or "Uncategorized"

        # CRITICAL FIX: Promote layer/category to top-level for Registry compatibility
        # The Registry expects 'sema_layer' and 'sema_category' in the pattern dict
        solution["sema_layer"] = layer_name
        solution["sema_category"] = category_name

        # Find/Create Layer
        layer_id = None
        for nid, data in self.get_nodes_by_type(NodeType.LAYER):
            if data["text"] == layer_name:
                layer_id = nid
                break
        if not layer_id:
            layer_id = self.create_node(NodeType.LAYER, layer_name, compute_embedding=False)

        # Find/Create Category
        category_id = None
        for nid, data in self.get_nodes_by_type(NodeType.CATEGORY):
            if data["text"] == category_name:
                category_id = nid
                break
        if not category_id:
            category_id = self.create_node(
                NodeType.CATEGORY, category_name, compute_embedding=False
            )
            self.create_edge(category_id, layer_id, EdgeType.IN_LAYER)
        else:
            # Ensure Layer link
            if not self.graph.has_edge(category_id, layer_id):
                self.create_edge(category_id, layer_id, EdgeType.IN_LAYER)

        # Link Pattern -> Category (Idempotent: remove old if changed)
        # Note: We support moving categories by checking existing edges
        for succ in list(self.graph.successors(pattern_id)):
            if succ == category_id:
                continue
            edge_ids = self.remove_edges_of_type(pattern_id, succ, EdgeType.IN_CATEGORY)
            for eid in edge_ids:
                conn = sqlite3.connect(self.db_path)
                conn.execute("DELETE FROM edges WHERE id = ?", (eid,))
                conn.commit()
                conn.close()

        if not self.has_edge_of_type(pattern_id, category_id, EdgeType.IN_CATEGORY):
            self.create_edge(pattern_id, category_id, EdgeType.IN_CATEGORY)

        # B. Dependencies (accepts, yields, composes_with, references)
        #    Use input_deps (extracted earlier) - NOT stored in pattern, only as edges
        if isinstance(input_deps, dict):
            # Map dependency keys to EdgeTypes
            dep_map = {
                "accepts": EdgeType.ACCEPTS,
                "yields": EdgeType.YIELDS,
                "composes_with": EdgeType.COMPOSES_WITH,
                "references": EdgeType.REFERENCES,
            }

            # Map EdgeTypes back to dependency categories for reverse lookup if needed
            edge_type_set = set(dep_map.values())

            # Pre-fetch all patterns to avoid N queries (Optimization)
            # fmt: off
            all_patterns = {
                data["text"]: nid
                for nid, data in self.get_nodes_by_type(NodeType.PATTERN)
            }
            # fmt: on

            # 1. Calculate DESIRED edges from input_deps
            # Key: (target_id, edge_type, alias) — alias preserves the
            # original dep key (e.g. "my_alias" → Target) so round-trips
            # through get_dependencies_from_edges restore the same key.
            desired_edges = set()

            for cat, edge_type in dep_map.items():
                if cat in input_deps and isinstance(input_deps[cat], dict):
                    for alias, val in input_deps[cat].items():
                        # Handle parsing: "sema:Handle#hash" -> "Handle"
                        if not isinstance(val, str):
                            continue

                        target_handle = val
                        if "sema:" in val:
                            target_handle = val.split(":")[1].split("#")[0]
                        else:
                            target_handle = val.split("#")[0]
                        target_handle = target_handle.strip()

                        target_id = all_patterns.get(target_handle)
                        if target_id:
                            desired_edges.add((target_id, edge_type, alias))

            # 2. Identify EXISTING dependency edges (multi-edge aware)
            existing_dep_edges = []  # (target_id, edge_type, alias, edge_id, key)

            for succ in self.graph.successors(pattern_id):
                for key, edge_data in self._edge_keys_between(pattern_id, succ):
                    e_type = edge_data.get("edge_type")
                    if e_type in edge_type_set:
                        existing_dep_edges.append(
                            (
                                succ,
                                e_type,
                                edge_data.get("alias"),
                                edge_data.get("id"),
                                key,
                            )
                        )

            existing_set = {(t, e, a) for t, e, a, _, _ in existing_dep_edges}

            # 3. Prune OBSOLETE edges (target+type+alias not in desired)
            for target_id, e_type, alias, edge_id, key in existing_dep_edges:
                if (target_id, e_type, alias) not in desired_edges:
                    conn = sqlite3.connect(self.db_path)
                    conn.execute("DELETE FROM edges WHERE id = ?", (edge_id,))
                    conn.commit()
                    conn.close()
                    self.graph.remove_edge(pattern_id, target_id, key=key)

            # 4. Add NEW edges (multi-edge: same target may have multiple edges
            # of different types or different aliases — all valid)
            for target_id, edge_type, alias in desired_edges:
                if (target_id, edge_type, alias) not in existing_set:
                    self.create_edge(pattern_id, target_id, edge_type, alias=alias)

        # C. Signatures (Interfaces)
        signatures = solution.get("signature", [])
        if signatures:
            all_patterns = {
                data["text"]: nid for nid, data in self.get_nodes_by_type(NodeType.PATTERN)
            }
            for sig in signatures:
                # "Deep(Research)" -> Link to 'Deep' and 'Research'
                matches = re.findall(r"\w+", sig)
                for m in matches:
                    target_id = all_patterns.get(m)
                    if target_id and not self.has_edge_of_type(
                        pattern_id, target_id, EdgeType.HAS_SIGNATURE
                    ):
                        self.create_edge(pattern_id, target_id, EdgeType.HAS_SIGNATURE)

        # D. Related (Metadata links)
        related = meta.get("related", [])
        if related:
            # Re-use pre-fetched map if available, else fetch
            if "all_patterns" not in locals():
                # fmt: off
                all_patterns = {
                    data["text"]: nid
                    for nid, data in self.get_nodes_by_type(NodeType.PATTERN)
                }
                # fmt: on

            for item in related:
                if not isinstance(item, str):
                    continue
                target_handle = item.split("#")[0]
                target_id = all_patterns.get(target_handle)

                if target_id:
                    # RELATED_TO is distinct from dependencies — only check for
                    # an existing edge of this exact type.
                    if not self.has_edge_of_type(pattern_id, target_id, EdgeType.RELATED_TO):
                        self.create_edge(pattern_id, target_id, EdgeType.RELATED_TO)

        created_nodes = {}
        linked_nodes = {}

        # 5. Process every field in schema
        for field_name, (node_type, edge_type) in self.REQUIRED_SCHEMA.items():
            content = solution.get(field_name)
            if not content:
                continue

            # Normalize to list
            items = content if isinstance(content, list) else [content]
            link_id = field_mappings.get(field_name)

            # Prepare result containers
            if field_name not in created_nodes:
                created_nodes[field_name] = []
            if field_name not in linked_nodes:
                linked_nodes[field_name] = []

            for text_item in items:
                if not isinstance(text_item, str):
                    continue  # Skip non-string items

                if link_id and link_id.upper() != "NEW":
                    # Case A: Explicit link (agent provided ID)
                    target_id = link_id
                    linked_nodes[field_name].append(
                        {"id": target_id, "existing_text": self.graph.nodes[target_id]["text"][:80]}
                    )
                else:
                    # Case B: Auto-link if similar exists, otherwise create new
                    similar = self.find_similar_node(node_type, text_item)

                    if similar:
                        target_id, sim = similar
                        linked_nodes[field_name].append(
                            {
                                "id": target_id,
                                "similarity": sim,
                                "existing_text": self.graph.nodes[target_id]["text"][:80],
                            }
                        )
                    else:
                        target_id = self.create_node(node_type, text_item)
                        created_nodes[field_name].append({"id": target_id, "text": text_item[:80]})

                # MultiDiGraph supports multiple typed edges between the same
                # (src, tgt). We only create a new edge of `edge_type` if no
                # edge of that exact type already exists between this pair.
                if not self.has_edge_of_type(pattern_id, target_id, edge_type):
                    self.create_edge(pattern_id, target_id, edge_type)

        # Compute hash AFTER edges exist (dependencies derived from edges)
        hash_info = self.compute_pattern_hash(solution)
        solution["sema_id"] = hash_info["full_id"]
        solution["sema_ref"] = hash_info["reference"]
        solution["sema_stub"] = hash_info["stub"]

        # Update stored_pattern with computed hash (kept without dependencies)
        stored_pattern["sema_id"] = hash_info["full_id"]
        stored_pattern["sema_ref"] = hash_info["reference"]
        stored_pattern["sema_stub"] = hash_info["stub"]
        # Also copy promoted fields
        stored_pattern["sema_layer"] = solution.get("sema_layer")
        stored_pattern["sema_category"] = solution.get("sema_category")

        # Update the stored pattern metadata (without dependencies)
        self._update_pattern_metadata(handle, stored_pattern)

        # Trigger cascade unless caller will run a single sweep at the end
        # (e.g. sema pull, which walks the DAG topologically and would
        # otherwise rewrite top-level patterns hundreds of times).
        if skip_cascade:
            cascade_result = {"updated": []}
        else:
            cascade_result = self._cascade_dependents(handle)

        return {
            "success": True,
            "solution_id": pattern_id,
            "created": created_nodes,
            "linked": linked_nodes,
            "cascade": cascade_result,
            "sema_ref": hash_info["reference"],
        }

    def get_solution_count_for_node(self, node_id: str) -> int:
        """Count how many solutions link to this node."""
        count = 0
        for pred in self.graph.predecessors(node_id):
            pred_data = self.graph.nodes[pred]
            if pred_data.get("node_type") == NodeType.SOLUTION:
                count += 1
        return count

    def find_gaps(self) -> dict[str, Any]:
        """Find unexplored regions in the solution space.

        Returns:
            Dict with underused_mechanisms, orphan_outcomes, unseen_combos
        """
        gaps = {
            "underused_mechanisms": [],
            "orphan_outcomes": [],
            "unseen_combos": [],
            "summary": {},
        }

        mechanisms = self.get_nodes_by_type(NodeType.MECHANISM)
        for mech_id, data in mechanisms:
            count = self.get_solution_count_for_node(mech_id)
            if count < 2:
                gaps["underused_mechanisms"].append(
                    {"id": mech_id, "text": data["text"][:100], "solution_count": count}
                )

        outcomes = self.get_nodes_by_type(NodeType.OUTCOME)
        for out_id, data in outcomes:
            count = self.get_solution_count_for_node(out_id)
            if count == 0:
                gaps["orphan_outcomes"].append({"id": out_id, "text": data["text"][:100]})

        mech_outcome_pairs = set()
        solutions = self.get_nodes_by_type(NodeType.SOLUTION)
        for sol_id, _ in solutions:
            sol_mechs = [
                succ
                for succ in self.graph.successors(sol_id)
                if self.graph.nodes[succ].get("node_type") == NodeType.MECHANISM
            ]
            sol_outcomes = [
                succ
                for succ in self.graph.successors(sol_id)
                if self.graph.nodes[succ].get("node_type") == NodeType.OUTCOME
            ]
            for m in sol_mechs:
                for o in sol_outcomes:
                    mech_outcome_pairs.add((m, o))

        all_mechs = [m[0] for m in mechanisms[:10]]
        all_outcomes = [o[0] for o in outcomes[:10]]
        for m in all_mechs:
            for o in all_outcomes:
                if (m, o) not in mech_outcome_pairs:
                    gaps["unseen_combos"].append(
                        {
                            "mechanism_id": m,
                            "mechanism_text": self.graph.nodes[m]["text"][:60],
                            "outcome_id": o,
                            "outcome_text": self.graph.nodes[o]["text"][:60],
                        }
                    )
                    if len(gaps["unseen_combos"]) >= 10:
                        break
            if len(gaps["unseen_combos"]) >= 10:
                break

        gaps["summary"] = {
            "total_solutions": len(solutions),
            "total_mechanisms": len(mechanisms),
            "total_outcomes": len(outcomes),
            "underused_mechanism_count": len(gaps["underused_mechanisms"]),
            "orphan_outcome_count": len(gaps["orphan_outcomes"]),
            "unseen_combo_count": len(gaps["unseen_combos"]),
        }

        return gaps

    def check_novelty(self, solution: dict[str, Any]) -> dict[str, Any]:
        """Check if a solution is novel enough to add.

        Returns:
            Dict with is_novel, similar_mechanism, suggestions for morphing
        """
        result = {
            "is_novel": True,
            "mechanism_overlap": None,
            "outcome_overlap": [],
            "suggestions": [],
        }

        mechanism_text = solution.get("core_mechanism", "")
        if mechanism_text:
            similar = self.find_similar_node(NodeType.MECHANISM, mechanism_text)
            if similar:
                mech_id, sim = similar
                result["mechanism_overlap"] = {
                    "node_id": mech_id,
                    "similarity": sim,
                    "existing_text": self.graph.nodes[mech_id]["text"][:200],
                }
                if sim > 0.92:
                    result["is_novel"] = False

        # Handle both field names for outcomes
        outcomes = solution.get("long_term_implications") or solution.get("long_term_vision", [])
        if isinstance(outcomes, str):
            outcomes = [outcomes]
        for outcome_text in outcomes:
            similar = self.find_similar_node(NodeType.OUTCOME, outcome_text, threshold=0.90)
            if similar:
                out_id, sim = similar
                result["outcome_overlap"].append(
                    {
                        "node_id": out_id,
                        "similarity": sim,
                        "new_text": outcome_text[:100],
                        "existing_text": self.graph.nodes[out_id]["text"][:100],
                    }
                )

        if not result["is_novel"]:
            gaps = self.find_gaps()
            if gaps["underused_mechanisms"]:
                result["suggestions"].append(
                    f"Try using underexplored mechanism: "
                    f"{gaps['underused_mechanisms'][0]['text'][:80]}"
                )
            if gaps["unseen_combos"]:
                combo = gaps["unseen_combos"][0]
                result["suggestions"].append(
                    f"Try combining '{combo['mechanism_text']}' "
                    f"with outcome '{combo['outcome_text']}'"
                )

        return result

    def merge_nodes(self, node_id_keep: str, node_id_remove: str) -> bool:
        """Merge two nodes, redirecting all edges to the kept node.

        Multi-edge aware: dedupes by (edge_type, alias) tuple, not just by
        edge_type. Otherwise multiple parallel edges of the same type but
        with distinct aliases (e.g. accepts: {"task1": T, "task2": T})
        would collapse to one — silent data loss on merge.
        """
        if node_id_keep not in self.graph or node_id_remove not in self.graph:
            return False

        def _has_exact(src, tgt, e_type, alias):
            return any(
                e.get("edge_type") == e_type and e.get("alias") == alias
                for e in self._edges_between(src, tgt)
            )

        for pred in list(self.graph.predecessors(node_id_remove)):
            for edge_data in self._edges_between(pred, node_id_remove):
                e_type = edge_data.get("edge_type")
                alias = edge_data.get("alias")
                if e_type and not _has_exact(pred, node_id_keep, e_type, alias):
                    self.create_edge(
                        pred,
                        node_id_keep,
                        e_type,
                        edge_data.get("metadata"),
                        alias=alias,
                    )

        for succ in list(self.graph.successors(node_id_remove)):
            for edge_data in self._edges_between(node_id_remove, succ):
                e_type = edge_data.get("edge_type")
                alias = edge_data.get("alias")
                if e_type and not _has_exact(node_id_keep, succ, e_type, alias):
                    self.create_edge(
                        node_id_keep,
                        succ,
                        e_type,
                        edge_data.get("metadata"),
                        alias=alias,
                    )

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM edges WHERE source_id = ? OR target_id = ?",
            (node_id_remove, node_id_remove),
        )
        cursor.execute("DELETE FROM nodes WHERE id = ?", (node_id_remove,))
        conn.commit()
        conn.close()

        self.graph.remove_node(node_id_remove)

        return True

    # =========================================================================
    # HIERARCHY OPERATIONS
    # =========================================================================

    def create_child(self, parent_id: str, text: str, node_type: NodeType | None = None) -> str:
        """Create a child node under a parent.

        If node_type not specified, inherits from parent.
        Returns the new child node ID.
        """
        if parent_id not in self.graph:
            raise ValueError(f"Parent node {parent_id} not found")

        parent_data = self.graph.nodes[parent_id]
        child_type = node_type or parent_data["node_type"]

        # Create the child node
        child_id = self.create_node(child_type, text)

        # Create parent -> child edge
        self.create_edge(parent_id, child_id, EdgeType.PARENT_OF)

        return child_id

    def set_parent(self, child_id: str, parent_id: str) -> bool:
        """Set or change a node's parent.

        Removes any existing parent relationship first.
        """
        if child_id not in self.graph:
            raise ValueError(f"Child node {child_id} not found")
        if parent_id not in self.graph:
            raise ValueError(f"Parent node {parent_id} not found")

        # Verify same type
        child_type = self.graph.nodes[child_id]["node_type"]
        parent_type = self.graph.nodes[parent_id]["node_type"]
        if child_type != parent_type:
            raise ValueError(f"Type mismatch: child is {child_type}, parent is {parent_type}")

        # Remove existing PARENT_OF edge(s) if any (multi-edge aware)
        for pred in list(self.graph.predecessors(child_id)):
            removed_ids = self.remove_edges_of_type(pred, child_id, EdgeType.PARENT_OF)
            for eid in removed_ids:
                conn = sqlite3.connect(self.db_path)
                conn.execute("DELETE FROM edges WHERE id = ?", (eid,))
                conn.commit()
                conn.close()

        # Create new parent -> child edge
        self.create_edge(parent_id, child_id, EdgeType.PARENT_OF)
        return True

    def get_children(self, node_id: str) -> list[tuple[str, dict]]:
        """Get all direct children of a node."""
        if node_id not in self.graph:
            return []

        children = []
        for succ in self.graph.successors(node_id):
            if self.has_edge_of_type(node_id, succ, EdgeType.PARENT_OF):
                children.append((succ, self.graph.nodes[succ]))
        return children

    def get_parent(self, node_id: str) -> tuple[str, dict] | None:
        """Get the parent of a node, if any."""
        if node_id not in self.graph:
            return None

        for pred in self.graph.predecessors(node_id):
            if self.has_edge_of_type(pred, node_id, EdgeType.PARENT_OF):
                return (pred, self.graph.nodes[pred])
        return None

    def get_roots(self, node_type: NodeType) -> list[tuple[str, dict]]:
        """Get all root nodes (no parent) of a given type."""
        roots = []
        for node_id, data in self.get_nodes_by_type(node_type):
            if self.get_parent(node_id) is None:
                roots.append((node_id, data))
        return roots

    def get_hierarchy_tree(self, node_type: NodeType, indent: int = 0) -> str:
        """Get a text representation of the hierarchy for a node type."""
        lines = []

        def add_node(node_id: str, data: dict, depth: int):
            prefix = "  " * depth + ("├── " if depth > 0 else "")
            count = self.get_solution_count_for_node(node_id)
            lines.append(f"{prefix}[{count}] {data['text'][:50]}... ({node_id[:8]})")
            for child_id, child_data in self.get_children(node_id):
                add_node(child_id, child_data, depth + 1)

        roots = self.get_roots(node_type)
        if not roots:
            return f"No {node_type.name} hierarchy (all nodes are flat)"

        for root_id, root_data in roots:
            add_node(root_id, root_data, 0)

        return "\n".join(lines)

    def _render_hierarchy(
        self, node_type: NodeType, root_nodes: list[str], visited: set, level: int = 0
    ) -> list[str]:
        """Recursively render a hierarchy of nodes as indented tree."""
        lines = []
        indent = "  " * level
        for node_id in root_nodes:
            if node_id in visited:
                continue
            visited.add(node_id)

            data = self.graph.nodes[node_id]
            count = self.get_solution_count_for_node(node_id)
            short_id = node_id[:8]

            # Formatting: "  [1a2b3c4d] Category Name (5 sols)"
            lines.append(f"{indent}[{short_id}] {data['text'][:60]} ({count} sols)")

            # Find children (nodes where THIS node is PARENT_OF child)
            children = []
            for successor in self.graph.successors(node_id):
                if self.has_edge_of_type(node_id, successor, EdgeType.PARENT_OF):
                    children.append(successor)

            if children:
                lines.extend(self._render_hierarchy(node_type, children, visited, level + 1))

        return lines

    def _get_roots_for_type(self, node_type: NodeType) -> list[str]:
        """Find root nodes (no parent) of a given type."""
        all_nodes = [n for n, d in self.graph.nodes(data=True) if d.get("node_type") == node_type]
        roots = []
        for n in all_nodes:
            has_parent = False
            for pred in self.graph.predecessors(n):
                if self.has_edge_of_type(pred, n, EdgeType.PARENT_OF):
                    has_parent = True
                    break
            if not has_parent:
                roots.append(n)
        return roots

    def get_graph_state_for_prompt(self) -> str:
        """Generate a hierarchical text summary of graph state for LLM prompts."""
        solutions = self.get_nodes_by_type(NodeType.SOLUTION)
        mechanisms = self.get_nodes_by_type(NodeType.MECHANISM)
        outcomes = self.get_nodes_by_type(NodeType.OUTCOME)
        principles = self.get_nodes_by_type(NodeType.PRINCIPLE)
        criticisms = self.get_nodes_by_type(NodeType.CRITICISM)
        justifications = self.get_nodes_by_type(NodeType.JUSTIFICATION)
        novelties = self.get_nodes_by_type(NodeType.NOVELTY)
        invariants = self.get_nodes_by_type(NodeType.INVARIANT)
        preconditions = self.get_nodes_by_type(NodeType.PRECONDITION)

        lines = ["=== CURRENT TAXONOMY ===", ""]
        lines.append(f"Solutions: {len(solutions)}")
        lines.append(f"Unique Mechanisms: {len(mechanisms)}")
        lines.append(f"Unique Outcomes: {len(outcomes)}")
        lines.append(f"Unique Principles: {len(principles)}")
        lines.append(f"Unique Criticisms: {len(criticisms)}")
        lines.append(f"Unique Justifications: {len(justifications)}")
        lines.append(f"Unique Novelties: {len(novelties)}")
        lines.append(f"Unique Invariants: {len(invariants)}")
        lines.append(f"Unique Preconditions: {len(preconditions)}")
        lines.append("")

        # Render hierarchies for key node types
        for n_type in [NodeType.MECHANISM, NodeType.OUTCOME, NodeType.PRINCIPLE]:
            type_nodes = self.get_nodes_by_type(n_type)
            if not type_nodes:
                continue

            lines.append(f"{n_type.name} HIERARCHY:")
            roots = self._get_roots_for_type(n_type)
            visited = set()
            tree_lines = self._render_hierarchy(n_type, roots, visited)
            if tree_lines:
                lines.extend(tree_lines)
            else:
                lines.append("  (no nodes)")
            lines.append("")

        # Show criticisms (shared failure modes) - flat for now
        if criticisms:
            lines.append("CRITICISMS (shared failure modes):")
            for crit_id, data in criticisms[:5]:
                count = self.get_solution_count_for_node(crit_id)
                short_id = crit_id[:8]
                lines.append(f"  [{short_id}] {data['text'][:60]} ({count} sols)")
            lines.append("")

        # Show justifications - flat for now
        if justifications:
            lines.append("JUSTIFICATIONS:")
            for just_id, data in justifications[:5]:
                count = self.get_solution_count_for_node(just_id)
                short_id = just_id[:8]
                lines.append(f"  [{short_id}] {data['text'][:60]} ({count} sols)")
            lines.append("")

        # Show gaps
        gaps = self.find_gaps()
        lines.append("=== UNEXPLORED GAPS ===")
        for gap in gaps["underused_mechanisms"][:3]:
            lines.append(
                f"  - Mechanism has only {gap['solution_count']} solution(s): {gap['text'][:60]}..."
            )
        for combo in gaps["unseen_combos"][:3]:
            lines.append(
                f"  - No solution combines: '{combo['mechanism_text'][:40]}' "
                f"with '{combo['outcome_text'][:40]}'"
            )

        return "\n".join(lines)

    def stats(self) -> dict[str, int]:
        """Get basic graph statistics."""
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "solutions": len(self.get_nodes_by_type(NodeType.SOLUTION)),
            "mechanisms": len(self.get_nodes_by_type(NodeType.MECHANISM)),
            "outcomes": len(self.get_nodes_by_type(NodeType.OUTCOME)),
            "principles": len(self.get_nodes_by_type(NodeType.PRINCIPLE)),
            "criticisms": len(self.get_nodes_by_type(NodeType.CRITICISM)),
            "justifications": len(self.get_nodes_by_type(NodeType.JUSTIFICATION)),
            "novelties": len(self.get_nodes_by_type(NodeType.NOVELTY)),
            "counterfactuals": len(self.get_nodes_by_type(NodeType.COUNTERFACTUAL)),
            "invariants": len(self.get_nodes_by_type(NodeType.INVARIANT)),
            "preconditions": len(self.get_nodes_by_type(NodeType.PRECONDITION)),
            "postconditions": len(self.get_nodes_by_type(NodeType.POSTCONDITION)),
            "inputs": len(self.get_nodes_by_type(NodeType.INPUT)),
            "outputs": len(self.get_nodes_by_type(NodeType.OUTPUT)),
            "parameters": len(self.get_nodes_by_type(NodeType.PARAMETER)),
        }

    # =========================================================================
    # MERKLE DAG: Content-Addressed Hashing with Cascade
    # =========================================================================

    def get_pattern_hash(self, handle: str) -> str | None:
        """Get the current hash for a pattern by handle.

        Returns the raw hash (not full sema_id), or None if not found.
        """
        for _, data in self.get_nodes_by_type(NodeType.PATTERN):
            if data["text"] == handle:
                pattern = data.get("metadata", {}).get("pattern", {})
                sema_id = pattern.get("sema_id", "")
                if "SHA-256:" in sema_id:
                    return sema_id.split("SHA-256:")[1]
        return None

    def get_all_pattern_hashes(self) -> dict[str, str]:
        """Get a map of handle -> current hash for all patterns.

        Used for batch hash resolution.
        """
        hashes = {}
        for _, data in self.get_nodes_by_type(NodeType.PATTERN):
            handle = data["text"]
            pattern = data.get("metadata", {}).get("pattern", {})
            sema_id = pattern.get("sema_id", "")
            if "SHA-256:" in sema_id:
                hashes[handle] = sema_id.split("SHA-256:")[1]
        return hashes

    def get_dependents(self, handle: str) -> list[str]:
        """Find all patterns that depend on the given handle.

        Uses graph edges (REFERENCES, COMPOSES_WITH, ACCEPTS, etc.)
        to find patterns that have this handle as a dependency.

        Returns list of dependent handles.
        """
        # Find the node ID for this handle
        target_node_id = None
        for nid, data in self.get_nodes_by_type(NodeType.PATTERN):
            if data["text"] == handle:
                target_node_id = nid
                break

        if not target_node_id:
            return []

        # Find all patterns that have edges pointing TO this node
        dependents = []
        dep_edge_types = {
            EdgeType.REFERENCES,
            EdgeType.COMPOSES_WITH,
            EdgeType.ACCEPTS,
            EdgeType.YIELDS,
        }

        for pred in self.graph.predecessors(target_node_id):
            pred_data = self.graph.nodes[pred]
            if pred_data.get("node_type") in [NodeType.PATTERN, NodeType.SOLUTION]:
                if any(
                    e.get("edge_type") in dep_edge_types
                    for e in self._edges_between(pred, target_node_id)
                ):
                    dependents.append(pred_data["text"])

        return dependents

    def get_dependencies_from_edges(self, handle: str) -> dict[str, dict[str, str]]:
        """Get dependencies for a pattern by reading graph edges.

        This is the source of truth for dependencies - edges in the graph,
        not a JSON field in the pattern content.

        Returns:
            {
                "references": {"key": "TargetHandle", ...},
                "composes_with": {"key": "TargetHandle", ...},
                ...
            }
        """
        # Find the node ID for this handle
        node_id = None
        for nid, data in self.get_nodes_by_type(NodeType.PATTERN):
            if data["text"] == handle:
                node_id = nid
                break

        if not node_id:
            return {}

        # Map edge types to dependency categories
        edge_to_dep = {
            EdgeType.REFERENCES: "references",
            EdgeType.COMPOSES_WITH: "composes_with",
            EdgeType.ACCEPTS: "accepts",
            EdgeType.YIELDS: "yields",
        }

        deps = {}
        for succ in self.graph.successors(node_id):
            for edge_data in self._edges_between(node_id, succ):
                edge_type = edge_data.get("edge_type")

                if edge_type not in edge_to_dep:
                    continue

                dep_category = edge_to_dep[edge_type]
                if dep_category not in deps:
                    deps[dep_category] = {}

                target_data = self.graph.nodes[succ]
                target_handle = target_data.get("text", "")
                target_meta = target_data.get("metadata", {})
                target_pattern = target_meta.get("pattern", {})
                target_ref = target_pattern.get(
                    "sema_id", target_pattern.get("sema_ref", target_handle)
                )

                # Prefer the alias stored on the edge (preserves the
                # original key the author used). Fall back to snake_case
                # of the handle for legacy edges that pre-date alias storage.
                alias = edge_data.get("alias")
                if not alias:
                    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", target_handle)
                    alias = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
                deps[dep_category][alias] = target_ref

        return deps

    def compute_pattern_hash(self, pattern: dict[str, Any]) -> dict[str, Any]:
        """Compute hash for a pattern, resolving dependencies to current hashes.

        Dependencies are derived from graph edges (source of truth),
        not from the pattern's JSON content.

        This is the Merkle DAG property: a pattern's hash includes
        the current hashes of all its dependencies.
        """
        from ..core.hashing import generate_sema_hash

        # Get dependencies from graph edges (not from pattern JSON)
        handle = pattern.get("handle")
        if handle:
            graph_deps = self.get_dependencies_from_edges(handle)
            if graph_deps:
                pattern = pattern.copy()
                pattern["dependencies"] = graph_deps

        # Create a hash lookup function that uses current DB state
        def hash_lookup(dep_handle: str) -> str | None:
            return self.get_pattern_hash(dep_handle)

        return generate_sema_hash(pattern, hash_lookup)

    def _cascade_dependents(self, handle: str, visited: set | None = None) -> dict[str, Any]:
        """Recursively update hashes of all patterns that depend on the given handle.

        This is called AFTER a pattern has been updated, to propagate hash changes
        to all dependents in the Merkle DAG.

        Returns:
            {"updated": [list of handles that were updated]}
        """
        if visited is None:
            visited = {handle}

        updated = []
        dependents = self.get_dependents(handle)

        for dep_handle in dependents:
            if dep_handle in visited:
                continue  # Cycle protection
            visited.add(dep_handle)

            dep_content = self._get_pattern_content(dep_handle)
            if not dep_content:
                continue

            old_hash = self.get_pattern_hash(dep_handle)
            # Recompute hash - uses compute_pattern_hash which calls generate_sema_hash
            new_hash_info = self.compute_pattern_hash(dep_content)

            # Only update if hash actually changed
            if old_hash != new_hash_info["hash"]:
                dep_content["sema_id"] = new_hash_info["full_id"]
                dep_content["sema_ref"] = new_hash_info["reference"]
                dep_content["sema_stub"] = new_hash_info["stub"]
                self._update_pattern_metadata(dep_handle, dep_content)
                updated.append(dep_handle)

                # Recurse: cascade to this pattern's dependents
                sub_result = self._cascade_dependents(dep_handle, visited)
                updated.extend(sub_result.get("updated", []))

        return {"updated": updated}

    def update_pattern_with_cascade(
        self, handle: str, new_content: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a pattern and cascade hash changes to all dependents.

        This is the core Merkle DAG operation:
        1. Normalize dependencies to handles only
        2. Compute new hash for this pattern
        3. Update the pattern
        4. Cascade to all dependents

        Returns:
            {
                "success": True/False,
                "updated": [list of handles that were updated],
                "error": "..." (if failed)
            }
        """
        from ..core.hashing import normalize_dependencies_to_handles

        try:
            # Normalize dependencies to handles only
            if "dependencies" in new_content:
                new_content["dependencies"] = normalize_dependencies_to_handles(
                    new_content["dependencies"]
                )

            # Compute new hash using THE hashing function
            new_hash_info = self.compute_pattern_hash(new_content)

            # Update the pattern
            new_content["sema_id"] = new_hash_info["full_id"]
            new_content["sema_ref"] = new_hash_info["reference"]
            new_content["sema_stub"] = new_hash_info["stub"]
            self._update_pattern_metadata(handle, new_content)

            # Cascade to dependents using shared helper
            cascade_result = self._cascade_dependents(handle)
            updated = [handle] + cascade_result.get("updated", [])

            return {"success": True, "updated": updated}
        except Exception as e:
            return {"success": False, "error": f"Cascade failed: {e}"}

    def _get_pattern_content(
        self, handle: str, include_deps: bool = False
    ) -> dict[str, Any] | None:
        """Get the current content of a pattern by handle.

        Args:
            handle: Pattern handle to get
            include_deps: If True, reconstructs dependencies from edges for export

        Returns:
            Pattern dict, optionally with dependencies reconstructed from edges
        """
        for _, data in self.get_nodes_by_type(NodeType.PATTERN):
            if data["text"] == handle:
                content = data.get("metadata", {}).get("pattern", {}).copy()
                if include_deps:
                    # Reconstruct dependencies from edges for export
                    edge_deps = self.get_dependencies_from_edges(handle)
                    if edge_deps:
                        content["dependencies"] = edge_deps
                return content
        return None

    def _update_pattern_metadata(self, handle: str, new_pattern: dict[str, Any]):
        """Update a pattern's metadata in both graph and DB."""
        for nid, data in self.get_nodes_by_type(NodeType.PATTERN):
            if data["text"] == handle:
                # Update in-memory
                data["metadata"]["pattern"] = new_pattern

                # Update in DB
                conn = sqlite3.connect(self.db_path)
                conn.execute(
                    "UPDATE nodes SET metadata = ? WHERE id = ?",
                    (json.dumps(data["metadata"]), nid),
                )
                conn.commit()
                conn.close()
                return

    def validate_dependency_refs(self, pattern: dict[str, Any]) -> list[str]:
        """Validate that all dependency references exist.

        Returns list of missing handles (empty if all valid).
        """
        from ..core.hashing import extract_handle_from_ref

        missing = []
        deps = pattern.get("dependencies", {})

        if not isinstance(deps, dict):
            return missing

        existing_handles = {data["text"] for _, data in self.get_nodes_by_type(NodeType.PATTERN)}

        for _, items in deps.items():
            if isinstance(items, dict):
                for _, ref in items.items():
                    if isinstance(ref, str):
                        dep_handle = extract_handle_from_ref(ref)
                        if dep_handle not in existing_handles:
                            missing.append(dep_handle)

        return missing

    # =========================================================================
    # TRANSACTIONAL RESTRUCTURING
    # =========================================================================

    def delete_node_cascade(self, node_id: str) -> dict[str, Any]:
        """Delete a node and cascade-delete its edges.

        Manually since FK lacks ON DELETE CASCADE.
        """
        if node_id not in self.graph:
            return {"success": False, "error": "Node not found"}

        # Count edges being removed
        edges_removed = self.graph.in_degree(node_id) + self.graph.out_degree(node_id)

        # Delete from DB - manually delete edges first (no CASCADE in schema)
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM edges WHERE source_id = ? OR target_id = ?", (node_id, node_id))
        conn.execute("DELETE FROM nodes WHERE id = ?", (node_id,))
        conn.commit()
        conn.close()

        # Remove from in-memory graph
        self.graph.remove_node(node_id)

        return {"success": True, "edges_removed": edges_removed}

    def _validate_orphans(self, graph: nx.DiGraph) -> list[str]:
        """Find solutions missing required links (mechanism or outcome)."""
        orphans = []
        for node_id, data in graph.nodes(data=True):
            if data.get("node_type") == NodeType.SOLUTION:
                has_mech = False
                has_out = False
                for succ in graph.successors(node_id):
                    succ_type = graph.nodes[succ].get("node_type")
                    if succ_type == NodeType.MECHANISM:
                        has_mech = True
                    if succ_type == NodeType.OUTCOME:
                        has_out = True
                if not has_mech or not has_out:
                    label = data.get("text", node_id)
                    missing = []
                    if not has_mech:
                        missing.append("MECHANISM")
                    if not has_out:
                        missing.append("OUTCOME")
                    orphans.append(f"{label} (missing: {', '.join(missing)})")
        return orphans

    def execute_transaction(self, operations: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Execute a batch of graph operations atomically with shadow validation.

        Operations format:
        [
            {'op': 'DELETE_NODE', 'id': 'node_uuid'},
            {'op': 'CREATE_NODE', 'type': 'MECHANISM', 'text': '...', 'temp_id': 'tmp1'},
            {'op': 'LINK', 'source_id': 'sol_id', 'target_temp_id': 'tmp1',
             'edge_type': 'USES_MECHANISM'}
        ]
        """
        # 1. Create shadow graph for validation
        shadow_graph = self.graph.copy()
        temp_id_map = {}  # 'tmp1' -> real_uuid

        # 2. Replay operations on shadow graph
        try:
            for op in operations:
                if op["op"] == "DELETE_NODE":
                    if op["id"] in shadow_graph:
                        shadow_graph.remove_node(op["id"])
                    else:
                        raise ValueError(f"Node not found: {op['id']}")

                elif op["op"] == "CREATE_NODE":
                    real_id = str(uuid.uuid4())
                    temp_id = op.get("temp_id", real_id)
                    temp_id_map[temp_id] = real_id

                    shadow_graph.add_node(
                        real_id, node_type=NodeType(op["type"]), text=op["text"], metadata={}
                    )

                elif op["op"] == "LINK":
                    # Resolve source
                    src = op.get("source_id")
                    if "source_temp_id" in op:
                        src = temp_id_map.get(op["source_temp_id"])

                    # Resolve target
                    tgt = op.get("target_id")
                    if "target_temp_id" in op:
                        tgt = temp_id_map.get(op["target_temp_id"])

                    if not src or not tgt:
                        raise ValueError(f"Invalid LINK: could not resolve IDs in {op}")

                    if src not in shadow_graph:
                        raise ValueError(f"Source not in graph: {src}")
                    if tgt not in shadow_graph:
                        raise ValueError(f"Target not in graph: {tgt}")

                    # Get edge type
                    edge_type = EdgeType(op.get("edge_type", "USES_MECHANISM"))

                    # Single-cardinality edges: replace existing (USES_MECHANISM, PRODUCES_OUTCOME)
                    # Multi-cardinality edges: add without removing (COMPOSES_WITH,
                    # HAS_INVARIANT, etc.)
                    single_cardinality = {EdgeType.USES_MECHANISM, EdgeType.PRODUCES_OUTCOME}

                    if edge_type in single_cardinality:
                        target_node_type = shadow_graph.nodes[tgt].get("node_type")
                        for existing_succ in list(shadow_graph.successors(src)):
                            succ_node = shadow_graph.nodes[existing_succ]
                            if succ_node.get("node_type") == target_node_type:
                                shadow_graph.remove_edge(src, existing_succ)

                    # Add new edge (skip if duplicate)
                    if not shadow_graph.has_edge(src, tgt):
                        shadow_graph.add_edge(src, tgt, edge_type=edge_type)

        except Exception as e:
            return {"success": False, "error": f"Shadow replay failed: {str(e)}"}

        # 3. Validate orphan invariant on shadow
        orphans = self._validate_orphans(shadow_graph)
        if orphans:
            return {
                "success": False,
                "error": f"Orphan solutions would be created: {orphans}",
                "rolled_back": True,
            }

        # 4. Commit to real graph + DB (replay operations)
        try:
            for op in operations:
                if op["op"] == "DELETE_NODE":
                    self.delete_node_cascade(op["id"])

                elif op["op"] == "CREATE_NODE":
                    # If temp_id not found, use the last created ID
                    fallback_id = list(temp_id_map.values())[-1]
                    real_id = temp_id_map.get(op.get("temp_id"), fallback_id)

                    # Create with specific ID
                    metadata = op.get("metadata", {})
                    embedding = None
                    embedding_blob = None

                    # Compute embedding if not explicitly disabled
                    if op.get("compute_embedding", True):
                        # Use embedding_text if provided (e.g. "Handle: Gloss")
                        content = op.get("embedding_text") or op["text"]
                        embedding = self.embedding_service.get_embedding(content)
                        embedding_blob = embedding.tobytes()

                    # fmt: off
                    conn = sqlite3.connect(self.db_path)
                    conn.execute(
                        "INSERT INTO nodes (id, node_type, text, metadata, embedding) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (
                            real_id,
                            op["type"],
                            op["text"],
                            json.dumps(metadata),
                            embedding_blob,
                        ),
                    )
                    conn.commit()
                    # fmt: on
                    conn.close()

                    self.graph.add_node(
                        real_id,
                        node_type=NodeType(op["type"]),
                        text=op["text"],
                        metadata=metadata,
                        embedding=embedding,
                    )

                elif op["op"] == "LINK":
                    src = op.get("source_id") or temp_id_map.get(op.get("source_temp_id"))
                    tgt = op.get("target_id") or temp_id_map.get(op.get("target_temp_id"))
                    edge_type = EdgeType(op.get("edge_type", "USES_MECHANISM"))

                    # Single-cardinality edges: replace existing (USES_MECHANISM, PRODUCES_OUTCOME)
                    # Multi-cardinality edges: add without removing (COMPOSES_WITH,
                    # HAS_INVARIANT, etc.)
                    single_cardinality = {EdgeType.USES_MECHANISM, EdgeType.PRODUCES_OUTCOME}

                    if edge_type in single_cardinality:
                        target_node_type = self.graph.nodes[tgt].get("node_type")
                        for existing_succ in list(self.graph.successors(src)):
                            if self.graph.nodes[existing_succ].get("node_type") == target_node_type:
                                # Remove from DB
                                conn = sqlite3.connect(self.db_path)
                                conn.execute(
                                    "DELETE FROM edges WHERE source_id = ? AND target_id = ?",
                                    (src, existing_succ),
                                )
                                conn.commit()
                                conn.close()
                                # Remove from graph
                                self.graph.remove_edge(src, existing_succ)

                    # Create new edge (skip if duplicate)
                    if not self.graph.has_edge(src, tgt):
                        self.create_edge(src, tgt, edge_type)

            return {"success": True, "temp_id_map": temp_id_map}

        except Exception as e:
            return {"success": False, "error": f"Commit failed: {str(e)}"}
