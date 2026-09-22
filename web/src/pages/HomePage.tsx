import { useMemo, useState } from 'react'
import type { MetaFunction } from 'react-router'
import { Link } from 'react-router-dom'
import { ArrowRight, Check, Copy, ExternalLink, Network } from 'lucide-react'
import { DbSwitcher } from '@/components/DbSwitcher'
import { LicenseLine } from '@/components/LicenseLine'
import { LocalLibraries } from '@/components/LocalLibraries'
import { LocalHeader } from '@/components/LocalHeader'
import { PatternBrowser } from '@/components/PatternBrowser'
import { SemaLogo } from '@/components/SemaLogo'
import { useActiveDb, useDbs, useIsLocal, usePatterns, useWorkspace } from '@/hooks/useApi'
import { useLiveStore } from '@/hooks/useLiveAdditions'
import { LAYER_COLORS } from '@/types/taxonomy'
import { cn } from '@/lib/utils'

export const meta: MetaFunction = () => [
  { title: 'Sema — Local view' },
  {
    name: 'description',
    content: 'Watch an agent build a Sema vocabulary on this computer, then publish it if you want to.',
  },
]

const KICKOFF_PROMPT =
  'Use the Sema tools to help me build a vocabulary. First call sema_use with no arguments ' +
  'and report which vocabulary is active and whether it is bundled/read-only. Search existing ' +
  'patterns before proposing new ones. Draft and validate each new pattern, and wait for my ' +
  'approval before calling sema_mint.'

function slugify(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'my-vocabulary'
}

function useCopy() {
  const [copied, setCopied] = useState<string | null>(null)
  const copy = async (key: string, text: string) => {
    await navigator.clipboard.writeText(text)
    setCopied(key)
    setTimeout(() => setCopied((current) => (current === key ? null : current)), 1600)
  }
  return { copied, copy }
}

