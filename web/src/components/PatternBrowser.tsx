import { useLayoutEffect, useMemo, useRef, useState } from 'react'
import {
  ArrowLeft,
  Check,
  ChevronDown,
  ChevronUp,
  Copy,
  LayoutGrid,
  List as ListIcon,
  Search,
  X,
} from 'lucide-react'
import { usePattern } from '@/hooks/useApi'
import type { Pattern } from '@/types/taxonomy'
import { LAYER_COLORS, RING_LABELS, TIER_LABELS } from '@/types/taxonomy'
import { ParsedText } from '@/components/DetailsPanel'
import { cn } from '@/lib/utils'

/**
 * The patterns of the active vocabulary in the two densities semahash.org
 * uses: cards for scanning and a master-detail list for comparison. Both
 * share the filters and the detail surface. Patterns that arrived while the
 * view was open carry a "New" mark.
 */
const LAYER_ORDER = ['Physics', 'Mind', 'Society', 'Infrastructure']
type PatternView = 'cards' | 'list'
type PatternGroups = Array<[string, Map<string, Pattern[]>]>

export function PatternBrowser({
  patterns,
  arrivedIds,
}: {
  patterns: Pattern[]
  arrivedIds: Set<string>
}) {
  const [query, setQuery] = useState('')
  const [layerFilter, setLayerFilter] = useState<string | null>(null)
  const [domainFilter, setDomainFilter] = useState<string | null>(null)
  const [jsonView, setJsonView] = useState(false)
  const [patternView, setPatternView] = useState<PatternView>('cards')
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const listScrollY = useRef(0)

  // The narrow-screen detail pane is a modal over the list. Lock the page
  // underneath it and restore the exact list position when it closes.
  useLayoutEffect(() => {
    if (selectedId === null || !window.matchMedia('(max-width: 1023px)').matches) return

    listScrollY.current = window.scrollY
    const { body } = document
    const previous = {
      position: body.style.position,
      top: body.style.top,
      left: body.style.left,
      right: body.style.right,
      width: body.style.width,
    }
    body.style.position = 'fixed'
    body.style.top = `-${listScrollY.current}px`
    body.style.left = '0'
    body.style.right = '0'
    body.style.width = '100%'

    return () => {
      body.style.position = previous.position
      body.style.top = previous.top
      body.style.left = previous.left
      body.style.right = previous.right
      body.style.width = previous.width
      window.scrollTo({ top: listScrollY.current, behavior: 'instant' })
    }
  }, [selectedId !== null])

  // Cross-cutting domain facet (_meta.domain). Vocabularies without domains
  // never see the chips.
  const domains = useMemo(
    () => [...new Set(patterns.map((p) => p.domain).filter(Boolean))].sort() as string[],
    [patterns],
  )

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    let base = layerFilter ? patterns.filter((p) => p.layer === layerFilter) : patterns
    if (domainFilter) base = base.filter((p) => p.domain === domainFilter)
    if (q.length < 2) return base
    return base.filter(
      (p) =>
        p.id.toLowerCase().includes(q) ||
        p.gloss?.toLowerCase().includes(q) ||
        p.mechanism?.toLowerCase().includes(q) ||
        p.category?.toLowerCase().includes(q),
    )
  }, [patterns, query, layerFilter, domainFilter])

  const byLayer: PatternGroups = useMemo(() => {
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
        (LAYER_ORDER.indexOf(b) + 99 * +(LAYER_ORDER.indexOf(b) < 0)),
    )
  }, [filtered])

  const selectPattern = (id: string) => {
    const clean = id.split('#')[0]
    setSelectedId(clean)
    document.getElementById(`pat-${clean}`)?.scrollIntoView({ block: 'nearest' })
  }

  return (
    <div>
      <div className="flex flex-wrap items-center gap-2">
        <div className="flex w-full max-w-xs items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900/80 px-3 py-1.5 sm:mr-2">
          <Search className="h-4 w-4 shrink-0 text-zinc-500" aria-hidden="true" />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search this vocabulary…"
            aria-label="Search this vocabulary"
            className="w-full bg-transparent text-sm outline-none placeholder:text-zinc-600"
          />
          {query && (
            <button
              type="button"
              onClick={() => setQuery('')}
              aria-label="Clear search"
              className="text-zinc-500 hover:text-zinc-300"
            >
              <X className="h-3.5 w-3.5" />
            </button>
          )}
        </div>
        <button
          type="button"
          onClick={() => setLayerFilter(null)}
          className={cn(
            'rounded-full px-3 py-1 text-xs transition-colors',
            layerFilter === null
              ? 'bg-zinc-100 font-medium text-zinc-900'
              : 'border border-zinc-800 text-zinc-400 hover:text-zinc-200',
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
                : 'border border-zinc-800 text-zinc-400 hover:text-zinc-200',
            )}
          >
            <span className="h-2 w-2 rounded-full" style={{ backgroundColor: LAYER_COLORS[layer] }} />
            {layer}
          </button>
        ))}
        {domains.length > 0 && (
          <>
            <span className="mx-1 hidden h-4 w-px bg-zinc-800 sm:block" />
            {domains.map((domain) => (
              <button
                key={domain}
                type="button"
                onClick={() => setDomainFilter(domainFilter === domain ? null : domain)}
                className={cn(
                  'rounded-full px-3 py-1 text-xs transition-colors',
                  domainFilter === domain
                    ? 'bg-emerald-500/20 font-medium text-emerald-200 ring-1 ring-inset ring-emerald-500/40'
                    : 'border border-emerald-500/25 text-emerald-300/80 hover:text-emerald-200',
                )}
              >
                {domain}
              </button>
            ))}
          </>
        )}
        <span className="mx-1 hidden h-4 w-px bg-zinc-800 sm:block" />
        <div
          role="group"
          aria-label="Pattern view"
          className="inline-flex items-center rounded-lg border border-zinc-800 bg-zinc-950/70 p-0.5"
        >
          <button
            type="button"
            aria-pressed={!jsonView && patternView === 'cards'}
            onClick={() => {
              setPatternView('cards')
              setJsonView(false)
            }}
            className={cn(
              'inline-flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400/60',
              !jsonView && patternView === 'cards'
                ? 'bg-zinc-800 font-medium text-zinc-100 shadow-sm'
                : 'text-zinc-500 hover:text-zinc-300',
            )}
          >
            <LayoutGrid className="h-3.5 w-3.5" aria-hidden="true" />
            Cards
          </button>
          <button
            type="button"
            aria-pressed={!jsonView && patternView === 'list'}
            onClick={() => {
              setPatternView('list')
              setJsonView(false)
            }}
            className={cn(
              'inline-flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400/60',
              !jsonView && patternView === 'list'
                ? 'bg-zinc-800 font-medium text-zinc-100 shadow-sm'
                : 'text-zinc-500 hover:text-zinc-300',
            )}
          >
            <ListIcon className="h-3.5 w-3.5" aria-hidden="true" />
            List
          </button>
        </div>
        <button
          type="button"
          aria-pressed={jsonView}
          onClick={() => setJsonView((value) => !value)}
          className={cn(
            'ref-mono rounded-lg px-2.5 py-1.5 text-xs transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400/60',
            jsonView
              ? 'bg-zinc-800 font-medium text-zinc-100 ring-1 ring-inset ring-zinc-600'
              : 'border border-zinc-800 text-zinc-400 hover:text-zinc-200',
          )}
        >
          JSON
        </button>
      </div>

      <div className="mt-8 min-w-0">
        {jsonView ? (
          <pre className="ref-mono overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-950 p-4 text-xs leading-5 text-zinc-400">
            {JSON.stringify(filtered, null, 2)}
          </pre>
        ) : filtered.length === 0 ? (
          <p className="py-16 text-center text-sm text-zinc-500">
            {query.trim() ? `No patterns match “${query.trim()}”.` : 'No patterns match these filters.'}
          </p>
        ) : patternView === 'cards' ? (
          <PatternCards
            groups={byLayer}
            selectedId={selectedId}
            arrivedIds={arrivedIds}
            onSelect={(id) => setSelectedId((current) => (current === id ? null : id))}
            onRef={selectPattern}
            onClose={() => setSelectedId(null)}
          />
        ) : (
          <PatternList
            groups={byLayer}
            selectedId={selectedId}
            arrivedIds={arrivedIds}
            onSelect={setSelectedId}
            onRef={selectPattern}
            onClose={() => setSelectedId(null)}
          />
        )}
      </div>
    </div>
  )
}

