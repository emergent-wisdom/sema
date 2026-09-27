import { ExternalLink, Loader2 } from 'lucide-react'
import { useDbs, useSwitchDb, type DbInfo } from '@/hooks/useApi'
import { cn } from '@/lib/utils'

// Link only to the GitHub repository a release came from, never to an
// arbitrary manifest host.
function githubRepository(url?: string): string | null {
  if (!url) return null
  try {
    const parsed = new URL(url)
    if (parsed.protocol !== 'https:' || parsed.hostname !== 'github.com') return null
    const [owner, repo] = parsed.pathname.split('/').filter(Boolean)
    return owner && repo ? `https://github.com/${owner}/${repo}` : null
  } catch {
    return null
  }
}

type Group = { key: string; title: string; body: string; items: DbInfo[] }

/**
 * Every vocabulary this computer's Sema configuration knows about: the ones
 * the person builds, the libraries they installed, and the bootstrap.
 */
export function LocalLibraries() {
  const { data } = useDbs()
  const switchDb = useSwitchDb()
  const databases = (data?.databases ?? []).filter((db) => db.exists)
  if (databases.length === 0) return null

  const groups: Group[] = [
    {
      key: 'own',
      title: 'Your vocabularies',
      body: 'Writable vocabularies you build with your agent.',
      items: databases.filter((db) => !db.bundled && db.kind !== 'installed-library'),
    },
    {
      key: 'installed',
      title: 'Installed libraries',
      body: 'Published libraries installed with sema install. They are read-only; sema update fetches a newer release.',
      items: databases.filter((db) => db.kind === 'installed-library'),
    },
    {
      key: 'bootstrap',
      title: 'Bootstrap',
      body: 'The starting vocabulary that ships with Sema.',
      items: databases.filter((db) => db.bundled),
    },
  ].filter((group) => group.items.length > 0)

  const open = (db: DbInfo) => {
    switchDb.mutate(db.bundled ? { default: true } : { path: db.path }, {
      onSuccess: () => window.scrollTo({ top: 0, behavior: 'smooth' }),
    })
  }

  return (
    <section id="on-this-computer" className="scroll-mt-20 border-t border-zinc-800/60">
      <div className="mx-auto max-w-[1400px] px-4 py-12 sm:px-6">
        <p className="text-xs font-medium uppercase tracking-[0.2em] text-emerald-400">On this computer</p>
        <h2 className="mt-3 text-2xl font-light tracking-tight text-zinc-50">Every vocabulary Sema knows about here.</h2>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-400">
          Opening one here also selects it for the CLI and your agent, the same as sema use. Nothing
          on this list leaves your computer.
        </p>
        {switchDb.isError ? (
          <p role="alert" className="mt-4 text-sm text-red-300">{String(switchDb.error)}</p>
        ) : null}

        {groups.map((group) => (
          <div key={group.key} className="mt-10">
            <div className="flex items-baseline gap-3">
              <h3 className="text-sm font-medium text-zinc-200">{group.title}</h3>
              <span className="text-xs tabular-nums text-zinc-600">{group.items.length}</span>
            </div>
            <p className="mt-1 text-xs text-zinc-500">{group.body}</p>
            <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {group.items.map((db) => (
                <LibraryItem
                  key={db.path}
                  db={db}
                  pending={switchDb.isPending && switchDb.variables?.path === db.path}
                  onOpen={() => open(db)}
                />
              ))}
            </div>
          </div>
        ))}

        {!groups.some((group) => group.key === 'installed') ? (
          <p className="mt-10 text-sm leading-6 text-zinc-500">
            No installed libraries yet. Find one on{' '}
            <a
              href="https://semahash.org/registry"
              target="_blank"
              rel="noopener noreferrer"
              className="text-emerald-300 underline decoration-emerald-500/30 underline-offset-2 hover:text-emerald-200"
            >
              semahash.org
            </a>{' '}
            and install it with <code className="ref-mono text-zinc-300">sema install &lt;library.json URL&gt;</code>.
          </p>
        ) : null}
      </div>
    </section>
  )
}

function LibraryItem({ db, pending, onOpen }: { db: DbInfo; pending: boolean; onOpen: () => void }) {
  // manifest_url is where the download finally came from, a GitHub CDN host;
  // the update and requested URLs keep the repository address.
  const repository =
    githubRepository(db.update_url) ??
    githubRepository(db.requested_manifest_url) ??
    githubRepository(db.manifest_url)
  const name = db.bundled ? 'Sema bootstrap' : db.name

  return (
    <article
      className={cn(
        'flex flex-col rounded-2xl border bg-zinc-900/40 p-5',
        db.active ? 'border-emerald-500/40' : 'border-zinc-800',
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="flex min-w-0 items-center gap-2">
            <span className="truncate font-medium text-zinc-100">{name}</span>
            {db.version ? <code className="ref-mono shrink-0 text-emerald-400/80">v{db.version}</code> : null}
          </p>
          <p className="ref-mono mt-1 truncate text-xs text-zinc-600" title={db.path}>{db.path}</p>
        </div>
        {db.active ? (
          <span className="shrink-0 rounded-full bg-emerald-400/10 px-2.5 py-1 text-xs font-medium text-emerald-300 ring-1 ring-inset ring-emerald-400/25">
            Open now
          </span>
        ) : (
          <button
            type="button"
            onClick={onOpen}
            disabled={pending}
            title="Open it here and select it for the CLI and your agent"
            className="inline-flex shrink-0 items-center gap-1.5 rounded-lg border border-zinc-700 px-3 py-1.5 text-xs text-zinc-300 transition-colors hover:border-zinc-600 hover:text-zinc-100 disabled:opacity-50"
          >
            {pending ? <Loader2 className="h-3.5 w-3.5 animate-spin" aria-hidden="true" /> : null}
            Open
          </button>
        )}
      </div>
      <dl className="ref-mono mt-4 flex flex-wrap gap-x-6 gap-y-2 text-xs">
        <div>
          <dt className="text-zinc-500">Access</dt>
          <dd className="mt-0.5 text-zinc-300">{db.read_only ? 'Read-only' : 'Writable'}</dd>
        </div>
        {typeof db.pattern_count === 'number' ? (
          <div>
            <dt className="text-zinc-500">Patterns</dt>
            <dd className="mt-0.5 text-zinc-300">{db.pattern_count}</dd>
          </div>
        ) : null}
        {db.semantic_root ? (
          <div>
            <dt className="text-zinc-500">Root</dt>
            <dd className="mt-0.5 text-emerald-400/90">{db.semantic_root.slice(0, 16)}…</dd>
          </div>
        ) : null}
      </dl>
      {repository ? (
        <a
          href={repository}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-auto inline-flex items-center gap-1.5 pt-4 text-xs text-zinc-400 transition-colors hover:text-zinc-200"
        >
          Source on GitHub
          <ExternalLink className="h-3 w-3" aria-hidden="true" />
        </a>
      ) : null}
    </article>
  )
}
