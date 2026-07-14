# Hosted Workspaces MVP

This is the proposed path for a multi-tenant Sema product where teams own their
graphs in GitHub and Sema hosts the viewing, validation, publishing, and MCP
connection layer.

## Product Model

- **GitHub remains the source of truth.** A workspace maps to a GitHub
  owner/repo/ref containing Sema pattern JSON and generated graph artifacts.
- **Sema hosts a materialized read model.** The hosted service can build or
  refresh a database for each workspace/ref and serve graph reads from that DB.
- **Writes happen through pull requests.** Pattern creation and edits should
  create GitHub branches/commits/PRs, not directly mutate a hosted production DB.
- **Publishing is explicit.** A merge, tag, release, or publish action produces a
  stable vocabulary root that agents can handshake against.
- **Hosted MCP is tenant-scoped.** MCP tools must be bound to one workspace and
  authorization context. Read tools can expose published graphs; write tools
  should create PRs.

## Current Foundation

The first code step is `sema.core.workspace.GraphWorkspace`, followed by the
in-process `WorkspaceCatalog` boundary.

It wraps a registry plus workspace identity so API and MCP code can ask:

```text
workspace/repo/ref -> registry -> search/resolve/validate/root/handshake
```

instead of reaching for a process-wide registry singleton. The local MCP server
still runs as one active workspace for compatibility, but the read and validation
operations now have a tenant-safe service boundary to move behind hosted routing.

The existing HTTP server exposes:

```text
GET /api/workspace
```

which returns the active workspace identity, read-only flag, pattern count, and
vocabulary root.

Registered workspaces also have tenant-scoped, read-only routes:

```text
GET /api/workspaces/{workspace_id}
GET /api/workspaces/{workspace_id}/search?q=...
GET /api/workspaces/{workspace_id}/patterns/{handle}
GET /api/workspaces/{workspace_id}/resolve/{handle}
GET /api/workspaces/{workspace_id}/root
```

The deployed process currently registers only its local default workspace. The
catalog deliberately does not list workspace IDs or expose materialized DB
paths. A persistent adapter will populate it with authorized, published
workspace sources.

## Next Steps

1. Back the workspace catalog with Supabase records that resolve
   `{workspace_id}` to a GitHub installation/repo/ref and materialized DB path.
2. Add authorization and visibility checks before registering private sources.
3. Add GitHub App authentication and installation selection.
4. Add import/sync: clone or fetch a repo ref, validate pattern JSON, and build a
   workspace DB.
5. Add publish metadata: root hash, pattern count, source commit SHA, generated
   at timestamp.
6. Add read-only hosted MCP bound to a workspace.
7. Add PR-backed write operations: propose pattern/edit -> branch -> commit -> PR.

## Deployment Notes

The repo already has Railway-compatible deployment files (`railway.json`,
`Dockerfile`, `Dockerfile.web`). Scaling the hosted process is plausible once the
workspace boundary is real, but deployment should wait until tenant state is not
held in process-wide globals.
