import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ArrowLeft, Bot, Check, ChevronDown, Copy, Network, Search, ShieldCheck } from 'lucide-react'
import { usePatterns } from '@/hooks/useApi'
import type { Pattern } from '@/types/taxonomy'
import { SemaLogo } from '@/components/SemaLogo'
import { LicenseLine } from '@/components/LicenseLine'
import { cn } from '@/lib/utils'

/**
 * One vocabulary, understood and browsable (site-architecture pass 2).
 * Every pattern card opens to show what the pattern actually says —
 * gloss, mechanism, invariants — not just a handle and a copy button.
 */
type WorkspaceSummary = {
  label?: string
  pattern_count?: number
  vocabulary_root_stub?: string
}

export function VocabularyPage() {
  const { slug = 'bootstrap' } = useParams()
  const { data: patterns = [], isLoading } = usePatterns()
  const [query, setQuery] = useState('')
  const [summary, setSummary] = useState<WorkspaceSummary | null>(null)

  // One template for every vocabulary: header facts come from the API.
  // Today only the default workspace exists; when multi-tenant lands,
  // this becomes /api/workspaces/{slug} + tenant-scoped pattern reads.
  useEffect(() => {
    let active = true
    fetch('/api/workspace')
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => { if (active) setSummary(d) })
      .catch(() => { if (active) setSummary(null) })
    return () => { active = false }
  }, [slug])

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (q.length < 2) return patterns
    return patterns.filter(
      (p) =>
        p.id.toLowerCase().includes(q) ||
        p.gloss?.toLowerCase().includes(q) ||
        p.mechanism?.toLowerCase().includes(q) ||
        p.category?.toLowerCase().includes(q)
    )
  }, [patterns, query])

  const byCategory = useMemo(() => {
    const map = new Map<string, Pattern[]>()
    for (const p of filtered) {
      const cat = p.category || 'Uncategorized'
      map.set(cat, [...(map.get(cat) ?? []), p])
    }
    return [...map.entries()].sort(([a], [b]) => a.localeCompare(b))
  }, [filtered])

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <header className="sticky top-0 z-40 border-b border-zinc-800/60 bg-zinc-950/85 backdrop-blur-xl">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-3">
          <Link to="/registry" className="inline-flex items-center gap-2 text-sm text-zinc-400 transition-colors hover:text-zinc-100">
            <ArrowLeft className="h-4 w-4" />
            Registry
          </Link>
          <div className="flex items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900/80 px-3 py-2 w-full max-w-sm">
            <Search className="h-4 w-4 shrink-0 text-zinc-500" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search this vocabulary…"
              className="w-full bg-transparent text-sm outline-none placeholder:text-zinc-600"
            />
          </div>
          <Link
            to="/connect"
            className="hidden sm:inline-flex items-center gap-2 rounded-lg bg-emerald-400/10 px-3 py-2 text-sm font-medium text-emerald-300 ring-1 ring-inset ring-emerald-400/25 transition-colors hover:bg-emerald-400/15"
          >
            <Bot className="h-4 w-4" />
            Connect agent
          </Link>
        </div>
      </header>

      <section className="border-b border-zinc-800/50">
        <div className="mx-auto max-w-6xl px-6 py-10">
          <div className="flex flex-wrap items-start justify-between gap-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500/20 to-emerald-500/5 ring-1 ring-inset ring-emerald-500/20 text-emerald-400">
                <SemaLogo className="h-7 w-7" />
              </div>
              <div>
                <div className="flex items-center gap-3">
                  <h1 className="text-2xl font-medium tracking-tight">{slug === 'bootstrap' ? 'Sema Bootstrap' : (summary?.label ?? slug)}</h1>
                  <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-2.5 py-1 text-[11px] font-medium text-emerald-300">
                    <ShieldCheck className="h-3.5 w-3.5" />
                    Public &amp; verified
                  </span>
                </div>
                <p className="mt-1 max-w-xl text-sm leading-6 text-zinc-400">
                  {slug === 'bootstrap'
                    ? 'The shared starting vocabulary for agent reasoning, coordination, verification, and infrastructure.'
                    : 'A published Sema vocabulary.'}
                </p>
              </div>
            </div>
            <dl className="ref-mono flex gap-8 text-sm">
              <div>
                <dt className="text-zinc-500">Patterns</dt>
                <dd className="mt-1 text-zinc-200">{summary?.pattern_count ?? patterns.length ?? '…'}</dd>
              </div>
              <div>
                <dt className="text-zinc-500">Root</dt>
                <dd className="mt-1 text-emerald-400/90">{summary?.vocabulary_root_stub ? `${summary.vocabulary_root_stub}…` : '…'}</dd>
              </div>
              <div>
                <dt className="text-zinc-500">License</dt>
                <dd className="mt-1 text-zinc-200">CC BY 4.0</dd>
              </div>
            </dl>
          </div>

          <nav className="mt-8 flex items-center gap-1 border-b border-zinc-800/60">
            <span className="border-b-2 border-emerald-400 px-3 py-2 text-sm font-medium text-zinc-100">
              Patterns
            </span>
            <Link
              to={`/vocabularies/${slug}/graph`}
              className="inline-flex items-center gap-1.5 px-3 py-2 text-sm text-zinc-400 transition-colors hover:text-zinc-100"
            >
              <Network className="h-4 w-4" />
              Graph
            </Link>
          </nav>
        </div>
      </section>

      <main className="mx-auto max-w-6xl px-6 py-10">
        {isLoading ? (
          <p className="py-16 text-center text-sm text-zinc-500">Loading vocabulary…</p>
        ) : filtered.length === 0 ? (
          <p className="py-16 text-center text-sm text-zinc-500">No patterns match “{query.trim()}”.</p>
        ) : (
          byCategory.map(([category, items]) => (
            <section key={category} className="mb-10">
              <div className="mb-4 flex items-baseline justify-between border-b border-zinc-800/60 pb-2">
                <h2 className="text-lg font-medium tracking-tight text-zinc-200">{category}</h2>
                <span className="text-xs tabular-nums text-zinc-500">{items.length}</span>
              </div>
              <div className="grid gap-3 md:grid-cols-2">
                {items.map((p) => (
                  <PatternCard key={p.id} pattern={p} />
                ))}
              </div>
            </section>
          ))
        )}
      </main>

      <footer className="border-t border-zinc-800/50">
        <div className="mx-auto flex max-w-6xl flex-col justify-between gap-3 px-6 py-6 text-sm text-zinc-500 sm:flex-row sm:items-center">
          <p>Part of the public registry</p>
          <LicenseLine />
        </div>
      </footer>
    </div>
  )
}

