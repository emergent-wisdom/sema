"""
Sema Core Hashing Logic.
Canonicalizes and hashes pattern definitions using Merkle Tree structure.
Supports addressing sub-components (e.g. pattern#hash/invariants/0#subhash).
"""

import hashlib
import json
import re
import unicodedata
from collections.abc import Iterable, Sequence
from typing import Any

# We use SHA-256 for all hashing to match the Sema v1 spec
HASH_ALGO = "SHA-256"

# Aggregate-root schemes are versioned independently from pattern
# canonicalization. Pattern hashes can stay byte-identical while a root
# construction changes, so callers need both the digest and its scheme.
SEMANTIC_ROOT_SCHEME = "sema-semantic-set-v1"
CATALOG_ROOT_SCHEME = "sema-catalog-v1"

_SEMANTIC_ROOT_DOMAIN = SEMANTIC_ROOT_SCHEME.encode("ascii") + b"\x00"
_CATALOG_ROOT_DOMAIN = CATALOG_ROOT_SCHEME.encode("ascii") + b"\x00"
_SHA256_HEX_RE = re.compile(r"[0-9a-f]{64}")
_HANDLE_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")


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


# Canonicalization v2 domain-separation tags (semahash 0.3.0).
#
# v1 hashed raw bytes with no type information, so structurally different
# values collided: merkle_hash("1") == merkle_hash(1),
# merkle_hash("") == merkle_hash([]) == merkle_hash({}), and a 2-element
# list collided with a 1-entry dict (both concatenate two digests). For a
# protocol whose invariant is word = hash(canonical(definition)), two
# different definitions sharing one address is the worst failure mode.
# Every node's hash input is now prefixed with its type. Digests are
# fixed-width hex, so tagged concatenations are unambiguous.
_TAG_STR = b"s:"
_TAG_PRIMITIVE = b"p:"
_TAG_LIST = b"l:"
_TAG_DICT = b"d:"


def merkle_hash(obj: Any) -> tuple[str, Any]:
    """
    Recursively hash an object, returning (hash, canonical_obj).

    Canonicalization v2 rules:
    - String: Hash("s:" + Normalize(s))
    - Number/Bool/Null: Hash("p:" + CanonicalJSON(v))
    - List: Hash("l:" + Hash(Item1) + Hash(Item2)...)  — order preserved
    - Dict: Hash("d:" + Hash(NormKey) + Hash(Value)...), entries sorted by
      NORMALIZED key so the hash is a function of the canonical form.
      Keys that collide after normalization raise ValueError (fail closed;
      v1 silently dropped one entry).
    """
    if isinstance(obj, str):
        norm = normalize_string(obj)
        return _sha256(_TAG_STR + norm.encode("utf-8")), norm

    elif isinstance(obj, int | float | bool | type(None)):
        canon = canonical_json(obj)
        return _sha256(_TAG_PRIMITIVE + canon), obj

    elif isinstance(obj, list):
        # Hash each item
        hashed_items = [merkle_hash(item) for item in obj]
        # Merkle of list is Hash of concatenation of item hashes
        # This preserves ORDER.
        concatenated = _TAG_LIST + "".join(h for h, _ in hashed_items).encode("utf-8")
        return _sha256(concatenated), [val for _, val in hashed_items]

    elif isinstance(obj, dict):
        entries = []
        values_by_canon_key: dict[str, Any] = {}

        for k, v in obj.items():
            # Key Hash (Keys must be strings)
            k_hash, k_canon = merkle_hash(str(k))
            if k_canon in values_by_canon_key:
                raise ValueError(
                    f"Dict keys collide after normalization: {k_canon!r} — "
                    "the canonical form would silently lose an entry"
                )
            # Value Hash
            v_hash, v_canon = merkle_hash(v)
            entries.append((k_canon, k_hash, v_hash))
            values_by_canon_key[k_canon] = v_canon

        # Sort by the NORMALIZED key: v1 sorted by raw key but hashed the
        # normalized key, so the same canonical dict could hash two ways.
        entries.sort(key=lambda entry: entry[0])
        concatenated = _TAG_DICT + b"".join(
            k_hash.encode("utf-8") + v_hash.encode("utf-8") for _, k_hash, v_hash in entries
        )
        canon_dict = {k_canon: values_by_canon_key[k_canon] for k_canon, _, _ in entries}

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
    "extends",
]

