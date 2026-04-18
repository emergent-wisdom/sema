"""
Sema Core Hashing Logic.
Canonicalizes and hashes pattern definitions using Merkle Tree structure.
Supports addressing sub-components (e.g. pattern#hash/invariants/0#subhash).
"""

import hashlib
import json
import unicodedata
from typing import Any

# We use SHA-256 for all hashing to match the Sema v1 spec
HASH_ALGO = "SHA-256"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_string(s: str) -> str:
    """NFC normalize and strip whitespace."""
    s = unicodedata.normalize("NFC", s.strip())
    return " ".join(s.split())


def canonical_json(obj: Any) -> bytes:
    """Produce deterministic JSON bytes."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode(
        "utf-8"
    )


def merkle_hash(obj: Any) -> tuple[str, Any]:
    """
    Recursively hash an object, returning (hash, canonical_obj).

    Rules:
    - String: Hash(Normalize(s))
    - Number/Bool/Null: Hash(CanonicalJSON(v))
    - List: Hash(Hash(Item1) + Hash(Item2)...)
    - Dict: Hash(Sort(Key) + Hash(Key) + Hash(Value)...)
    """
    if isinstance(obj, str):
        norm = normalize_string(obj)
        return _sha256(norm.encode("utf-8")), norm

    elif isinstance(obj, int | float | bool | type(None)):
        canon = canonical_json(obj)
        return _sha256(canon), obj

    elif isinstance(obj, list):
        # Hash each item
        hashed_items = [merkle_hash(item) for item in obj]
        # Merkle of list is Hash of concatenation of item hashes
        # This preserves ORDER.
        concatenated = "".join(h for h, _ in hashed_items).encode("utf-8")
        return _sha256(concatenated), [val for _, val in hashed_items]

    elif isinstance(obj, dict):
        # Hash keys and values
        # Sort by Key
        sorted_items = sorted(obj.items(), key=lambda x: x[0])

        concatenated = b""
        canon_dict = {}

        for k, v in sorted_items:
            # Key Hash (Keys must be strings)
            k_hash, k_canon = merkle_hash(str(k))
            # Value Hash
            v_hash, v_canon = merkle_hash(v)

            concatenated += k_hash.encode("utf-8") + v_hash.encode("utf-8")
            canon_dict[k_canon] = v_canon

        return _sha256(concatenated), canon_dict

    else:
        raise ValueError(f"Unsupported type for hashing: {type(obj)}")


# Semantic fields that get hashed (from INSTRUCTION.md Section 4)
SEMANTIC_FIELDS = [
    "dependencies",
    "signature",
    "data_schema",
    "mechanism",
    "gloss",
    "invariants",
    "preconditions",
    "postconditions",
    "parameters",
    "failure_modes",
    "derived_from",
]


def extract_handle_from_ref(ref: str) -> str:
    """Extract clean handle from various reference formats.

    Handles:
        "Gate" -> "Gate"
        "Gate#7f09" -> "Gate"
        "sema:Gate#mh:SHA-256:abc..." -> "Gate"
        None -> None
        "" -> ""
    """
    if not ref:
        return ref
    # Strip sema: prefix if present
    if ref.startswith("sema:"):
        ref = ref[5:]
    # Extract handle before any # delimiter
    return ref.split("#")[0]


def normalize_dependencies_to_handles(deps: dict[str, Any]) -> dict[str, Any]:
    """Convert all dependency references to handle-only format.

    Input: {"references": {"gate": "sema:Gate#mh:SHA-256:abc..."}}
    Output: {"references": {"gate": "Gate"}}
    """
    if not isinstance(deps, dict):
        return deps

    normalized = {}
    for dep_type, items in deps.items():
        if isinstance(items, dict):
            normalized[dep_type] = {
                key: extract_handle_from_ref(val) if isinstance(val, str) else val
                for key, val in items.items()
            }
        else:
            normalized[dep_type] = items
    return normalized


def canonicalize_dependency_keys(deps: dict[str, Any]) -> dict[str, Any]:
    """Canonicalize dependency keys for consistent hashing.

    Uses lowercased target handle as the key, ensuring consistent
    hashing regardless of the user-provided alias.

    Input: {"references": {"base": "TargetHandle#abc1"}}
    Output: {"references": {"targethandle": "TargetHandle#abc1"}}
    """
    if not isinstance(deps, dict):
        return deps

    normalized = {}
    for dep_type, items in deps.items():
        if isinstance(items, dict):
            normalized[dep_type] = {}
            for key, val in items.items():
                if isinstance(val, str):
                    # Extract handle and use lowercased as canonical key
                    handle = extract_handle_from_ref(val)
                    canonical_key = handle.lower()
                    normalized[dep_type][canonical_key] = val
                else:
                    normalized[dep_type][key] = val
        else:
            normalized[dep_type] = items
    return normalized


def resolve_dependencies_to_sema_ids(deps: dict[str, Any], hash_lookup: callable) -> dict[str, Any]:
    """Resolve handle references to full sema IDs.

    Args:
        deps: Dependencies with handle references (any format)
        hash_lookup: Function that takes clean handle -> returns current hash (or None)

    Input: {"references": {"gate": "Gate#stub"}} or {"references": {"gate": "Gate"}}
    Output: {"references": {"gate": "sema:Gate#mh:SHA-256:abc123..."}}
    """
    if not isinstance(deps, dict):
        return deps

    resolved = {}
    for dep_type, items in deps.items():
        if isinstance(items, dict):
            resolved[dep_type] = {}
            for key, ref in items.items():
                if isinstance(ref, str):
                    # Extract clean handle from any format
                    clean_handle = extract_handle_from_ref(ref)
                    current_hash = hash_lookup(clean_handle)
                    if current_hash:
                        resolved[dep_type][key] = (
                            f"sema:{clean_handle}#mh:{HASH_ALGO}:{current_hash}"
                        )
                    else:
                        # Keep original if not found (will fail validation)
                        resolved[dep_type][key] = ref
                else:
                    resolved[dep_type][key] = ref
        else:
            resolved[dep_type] = items
    return resolved


def generate_sema_hash(pattern: dict[str, Any], hash_lookup: callable = None) -> dict[str, Any]:
    """Generate a Sema hash for a pattern using Merkle Root.

    Args:
        pattern: The pattern dict with handle and semantic fields
        hash_lookup: Optional function(handle) -> hash for resolving dependencies.
                     If None, dependencies are hashed as-is.

    Returns:
        {
            "full_id": "sema:Handle#mh:SHA-256:abc123...",
            "stub": "abc1",
            "handle": "Handle",
            "reference": "Handle#abc1",
            "hash": "abc123...",
        }
    """
    # 1. Extract semantic fields only
    content = {k: pattern[k] for k in SEMANTIC_FIELDS if k in pattern}

    # 2. Canonicalize dependency keys for consistent hashing
    #    This ensures "base" -> "targethandle" normalization
    if "dependencies" in content:
        content["dependencies"] = canonicalize_dependency_keys(content["dependencies"])

    # 3. If hash_lookup provided, resolve dependencies to full sema IDs
    #    This creates the Merkle DAG property: our hash depends on dep hashes
    if hash_lookup and "dependencies" in content:
        content["dependencies"] = resolve_dependencies_to_sema_ids(
            content["dependencies"], hash_lookup
        )

    # 3. Compute Merkle Root
    root_hash, canonical_content = merkle_hash(content)

    handle = pattern.get("handle", "Unknown")
    clean_handle = "".join(c for c in handle if c.isalnum() or c in ["_", "-"])
    stub = root_hash[:4]

    return {
        "full_id": f"sema:{clean_handle}#mh:{HASH_ALGO}:{root_hash}",
        "stub": stub,
        "handle": clean_handle,
        "reference": f"{clean_handle}#{stub}",
        "hash": root_hash,
    }


def vocabulary_root(pattern_hashes: list[str]) -> str:
    """Compute the vocabulary-wide root hash over a list of pattern hashes.

    SHA-256 over the concatenation of hashes in the order given. The caller
    is responsible for sorting — convention is ascending-by-handle, so two
    agents with the same set of patterns produce the same root regardless
    of insertion order.

    This is the single source of truth for "do two vocabularies agree?"
    — used by `sema root`, `sema_root()` / `sema_handshake(ref="vocab")`,
    and the `scripts/vocabulary_merkle_root.py` doc generator.
    """
    return _sha256("".join(pattern_hashes).encode("utf-8"))


def vocabulary_info(db_path: str) -> dict:
    """Read a taxonomy.db and return a load-line-sized state fingerprint.

    Returns:
        {
            "root": "sha256-hex-string",         # vocabulary Merkle root
            "pattern_count": int,
            "db_path": str,
            "stamped_version": str | None,        # placeholder for future version-stamping
        }

    The root is the authoritative cryptographic fingerprint — two DBs with
    the same set of pattern sema_ids produce the same root regardless of
    insertion order, SQLite page layout, or anything non-semantic.
    """
    import json
    import sqlite3

    con = sqlite3.connect(db_path)
    try:
        rows = con.execute("SELECT text, metadata FROM nodes WHERE node_type='PATTERN'").fetchall()
    finally:
        con.close()

    pairs = []
    for text, meta_json in rows:
        if not meta_json:
            continue
        meta = json.loads(meta_json)
        sema_id = meta.get("pattern", {}).get("sema_id", "")
        if "SHA-256:" in sema_id:
            pairs.append((text, sema_id.split("SHA-256:")[1]))

    pairs.sort(key=lambda p: p[0])
    hashes = [h for _, h in pairs]
    return {
        "root": vocabulary_root(hashes),
        "pattern_count": len(pairs),
        "db_path": db_path,
        "stamped_version": None,
    }


def format_load_line(info: dict) -> str:
    """Banner for a vocabulary DB. Two lines — full root first (verifiable),
    context below (scannable).

    Example:
        📚 sema:vocab#mh:SHA-256:39ca671a4dcb3075855cb293380d1796105e2eca0de49b0537279b798b675ee6
           452 patterns (data/taxonomy.db)

    When a stamped version becomes available, it's appended inline to the
    second line without disturbing the root:
        📚 sema:vocab#mh:SHA-256:39ca671a...
           452 patterns, v0.2.0 (data/taxonomy.db)
    """
    root = info.get("root", "") or "unknown"
    count = info.get("pattern_count", 0)
    db = info.get("db_path", "?")
    version = info.get("stamped_version")
    second = f"{count} patterns"
    if version:
        second += f", v{version}"
    second += f" ({db})"
    return f"📚 sema:vocab#mh:SHA-256:{root}\n   {second}"
