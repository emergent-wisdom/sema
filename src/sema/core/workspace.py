"""Tenant-aware graph workspace services.

This module is the first hosted-Sema seam: API, MCP, and future GitHub-backed
workflows can all talk to a workspace object instead of reaching for process-
wide registry globals directly.
"""

from __future__ import annotations

import os
from collections import defaultdict
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from threading import RLock
from typing import Any

from .handshake import HandshakeMode, HandshakeVerdict, decide_handshake
from .hashing import (
    HASH_ALGO,
    pattern_hash_from_sema_id,
    strict_json_loads,
    vocabulary_info,
    vocabulary_roots,
)
from .registry import RegistryManager
from .validator import validate_pattern


@dataclass
class WorkspaceSource:
    """Where a graph workspace comes from.

    For the hosted MVP, ``workspace_id`` can map to a GitHub installation/repo/ref
    while ``db_path`` points at the materialized read model used by Sema.
    """

    workspace_id: str = "local"
    label: str = "Local vocabulary"
    db_path: str | None = None
    vocab_dir: str | None = None
    owner: str | None = None
    repo: str | None = None
    ref: str | None = None
    read_only: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkspaceSession:
    """Per-client memory for compact MCP responses.

    Hosted MCP must not share "already seen" state across tenants or clients.
    Local stdio MCP can keep one process-level instance for backwards-compatible
    behavior.
    """

    served_patterns: set[str] = field(default_factory=set)

    def reset(self) -> int:
        count = len(self.served_patterns)
        self.served_patterns.clear()
        return count

    def mark(self, ref: str) -> None:
        if ref:
            self.served_patterns.add(ref)

    def has_seen(self, ref: str) -> bool:
        return bool(ref and ref in self.served_patterns)