function NewMark() {
  return (
    <span className="rounded-full bg-emerald-400/15 px-1.5 py-0.5 text-[10px] font-medium text-emerald-300 ring-1 ring-inset ring-emerald-400/30">
      New
    </span>
  )
}

function PatternCards({
  groups,
  selectedId,
  arrivedIds,
  onSelect,
  onRef,
  onClose,
}: {
  groups: PatternGroups
  selectedId: string | null
  arrivedIds: Set<string>
  onSelect: (id: string) => void
  onRef: (handle: string) => void
  onClose: () => void
}) {
  return (
    <div className="space-y-12">
      {groups.map(([layer, cats]) => (
        <section key={layer}>
          <div className="mb-6 flex items-center gap-4">
            <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: LAYER_COLORS[layer] || '#71717a' }} />
            <h2 className="text-lg font-medium text-zinc-200">{layer}</h2>
            <div className="h-px flex-1 bg-gradient-to-r from-zinc-800 to-transparent" />
            <span className="text-sm tabular-nums text-zinc-600">
              {[...cats.values()].reduce((count, items) => count + items.length, 0)}
            </span>
          </div>

          <div className="space-y-8">
            {[...cats.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([category, items]) => (
              <div key={category}>
                <div className="mb-3 flex items-center gap-3">
                  <h3 className="text-[11px] font-medium uppercase tracking-widest text-zinc-500">{category}</h3>
                  <div className="h-px flex-1 bg-zinc-900" />
                  <span className="text-xs tabular-nums text-zinc-700">{items.length}</span>
                </div>
                <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                  {items.map((pattern) => {
                    const selected = selectedId === pattern.id
                    return (
                      <PatternCard
                        key={pattern.id}
                        pattern={pattern}
                        selected={selected}
                        arrived={arrivedIds.has(pattern.id)}
                        onSelect={() => onSelect(pattern.id)}
                      >
                        {selected ? (
                          <DetailPane selectedId={selectedId} onRef={onRef} onClose={onClose} embedded />
                        ) : null}
                      </PatternCard>
                    )
                  })}
                </div>
              </div>
            ))}
          </div>
        </section>
      ))}
    </div>
  )
}

