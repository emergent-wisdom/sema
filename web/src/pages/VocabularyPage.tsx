import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ArrowLeft, Bot, Check, Copy, Network, Search, ShieldCheck, X } from 'lucide-react'
import { usePattern, usePatterns } from '@/hooks/useApi'
import type { Pattern } from '@/types/taxonomy'
import { LAYER_COLORS, RING_LABELS, TIER_LABELS } from '@/types/taxonomy'
import { ParsedText } from '@/components/DetailsPanel'
import { SemaLogo } from '@/components/SemaLogo'
import { LicenseLine } from '@/components/LicenseLine'
import { cn } from '@/lib/utils'

/**
 * One vocabulary as master–detail: a compact, layer-colored pattern
 * list on the left; a persistent detail panel on the right that
 * updates on selection. Same interaction model as the graph view
 * (select → inspect), so the two lenses feel like one tool.
 */
type WorkspaceSummary = {
  label?: string
  pattern_count?: number
  vocabulary_root_stub?: string
}

const LAYER_ORDER = ['Physics', 'Mind', 'Society', 'Infrastructure']

export function VocabularyPage() {
  const { slug = 'bootstrap' } = useParams()
  const { data: patterns = [], isLoading } = usePatterns()
  const [query, setQuery] = useState('')
  const [layerFilter, setLayerFilter] = useState<string | null>(null)
  const [jsonView, setJsonView] = useState(false)
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [summary, setSummary] = useState<WorkspaceSummary | null>(null)

  // One template for every vocabulary: header facts come from the API.
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
    const base = layerFilter ? patterns.filter((p) => p.layer === layerFilter) : patterns
    if (q.length < 2) return base
    return base.filter(
      (p) =>
        p.id.toLowerCase().includes(q) ||
        p.gloss?.toLowerCase().includes(q) ||
        p.mechanism?.toLowerCase().includes(q) ||
        p.category?.toLowerCase().includes(q)
    )
  }, [patterns, query, layerFilter])

  const byLayer = useMemo(() => {
    const layers = new Map<string, Map<string, Pattern[]>>()
    for (const p of filtered) {
      const layer = p.layer || 'Unknown'
      const cat = p.category || 'Uncategorized'
      if (!layers.has(layer)) layers.set(layer, new Map())
      const cats = layers.get(layer)!
      cats.set(cat, [...(cats.get(cat) ?? []), p])
    }
    return [...layers.entries()].sort(
      ([a], [b]) =>
        (LAYER_ORDER.indexOf(a) + 99 * +(LAYER_ORDER.indexOf(a) < 0)) -
        (LAYER_ORDER.indexOf(b) + 99 * +(LAYER_ORDER.indexOf(b) < 0))
    )
  }, [filtered])

  const selectPattern = (id: string) => {
    const clean = id.split('#')[0]
    setSelectedId(clean)
    document.getElementById(`pat-${clean}`)?.scrollIntoView({ block: 'nearest' })
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <header className="sticky top-0 z-40 border-b border-zinc-800/60 bg-zinc-950/85 backdrop-blur-xl">
        <div className="mx-auto flex max-w-[1400px] items-center justify-between gap-4 px-6 py-3">
          <Link to="/registry" className="inline-flex items-center gap-2 text-sm text-zinc-400 transition-colors hover:text-zinc-100">
            <ArrowLeft className="h-4 w-4" />
            Registry
          </Link>
          <div className="flex w-full max-w-sm items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900/80 px-3 py-2">
            <Search className="h-4 w-4 shrink-0 text-zinc-500" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search this vocabulary…"
              className="w-full bg-transparent text-sm outline-none placeholder:text-zinc-600"
            />
            {query && (
              <button type="button" onClick={() => setQuery('')} className="text-zinc-500 hover:text-zinc-300">
                <X className="h-3.5 w-3.5" />
              </button>
            )}
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
        <div className="mx-auto max-w-[1400px] px-6 py-8">
          <div className="flex flex-wrap items-start justify-between gap-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500/20 to-emerald-500/5 ring-1 ring-inset ring-emerald-500/20 text-emerald-400">
                <SemaLogo className="h-7 w-7" />
              </div>
              <div>
                <div className="flex items-center gap-3">
                  <h1 className="text-2xl font-medium tracking-tight">
                    {slug === 'bootstrap' ? 'Sema Bootstrap' : (summary?.label ?? slug)}
                  </h1>
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

          <nav className="mt-6 flex items-center gap-1 border-b border-zinc-800/60">
            <span className="border-b-2 border-emerald-400 px-3 py-2 text-sm font-medium text-zinc-100">Patterns</span>
            <Link
              to={`/vocabularies/${slug}/graph`}
              className="inline-flex items-center gap-1.5 px-3 py-2 text-sm text-zinc-400 transition-colors hover:text-zinc-100"
            >
              <Network className="h-4 w-4" />
              Graph
            </Link>
          </nav>

          <div className="mt-4 flex flex-wrap items-center gap-2">
            <button
              type="button"
              onClick={() => setLayerFilter(null)}
              className={cn(
                'rounded-full px-3 py-1 text-xs transition-colors',
                layerFilter === null
                  ? 'bg-zinc-100 font-medium text-zinc-900'
                  : 'border border-zinc-800 text-zinc-400 hover:text-zinc-200'
              )}
            >
              All layers
            </button>
            {LAYER_ORDER.map((layer) => (
              <button
                key={layer}
                type="button"
                onClick={() => setLayerFilter(layerFilter === layer ? null : layer)}
                className={cn(
                  'inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs transition-colors',
                  layerFilter === layer
                    ? 'bg-zinc-800 font-medium text-zinc-100 ring-1 ring-inset ring-zinc-600'
                    : 'border border-zinc-800 text-zinc-400 hover:text-zinc-200'
                )}
              >
                <span className="h-2 w-2 rounded-full" style={{ backgroundColor: LAYER_COLORS[layer] }} />
                {layer}
              </button>
            ))}
            <span className="mx-1 hidden h-4 w-px bg-zinc-800 sm:block" />
            <button
              type="button"
              onClick={() => setJsonView((v) => !v)}
              className={cn(
                'ref-mono rounded-full px-3 py-1 text-xs transition-colors',
                jsonView
                  ? 'bg-zinc-800 font-medium text-zinc-100 ring-1 ring-inset ring-zinc-600'
                  : 'border border-zinc-800 text-zinc-400 hover:text-zinc-200'
              )}
            >
              {jsonView ? 'List view' : 'JSON view'}
            </button>
          </div>
        </div>
      </section>

      <main className="mx-auto max-w-[1400px] px-6 py-8">
        {isLoading ? (
          <p className="py-16 text-center text-sm text-zinc-500">Loading vocabulary…</p>
        ) : jsonView ? (
          <pre className="ref-mono overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-950 p-4 text-xs leading-5 text-zinc-400">
            {JSON.stringify(filtered, null, 2)}
          </pre>
        ) : filtered.length === 0 ? (
          <p className="py-16 text-center text-sm text-zinc-500">No patterns match “{query.trim()}”.</p>
        ) : (
          <div className="grid items-start gap-8 lg:grid-cols-[minmax(300px,380px)_minmax(0,1fr)]">
            {/* Master list */}
            <div className="max-h-[calc(100vh-140px)] overflow-y-auto pr-1 lg:sticky lg:top-[76px]">
              {byLayer.map(([layer, cats]) => (
                <section key={layer} className="mb-6">
                  <div className="sticky top-0 z-10 flex items-center gap-2 bg-zinc-950/95 py-1.5 backdrop-blur">
                    <span className="h-2 w-2 rounded-full" style={{ backgroundColor: LAYER_COLORS[layer] || '#71717a' }} />
                    <h2 className="text-sm font-medium tracking-wide text-zinc-200">{layer}</h2>
                    <span className="text-xs tabular-nums text-zinc-600">
                      {[...cats.values()].reduce((n, items) => n + items.length, 0)}
                    </span>
                  </div>
                  {[...cats.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([category, items]) => (
                    <div key={category} className="mb-2">
                      <h3 className="px-2 py-1 text-[10px] font-medium uppercase tracking-widest text-zinc-600">
                        {category}
                      </h3>
                      {items.map((p) => (
                        <button
                          key={p.id}
                          id={`pat-${p.id}`}
                          type="button"
                          onClick={() => setSelectedId(p.id)}
                          className={cn(
                            'block w-full rounded-lg border-l-2 px-3 py-2 text-left transition-colors',
                            selectedId === p.id ? 'bg-zinc-800/80' : 'hover:bg-zinc-900/70'
                          )}
                          style={{ borderLeftColor: `${LAYER_COLORS[p.layer] || '#71717a'}${selectedId === p.id ? 'ff' : '55'}` }}
                        >
                          <span className="flex items-baseline gap-2">
                            <span className={cn('text-sm font-medium', selectedId === p.id ? 'text-zinc-50' : 'text-zinc-200')}>
                              {p.id}
                            </span>
                            <code className="ref-mono text-emerald-400/70">#{p.stub}</code>
                          </span>
                          <span className="mt-0.5 block truncate text-xs text-zinc-500">{p.gloss}</span>
                        </button>
                      ))}
                    </div>
                  ))}
                </section>
              ))}
            </div>

            {/* Detail panel */}
            <DetailPane selectedId={selectedId} onRef={selectPattern} onClose={() => setSelectedId(null)} />
          </div>
        )}
      </main>

      <footer className="border-t border-zinc-800/50">
        <div className="mx-auto flex max-w-[1400px] flex-col justify-between gap-3 px-6 py-6 text-sm text-zinc-500 sm:flex-row sm:items-center">
          <p>Part of the public registry</p>
          <LicenseLine />
        </div>
      </footer>
    </div>
  )
}