function CommandBlock({ id, command, copied, copy }: {
  id: string
  command: string
  copied: string | null
  copy: (key: string, text: string) => Promise<void>
}) {
  return (
    <div className="group relative mt-3">
      <pre className="ref-mono overflow-x-auto rounded-lg border border-zinc-800 bg-zinc-950/80 p-3 pr-12 text-xs leading-5 text-zinc-300">
        {command}
      </pre>
      <button
        type="button"
        onClick={() => void copy(id, command)}
        aria-label="Copy command"
        className="absolute right-2 top-2 rounded-md border border-zinc-800 bg-zinc-900 p-1.5 text-zinc-400 transition-colors hover:border-zinc-700 hover:text-zinc-100"
      >
        {copied === id ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
      </button>
    </div>
  )
}

export function HomePage() {
  const isLocal = useIsLocal()
  const activeDb = useActiveDb()
  const { data: dbs } = useDbs()
  const canSwitch = (dbs?.databases?.length ?? 0) >= 2
  const { data: workspace } = useWorkspace()
  const { data: patterns, error } = usePatterns()
  // The page is prerendered without data. Treat "no data yet" as loading so
  // the first client render matches the prerendered markup.
  const isLoading = patterns === undefined && !error
  const arrivals = useLiveStore((state) => state.arrivals)
  const arrivedIds = useMemo(() => new Set(arrivals.map((arrival) => arrival.id)), [arrivals])
  const { copied, copy } = useCopy()

  const bootstrap = Boolean(activeDb?.bundled)
  const readOnly = Boolean(activeDb?.read_only)
  const installed = activeDb?.kind === 'installed-library'
  const name = !activeDb
    ? (workspace?.label ?? 'Vocabulary')
    : bootstrap
      ? 'Sema bootstrap'
      : activeDb.name
  const slug = slugify(bootstrap || !activeDb ? 'my-vocabulary' : activeDb.name)
  const dbPath = activeDb?.path ?? workspace?.db_path ?? ''
  const patternCount = patterns?.length ?? workspace?.pattern_count

  const description = bootstrap
    ? 'The shared starting vocabulary that ships with Sema. It is read-only, so build your own vocabulary to add patterns.'
    : installed
      ? 'A library installed from its published release. It is read-only here; its author publishes updates.'
      : isLocal
        ? 'A writable vocabulary on this computer. Patterns your agent mints appear here and in the graph as they land.'
        : 'The vocabulary this Sema server has open.'

  const packageCommand =
    `sema package '${dbPath || `${slug}.db`}' \\\n` +
    `  --name ${slug} \\\n` +
    '  --version 0.1.0 \\\n' +
    `  --output-dir dist/${slug}-0.1.0 \\\n` +
    `  --github-repo USER/${slug}`
  const releaseCommand =
    `gh release create v0.1.0 dist/${slug}-0.1.0/* \\\n` +
    `  --repo USER/${slug} --title "${slug} 0.1.0" --generate-notes --latest`
  const importCommand =
    'sema login\n' +
    `sema registry import 'https://github.com/USER/${slug}/releases/latest/download/library.json'`

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <LocalHeader />

      <section className="relative overflow-hidden border-b border-zinc-800/50">
        <div className="absolute left-1/2 top-0 h-[360px] w-[900px] -translate-x-1/2 rounded-full bg-emerald-900/10 blur-3xl" />
        <div className="relative mx-auto max-w-[1400px] px-4 py-10 sm:px-6 sm:py-14">
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-emerald-400">
            {isLocal ? 'Open on this computer' : 'Open vocabulary'}
          </p>
          <div className="mt-4 flex flex-wrap items-start justify-between gap-8">
            <div className="flex min-w-0 items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500/20 to-emerald-500/5 text-emerald-400 ring-1 ring-inset ring-emerald-500/20">
                <SemaLogo className="h-7 w-7" />
              </div>
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-3">
                  <h1 className="text-3xl font-light tracking-tight text-zinc-50 sm:text-4xl">{name}</h1>
                  {activeDb ? (
                    <span
                      className={cn(
                        'rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset',
                        readOnly
                          ? 'bg-zinc-800/70 text-zinc-300 ring-zinc-700'
                          : 'bg-emerald-400/10 text-emerald-300 ring-emerald-400/25',
                      )}
                    >
                      {readOnly ? 'Read-only' : 'Writable'}
                    </span>
                  ) : null}
                  {isLocal ? (
                    <span className="inline-flex items-center gap-1.5 text-xs text-zinc-400" title="Checks for new patterns every few seconds">
                      <span className="live-dot h-1.5 w-1.5 rounded-full bg-emerald-400" aria-hidden="true" />
                      Live
                    </span>
                  ) : null}
                </div>
                <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-400">{description}</p>
                {dbPath ? (
                  <p className="ref-mono mt-2 max-w-2xl truncate text-xs text-zinc-600" title={dbPath}>
                    {dbPath}
                  </p>
                ) : null}
              </div>
            </div>

            <div className="flex flex-col items-start gap-4 lg:items-end">
              <div className="flex flex-wrap items-center gap-2">
                <Link
                  to="/graph"
                  className="inline-flex items-center gap-2 rounded-lg bg-emerald-400 px-4 py-2.5 text-sm font-medium text-zinc-950 transition-colors hover:bg-emerald-300"
                >
                  <Network className="h-4 w-4" aria-hidden="true" />
                  Watch it grow in 3D
                  <ArrowRight className="h-4 w-4" aria-hidden="true" />
                </Link>
                {canSwitch ? (
                  <span className="rounded-lg border border-zinc-800 bg-zinc-900/60 px-1.5 py-1">
                    <DbSwitcher />
                  </span>
                ) : null}
                {isLocal ? (
                  <a
                    href="#on-this-computer"
                    className="rounded-lg px-2 py-2 text-sm text-zinc-400 transition-colors hover:text-zinc-100"
                  >
                    On this computer
                  </a>
                ) : null}
              </div>
              <dl className="ref-mono flex flex-wrap gap-6 text-sm sm:gap-8">
                <div>
                  <dt className="text-zinc-500">Patterns</dt>
                  <dd className="mt-1 text-zinc-200">{patternCount ?? '…'}</dd>
                </div>
                <div>
                  <dt className="text-zinc-500">Root</dt>
                  <dd className="mt-1 text-emerald-400/90">
                    {workspace?.vocabulary_root_stub ? `${workspace.vocabulary_root_stub}…` : '…'}
                  </dd>
                </div>
              </dl>
            </div>
          </div>

          {arrivals.length > 0 ? (
            <div className="mt-8 flex flex-wrap items-center gap-2" aria-live="polite">
              <span className="text-xs text-zinc-500">Added while this page is open:</span>
              {arrivals.slice(0, 8).map((arrival) => (
                <Link
                  key={arrival.id}
                  to={`/graph?node=${encodeURIComponent(arrival.id)}`}
                  className="inline-flex items-center gap-1.5 rounded-full border border-emerald-500/25 bg-emerald-500/[0.06] px-2.5 py-1 text-xs text-emerald-200 transition-colors hover:border-emerald-400/50"
                >
                  <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: LAYER_COLORS[arrival.layer] || '#71717a' }} />
                  {arrival.id}
                </Link>
              ))}
            </div>
          ) : null}
        </div>
      </section>

      {bootstrap ? (
        <section className="border-b border-zinc-800/50 bg-zinc-900/20">
          <div className="mx-auto grid max-w-[1400px] gap-6 px-4 py-10 sm:px-6 lg:grid-cols-2">
            <div>
              <h2 className="text-lg font-medium text-zinc-100">Build your own vocabulary</h2>
              <p className="mt-2 max-w-xl text-sm leading-6 text-zinc-400">
                Ask your agent to create a writable vocabulary, or run these commands yourself. This
                view switches to the new vocabulary on its own.
              </p>
              <CommandBlock
                id="build"
                command={'sema build my-vocabulary.db --preset empty\nsema use my-vocabulary.db'}
                copied={copied}
                copy={copy}
              />
              <p className="mt-2 text-xs text-zinc-500">
                Use <code className="ref-mono text-zinc-300">--preset full</code> to start from a copy of the bootstrap.
              </p>
            </div>
            <AgentPrompt copied={copied} copy={copy} />
          </div>
        </section>
      ) : isLocal && !readOnly ? (
        <section className="border-b border-zinc-800/50 bg-zinc-900/20">
          <div className="mx-auto max-w-[1400px] px-4 py-10 sm:px-6">
            <AgentPrompt copied={copied} copy={copy} />
          </div>
        </section>
      ) : null}

      <main className="mx-auto min-w-0 max-w-[1400px] px-4 py-10 sm:px-6">
        {isLoading ? (
          <p className="py-16 text-center text-sm text-zinc-500">Loading vocabulary…</p>
        ) : error ? (
          <div role="alert" className="rounded-xl border border-red-500/20 bg-red-500/[0.06] px-5 py-4 text-sm text-red-200">
            The vocabulary could not be loaded. Check that the Sema server is still running.
          </div>
        ) : patterns && patterns.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-zinc-700 bg-zinc-950/30 p-8 text-center">
            <p className="text-sm font-medium text-zinc-200">No patterns yet</p>
            <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-zinc-500">
              When your agent mints the first pattern, it appears here and in the 3D graph within a few seconds.
            </p>
          </div>
        ) : (
          <PatternBrowser patterns={patterns ?? []} arrivedIds={arrivedIds} />
        )}
      </main>

      {isLocal && !readOnly && !bootstrap ? (
        <section className="border-t border-zinc-800/60 bg-zinc-900/20">
          <div className="mx-auto max-w-[1400px] px-4 py-12 sm:px-6">
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-emerald-400">When it is ready</p>
            <h2 className="mt-3 text-2xl font-light tracking-tight text-zinc-50">Publish it on semahash.org, if you want to.</h2>
            <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-400">
              A vocabulary on this computer works without publishing. To share it, turn it into a library,
              put the release on GitHub, and import that release into the public registry. Your GitHub
              release stays the source. Your agent can run these steps for you.
            </p>
            <ol className="mt-8 grid gap-6 lg:grid-cols-3">
              <li className="rounded-2xl border border-zinc-800 bg-zinc-950/40 p-5">
                <p className="text-xs font-medium text-zinc-500">01</p>
                <h3 className="mt-2 text-sm font-medium text-zinc-100">Package the library</h3>
                <p className="mt-1 text-sm leading-6 text-zinc-500">Replace USER with your GitHub login.</p>
                <CommandBlock id="package" command={packageCommand} copied={copied} copy={copy} />
              </li>
              <li className="rounded-2xl border border-zinc-800 bg-zinc-950/40 p-5">
                <p className="text-xs font-medium text-zinc-500">02</p>
                <h3 className="mt-2 text-sm font-medium text-zinc-100">Publish a GitHub release</h3>
                <p className="mt-1 text-sm leading-6 text-zinc-500">Attach both files. Do not replace them later.</p>
                <CommandBlock id="release" command={releaseCommand} copied={copied} copy={copy} />
              </li>
              <li className="rounded-2xl border border-zinc-800 bg-zinc-950/40 p-5">
                <p className="text-xs font-medium text-zinc-500">03</p>
                <h3 className="mt-2 text-sm font-medium text-zinc-100">List it on semahash.org</h3>
                <p className="mt-1 text-sm leading-6 text-zinc-500">Approve the login code in your browser once.</p>
                <CommandBlock id="import" command={importCommand} copied={copied} copy={copy} />
              </li>
            </ol>
            <div className="mt-6 flex flex-wrap gap-x-6 gap-y-2 text-sm">
              <a
                href="https://semahash.org/docs#publish-library"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 text-emerald-300 transition-colors hover:text-emerald-200"
              >
                The full publishing guide
                <ExternalLink className="h-3.5 w-3.5" aria-hidden="true" />
              </a>
              <a
                href="https://semahash.org/registry"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 text-zinc-400 transition-colors hover:text-zinc-200"
              >
                Libraries others have published
                <ExternalLink className="h-3.5 w-3.5" aria-hidden="true" />
              </a>
            </div>
          </div>
        </section>
      ) : null}

      {isLocal ? <LocalLibraries /> : null}

      <footer className="border-t border-zinc-800/50">
        <div className="mx-auto flex max-w-[1400px] flex-col justify-between gap-3 px-4 py-6 text-sm text-zinc-500 sm:flex-row sm:items-center sm:px-6">
          <p>Sema local view · runs on this computer</p>
          <LicenseLine />
        </div>
      </footer>
    </div>
  )
}