function PatternCard({
  pattern,
  selected,
  arrived,
  onSelect,
  children,
}: {
  pattern: Pattern
  selected: boolean
  arrived: boolean
  onSelect: () => void
  children?: React.ReactNode
}) {
  const layerColor = LAYER_COLORS[pattern.layer] || '#71717a'
  const detailId = `pat-${pattern.id}-details`

  return (
    <article
      id={`pat-${pattern.id}`}
      className={cn(
        'group relative flex flex-col overflow-hidden rounded-xl border border-zinc-800/50 bg-zinc-900/50 transition-all duration-300',
        arrived && 'live-arrive border-emerald-500/30',
        selected
          ? 'col-span-full border-zinc-700/60 bg-zinc-900/80'
          : 'hover:border-zinc-700/60 hover:bg-zinc-900/80 hover:shadow-lg hover:shadow-black/20',
      )}
    >
      <span
        className="absolute bottom-4 left-0 top-4 w-0.5 rounded-full transition-opacity duration-300"
        style={{ backgroundColor: layerColor, opacity: selected ? 1 : 0.5 }}
        aria-hidden="true"
      />
      <button
        type="button"
        aria-expanded={selected}
        aria-controls={detailId}
        onClick={onSelect}
        className="flex w-full flex-1 flex-col p-5 pl-4 text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-emerald-400/60"
      >
        <span className="mb-2 flex items-start justify-between gap-3">
          <span className="flex min-w-0 items-center gap-2">
            <span className="truncate font-medium text-zinc-100 transition-colors group-hover:text-white">
              {pattern.id}
            </span>
            <code className="ref-mono rounded bg-zinc-800/50 px-1.5 py-0.5 text-[10px] text-emerald-400/75">
              #{pattern.stub}
            </code>
            {arrived ? <NewMark /> : null}
          </span>
          <span
            className={cn('rounded-md p-1 transition-colors', selected ? 'bg-zinc-800' : 'group-hover:bg-zinc-800/50')}
            aria-hidden="true"
          >
            {selected ? (
              <ChevronUp className="h-4 w-4 text-zinc-400" />
            ) : (
              <ChevronDown className="h-4 w-4 text-zinc-500 group-hover:text-zinc-400" />
            )}
          </span>
        </span>
        <span
          className={cn(
            'block text-sm leading-relaxed text-zinc-500 transition-colors group-hover:text-zinc-400',
            !selected && 'line-clamp-2',
          )}
        >
          {pattern.gloss}
        </span>
        <span className="mt-auto flex flex-wrap items-center gap-2 pt-4">
          <span
            className="rounded-md border px-2 py-1 text-[11px] font-medium"
            style={{ backgroundColor: `${layerColor}15`, borderColor: `${layerColor}20`, color: layerColor }}
          >
            {pattern.layer}
          </span>
          {pattern.category ? (
            <span className="rounded-md border border-zinc-800 px-2 py-1 text-[11px] font-medium text-zinc-400">
              {pattern.category}
            </span>
          ) : null}
          {pattern.domain ? (
            <span className="rounded-md border border-emerald-500/20 bg-emerald-500/[0.06] px-2 py-1 text-[11px] font-medium text-emerald-300/80">
              {pattern.domain}
            </span>
          ) : null}
        </span>
      </button>
      {children ? <div id={detailId}>{children}</div> : null}
    </article>
  )
}

