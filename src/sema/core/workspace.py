"""Tenant-aware graph workspace services.

This module is the first hosted-Sema seam: API, MCP, and future GitHub-backed
workflows can all talk to a workspace object instead of reaching for process-
wide registry globals directly.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from .hashing import HASH_ALGO, vocabulary_root
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
            pattern = json.loads(pattern_json)
        except json.JSONDecodeError as e:
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
        rows = []
        for handle, data in self.registry.items():
            sema_id = data.get("sema_id", "")
            if "#mh:SHA-256:" in sema_id:
                rows.append((handle, sema_id.split("#mh:SHA-256:")[1]))
        rows.sort(key=lambda row: row[0])
        root = vocabulary_root([hash_value for _, hash_value in rows])
        return {"hash": root, "stub": root[:16], "pattern_count": len(rows)}

    def root_payload(self) -> dict[str, Any]:
        root = self.vocabulary_root()
        return {
            "full_sema_id": f"sema:vocab#mh:{HASH_ALGO}:{root['hash']}",
            "stub": root["stub"],
            "hash": root["hash"],
            "pattern_count": root["pattern_count"],
            "db_path": self.db_path,
        }

    def handshake(self, ref: str, your_hash: str | None = None) -> dict[str, Any]:
        if ref.strip().lower() == "vocab":
            root = self.vocabulary_root()
            canonical_hash = root["hash"]
            canonical_stub = root["stub"]
            canonical_ref = f"sema:vocab#mh:{HASH_ALGO}:{canonical_hash}"

            if your_hash is None:
                return {
                    "verdict": "PROVIDE_HASH",
                    "scope": "vocab",
                    "canonical_stub": canonical_stub,
                    "canonical_ref": canonical_ref,
                    "full_sema_id": canonical_ref,
                    "pattern_count": root["pattern_count"],
                    "action": (
                        "Compare this vocabulary root with yours. Call again "
                        "with your_hash (16-char stub or 64-char full hash) to verify."
                    ),
                }

            normalized = your_hash.strip().lower()
            if normalized == canonical_stub or normalized == canonical_hash:
                return {
                    "verdict": "PROCEED",
                    "scope": "vocab",
                    "verified_ref": canonical_ref,
                    "pattern_count": root["pattern_count"],
                    "message": "Vocabulary alignment confirmed. Safe to coordinate.",
                }

            return {
                "verdict": "HALT",
                "scope": "vocab",
                "your_hash": your_hash,
                "canonical_stub": canonical_stub,
                "reason": "VOCABULARY DRIFT DETECTED",
                "action": (
                    "DO NOT PROCEED. Your vocabulary root differs. At least one "
                    "pattern's definition or the set of patterns itself differs "
                    "between you. Run `sema pull` to converge, or use "
                    "`sema_propose_context` on a shared subset instead."
                ),
                "canonical_ref": canonical_ref,
                "pattern_count": root["pattern_count"],
            }

        self.refresh()
        registry = self.registry
        parts = ref.split("#")
        handle = parts[0]
        ref_stub = parts[1] if len(parts) > 1 else None

        if handle not in registry:
            return {
                "verdict": "HALT",
                "reason": f"Pattern '{handle}' not found in vocabulary",
                "action": "Cannot coordinate - pattern unknown",
            }

        pattern = registry[handle]
        canonical_stub = pattern.get("sema_stub", "")
        canonical_ref = pattern.get("sema_ref", f"{handle}#{canonical_stub}")
        full_hash = pattern.get("sema_id", "")

        compare_hash = (your_hash or ref_stub or "").strip().lower()
        if not compare_hash:
            return {
                "verdict": "PROVIDE_HASH",
                "handle": handle,
                "canonical_stub": canonical_stub,
                "canonical_ref": canonical_ref,
                "full_sema_id": full_hash,
                "action": (
                    "Compare this hash with your local definition. "
                    "Call again with your_hash to verify."
                ),
            }

        # Accept the short stub or the full hash, like the vocab scope above.
        # A full-hash match is stronger evidence of alignment than the stub;
        # rejecting it would be a false HALT.
        canonical_full = ""
        marker = f"#mh:{HASH_ALGO}:"
        if isinstance(full_hash, str) and marker in full_hash:
            canonical_full = full_hash.split(marker, 1)[1].lower()
        if compare_hash == canonical_stub.lower() or (
            canonical_full and compare_hash == canonical_full
        ):
            return {
                "verdict": "PROCEED",
                "handle": handle,
                "verified_ref": canonical_ref,
                "message": "Semantic alignment confirmed. Safe to coordinate.",
                "invariants": pattern.get("invariants", []),
                "tier": pattern.get("tier", 1),
            }

        return {
            "verdict": "HALT",
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