# 0.3 and earlier called the specialization field `derived_from`. Keep that
# spelling readable and hash-verifiable so an upgraded client can still resolve
# an existing content-addressed card. New cards use `extends`; carrying both is
# ambiguous and rejected by generate_sema_hash and the schema.
LEGACY_SPECIALIZATION_FIELD = "derived_from"


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

    Uses the lowercased target handle as the key, ensuring consistent
    hashing regardless of the user-provided alias.

    When multiple aliases point at the same handle (e.g. gate_in/gate_out
    both referencing Gate), the canonical value is the sorted LIST of refs
    — v1 collapsed them to one insertion-order-dependent entry, silently
    dropping a dependency from the hash input. Multiplicity is semantic
    (two slots vs one); alias spelling is not.

    Input: {"references": {"base": "TargetHandle#abc1"}}
    Output: {"references": {"targethandle": "TargetHandle#abc1"}}
    """
    if not isinstance(deps, dict):
        return deps

    normalized = {}
    for dep_type, items in deps.items():
        if isinstance(items, dict):
            grouped: dict[str, list[str]] = {}
            passthrough = {}
            for key, val in items.items():
                if isinstance(val, str):
                    # Extract handle and use lowercased as canonical key
                    handle = extract_handle_from_ref(val)
                    grouped.setdefault(handle.lower(), []).append(val)
                else:
                    passthrough[key] = val

            normalized[dep_type] = {}
            for canonical_key, refs in grouped.items():
                normalized[dep_type][canonical_key] = refs[0] if len(refs) == 1 else sorted(refs)
            normalized[dep_type].update(passthrough)
        else:
            normalized[dep_type] = items
    return normalized


def resolve_ref_to_sema_id(ref: str, hash_lookup: callable) -> str:
    """Rewrite one handle reference to the target's current full sema_id.

    Returns the input unchanged when the handle does not resolve, so the failure
    surfaces in validation rather than silently pointing at nothing.
    """
    if not isinstance(ref, str) or not ref:
        return ref
    clean_handle = extract_handle_from_ref(ref)
    current_hash = hash_lookup(clean_handle)
    if current_hash:
        return f"sema:{clean_handle}#mh:{HASH_ALGO}:{current_hash}"
    return ref


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

    def _resolve_ref(ref: str) -> str:
        # Extract clean handle from any format
        clean_handle = extract_handle_from_ref(ref)
        current_hash = hash_lookup(clean_handle)
        if current_hash:
            return f"sema:{clean_handle}#mh:{HASH_ALGO}:{current_hash}"
        # Keep original if not found (will fail validation)
        return ref

    resolved = {}
    for dep_type, items in deps.items():
        if isinstance(items, dict):
            resolved[dep_type] = {}
            for key, ref in items.items():
                if isinstance(ref, str):
                    resolved[dep_type][key] = _resolve_ref(ref)
                elif isinstance(ref, list):
                    # Multi-ref entry from canonicalize_dependency_keys
                    # (several aliases to one handle). Re-sort after
                    # resolution so the canonical order doesn't depend on
                    # the pre-resolution ref format.
                    resolved[dep_type][key] = sorted(
                        _resolve_ref(r) if isinstance(r, str) else r for r in ref
                    )
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
    if "extends" in pattern and LEGACY_SPECIALIZATION_FIELD in pattern:
        raise ValueError("Pattern cannot contain both `extends` and legacy `derived_from`")

    # 1. Extract semantic fields only. For a legacy card, retain the legacy key
    # itself in the Merkle input: renaming it before hashing would change the ID
    # that compatibility support exists to verify.
    content = {k: pattern[k] for k in SEMANTIC_FIELDS if k in pattern}
    if LEGACY_SPECIALIZATION_FIELD in pattern:
        content[LEGACY_SPECIALIZATION_FIELD] = pattern[LEGACY_SPECIALIZATION_FIELD]

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


def _decode_sha256_digest(value: str, *, label: str = "pattern hash") -> bytes:
    """Decode one canonical SHA-256 digest or fail closed."""
    if not isinstance(value, str) or not _SHA256_HEX_RE.fullmatch(value):
        raise ValueError(f"{label} must be exactly 64 lowercase hexadecimal characters")
    return bytes.fromhex(value)


def pattern_hash_from_sema_id(sema_id: str, *, expected_handle: str | None = None) -> str:
    """Extract and validate the digest in a canonical full Sema identifier.

    Aggregate roots must not silently omit malformed entries. When a caller
    knows the catalog handle, ``expected_handle`` also verifies that the
    identifier is bound to the same name.
    """
    if not isinstance(sema_id, str):
        raise ValueError("sema_id must be a string")

    match = re.fullmatch(
        r"sema:([A-Za-z][A-Za-z0-9_-]*)#mh:SHA-256:([0-9a-f]{64})",
        sema_id,
    )
    if not match:
        raise ValueError("sema_id must be a canonical full SHA-256 Sema identifier")

    handle, digest = match.groups()
    if expected_handle is not None and handle != expected_handle:
        raise ValueError(
            f"sema_id handle {handle!r} does not match catalog handle {expected_handle!r}"
        )
    return digest


def _merkle_tree_hash(entries: Sequence[bytes]) -> bytes:
    """Apply the Merkle Tree Hash construction from RFC 9162 §2.1.1.

    The input is an ordered sequence. Leaves are ``H(0x00 || entry)``;
    internal nodes are ``H(0x01 || left || right)``. For a non-power-of-two
    tree, recursion splits at the largest power of two smaller than the
    number of entries. This uniquely defines the tree without duplicating
    an unpaired node.
    """
    count = len(entries)
    if count == 0:
        return hashlib.sha256(b"").digest()
    if count == 1:
        return hashlib.sha256(b"\x00" + entries[0]).digest()

    split = 1 << ((count - 1).bit_length() - 1)
    left = _merkle_tree_hash(entries[:split])
    right = _merkle_tree_hash(entries[split:])
    return hashlib.sha256(b"\x01" + left + right).digest()


def vocabulary_root(pattern_hashes: Iterable[str]) -> str:
    """Commit to the unordered set of semantic pattern identities.

    Inputs are canonical SHA-256 hex digests. They are decoded to raw bytes,
    deduplicated (set semantics), sorted by unsigned bytewise order, framed
    with :data:`SEMANTIC_ROOT_SCHEME`, and passed to the RFC 9162 Merkle Tree
    Hash construction. Caller order and human-readable handles cannot affect
    this root.
    """
    digests = sorted({_decode_sha256_digest(value) for value in pattern_hashes})
    entries = [_SEMANTIC_ROOT_DOMAIN + digest for digest in digests]
    return _merkle_tree_hash(entries).hex()


def catalog_root(bindings: Iterable[tuple[str, str]]) -> str:
    """Commit to the catalog's exact ``handle -> pattern digest`` bindings.

    Handles are canonical ASCII identifiers, sorted by their raw bytes. Each
    leaf payload contains a four-byte big-endian handle length, the handle,
    and the raw 32-byte digest, framed with :data:`CATALOG_ROOT_SCHEME`.
    Duplicate handles are rejected; two handles may intentionally bind to the
    same semantic digest.
    """
    canonical: list[tuple[bytes, bytes]] = []
    seen_handles: set[str] = set()

    for handle, pattern_hash in bindings:
        if not isinstance(handle, str) or not _HANDLE_RE.fullmatch(handle):
            raise ValueError("catalog handle must match [A-Za-z][A-Za-z0-9_-]* exactly")
        if handle in seen_handles:
            raise ValueError(f"duplicate catalog handle: {handle}")
        seen_handles.add(handle)

        handle_bytes = handle.encode("ascii")
        digest = _decode_sha256_digest(pattern_hash, label=f"hash for {handle}")
        canonical.append((handle_bytes, digest))

    canonical.sort(key=lambda item: item[0])
    entries = [
        _CATALOG_ROOT_DOMAIN + len(handle_bytes).to_bytes(4, "big") + handle_bytes + digest
        for handle_bytes, digest in canonical
    ]
    return _merkle_tree_hash(entries).hex()


def vocabulary_roots(bindings: Iterable[tuple[str, str]]) -> dict[str, Any]:
    """Return both aggregate commitments for a catalog snapshot."""
    materialized = list(bindings)
    hashes = [pattern_hash for _, pattern_hash in materialized]
    unique_hashes = {_decode_sha256_digest(value) for value in hashes}
    semantic = vocabulary_root(hashes)
    catalog = catalog_root(materialized)
    return {
        "hash": semantic,
        "stub": semantic[:16],
        "root_scheme": SEMANTIC_ROOT_SCHEME,
        "semantic_root": semantic,
        "semantic_root_stub": semantic[:16],
        "semantic_root_scheme": SEMANTIC_ROOT_SCHEME,
        "catalog_root": catalog,
        "catalog_root_stub": catalog[:16],
        "catalog_root_scheme": CATALOG_ROOT_SCHEME,
        "pattern_count": len(materialized),
        "definition_count": len(unique_hashes),
    }


def vocabulary_info(db_path: str) -> dict:
    """Read a taxonomy.db and return a load-line-sized state fingerprint.

    Returns:
        {
            "root": "sha256-hex-string",         # semantic-set root
            "root_scheme": "sema-semantic-set-v1",
            "catalog_root": "sha256-hex-string",
            "catalog_root_scheme": "sema-catalog-v1",
            "pattern_count": int,
            "definition_count": int,
            "db_path": str,
            "stamped_version": str | None,        # placeholder for future version-stamping
        }

    The semantic root compares definition sets; the catalog root compares
    handle bindings. Both are independent of insertion order and SQLite
    layout. Any malformed pattern row aborts the fingerprint.
    """
    import json
    import sqlite3

    con = sqlite3.connect(db_path)
    try:
        rows = con.execute("SELECT text, metadata FROM nodes WHERE node_type='PATTERN'").fetchall()
    finally:
        con.close()

    bindings = []
    for text, meta_json in rows:
        if not meta_json:
            raise ValueError(f"pattern {text!r} has no metadata")
        try:
            meta = json.loads(meta_json)
        except json.JSONDecodeError as exc:
            raise ValueError(f"pattern {text!r} has invalid metadata JSON") from exc
        sema_id = meta.get("pattern", {}).get("sema_id")
        try:
            pattern_hash = pattern_hash_from_sema_id(sema_id, expected_handle=text)
        except ValueError as exc:
            raise ValueError(f"pattern {text!r} has an invalid sema_id: {exc}") from exc
        bindings.append((text, pattern_hash))

    roots = vocabulary_roots(bindings)
    return {
        "root": roots["semantic_root"],
        "hash": roots["semantic_root"],
        "stub": roots["semantic_root_stub"],
        "root_scheme": roots["semantic_root_scheme"],
        "semantic_root": roots["semantic_root"],
        "semantic_root_stub": roots["semantic_root_stub"],
        "semantic_root_scheme": roots["semantic_root_scheme"],
        "catalog_root": roots["catalog_root"],
        "catalog_root_stub": roots["catalog_root_stub"],
        "catalog_root_scheme": roots["catalog_root_scheme"],
        "pattern_count": roots["pattern_count"],
        "definition_count": roots["definition_count"],
        "db_path": db_path,
        "stamped_version": None,
    }


def format_load_line(info: dict) -> str:
    """Banner for a vocabulary DB. Two lines — full root first (verifiable),
    context below (scannable).

    Example:
        📚 sema:vocab#mh:SHA-256:<64-character-root>
           N patterns, sema-semantic-set-v1 (path/to/taxonomy.db)

    When a stamped version becomes available, it's appended inline to the
    second line without disturbing the root:
        📚 sema:vocab#mh:SHA-256:<64-character-root>
           N patterns, v0.4.0, sema-semantic-set-v1 (path/to/taxonomy.db)
    """
    root = info.get("root", "") or "unknown"
    count = info.get("pattern_count", 0)
    db = info.get("db_path", "?")
    version = info.get("stamped_version")
    scheme = info.get("root_scheme")
    second = f"{count} patterns"
    if version:
        second += f", v{version}"
    if scheme:
        second += f", {scheme}"
    second += f" ({db})"
    return f"📚 sema:vocab#mh:SHA-256:{root}\n   {second}"