function PatternList({
  groups,
  selectedId,
  arrivedIds,
  onSelect,
  onRef,
  onClose,
}: {
  groups: PatternGroups
  selectedId: string | null
  arrivedIds: Set<string>
  onSelect: (id: string) => void
  onRef: (handle: string) => void
  onClose: () => void
}) {
  return (
    <div className="grid min-w-0 grid-cols-[minmax(0,1fr)] items-start gap-8 lg:grid-cols-[minmax(300px,380px)_minmax(0,1fr)]">
      <div className="scroll-slim min-w-0 lg:sticky lg:top-[76px] lg:h-[calc(100vh-92px)] lg:overflow-y-auto lg:pr-3">
        {groups.map(([layer, cats]) => (
          <section key={layer} className="mb-6">
            <div className="sticky top-0 z-10 flex items-center gap-2 bg-zinc-950/95 py-1.5 backdrop-blur">
              <span className="h-2 w-2 rounded-full" style={{ backgroundColor: LAYER_COLORS[layer] || '#71717a' }} />
              <h2 className="text-sm font-medium tracking-wide text-zinc-200">{layer}</h2>
              <span className="text-xs tabular-nums text-zinc-600">
                {[...cats.values()].reduce((count, items) => count + items.length, 0)}
              </span>
            </div>
            {[...cats.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([category, items]) => (
              <div key={category} className="mb-2">
                <h3 className="px-2 py-1 text-[10px] font-medium uppercase tracking-widest text-zinc-600">{category}</h3>
                {items.map((pattern) => (
                  <button
                    key={pattern.id}
                    id={`pat-${pattern.id}`}
                    type="button"
                    aria-pressed={selectedId === pattern.id}
                    onClick={() => onSelect(pattern.id)}
                    className={cn(
                      'block w-full min-w-0 overflow-hidden rounded-lg border-l-2 px-3 py-2 text-left transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-emerald-400/60',
                      selectedId === pattern.id ? 'bg-zinc-800/80' : 'hover:bg-zinc-900/70',
                    )}
                    style={{
                      borderLeftColor: `${LAYER_COLORS[pattern.layer] || '#71717a'}${selectedId === pattern.id ? 'ff' : '55'}`,
                    }}
                  >
                    <span className="flex min-w-0 items-baseline gap-2">
                      <span
                        className={cn(
                          'min-w-0 truncate text-sm font-medium',
                          selectedId === pattern.id ? 'text-zinc-50' : 'text-zinc-200',
                        )}
                      >
                        {pattern.id}
                      </span>
                      <code className="ref-mono text-emerald-400/70">#{pattern.stub}</code>
                      {arrivedIds.has(pattern.id) ? <NewMark /> : null}
                    </span>
                    <span className="mt-0.5 block truncate text-xs text-zinc-500">{pattern.gloss}</span>
                  </button>
                ))}
              </div>
            ))}
          </section>
        ))}
      </div>

      <DetailPane selectedId={selectedId} onRef={onRef} onClose={onClose} />
    </div>
  )
}

