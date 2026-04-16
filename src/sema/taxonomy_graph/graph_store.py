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
        # Handle → node_id cache for PATTERN nodes. Avoids O(N) scans of the
        # whole graph on every pattern lookup (pull/cascade hit this
        # hundreds of times per run). Maintained by create_node,
        # delete_node_cascade, merge_nodes, and execute_transaction.
        self._handle_to_id: dict[str, str] = {}
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
            nt = NodeType(node_type)
            self.graph.add_node(
                node_id,
                node_type=nt,
                text=text,
                metadata=json.loads(metadata_json),
                embedding=embedding,
            )
            if nt == NodeType.PATTERN:
                self._handle_to_id[text] = node_id

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
        if node_type == NodeType.PATTERN:
            self._handle_to_id[text] = node_id

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

    def _find_pattern_id(self, handle: str) -> str | None:
        """O(1) handle → node_id lookup for PATTERN nodes.

        Backed by self._handle_to_id, kept in sync by create_node,
        delete_node_cascade, merge_nodes, and execute_transaction.
        A missing entry means the handle does not exist.
        """
        return self._handle_to_id.get(handle)

    def get_nodes_by_type(self, node_type: NodeType) -> list[tuple[str, dict]]:
        """Get all nodes of a specific type."""
        return [
            (node_id, data)
            for node_id, data in self.graph.nodes(data=True)
            if data.get("node_type") == node_type
        ]

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
            existing_handles = set(self._handle_to_id)
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
        existing_nid = self._find_pattern_id(handle)
        if existing_nid is not None:
            pattern_id = existing_nid
            data = self.graph.nodes[existing_nid]
            if "metadata" in data:
                data["metadata"]["pattern"] = stored_pattern

                # Also promote layer/category to root metadata for easy access/indexing
                meta_block = solution.get("_meta", {})
                data["metadata"]["layer"] = (
                    meta_block.get("layer") or solution.get("sema_layer") or "Unknown"
                )
                data["metadata"]["category"] = (
                    meta_block.get("category") or solution.get("sema_category") or "Uncategorized"
                )

                # Persist metadata update
                conn = sqlite3.connect(self.db_path)
                conn.execute(
                    "UPDATE nodes SET metadata = ? WHERE id = ?",
                    (json.dumps(data["metadata"]), existing_nid),
                )
                conn.commit()
                conn.close()

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

            # Handle→id is already cached on self; no graph scan needed.
            all_patterns = self._handle_to_id

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
            for sig in signatures:
                # "Deep(Research)" -> Link to 'Deep' and 'Research'
                matches = re.findall(r"\w+", sig)
                for m in matches:
                    target_id = self._handle_to_id.get(m)
                    if target_id and not self.has_edge_of_type(
                        pattern_id, target_id, EdgeType.HAS_SIGNATURE
                    ):
                        self.create_edge(pattern_id, target_id, EdgeType.HAS_SIGNATURE)

        # D. Related (Metadata links)
        related = meta.get("related", [])
        if related:
            for item in related:
                if not isinstance(item, str):
                    continue
                target_handle = item.split("#")[0]
                target_id = self._handle_to_id.get(target_handle)

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

    def merge_nodes(self, node_id_keep: str, node_id_remove: str) -> bool:
        """Merge two nodes, redirecting all edges to the kept node.

        Multi-edge aware: dedupes by (edge_type, alias) tuple, not just by
        edge_type. Otherwise multiple parallel edges of the same type but
        with distinct aliases (e.g. accepts: {"task1": T, "task2": T})
        would collapse to one — silent data loss on merge.
        """
        if node_id_keep not in self.graph or node_id_remove not in self.graph:
            return False

        # Snapshot the removed node's handle (if it's a PATTERN) so we can
        # evict it from the index after the final graph.remove_node call.
        removed_data = self.graph.nodes[node_id_remove]
        removed_handle = (
            removed_data.get("text") if removed_data.get("node_type") == NodeType.PATTERN else None
        )

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
        if removed_handle is not None and self._handle_to_id.get(removed_handle) == node_id_remove:
            del self._handle_to_id[removed_handle]

        return True

    def stats(self) -> dict[str, int]:
        """Get basic graph statistics."""
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "patterns": len(self.get_nodes_by_type(NodeType.PATTERN)),
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
        target_node_id = self._find_pattern_id(handle)
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
            if pred_data.get("node_type") == NodeType.PATTERN:
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
        node_id = self._find_pattern_id(handle)
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
        nid = self._find_pattern_id(handle)
        if nid is None:
            return None
        data = self.graph.nodes[nid]
        content = data.get("metadata", {}).get("pattern", {}).copy()
        if include_deps:
            # Reconstruct dependencies from edges for export
            edge_deps = self.get_dependencies_from_edges(handle)
            if edge_deps:
                content["dependencies"] = edge_deps
        return content

    def _update_pattern_metadata(self, handle: str, new_pattern: dict[str, Any]):
        """Update a pattern's metadata in both graph and DB."""
        nid = self._find_pattern_id(handle)
        if nid is None:
            return
        data = self.graph.nodes[nid]
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

    def validate_dependency_refs(self, pattern: dict[str, Any]) -> list[str]:
        """Validate that all dependency references exist.

        Returns list of missing handles (empty if all valid).
        """
        from ..core.hashing import extract_handle_from_ref

        missing = []
        deps = pattern.get("dependencies", {})

        if not isinstance(deps, dict):
            return missing

        existing_handles = set(self._handle_to_id)

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

        # Snapshot node attrs before removal so we can evict from the
        # handle index after the in-memory graph has been mutated.
        node_data = self.graph.nodes[node_id]
        handle_to_evict = (
            node_data.get("text") if node_data.get("node_type") == NodeType.PATTERN else None
        )

        # Delete from DB - manually delete edges first (no CASCADE in schema)
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM edges WHERE source_id = ? OR target_id = ?", (node_id, node_id))
        conn.execute("DELETE FROM nodes WHERE id = ?", (node_id,))
        conn.commit()
        conn.close()

        # Remove from in-memory graph
        self.graph.remove_node(node_id)
        if handle_to_evict is not None and self._handle_to_id.get(handle_to_evict) == node_id:
            del self._handle_to_id[handle_to_evict]

        return {"success": True, "edges_removed": edges_removed}
