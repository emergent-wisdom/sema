import json
import os
import sqlite3
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ..client import get_default_client

# Relative Imports
from ..core.registry import RegistryManager
from ..core.utils import compact_dict

app = FastAPI(
    title="Sema API",
    description="API for Sema Knowledge Graph",
    docs_url="/api/swagger",
    redoc_url="/api/redoc",
)

# CORS: default to the known-safe set (semahash.org + local dev). Operators
# can widen via SEMA_CORS_ORIGINS=comma,separated,list or SEMA_CORS_ORIGINS=*
# when they've deliberately chosen to host a public API.
_DEFAULT_CORS_ORIGINS = [
    "https://semahash.org",
    "https://www.semahash.org",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]
_cors_env = os.environ.get("SEMA_CORS_ORIGINS", "").strip()
if _cors_env == "*":
    # Wildcard + credentials is invalid per the CORS spec (browsers ignore it).
    # Drop credentials so the wildcard actually works for the operator who
    # asked for it.
    _cors_origins: list[str] = ["*"]
    _cors_credentials = False
elif _cors_env:
    _cors_origins = [o.strip() for o in _cors_env.split(",") if o.strip()]
    _cors_credentials = True
else:
    _cors_origins = _DEFAULT_CORS_ORIGINS
    _cors_credentials = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=_cors_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


# www → apex 301 redirect.
# Only matches hosts that literally start with "www.", so Railway's
# internal health check (Host: healthcheck.railway.app) and apex
# requests pass through untouched. Hardcoding https:// is safe here:
# Railway terminates TLS at the edge and only public traffic reaches
# this process, so any www.* request originated as HTTPS.
@app.middleware("http")
async def www_to_apex_redirect(request: Request, call_next):
    host = request.headers.get("host", "")
    # Strip optional :port suffix before the prefix check
    host_no_port = host.split(":", 1)[0]
    if host_no_port.startswith("www."):
        apex = host_no_port[4:]
        path = request.url.path
        query = f"?{request.url.query}" if request.url.query else ""
        return RedirectResponse(url=f"https://{apex}{path}{query}", status_code=301)
    return await call_next(request)


# Configuration — DB discovery order:
#   1. SEMA_DB_PATH env var (explicit override)
#   2. Bundled DB next to the installed package (`sema/data/taxonomy.db` — wheel force-include)
#   3. Bundled DB in the source tree (`<repo>/data/taxonomy.db` — editable install / direct run)
#   4. Bundled DB relative to CWD (`./data/taxonomy.db` — running from repo root)
#   5. User DB via platformdirs client (may try to download)
env_db_path = os.environ.get("SEMA_DB_PATH")
if env_db_path:
    DB_PATH = env_db_path
    print(f"Using DB from ENV: {DB_PATH}")
else:
    from pathlib import Path as _Path

    import sema as _sema_pkg

    _candidate_paths = [
        _Path(_sema_pkg.__file__).parent / "data" / "taxonomy.db",
        _Path(__file__).resolve().parents[3] / "data" / "taxonomy.db",
        _Path.cwd() / "data" / "taxonomy.db",
    ]
    DB_PATH = None
    for _p in _candidate_paths:
        if _p.exists():
            DB_PATH = str(_p)
            print(f"Using bundled DB: {DB_PATH}")
            break

    if DB_PATH is None:
        # Last resort: ask the Client (which may try to download)
        try:
            client = get_default_client()
            DB_PATH = client.get_db_path()
            print(f"Using User DB: {DB_PATH}")
        except Exception as e:
            print(f"Warning: Could not initialize client DB: {e}")
            DB_PATH = "taxonomy.db"

print(f"Loading Registry with DB: {DB_PATH}")

# Registry loads from database only
registry = RegistryManager(db_path=DB_PATH)


# Models
class PatternNode(BaseModel):
    id: str
    text: str
    type: str
    layer: str | None = None
    category: str | None = None
    handle: str | None = None
    gloss: str | None = None
    metadata: dict[str, Any]


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    type: str


class GraphData(BaseModel):
    nodes: list[PatternNode]
    edges: list[GraphEdge]