function AgentPrompt({ copied, copy }: {
  copied: string | null
  copy: (key: string, text: string) => Promise<void>
}) {
  return (
    <div>
      <h2 className="text-lg font-medium text-zinc-100">Work on it with your agent</h2>
      <p className="mt-2 max-w-xl text-sm leading-6 text-zinc-400">
        Give your agent this prompt. It searches what exists, drafts each card, validates it, and mints
        only after you approve. Keep this page or the graph open to watch the patterns arrive.
      </p>
      <blockquote className="mt-3 rounded-lg border border-zinc-800 bg-zinc-950/80 p-3 text-sm leading-6 text-zinc-300">
        {KICKOFF_PROMPT}
      </blockquote>
      <button
        type="button"
        onClick={() => void copy('prompt', KICKOFF_PROMPT)}
        className="mt-3 inline-flex items-center gap-2 rounded-lg border border-zinc-700 px-3.5 py-2 text-sm text-zinc-300 transition-colors hover:border-zinc-600 hover:text-zinc-100"
      >
        {copied === 'prompt' ? <Check className="h-4 w-4 text-emerald-400" /> : <Copy className="h-4 w-4" />}
        {copied === 'prompt' ? 'Copied' : 'Copy the prompt'}
      </button>
    </div>
  )
}

export default HomePage