function DetailPane({
  selectedId,
  onRef,
  onClose,
}: {
  selectedId: string | null
  onRef: (handle: string) => void
  onClose: () => void
}) {
  const { data: pattern, isLoading } = usePattern(selectedId)
  const [copied, setCopied] = useState(false)
  const [showJson, setShowJson] = useState(false)

  if (!selectedId) {
    return (
      <div className="hidden rounded-xl border border-dashed border-zinc-800 px-8 py-24 text-center lg:block">
        <p className="text-sm text-zinc-500">Select a pattern to inspect it.</p>
        <p className="mt-2 text-xs text-zinc-600">
          Gloss, mechanism, invariants, contracts, and dependencies appear here.
        </p>
      </div>
    )
  }

  const layerColor = pattern ? LAYER_COLORS[pattern.layer] || '#71717a' : '#71717a'
  const handle = pattern ? `${pattern.id}#${pattern.stub}` : selectedId

  const copyHandle = async () => {
    await navigator.clipboard.writeText(handle)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  return (
    <div
      className="fixed inset-0 z-50 overflow-y-auto bg-zinc-950 p-6 lg:static lg:z-auto lg:max-h-[calc(100vh-140px)] lg:rounded-xl lg:border lg:border-zinc-800 lg:bg-zinc-900/30 lg:p-8"
      style={{ borderTop: `3px solid ${layerColor}` }}
    >
      <button
        type="button"
        onClick={onClose}
        className="mb-4 inline-flex items-center gap-1.5 text-sm text-zinc-400 hover:text-zinc-100 lg:hidden"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to list
      </button>

      {isLoading || !pattern ? (
        <p className="py-16 text-center text-sm text-zinc-500">Loading pattern…</p>
      ) : (
        <>
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-3">
                <h2 className="text-2xl font-medium tracking-tight text-zinc-50">{pattern.id}</h2>
                <code className="ref-mono text-emerald-400/90">#{pattern.stub}</code>
              </div>
              <p className="ref-mono mt-1 text-xs text-zinc-500">
                <span className="inline-flex items-center gap-1.5">
                  <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: layerColor }} />
                  {pattern.layer} / {pattern.category}
                </span>
                {pattern.meta?.ring !== undefined && (
                  <span className="ml-3">Ring {pattern.meta.ring}: {RING_LABELS[pattern.meta.ring] || '—'}</span>
                )}
                {pattern.meta?.tier !== undefined && (
                  <span className="ml-3">Tier {pattern.meta.tier}: {TIER_LABELS[pattern.meta.tier] || '—'}</span>
                )}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setShowJson((v) => !v)}
                className={cn(
                  'ref-mono rounded-lg px-3 py-1.5 text-xs transition-colors',
                  showJson ? 'bg-zinc-800 text-zinc-100' : 'border border-zinc-800 text-zinc-400 hover:text-zinc-200'
                )}
              >
                json
              </button>
              <button
                type="button"
                onClick={copyHandle}
                className="inline-flex items-center gap-1.5 rounded-lg border border-zinc-800 px-3 py-1.5 text-xs text-zinc-300 transition-colors hover:border-zinc-700 hover:text-zinc-100"
              >
                {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                {copied ? 'Copied' : handle}
              </button>
            </div>
          </div>

          {showJson ? (
            <pre className="ref-mono mt-6 overflow-auto rounded-lg border border-zinc-800 bg-zinc-950 p-4 text-xs leading-5 text-zinc-400">
              {JSON.stringify(pattern, null, 2)}
            </pre>
          ) : (
            <>
              <p className="mt-5 text-base leading-7 text-zinc-300">
                <ParsedText text={pattern.gloss} onPatternClick={onRef} />
              </p>

              {pattern.mechanism && (
                <DetailSection label="Mechanism">
                  <p className="text-sm leading-7 text-zinc-300">
                    <ParsedText text={pattern.mechanism} onPatternClick={onRef} />
                  </p>
                </DetailSection>
              )}

              {pattern.invariants?.length > 0 && (
                <DetailSection label="Invariants">
                  <BulletList items={pattern.invariants} onRef={onRef} />
                </DetailSection>
              )}
              {pattern.preconditions && pattern.preconditions.length > 0 && (
                <DetailSection label="Preconditions">
                  <BulletList items={pattern.preconditions} onRef={onRef} />
                </DetailSection>
              )}
              {pattern.postconditions && pattern.postconditions.length > 0 && (
                <DetailSection label="Postconditions">
                  <BulletList items={pattern.postconditions} onRef={onRef} />
                </DetailSection>
              )}
              {pattern.failureModes && pattern.failureModes.length > 0 && (
                <DetailSection label="Failure modes">
                  <BulletList items={pattern.failureModes} onRef={onRef} halt />
                </DetailSection>
              )}

              {pattern.relatedPatterns?.length > 0 && (
                <DetailSection label="Related">
                  <div className="flex flex-wrap gap-2">
                    {pattern.relatedPatterns.map((r) => (
                      <button
                        key={r.id}
                        type="button"
                        onClick={() => onRef(r.id)}
                        className="ref-mono rounded-md bg-white/[0.04] px-2 py-1 text-xs text-zinc-300 transition-colors hover:bg-white/[0.08] hover:text-zinc-100"
                      >
                        {r.id}
                        <span className="text-emerald-400/70">#{r.stub}</span>
                      </button>
                    ))}
                  </div>
                </DetailSection>
              )}
            </>
          )}
        </>
      )}
    </div>
  )
}

function DetailSection({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="mt-6">
      <p className="mb-2 text-[11px] font-medium uppercase tracking-widest text-zinc-500">{label}</p>
      {children}
    </div>
  )
}

function BulletList({ items, onRef, halt }: { items: string[]; onRef: (h: string) => void; halt?: boolean }) {
  return (
    <ul className="space-y-1.5">
      {items.map((item) => (
        <li key={item} className="flex gap-2 text-sm leading-6 text-zinc-300">
          <span className={cn('mt-2 h-1 w-1 shrink-0 rounded-full', halt ? 'bg-red-400/70' : 'bg-emerald-400/70')} />
          <span><ParsedText text={item} onPatternClick={onRef} /></span>
        </li>
      ))}
    </ul>
  )
}

export default VocabularyPage