@app.get("/api/graph")
def get_graph():
    """Get the full graph structure for visualization."""
    nodes = []
    edges = []

    if not os.path.exists(DB_PATH):
        return {"nodes": [], "edges": []}

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        # Get Nodes and build UUID->handle mapping
        cursor = conn.cursor()
        cursor.execute("SELECT id, node_type, text, metadata FROM nodes")
        uuid_to_id = {}  # Map UUID to our node ID

        for row in cursor.fetchall():
            meta = json.loads(row["metadata"] or "{}")
            pattern_meta = meta.get("pattern", {})

            # Apply Overlay Logic
            raw_handle = pattern_meta.get("handle") or row["text"]
            overlaid_handle = pattern_meta.get("sema_ref") or raw_handle

            # For PATTERN nodes, use the raw handle as ID (for API lookups)
            # For other nodes, use the UUID
            node_id = raw_handle if row["node_type"] == "PATTERN" and raw_handle else row["id"]
            uuid_to_id[row["id"]] = node_id

            nodes.append(
                {
                    "id": node_id,
                    "text": overlaid_handle,  # Use overlaid handle as primary text
                    "type": row["node_type"],
                    "layer": pattern_meta.get("sema_layer") or meta.get("sema_layer"),
                    "category": pattern_meta.get("sema_category") or meta.get("sema_category"),
                    "handle": overlaid_handle,
                    "gloss": pattern_meta.get("gloss"),
                    "stub": pattern_meta.get("sema_stub"),
                    "metadata": meta,
                }
            )

        # Get Edges - translate UUIDs to our node IDs
        cursor.execute("SELECT id, source_id, target_id, edge_type FROM edges")
        for row in cursor.fetchall():
            source_id = uuid_to_id.get(row["source_id"], row["source_id"])
            target_id = uuid_to_id.get(row["target_id"], row["target_id"])
            edges.append(
                {
                    "id": row["id"],
                    "source": source_id,
                    "target": target_id,
                    "type": row["edge_type"],
                }
            )

        conn.close()
    except Exception as e:
        print(f"Error reading DB: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e

    return {"nodes": nodes, "edges": edges}


@app.get("/api/patterns")
def list_patterns(category: str | None = None, layer: str | None = None, q: str | None = None):
    """List all patterns, optionally filtered or searched."""
    registry.refresh()

    # If search query provided, use search
    if q:
        return registry.search(q)

    results = []
    for handle, raw_data in registry.registry.items():
        if category and raw_data.get("sema_category") != category:
            continue
        if layer and raw_data.get("sema_layer") != layer:
            continue

        # Get resolved pattern data (templates converted to overlay format)
        data = registry.get_pattern(handle) or raw_data

        # Use Overlay Handle
        overlaid_handle = data.get("sema_ref", handle)

        results.append(
            {
                "id": handle,
                "handle": overlaid_handle,
                "gloss": data.get("gloss", ""),
                "mechanism": data.get("mechanism", ""),
                "invariants": data.get("invariants", []),
                "parameters": data.get("parameters", {}),
                "hash": data.get("sema_id", ""),
                "stub": data.get("sema_stub", ""),
                "category": data.get("sema_category", ""),
                "layer": data.get("sema_layer", ""),
                "signature": data.get("signature", []),
                "preconditions": data.get("preconditions", []),
                "postconditions": data.get("postconditions", []),
                "failureModes": data.get("failureModes", []),
                "dependencies": data.get("dependencies", {}),
            }
        )
    return results


@app.get("/api/patterns/{handle}")
def get_pattern_details(handle: str):
    """Get full details for a pattern (with templates resolved)."""
    # handle might be "Vote" or "Vote#1234" or a UUID
    # Registry keys are "Vote". Strip hash if present for lookup.
    lookup_key = handle.split("#")[0]

    # First try direct lookup
    data = registry.get_pattern(lookup_key)

    # If not found, it might be a UUID - search for it
    if not data:
        # Check if handle looks like a UUID
        registry.refresh()
        for h, d in registry.registry.items():
            if d.get("id") == handle or h == handle:
                data = d
                lookup_key = h
                break

    if not data:
        raise HTTPException(status_code=404, detail="Pattern not found")

    # Transform to frontend expected format
    overlaid_handle = data.get("sema_ref", lookup_key)
    meta = data.get("_meta", {})

    # Get related patterns from dependencies and _meta.related
    related_patterns = []
    seen_handles = set()

    # From dependencies (references, composes_with, etc.)
    # Dependencies are already in overlay format: {'chain': 'Chain#3abd', ...}
    dependencies = data.get("dependencies", {})
    for rel_type, targets in dependencies.items():
        if isinstance(targets, dict):
            for _name, overlay_ref in targets.items():
                # Extract handle from overlay format: "Chain#3abd" -> "Chain"
                target_handle = overlay_ref.split("#")[0] if isinstance(overlay_ref, str) else None
                if target_handle and target_handle not in seen_handles:
                    seen_handles.add(target_handle)
                    target_data = registry.get_pattern(target_handle)
                    if target_data:
                        related_patterns.append(
                            {
                                "id": target_handle,
                                "handle": target_data.get("sema_ref", target_handle),
                                "gloss": target_data.get("gloss", ""),
                                "stub": target_data.get("sema_stub", ""),
                                "layer": target_data.get("sema_layer", ""),
                                "category": target_data.get("sema_category", ""),
                                "relation": rel_type,
                            }
                        )

    # From _meta.related list (also in overlay format: ["ProgramOfThought#6af2", ...])
    meta_related = meta.get("related", [])
    for overlay_ref in meta_related:
        target_handle = overlay_ref.split("#")[0] if isinstance(overlay_ref, str) else None
        if target_handle and target_handle not in seen_handles:
            seen_handles.add(target_handle)
            target_data = registry.get_pattern(target_handle)
            if target_data:
                related_patterns.append(
                    {
                        "id": target_handle,
                        "handle": target_data.get("sema_ref", target_handle),
                        "gloss": target_data.get("gloss", ""),
                        "stub": target_data.get("sema_stub", ""),
                        "layer": target_data.get("sema_layer", ""),
                        "category": target_data.get("sema_category", ""),
                        "relation": "related",
                    }
                )

    result = {
        "id": lookup_key,
        "handle": overlaid_handle,
        "gloss": data.get("gloss", ""),
        "mechanism": data.get("mechanism", ""),
        "invariants": data.get("invariants", []),
        "parameters": data.get("parameters", {}),
        "hash": data.get("sema_id", ""),
        "stub": data.get("sema_stub", ""),
        "layer": data.get("sema_layer", ""),
        "category": data.get("sema_category", ""),
        "signature": data.get("signature", []),
        "preconditions": data.get("preconditions", []),
        "postconditions": data.get("postconditions", []),
        "failureModes": data.get("failureModes", []),
        "dataSchema": data.get("data_schema"),
        "meta": {
            "tier": meta.get("tier"),
            "ring": meta.get("ring"),
            "layer": data.get("sema_layer"),
            "category": data.get("sema_category"),
            "caution": meta.get("caution"),
        },
        "relatedPatterns": related_patterns,
        "dependencies": data.get("dependencies", {}),
    }

    return compact_dict(result)


@app.get("/api/search")
def search_patterns(q: str, semantic: bool = True):
    """Search patterns (Hybrid: Keyword + Semantic if available)."""
    # 1. Keyword search (always)
    keyword_results = registry.search(q)

    if not semantic:
        return keyword_results

    # 2. Semantic search (optional)
    try:
        # Import dynamically to avoid heavy dep requirement unless used
        pass
    except Exception:
        pass

    # 3. Merge results with name-match boosting
    merged = {}
    query_lower = q.lower().strip()

    def calculate_name_boost(handle: str) -> float:
        import re

        name = handle.split("#")[0].lower()
        if name == query_lower:
            return 3.0
        if name.startswith(query_lower):
            return 2.5
        if query_lower in name:
            return 2.0
        name_words = [w.lower() for w in re.findall(r"[A-Z][a-z]*", handle.split("#")[0])]
        query_words = query_lower.split()
        if any(
            qw in name_words or any(nw.startswith(qw) for nw in name_words) for qw in query_words
        ):
            return 1.5
        return 0.0

    for r in keyword_results:
        h = r["handle"]
        r["source"] = "keyword"
        name_boost = calculate_name_boost(h)
        r["score"] = 1.0 + name_boost
        merged[h] = r

    results = sorted(merged.values(), key=lambda x: x.get("score", 0), reverse=True)
    return results


@app.get("/api/patterns/by-category/{category}")
def get_patterns_by_category(category: str):
    """Get all patterns in a category."""
    registry.refresh()
    results = []
    for handle, data in registry.registry.items():
        if data.get("sema_category") == category:
            overlaid_handle = data.get("sema_ref", handle)
            results.append(
                {
                    "id": handle,
                    "handle": overlaid_handle,
                    "gloss": data.get("gloss", ""),
                    "stub": data.get("sema_stub", ""),
                    "category": data.get("sema_category", ""),
                    "layer": data.get("sema_layer", ""),
                }
            )
    return results


@app.get("/api/patterns/by-layer/{layer}")
def get_patterns_by_layer(layer: str):
    """Get all patterns in a layer."""
    registry.refresh()
    results = []
    for handle, data in registry.registry.items():
        if data.get("sema_layer") == layer:
            overlaid_handle = data.get("sema_ref", handle)
            results.append(
                {
                    "id": handle,
                    "handle": overlaid_handle,
                    "gloss": data.get("gloss", ""),
                    "stub": data.get("sema_stub", ""),
                    "category": data.get("sema_category", ""),
                    "layer": data.get("sema_layer", ""),
                }
            )
    return results


@app.get("/api/patterns/{handle}/source")
def get_pattern_source(handle: str):
    """Get the canonical source for a pattern from the database."""
    lookup_key = handle.split("#")[0]
    data = registry.get_pattern(lookup_key)

    if not data:
        raise HTTPException(status_code=404, detail="Pattern not found")

    return data


# --- Documentation API ---
DOCS_ORDER = [
    # --- ORIENTATION ---
    ("guides/getting-started", "Getting Started"),
    ("README", "Overview"),
    ("core/philosophy", "Core Philosophy"),
    # --- THE PATTERN CARD ---
    ("specification/schema", "The Pattern Card"),
    ("specification/naming", "Naming Taxonomy"),
    # --- GUIDES ---
    ("guides/authoring", "Pattern Authoring Guide"),
    ("tools/cli", "CLI Reference"),
    # --- INTEGRATIONS ---
    ("guides/understanding-graph", "Using with Understanding Graph"),
    # Full specification (validation rules, versioning, etc.) at
    # https://github.com/emergent-wisdom/sema/tree/main/docs/specification
]


def _get_repo_root() -> Path | None:
    """Find the repo root (parent of docs/ and integrations/)."""
    # Try relative to __file__ (editable install / running from src)
    d = Path(__file__).resolve().parent.parent.parent.parent
    if (d / "docs").exists():
        return d
    # Fallback: CWD (installed package, uvicorn from repo root)
    d = Path.cwd()
    if (d / "docs").exists():
        return d
    return None


def _get_docs_dir() -> Path | None:
    root = _get_repo_root()
    return root / "docs" if root else None


def _get_doc_path(slug: str) -> Path | None:
    root = _get_repo_root()
    if not root:
        return None

    # Try docs/ first, then repo root (for integrations/ etc.)
    for base in [root / "docs", root]:
        path = base / f"{slug}.md"
        if path.exists():
            return path

    return None


@app.get("/api/docs")
def list_docs():
    docs_dir = _get_docs_dir()
    if not docs_dir:
        return []

    docs = []
    for slug, default_title in DOCS_ORDER:
        doc_path = _get_doc_path(slug)
        if doc_path and doc_path.exists():
            with open(doc_path) as file:
                first_line = file.readline().strip()
                title = (
                    first_line.lstrip("#").strip() if first_line.startswith("#") else default_title
                )

            docs.append(
                {
                    "slug": slug.replace("/", "__"),
                    "title": title,
                    "filename": doc_path.name,
                    "path": slug,
                }
            )
    return docs


@app.get("/api/docs/{slug:path}")
def get_doc(slug: str):
    path_slug = slug.replace("__", "/")
    doc_path = _get_doc_path(path_slug)

    if not doc_path:
        raise HTTPException(status_code=404, detail="Document not found")

    with open(doc_path) as f:
        content = f.read()

    lines = content.split("\n")
    title = lines[0].lstrip("#").strip() if lines and lines[0].startswith("#") else slug

    return {
        "slug": slug,
        "title": title,
        "content": content,
    }


# ── Paper ──────────────────────────────────────────────────────────────────────


@app.get("/api/paper")
def get_paper():
    from fastapi.responses import FileResponse

    # Look for paper PDF relative to repo root
    paper_path = Path(__file__).resolve().parent.parent.parent.parent / "paper" / "sema.pdf"
    if not paper_path.exists():
        paper_path = Path.cwd() / "paper" / "sema.pdf"
    if paper_path.exists():
        return FileResponse(paper_path, media_type="application/pdf", filename="sema.pdf")
    return JSONResponse({"error": "Paper not found"}, status_code=404)


# ── Install Guide ──────────────────────────────────────────────────────────────


@app.get("/install.md")
def get_install_md():
    from fastapi.responses import PlainTextResponse

    root = _get_repo_root()
    if root and (root / "install.md").exists():
        return PlainTextResponse((root / "install.md").read_text(), media_type="text/markdown")
    cwd = Path.cwd() / "install.md"
    if cwd.exists():
        return PlainTextResponse(cwd.read_text(), media_type="text/markdown")
    raise HTTPException(status_code=404, detail="install.md not found")


# ── DB Management ──────────────────────────────────────────────────────────────


def _is_local_server() -> bool:
    """True when running locally (not deployed to production)."""
    # Production sets RAILWAY_ENVIRONMENT; local does not.
    return not os.environ.get("RAILWAY_ENVIRONMENT") and not os.environ.get("PRODUCTION")


@app.get("/api/dbs")
def get_dbs():
    """List all known vocabulary databases. Local-only."""
    if not _is_local_server():
        raise HTTPException(status_code=404, detail="DB management is local-only")

    from ..core.registry import list_dbs

    dbs = list_dbs()
    for db in dbs:
        db["active"] = db["path"] == DB_PATH
    return {"current": DB_PATH, "databases": dbs, "local": True}


@app.post("/api/use")
def use_db_endpoint(payload: dict):
    """Switch the active database for this server process. Local-only."""
    if not _is_local_server():
        raise HTTPException(status_code=404, detail="DB management is local-only")

    from ..core.registry import is_bundled_db, register_db, set_active_db

    global DB_PATH, registry

    target = payload.get("path")
    use_default = payload.get("default", False)

    if use_default:
        from ..core.registry import get_bundled_db_path

        bundled = get_bundled_db_path()
        if not bundled:
            raise HTTPException(status_code=500, detail="Bundled DB not found")
        DB_PATH = bundled
        registry = RegistryManager(db_path=bundled)
        set_active_db(None)
        count = len(registry.registry)
        return {"success": True, "db_path": bundled, "total_patterns": count}

    if not target:
        raise HTTPException(status_code=400, detail="Missing 'path' or 'default' field")

    resolved = Path(target).expanduser().resolve()
    if not resolved.exists():
        raise HTTPException(status_code=404, detail=f"Database not found: {resolved}")
    if is_bundled_db(str(resolved)):
        raise HTTPException(
            status_code=400,
            detail="Cannot use the bundled DB as active — it gets overwritten on upgrade.",
        )

    DB_PATH = str(resolved)
    registry = RegistryManager(db_path=str(resolved))
    set_active_db(str(resolved))
    register_db(str(resolved))
    count = len(registry.registry)
    return {"success": True, "db_path": str(resolved), "total_patterns": count}


# ── MCP Registry ───────────────────────────────────────────────────────────────
# Serve server.json at /.well-known/mcp/server.json per the 2026 MCP Registry
# discovery convention (registry.modelcontextprotocol.io). Also available at
# /server.json for convenience.


def _find_server_json() -> Path | None:
    """Locate server.json in the repo root (editable install) or CWD (deployed)."""
    root = _get_repo_root()
    if root and (root / "server.json").exists():
        return root / "server.json"
    cwd_candidate = Path.cwd() / "server.json"
    if cwd_candidate.exists():
        return cwd_candidate
    return None


@app.get("/.well-known/mcp/server.json")
def get_well_known_server_json():
    from fastapi.responses import FileResponse

    path = _find_server_json()
    if path is None:
        raise HTTPException(status_code=404, detail="server.json not found")
    return FileResponse(path, media_type="application/json")


@app.get("/server.json")
def get_server_json():
    return get_well_known_server_json()


# ── Static Frontend ───────────────────────────────────────────────────────────
# Serve the built semahash-web frontend if available.
# This enables `sema serve` to provide both API and UI at localhost:3000.

_static_dir = Path(__file__).parent / "static"
if _static_dir.exists() and (_static_dir / "index.html").exists():
    from fastapi.responses import FileResponse

    # Mount static assets (js, css, etc.)
    _assets_dir = _static_dir / "assets"
    if _assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(_assets_dir)), name="assets")

    # SPA catch-all: any non-API path serves index.html
    @app.get("/{path:path}")
    def serve_spa(path: str):
        if path.startswith("api/"):
            raise HTTPException(status_code=404)
        file_path = _static_dir / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(_static_dir / "index.html")
