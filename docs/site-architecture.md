# Site architecture (APPROVED — build against this, do not re-propose)

Principle: agents build, humans watch/curate. List pages help choose;
detail pages help understand; the connect page helps act. One page, one job.

| Route | Job | Contents |
|---|---|---|
| `/` | Orient + route | One-sentence claim, ONE proof element (handshake demo), two buttons: Browse vocabularies / Connect my agent. Nothing else. |
| `/registry` | Choose a vocabulary | Search, filters, vocabulary cards (owner, description, pattern count, verified root). |
| `/vocabularies/:slug` | Understand one vocabulary | About, owner, root/version, license, connect instructions, searchable pattern list. |
| `/vocabularies/:slug/patterns/:handle` | Understand one pattern | Gloss, mechanism, invariants, parameters, pre/post, failure modes, deps, full hash. Graph-centrality counts live here as technical metadata, nowhere else. |
| `/connect` | Act | Renders install.md (single source), client-specific MCP setup, blind-agent prompt, handshake verification. |
| `/dashboard` | Private: observe + curate | Login required. Your vocabularies, drafts, agent activity, publish controls. |
| `/docs`, paper | Deep understanding | Unchanged content, design-system styling. |

Naming: Registry / Vocabulary / Pattern / Dashboard. "Workspace" is
internal-only — remove from public nav; `/workspace` becomes `/registry`.
"Sema Bootstrap" needs Henrik's naming confirmation before public use.

No invented rankings: no toplists until a real, labelled usage metric
exists (e.g. unique agents resolving a pattern in 30 days). Bundled
commons = first registry entry, not the homepage.

Implementation order: (1) remove toplist, homepage → two-path front
door; (2) vocabulary + pattern detail pages; (3) /connect; (4)
/dashboard when multi-tenant backend lands. All on `site/rebuild`,
no PRs until Henrik approves on the tryout service.