function PatternCard({ pattern }: { pattern: Pattern }) {
  const [open, setOpen] = useState(false)
  const [copied, setCopied] = useState(false)

  const copyHandle = async () => {
    await navigator.clipboard.writeText(pattern.handle)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  return (
    <article className="rounded-xl border border-zinc-800/80 bg-zinc-900/40 transition-colors hover:border-zinc-700">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-start justify-between gap-4 p-4 text-left"
      >
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="font-medium tracking-tight text-zinc-100">{pattern.id}</h3>
            <code className="ref-mono text-emerald-400/80">#{pattern.stub}</code>
          </div>
          {/* The gloss is always visible — a card must say what the pattern IS. */}
          <p className={cn('mt-1.5 text-sm leading-6 text-zinc-400', !open && 'line-clamp-2')}>
            {pattern.gloss}
          </p>
        </div>
        <ChevronDown className={cn('mt-1 h-4 w-4 shrink-0 text-zinc-500 transition-transform', open && 'rotate-180')} />
      </button>

      {open && (
        <div className="border-t border-zinc-800/60 px-4 pb-4">
          {pattern.mechanism && (
            <PatternSection label="Mechanism">
              <p className="text-sm leading-6 text-zinc-300">{pattern.mechanism}</p>
            </PatternSection>
          )}
          {pattern.invariants?.length > 0 && (
            <PatternSection label="Invariants">
              <ul className="space-y-1.5">
                {pattern.invariants.map((inv) => (
                  <li key={inv} className="flex gap-2 text-sm leading-6 text-zinc-300">
                    <span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-emerald-400/70" />
                    {inv}
                  </li>
                ))}
              </ul>
            </PatternSection>
          )}
          <div className="mt-4 flex items-center justify-between">
            <code className="ref-mono text-xs text-zinc-500">{pattern.layer} / {pattern.category}</code>
            <button
              type="button"
              onClick={copyHandle}
              className="inline-flex items-center gap-1.5 text-sm text-zinc-400 transition-colors hover:text-zinc-100"
            >
              {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
              {copied ? 'Copied' : `Copy ${pattern.handle}`}
            </button>
          </div>
        </div>
      )}
    </article>
  )
}

function PatternSection({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="mt-4">
      <p className="mb-1.5 text-[11px] font-medium uppercase tracking-widest text-zinc-500">{label}</p>
      {children}
    </div>
  )
}

export default VocabularyPage