class GraphWorkspace:
    """Read/validate operations scoped to one graph workspace."""

    def __init__(
        self,
        source: WorkspaceSource | None = None,
        registry_manager: RegistryManager | None = None,
    ):
        self.source = source or WorkspaceSource()
        self.registry_manager = registry_manager or RegistryManager(
            self.source.vocab_dir,
            db_path=self.source.db_path,
        )

    @property
    def registry(self) -> dict[str, dict[str, Any]]:
        return self.registry_manager.registry

    @property
    def db_path(self) -> str | None:
        return getattr(self.registry_manager, "db_path", None) or self.source.db_path

    @property
    def vocab_dir(self) -> str | None:
        return getattr(self.registry_manager, "vocab_dir", None) or self.source.vocab_dir

    def refresh(self) -> None:
        self.registry_manager.refresh()

    def describe(self) -> dict[str, Any]:
        root = self.vocabulary_root()
        return {
            "workspace_id": self.source.workspace_id,
            "label": self.source.label,
            "owner": self.source.owner,
            "repo": self.source.repo,
            "ref": self.source.ref,
            "read_only": self.source.read_only,
            "db_path": self.db_path,
            "vocab_dir": self.vocab_dir,
            "data_source": getattr(self.registry_manager, "source", "unknown"),
            "pattern_count": len(self.registry),
            "vocabulary_root": root["hash"],
            "vocabulary_root_stub": root["stub"],
            "vocabulary_root_scheme": root["root_scheme"],
            "catalog_root": root["catalog_root"],
            "catalog_root_stub": root["catalog_root_stub"],
            "catalog_root_scheme": root["catalog_root_scheme"],
            "definition_count": root["definition_count"],
            "metadata": self.source.metadata,
        }

    def search(
        self,
        query: str,
        *,
        session: WorkspaceSession | None = None,
        use_semantic: bool = True,
        enrich_top_n: int = 3,
    ) -> list[dict[str, Any]]:
        self.refresh()
        results = self.registry_manager.search(query, use_semantic=use_semantic)
        if session is None:
            return results

        compacted = []
        new_count = 0
        for result in results:
            ref = result.get("sema_ref") or result.get("handle", "")
            if session.has_seen(ref):
                compacted.append(
                    {
                        "handle": result.get("handle"),
                        "sema_ref": ref,
                        "gloss": result.get("gloss"),
                        "score": result.get("score"),
                        "_seen": True,
                    }
                )
                continue

            session.mark(ref)
            if new_count < enrich_top_n:
                handle = result.get("handle")
                clean_handle = handle.split("#")[0] if isinstance(handle, str) else None
                if clean_handle and hasattr(self.registry_manager, "get_context"):
                    context = self.registry_manager.get_context(clean_handle)
                    if context.get("dependencies") or context.get("used_by"):
                        result["graph_context"] = context
            new_count += 1
            compacted.append(result)

        return compacted

    def resolve(
        self,
        handle: str,
        *,
        depth: int = 1,
        session: WorkspaceSession | None = None,
    ) -> dict[str, Any]:
        self.refresh()
        subgraph = self.registry_manager.resolve(handle, depth=depth)
        if not subgraph:
            return {"error": f"Pattern '{handle}' not found"}

        rendered = {}
        for entry_handle in subgraph.keys():
            clean = entry_handle.split("#")[0]
            resolved_pattern = self.registry_manager.get_pattern(clean)
            rendered[entry_handle] = resolved_pattern or subgraph[entry_handle]
            if session is not None:
                session.mark(entry_handle)

        return {"root": handle, "depth": depth, "patterns": rendered, "count": len(rendered)}

    def lookup(self, ref: str) -> dict[str, Any]:
        self.refresh()
        parts = ref.split("#")
        handle = parts[0]
        stub = parts[1] if len(parts) > 1 else None

        pattern = self.registry_manager.get_pattern(handle)
        if not pattern:
            return {"error": f"Pattern '{handle}' not found"}

        if stub:
            pattern_stub = pattern.get("sema_stub", "")
            if stub != pattern_stub:
                return {
                    "warning": (
                        f"Stub mismatch: requested '{stub}' but pattern has '{pattern_stub}'"
                    ),
                    "pattern": pattern,
                }

        return pattern

    def validate_pattern_json(self, pattern_json: str) -> dict[str, Any]:
        try:
            pattern = strict_json_loads(pattern_json, label="Pattern JSON")
        except ValueError as e:
            return {"valid": False, "errors": [f"Invalid JSON: {e}"], "warnings": []}

        if not isinstance(pattern, dict):
            return {"valid": False, "errors": ["Pattern JSON must be an object"], "warnings": []}

        return self.validate_pattern(pattern)

    def validate_pattern(self, pattern: dict[str, Any]) -> dict[str, Any]:
        self.refresh()
        is_valid, errors, warnings = validate_pattern(
            pattern,
            known_handles=set(self.registry.keys()),
        )
        specialization = pattern.get("extends")
        if specialization:
            parent_handle = specialization.removeprefix("sema:").split("#", 1)[0]
            parent = self.registry.get(parent_handle) or {}
            active_parent_ref = parent.get("sema_id")
            if parent_handle in self.registry and specialization != active_parent_ref:
                errors.append(
                    f"❌ UNRESOLVABLE SPECIALIZATION: {specialization!r} is not the active "
                    f"definition of '{parent_handle}' in this workspace."
                )
                is_valid = False
        return {
            "valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "handle": pattern.get("handle", "Unknown"),
        }

    def stats(self) -> dict[str, Any]:
        self.refresh()
        layers: defaultdict[str, int] = defaultdict(int)
        categories: defaultdict[str, int] = defaultdict(int)

        for _handle, data in self.registry.items():
            layers[data.get("sema_layer") or data.get("layer", "Unknown")] += 1
            categories[data.get("sema_category") or data.get("category", "Unknown")] += 1

        return {
            "workspace_id": self.source.workspace_id,
            "total_patterns": len(self.registry),
            "by_layer": dict(layers),
            "by_category": dict(categories),
            "vocab_dir": self.vocab_dir,
            "data_source": getattr(self.registry_manager, "source", "unknown"),
            "db_path": self.db_path,
        }

    def tree(
        self,
        *,
        layer: str | None = None,
        category: str | None = None,
        verbose: bool = False,
    ) -> dict[str, Any]:
        self.refresh()
        patterns = []
        for handle, data in self.registry.items():
            p_layer = data.get("sema_layer") or data.get("layer", "Unknown")
            p_category = data.get("sema_category") or data.get("category", "UNCATEGORIZED")

            if layer and p_layer != layer:
                continue
            if category and p_category != category:
                continue

            if verbose:
                gloss = data.get("gloss", "")
                entry = f"{handle}: {gloss}" if gloss else handle
            else:
                entry = handle

            patterns.append({"entry": entry, "category": p_category, "layer": p_layer})

        tree = defaultdict(lambda: defaultdict(list))
        for pattern in patterns:
            tree[pattern["layer"]][pattern["category"]].append(pattern["entry"])

        result = {
            layer_name: {cat: sorted(entries) for cat, entries in cats.items()}
            for layer_name, cats in tree.items()
        }
        return {
            "tree": result,
            "total_patterns": len(patterns),
            "layers": list(tree.keys()),
            "filter": {"layer": layer, "category": category, "verbose": verbose},
        }

    def graph_skeleton(self) -> str:
        self.refresh()
        return self.registry_manager.get_graph_skeleton()

    def vocabulary_root(self) -> dict[str, Any]:
        self.refresh()

        # A RegistryManager dictionary is a convenient read model, not a
        # complete catalog proof: its loader may omit malformed rows and a
        # dict cannot represent duplicate handles. Fingerprint the database
        # rows directly whenever a materialized database is available.
        if self.db_path and os.path.isfile(self.db_path):
            return vocabulary_info(self.db_path)
        if self.db_path and isinstance(self.registry_manager, RegistryManager):
            raise FileNotFoundError(f"workspace database not found: {self.db_path}")

        bindings = []
        for handle, data in self.registry.items():
            sema_id = data.get("sema_id")
            try:
                pattern_hash = pattern_hash_from_sema_id(sema_id, expected_handle=handle)
            except ValueError as exc:
                raise ValueError(f"pattern {handle!r} has an invalid sema_id: {exc}") from exc
            bindings.append((handle, pattern_hash))
        return vocabulary_roots(bindings)

    def root_payload(self) -> dict[str, Any]:
        root = self.vocabulary_root()
        return {
            "full_sema_id": f"sema:vocab#mh:{HASH_ALGO}:{root['hash']}",
            "stub": root["stub"],
            "hash": root["hash"],
            "root_scheme": root["root_scheme"],
            "semantic_root": root["semantic_root"],
            "semantic_root_scheme": root["semantic_root_scheme"],
            "catalog_full_sema_id": (f"sema:catalog#mh:{HASH_ALGO}:{root['catalog_root']}"),
            "catalog_root": root["catalog_root"],
            "catalog_root_stub": root["catalog_root_stub"],
            "catalog_root_scheme": root["catalog_root_scheme"],
            "pattern_count": root["pattern_count"],
            "definition_count": root["definition_count"],
            "db_path": self.db_path,
        }

    def handshake(
        self,
        ref: str,
        your_hash: str | None = None,
        *,
        strict: bool = False,
        your_scheme: str | None = None,
    ) -> dict[str, Any]:
        mode = HandshakeMode.STRICT if strict else HandshakeMode.COOPERATIVE
        aggregate_scope = ref.strip().lower()
        if aggregate_scope in {"vocab", "catalog"}:
            root = self.vocabulary_root()
            if aggregate_scope == "catalog":
                canonical_hash = root["catalog_root"]
                canonical_stub = root["catalog_root_stub"]
                canonical_scheme = root["catalog_root_scheme"]
                canonical_ref = f"sema:catalog#mh:{HASH_ALGO}:{canonical_hash}"
                count_name = "pattern_count"
                count = root["pattern_count"]
                alignment_name = "Catalog"
            else:
                canonical_hash = root["semantic_root"]
                canonical_stub = root["semantic_root_stub"]
                canonical_scheme = root["semantic_root_scheme"]
                canonical_ref = f"sema:vocab#mh:{HASH_ALGO}:{canonical_hash}"
                count_name = "definition_count"
                count = root["definition_count"]
                alignment_name = "Semantic-set"

            common = {
                "scope": aggregate_scope,
                "root_scheme": canonical_scheme,
                count_name: count,
                "pattern_count": root["pattern_count"],
            }

            presented_hash = None if your_hash is None else your_hash.strip().lower()
            if presented_hash and your_scheme is None:
                return {
                    "verdict": HandshakeVerdict.HALT.value,
                    **common,
                    "reason": "ROOT SCHEME REQUIRED",
                    "canonical_ref": canonical_ref,
                    "action": (
                        "DO NOT PROCEED. Supply the root_scheme that accompanied "
                        "the remote root; a digest alone does not identify the "
                        "aggregate construction."
                    ),
                }

            if presented_hash and your_scheme != canonical_scheme:
                return {
                    "verdict": HandshakeVerdict.HALT.value,
                    **common,
                    "your_scheme": your_scheme,
                    "reason": "ROOT SCHEME MISMATCH",
                    "canonical_ref": canonical_ref,
                    "action": (
                        "DO NOT PROCEED. Upgrade both Sema installations to a version "
                        "that uses the same root scheme; pulling pattern data cannot "
                        "repair an aggregate-algorithm mismatch."
                    ),
                }

            verdict = decide_handshake(
                available=True,
                presented_hash=presented_hash,
                canonical_stub=canonical_stub,
                canonical_full=canonical_hash,
                mode=mode,
            )

            if verdict is HandshakeVerdict.PROVIDE_HASH:
                return {
                    "verdict": verdict.value,
                    **common,
                    "canonical_stub": canonical_stub,
                    "canonical_ref": canonical_ref,
                    "full_sema_id": canonical_ref,
                    "action": (
                        f"Compare this {aggregate_scope} root and root_scheme with yours. "
                        "Call again with your_hash (16-char stub or 64-char full hash) "
                        "and your_scheme to verify."
                    ),
                }

            if verdict is HandshakeVerdict.PROCEED:
                assurance = "full_hash" if presented_hash == canonical_hash else "prefix"
                return {
                    "verdict": verdict.value,
                    **common,
                    "verified_ref": canonical_ref,
                    "assurance": assurance,
                    "mode": mode.value,
                    "message": f"{alignment_name} alignment confirmed. Safe to coordinate.",
                }

            if verdict is HandshakeVerdict.REQUIRE_FULL_HASH:
                return {
                    "verdict": verdict.value,
                    **common,
                    "canonical_stub": canonical_stub,
                    "canonical_ref": canonical_ref,
                    "full_sema_id": canonical_ref,
                    "mode": mode.value,
                    "action": (
                        f"The {aggregate_scope} prefix matches, but strict verification requires "
                        "the full 64-character hash. Call again with the full hash."
                    ),
                }

            return {
                "verdict": verdict.value,
                **common,
                "your_hash": your_hash,
                "canonical_stub": canonical_stub,
                "reason": f"{alignment_name.upper()} DRIFT DETECTED",
                "action": (
                    f"DO NOT PROCEED. Your {aggregate_scope} root differs. First verify "
                    f"that both sides use root_scheme={canonical_scheme!r}. If schemes "
                    "match, run `sema pull` to converge pattern data or use "
                    "`sema_propose_context` on a known-shared subset."
                ),
                "canonical_ref": canonical_ref,
            }

        self.refresh()
        registry = self.registry
        parts = ref.split("#")
        handle = parts[0]
        ref_stub = parts[1] if len(parts) > 1 else None

        if handle not in registry:
            verdict = decide_handshake(
                available=False,
                presented_hash=your_hash or ref_stub,
                canonical_stub="",
                canonical_full=None,
                mode=mode,
            )
            return {
                "verdict": verdict.value,
                "reason": f"Pattern '{handle}' not found in vocabulary",
                "action": "Cannot coordinate - pattern unknown",
            }

        pattern = registry[handle]
        canonical_stub = pattern.get("sema_stub", "")
        canonical_ref = pattern.get("sema_ref", f"{handle}#{canonical_stub}")
        full_hash = pattern.get("sema_id", "")

        compare_hash = (your_hash or ref_stub or "").strip().lower()
        # Accept the short stub or the full hash, like the vocab scope above.
        # A full-hash match is stronger evidence of alignment than the stub;
        # rejecting it would be a false HALT.
        canonical_full = ""
        marker = f"#mh:{HASH_ALGO}:"
        if isinstance(full_hash, str) and marker in full_hash:
            canonical_full = full_hash.split(marker, 1)[1].lower()
        verdict = decide_handshake(
            available=True,
            presented_hash=compare_hash or None,
            canonical_stub=canonical_stub.lower(),
            canonical_full=canonical_full or None,
            mode=mode,
        )
        if verdict is HandshakeVerdict.PROVIDE_HASH:
            return {
                "verdict": verdict.value,
                "handle": handle,
                "canonical_stub": canonical_stub,
                "canonical_ref": canonical_ref,
                "full_sema_id": full_hash,
                "action": (
                    "Compare this hash with your local definition. "
                    "Call again with your_hash to verify."
                ),
            }

        if verdict is HandshakeVerdict.PROCEED:
            assurance = "full_hash" if compare_hash == canonical_full else "prefix"
            return {
                "verdict": verdict.value,
                "handle": handle,
                "verified_ref": canonical_ref,
                "assurance": assurance,
                "mode": mode.value,
                "message": "Semantic alignment confirmed. Safe to coordinate.",
                "invariants": pattern.get("invariants", []),
                "tier": pattern.get("tier", 1),
            }

        if verdict is HandshakeVerdict.REQUIRE_FULL_HASH:
            return {
                "verdict": verdict.value,
                "handle": handle,
                "canonical_stub": canonical_stub,
                "canonical_ref": canonical_ref,
                "full_sema_id": full_hash,
                "mode": mode.value,
                "action": (
                    "The pattern prefix matches, but strict verification requires the full "
                    "64-character hash. Call again with the full hash."
                ),
            }

        return {
            "verdict": verdict.value,
            "handle": handle,
            "your_hash": compare_hash,
            "canonical_hash": canonical_stub,
            "reason": "SEMANTIC DRIFT DETECTED",
            "action": (
                "DO NOT PROCEED. Your definition differs from the canonical vocabulary. "
                "Either update your local definition or escalate to OntologyHandshake."
            ),
            "canonical_ref": canonical_ref,
            "full_sema_id": full_hash,
        }