function DetailPane({
  selectedId,
  onRef,
  onClose,
  embedded = false,
}: {
  selectedId: string | null
  onRef: (handle: string) => void
  onClose: () => void
  embedded?: boolean
}) {
  const { data: pattern, isLoading } = usePattern(selectedId)
  const [copied, setCopied] = useState(false)
  const [showJson, setShowJson] = useState(false)

  if (!selectedId) {
    return (
      <div className="hidden rounded-xl border border-dashed border-zinc-800 px-8 py-24 text-center lg:sticky lg:top-[76px] lg:block">
        <p className="text-sm text-zinc-500">Select a pattern to inspect it.</p>
        <p className="mt-2 text-xs text-zinc-600">
          Gloss, mechanism, invariants, contracts, and dependencies appear here.
        </p>
      </div>
    )
  }

  const layerColor = pattern ? LAYER_COLORS[pattern.layer] || '#71717a' : '#71717a'
  const handle = pattern ? `${pattern.id}#${pattern.stub}` : selectedId
  const relatedPatterns = pattern?.relatedPatterns ?? []

  const copyHandle = async () => {
    await navigator.clipboard.writeText(handle)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  return (
    <div
      className={cn(
        'fixed inset-0 z-50 overscroll-contain overflow-y-auto bg-zinc-950 p-6 lg:static lg:z-auto lg:overflow-visible',
        embedded
          ? 'lg:border-t lg:border-zinc-800/60 lg:bg-transparent lg:px-5 lg:pb-6 lg:pt-5'
          : 'lg:rounded-xl lg:border lg:border-zinc-800 lg:bg-zinc-900/30 lg:p-8',
      )}
      style={embedded ? undefined : { borderTop: `3px solid ${layerColor}` }}
    >
      <button
        type="button"
        onClick={onClose}
        className="mb-4 inline-flex items-center gap-1.5 text-sm text-zinc-400 hover:text-zinc-100 lg:hidden"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to list
      </button>

      {isLoading ? (
        <p className="py-16 text-center text-sm text-zinc-500">Loading pattern…</p>
      ) : !pattern ? (
        <p className="py-16 text-center text-sm text-zinc-500">Pattern details are not available.</p>
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
                onClick={() => setShowJson((value) => !value)}
                className={cn(
                  'ref-mono rounded-lg px-3 py-1.5 text-xs transition-colors',
                  showJson ? 'bg-zinc-800 text-zinc-100' : 'border border-zinc-800 text-zinc-400 hover:text-zinc-200',
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

              {relatedPatterns.length > 0 && (
                <DetailSection label="Related">
                  <div className="flex flex-wrap gap-2">
                    {relatedPatterns.map((related) => (
                      <button
                        key={related.id}
                        type="button"
                        onClick={() => onRef(related.id)}
                        className="ref-mono rounded-md bg-white/[0.04] px-2 py-1 text-xs text-zinc-300 transition-colors hover:bg-white/[0.08] hover:text-zinc-100"
                      >
                        {related.id}
                        <span className="text-emerald-400/70">#{related.stub}</span>
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

function BulletList({
  items,
  onRef,
  halt,
}: {
  items: string[]
  onRef: (handle: string) => void
  halt?: boolean
}) {
  return (
    <ul className="space-y-1.5">
      {items.map((item) => (
        <li key={item} className="flex gap-2 text-sm leading-6 text-zinc-300">
          <span className={cn('mt-2 h-1 w-1 shrink-0 rounded-full', halt ? 'bg-red-400/70' : 'bg-emerald-400/70')} />
          <span>
            <ParsedText text={item} onPatternClick={onRef} />
          </span>
        </li>
      ))}
    </ul>
  )
}