class WorkspaceNotFoundError(LookupError):
    """Raised when a tenant workspace ID is not registered."""

    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        super().__init__(f"Workspace '{workspace_id}' not found")


class WorkspaceCatalog:
    """Resolve registered tenant IDs to isolated graph workspaces.

    Sources are cheap catalog records. ``GraphWorkspace`` instances are opened
    lazily and cached per ID so one tenant can never fall through to another
    tenant's process-wide registry. A future Supabase adapter can refresh the
    registered sources without changing the hosted route boundary.
    """

    def __init__(
        self,
        sources: Iterable[WorkspaceSource] = (),
        *,
        workspace_factory: Callable[[WorkspaceSource], GraphWorkspace] = GraphWorkspace,
    ):
        self._sources: dict[str, WorkspaceSource] = {}
        self._workspaces: dict[str, GraphWorkspace] = {}
        self._workspace_factory = workspace_factory
        self._lock = RLock()
        for source in sources:
            self.register_source(source)

    @staticmethod
    def _source_id(source: WorkspaceSource) -> str:
        workspace_id = source.workspace_id.strip()
        if not workspace_id:
            raise ValueError("workspace_id must not be blank")
        if workspace_id != source.workspace_id:
            raise ValueError("workspace_id must not have surrounding whitespace")
        return workspace_id

    def register_source(self, source: WorkspaceSource) -> None:
        """Add or replace a source and invalidate any cached workspace."""

        workspace_id = self._source_id(source)
        with self._lock:
            self._sources[workspace_id] = source
            self._workspaces.pop(workspace_id, None)

    def register_workspace(self, workspace: GraphWorkspace) -> None:
        """Register an already-open workspace, such as the local default."""

        workspace_id = self._source_id(workspace.source)
        with self._lock:
            self._sources[workspace_id] = workspace.source
            self._workspaces[workspace_id] = workspace

    def resolve(self, workspace_id: str) -> GraphWorkspace:
        """Return the isolated workspace for ``workspace_id``, opening it once."""

        with self._lock:
            cached = self._workspaces.get(workspace_id)
            if cached is not None:
                return cached

            source = self._sources.get(workspace_id)
            if source is None:
                raise WorkspaceNotFoundError(workspace_id)

            workspace = self._workspace_factory(source)
            self._workspaces[workspace_id] = workspace
            return workspace
