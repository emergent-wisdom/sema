import { useState, useMemo, useRef, useCallback, createContext, useContext, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Search, Box, Filter, X, ChevronDown, ChevronUp, Copy, Check, Book, FileText, Github, MessageCircle } from 'lucide-react'
import { usePatterns, usePattern, useSearchPatterns } from '@/hooks/useApi'
import { LAYER_COLORS, RING_LABELS, TIER_LABELS } from '@/types/taxonomy'
import { cn } from '@/lib/utils'
import { ParsedText } from '@/components/DetailsPanel'
import { SemaLogo } from '@/components/SemaLogo'
import { LicenseLine } from '@/components/LicenseLine'
import { DbSwitcher } from '@/components/DbSwitcher'

// Context to allow pattern cards to register themselves and handle navigation
type PatternNavigationContextType = {
  scrollToPattern: (patternId: string) => void
  registerCard: (patternId: string, element: HTMLDivElement, setExpanded: (v: boolean) => void) => void
  unregisterCard: (patternId: string) => void
  expandAll: boolean
  jsonView: boolean
}

const PatternNavigationContext = createContext<PatternNavigationContextType | null>(null)

const LAYERS = ['Physics', 'Mind', 'Society', 'Infrastructure']

// Layer descriptions for the hero section
const LAYER_DESCRIPTIONS: Record<string, string> = {
  Physics: 'Immutable laws of state and time',
  Mind: 'Reasoning and self-correction',
  Society: 'Multi-agent coordination',
  Infrastructure: 'Safety rails and constraints',
}

export function HomePage() {
  const { data: patterns, isLoading } = usePatterns()
  const [searchQuery, setSearchQuery] = useState('')
  const { data: searchResults, isLoading: isSearching } = useSearchPatterns(searchQuery)
  const [selectedLayer, setSelectedLayer] = useState<string | null>(null)
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [expandAll, setExpandAll] = useState(false)
  const [jsonView, setJsonView] = useState(false)
  const [copiedAllJson, setCopiedAllJson] = useState(false)

  // Pattern card registry for scroll-to navigation
  const cardRegistry = useRef<Map<string, { element: HTMLDivElement; setExpanded: (v: boolean) => void }>>(new Map())

  const scrollToPattern = useCallback((patternId: string) => {
    // Clear filters to ensure pattern is visible
    setSearchQuery('')
    setSelectedLayer(null)
    setSelectedCategory(null)

    // Small delay to let filters clear and DOM update
    setTimeout(() => {
      const card = cardRegistry.current.get(patternId)
      if (card) {
        card.element.scrollIntoView({ behavior: 'smooth', block: 'center' })
        card.setExpanded(true)
        // Flash highlight
        card.element.classList.add('ring-2', 'ring-emerald-500/50')
        setTimeout(() => card.element.classList.remove('ring-2', 'ring-emerald-500/50'), 2000)
      }
    }, 100)
  }, [])

  const registerCard = useCallback((patternId: string, element: HTMLDivElement, setExpanded: (v: boolean) => void) => {
    cardRegistry.current.set(patternId, { element, setExpanded })
  }, [])

  const unregisterCard = useCallback((patternId: string) => {
    cardRegistry.current.delete(patternId)
  }, [])

  // Get unique categories
  const categories = useMemo(() => {
    if (!patterns) return []
    const cats = new Set(patterns.map((p) => p.category).filter(Boolean))
    return Array.from(cats).sort()
  }, [patterns])

  // Filter patterns
  const filteredPatterns = useMemo(() => {
    // Use search results if we have a query and results
    let result: typeof patterns = patterns || []

    if (searchQuery.length >= 2 && searchResults) {
      // Map search results to Pattern-like structure
      result = searchResults.map((r) => ({
        id: r.handle.split('#')[0], // Extract ID from handle
        handle: r.handle,
        gloss: r.gloss,
        mechanism: r.mechanism,
        category: r.category,
        layer: r.layer,
        stub: r.handle.split('#')[1] || '',
        hash: '',
        invariants: [],
        parameters: {},
        // Score for display
        _score: r.score,
        _source: r.source,
      })) as typeof patterns
    }

    if (selectedLayer) {
      result = result?.filter((p) => p.layer === selectedLayer)
    }

    if (selectedCategory) {
      result = result?.filter((p) => p.category === selectedCategory)
    }

    return result || []
  }, [patterns, searchQuery, searchResults, selectedLayer, selectedCategory])

  // Group by category
  const patternsByCategory = useMemo(() => {
    const map = new Map<string, typeof filteredPatterns>()
    for (const p of filteredPatterns) {
      const cat = p.category || 'Uncategorized'
      const existing = map.get(cat) || []
      existing.push(p)
      map.set(cat, existing)
    }
    return map
  }, [filteredPatterns])

  // Layer counts
  const layerCounts = useMemo(() => {
    if (!patterns) return {}
    return LAYERS.reduce((acc, layer) => {
      acc[layer] = patterns.filter(p => p.layer === layer).length
      return acc
    }, {} as Record<string, number>)
  }, [patterns])

  const navigationContext = useMemo(() => ({
    scrollToPattern,
    registerCard,
    unregisterCard,
    expandAll,
    jsonView,
  }), [scrollToPattern, registerCard, unregisterCard, expandAll, jsonView])

  return (
    <PatternNavigationContext.Provider value={navigationContext}>
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      {/* Subtle background texture */}
      <div
        className="fixed inset-0 pointer-events-none opacity-[0.02]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Hero Section */}
      <div className="relative overflow-hidden border-b border-zinc-800/50">
        {/* Background gradient mesh */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-1/2 -left-1/4 w-full h-full bg-gradient-radial from-emerald-900/20 via-transparent to-transparent blur-3xl" />
          <div className="absolute -bottom-1/2 -right-1/4 w-full h-full bg-gradient-radial from-zinc-800/30 via-transparent to-transparent blur-3xl" />
        </div>

        <div className="relative max-w-6xl mx-auto px-6 pt-12 pb-16">
          {/* Header */}
          <div className="flex flex-col sm:flex-row items-start sm:justify-between gap-6 mb-12">
            <div className="flex items-center gap-5">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-emerald-500/20 to-emerald-500/5 border border-emerald-500/20 flex items-center justify-center shadow-lg shadow-emerald-900/20 text-emerald-400">
                <SemaLogo className="w-8 h-8" />
              </div>
              <div>
                <h1 className="text-3xl font-semibold tracking-tight">Sema</h1>
                <p className="text-sm text-zinc-500">When the hash is the word</p>
              </div>
            </div>
            <div className="flex items-center gap-2 flex-wrap">
              <a
                href="/api/paper"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-4 py-2.5 bg-zinc-800/50 hover:bg-zinc-800 border border-zinc-700/50 rounded-lg transition-all text-sm text-zinc-300 hover:text-zinc-100 hover:border-zinc-600"
              >
                <FileText className="w-4 h-4" />
                Paper
              </a>
              <a
                href="https://github.com/emergent-wisdom/sema"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-4 py-2.5 bg-zinc-800/50 hover:bg-zinc-800 border border-zinc-700/50 rounded-lg transition-all text-sm text-zinc-300 hover:text-zinc-100 hover:border-zinc-600"
              >
                <Github className="w-4 h-4" />
                GitHub
              </a>
              <a
                href="https://discord.gg/hRhVqAuDYQ"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-4 py-2.5 bg-zinc-800/50 hover:bg-zinc-800 border border-zinc-700/50 rounded-lg transition-all text-sm text-zinc-300 hover:text-zinc-100 hover:border-zinc-600"
              >
                <MessageCircle className="w-4 h-4" />
                Discord
              </a>
              <Link
                to="/docs"
                className="flex items-center gap-2 px-4 py-2.5 bg-zinc-800/50 hover:bg-zinc-800 border border-zinc-700/50 rounded-lg transition-all text-sm text-zinc-300 hover:text-zinc-100 hover:border-zinc-600"
              >
                <Book className="w-4 h-4" />
                Docs
              </Link>
              <Link
                to="/graph"
                className="flex items-center gap-2 px-4 py-2.5 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/20 rounded-lg transition-all text-sm text-emerald-400 hover:text-emerald-300 hover:border-emerald-500/30"
              >
                <Box className="w-4 h-4" />
                3D Graph
              </Link>
            </div>
          </div>

          {/* Hero content */}
          <div className="max-w-4xl mb-12">
            <h2 className="text-4xl font-light tracking-tight text-zinc-100 mb-4">
              Content-addressed patterns for{' '}
              <span className="text-emerald-400">autonomous agents</span>
            </h2>
            <p className="text-lg text-zinc-500 leading-relaxed">
              A taxonomy of cognitive patterns with cryptographic identity.
              When agents share a pattern hash, they share exact semantics.
            </p>
          </div>

          {/* Layer stats */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {LAYERS.map((layer, i) => (
              <button
                key={layer}
                type="button"
                onClick={() => setSelectedLayer(selectedLayer === layer ? null : layer)}
                className={cn(
                  "group relative p-4 rounded-xl border transition-all duration-300 text-left",
                  selectedLayer === layer
                    ? "bg-zinc-800/80 border-zinc-600"
                    : "bg-zinc-900/50 border-zinc-800/50 hover:bg-zinc-800/50 hover:border-zinc-700"
                )}
                style={{
                  animationDelay: `${i * 100}ms`,
                }}
              >
                <div className="flex items-center gap-3 mb-1">
                  <div
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: LAYER_COLORS[layer] }}
                  />
                  <span className="text-sm font-medium text-zinc-200">{layer}</span>
                </div>
                <div className="text-2xl font-light text-zinc-400 tabular-nums mb-1">
                  {layerCounts[layer] || 0}
                </div>
                <p className="text-xs text-zinc-600 leading-relaxed">
                  {LAYER_DESCRIPTIONS[layer]}
                </p>
                {selectedLayer === layer && (
                  <div className="absolute inset-0 rounded-xl ring-1 ring-inset ring-white/5" />
                )}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Filters Bar */}
      <div className="sticky top-0 z-50 border-b border-zinc-800/50 bg-zinc-950/80 backdrop-blur-xl">
        <div className="max-w-6xl mx-auto px-6 py-3">
          <div className="flex items-center gap-4 flex-wrap">
            {/* DB Switcher (local only) */}
            <DbSwitcher />

            {/* Search */}
            <div className="flex items-center gap-2 bg-zinc-900/80 border border-zinc-800/50 rounded-lg px-4 py-2.5 flex-1 max-w-md focus-within:border-zinc-700 focus-within:bg-zinc-900 transition-all">
              <Search className="w-4 h-4 text-zinc-500" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search patterns semantically..."
                className="bg-transparent outline-none text-sm w-full placeholder:text-zinc-600"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery('')}
                  className="text-zinc-500 hover:text-zinc-300 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* Category dropdown */}
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-zinc-600" />
              <select
                value={selectedCategory || ''}
                onChange={(e) => setSelectedCategory(e.target.value || null)}
                className="bg-zinc-900/80 border border-zinc-800/50 text-sm rounded-lg px-3 py-2.5 outline-none text-zinc-300 hover:border-zinc-700 focus:border-zinc-700 transition-all cursor-pointer"
              >
                <option value="">All Categories</option>
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>

            {/* View toggles */}
            <div className="flex items-center gap-2 ml-auto">
              <button
                type="button"
                onClick={() => setExpandAll(!expandAll)}
                className={cn(
                  "px-3 py-2 rounded-lg text-xs font-medium transition-all border",
                  expandAll
                    ? "bg-zinc-800 border-zinc-700 text-zinc-200"
                    : "bg-transparent border-zinc-800/50 text-zinc-500 hover:text-zinc-300 hover:border-zinc-700"
                )}
              >
                {expandAll ? 'Collapse All' : 'Expand All'}
              </button>
              <button
                type="button"
                onClick={() => setJsonView(!jsonView)}
                className={cn(
                  "px-3 py-2 rounded-lg text-xs font-medium transition-all border",
                  jsonView
                    ? "bg-zinc-800 border-zinc-700 text-zinc-200"
                    : "bg-transparent border-zinc-800/50 text-zinc-500 hover:text-zinc-300 hover:border-zinc-700"
                )}
              >
                {jsonView ? 'Card View' : 'JSON View'}
              </button>
              <div className="h-4 w-px bg-zinc-800 mx-1" />
              <span className="text-sm text-zinc-600 tabular-nums">
                <strong className="text-zinc-400">{filteredPatterns.length}</strong> patterns
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <main className="max-w-6xl mx-auto px-6 py-10">
        {isLoading || (searchQuery.length >= 2 && isSearching) ? (
          <div className="flex flex-col items-center justify-center py-24 gap-4">
            <div className="w-8 h-8 border-2 border-emerald-500/20 border-t-emerald-500 rounded-full animate-spin" />
            <span className="text-zinc-500 text-sm">
              {isSearching ? 'Searching semantically...' : 'Loading patterns...'}
            </span>
          </div>
        ) : filteredPatterns.length === 0 ? (
          <div className="text-center py-24">
            <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-zinc-900 border border-zinc-800 flex items-center justify-center">
              <Search className="w-6 h-6 text-zinc-600" />
            </div>
            <p className="text-zinc-500">No patterns found</p>
            <p className="text-zinc-600 text-sm mt-1">Try adjusting your search or filters</p>
          </div>
        ) : jsonView ? (
          /* JSON View - all patterns as one big JSON array */
          <div className="relative">
            <button
              type="button"
              onClick={async () => {
                await navigator.clipboard.writeText(JSON.stringify(filteredPatterns, null, 2))
                setCopiedAllJson(true)
                setTimeout(() => setCopiedAllJson(false), 2000)
              }}
              className="absolute top-4 right-4 px-3 py-2 rounded-lg bg-zinc-800/80 hover:bg-zinc-700 border border-zinc-700/50 text-zinc-400 hover:text-zinc-200 text-sm flex items-center gap-2 transition-all z-10"
            >
              {copiedAllJson ? (
                <>
                  <Check className="w-4 h-4 text-emerald-500" />
                  Copied
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  Copy All
                </>
              )}
            </button>
            <pre className="p-6 bg-zinc-900/50 border border-zinc-800/50 rounded-xl text-xs text-zinc-400 overflow-x-auto max-h-[80vh] overflow-y-auto font-mono">
              {JSON.stringify(filteredPatterns, null, 2)}
            </pre>
          </div>
        ) : (
          <div className="space-y-12">
            {Array.from(patternsByCategory.entries()).map(([category, categoryPatterns], categoryIndex) => (
              <section
                key={category}
                className="animate-in fade-in slide-in-from-bottom-4 duration-500"
                style={{ animationDelay: `${categoryIndex * 50}ms` }}
              >
                <div className="flex items-center gap-4 mb-6">
                  <h2 className="text-lg font-medium text-zinc-200">{category}</h2>
                  <div className="flex-1 h-px bg-gradient-to-r from-zinc-800 to-transparent" />
                  <span className="text-sm text-zinc-600 tabular-nums">{categoryPatterns.length}</span>
                </div>
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {categoryPatterns.map((pattern, i) => (
                    <PatternCard
                      key={pattern.id}
                      pattern={pattern}
                      index={i}
                    />
                  ))}
                </div>
              </section>
            ))}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-zinc-800/50 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="flex items-center justify-between text-sm text-zinc-600">
            <p>Sema Pattern Vocabulary</p>
            <p>Content-addressed semantic coordination</p>
          </div>
          <div className="mt-3 flex justify-end">
            <LicenseLine />
          </div>
        </div>
      </footer>
    </div>
    </PatternNavigationContext.Provider>
  )
}

function PatternCard({
  pattern,
  index,
}: {
  pattern: {
    id: string
    handle: string
    gloss: string
    stub: string
    layer: string
    category: string
  }
  index: number
}) {
  const navigation = useContext(PatternNavigationContext)
  const [isLocalExpanded, setIsLocalExpanded] = useState(false)
  // Expand if expandAll is true OR if locally expanded
  const isExpanded = navigation?.expandAll || isLocalExpanded
  const layerColor = LAYER_COLORS[pattern.layer] || '#71717a'
  const cardRef = useRef<HTMLDivElement>(null)

  // Register this card for scroll-to navigation
  useEffect(() => {
    if (cardRef.current && navigation) {
      navigation.registerCard(pattern.id, cardRef.current, setIsLocalExpanded)
      return () => navigation.unregisterCard(pattern.id)
    }
  }, [pattern.id, navigation])

  return (
    <div
      ref={cardRef}
      className={cn(
        "group relative bg-zinc-900/50 border border-zinc-800/50 rounded-xl transition-all duration-300",
        isExpanded
          ? "col-span-full bg-zinc-900/80 border-zinc-700/50"
          : "hover:bg-zinc-900/80 hover:border-zinc-700/50 hover:shadow-lg hover:shadow-black/20"
      )}
      style={{
        animationDelay: `${index * 30}ms`,
      }}
    >
      {/* Layer indicator line */}
      <div
        className="absolute left-0 top-4 bottom-4 w-0.5 rounded-full transition-all duration-300"
        style={{
          backgroundColor: layerColor,
          opacity: isExpanded ? 1 : 0.5,
        }}
      />

      {/* Header - always visible */}
      <button
        type="button"
        onClick={() => setIsLocalExpanded(!isLocalExpanded)}
        className="w-full text-left p-5 pl-4"
      >
        <div className="flex items-start justify-between gap-3 mb-2">
          <div className="flex items-center gap-2">
            <h3 className="font-medium text-zinc-100 group-hover:text-white transition-colors">
              {pattern.handle.split('#')[0]}
            </h3>
            <code className="text-[10px] text-zinc-600 font-mono bg-zinc-800/50 px-1.5 py-0.5 rounded">
              #{pattern.stub}
            </code>
          </div>
          <div className={cn(
            "p-1 rounded-md transition-all",
            isExpanded ? "bg-zinc-800" : "bg-transparent group-hover:bg-zinc-800/50"
          )}>
            {isExpanded ? (
              <ChevronUp className="w-4 h-4 text-zinc-400" />
            ) : (
              <ChevronDown className="w-4 h-4 text-zinc-500 group-hover:text-zinc-400" />
            )}
          </div>
        </div>
        <p className={cn(
          "text-sm text-zinc-500 leading-relaxed transition-colors",
          !isExpanded && "line-clamp-2",
          "group-hover:text-zinc-400"
        )}>
          {pattern.gloss}
        </p>
        <div className="mt-4 flex items-center gap-2">
          <span
            className="text-[11px] font-medium px-2 py-1 rounded-md transition-all"
            style={{
              backgroundColor: layerColor + '15',
              color: layerColor,
              borderWidth: 1,
              borderColor: layerColor + '20',
            }}
          >
            {pattern.layer}
          </span>
        </div>
      </button>

      {/* Expanded content */}
      {isExpanded && <PatternDetails patternId={pattern.id} />}
    </div>
  )
}

function PatternDetails({ patternId }: { patternId: string }) {
  const { data: pattern, isLoading } = usePattern(patternId)
  const [copiedRef, setCopiedRef] = useState(false)
  const [copiedHash, setCopiedHash] = useState(false)
  const [copiedJson, setCopiedJson] = useState(false)
  const [showJson, setShowJson] = useState(false)
  const navigation = useContext(PatternNavigationContext)

  const handlePatternClick = useCallback((targetId: string) => {
    navigation?.scrollToPattern(targetId)
  }, [navigation])

  if (isLoading) {
    return (
      <div className="px-5 pb-5 pt-0">
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-zinc-800/50 rounded w-1/3" />
          <div className="h-4 bg-zinc-800/30 rounded w-full" />
          <div className="h-4 bg-zinc-800/30 rounded w-2/3" />
        </div>
      </div>
    )
  }

  if (!pattern) {
    return <div className="px-5 pb-5 text-sm text-zinc-500">Pattern not found</div>
  }

  // Handle already includes stub (e.g., "Hypothesis#f480")
  const reference = pattern.handle

  const handleCopyRef = async () => {
    await navigator.clipboard.writeText(reference)
    setCopiedRef(true)
    setTimeout(() => setCopiedRef(false), 2000)
  }

  const handleCopyHash = async () => {
    await navigator.clipboard.writeText(pattern.hash)
    setCopiedHash(true)
    setTimeout(() => setCopiedHash(false), 2000)
  }

  return (
    <div className="px-5 pb-5 pt-0 border-t border-zinc-800/50 mt-0 space-y-5">
      {/* Reference and Hash */}
      <div className="flex flex-col gap-2 pt-5">
        <div className="flex items-center gap-2">
          <code className="text-sm text-emerald-400/80 font-mono">{reference}</code>
          <button
            type="button"
            onClick={handleCopyRef}
            className="p-1.5 rounded-md hover:bg-zinc-800 text-zinc-500 hover:text-zinc-300 transition-all"
            title="Copy reference"
          >
            {copiedRef ? (
              <Check className="w-3.5 h-3.5 text-emerald-500" />
            ) : (
              <Copy className="w-3.5 h-3.5" />
            )}
          </button>
        </div>
        {pattern.hash && (
          <div className="flex items-center gap-2">
            <code className="text-xs text-zinc-600 font-mono break-all">{pattern.hash}</code>
            <button
              type="button"
              onClick={handleCopyHash}
              className="p-1.5 rounded-md hover:bg-zinc-800 text-zinc-500 hover:text-zinc-300 transition-all flex-shrink-0"
              title="Copy full hash"
            >
              {copiedHash ? (
                <Check className="w-3.5 h-3.5 text-emerald-500" />
              ) : (
                <Copy className="w-3.5 h-3.5" />
              )}
            </button>
          </div>
        )}
      </div>

      {/* Meta badges */}
      {(pattern.meta?.ring !== undefined || pattern.meta?.tier !== undefined) && (
        <div className="flex flex-wrap gap-2">
          {pattern.meta?.ring !== undefined && (
            <span className="px-2.5 py-1 bg-zinc-800/50 border border-zinc-700/50 text-zinc-400 rounded-lg text-xs">
              Ring {pattern.meta.ring}: {RING_LABELS[pattern.meta.ring] || 'Unknown'}
            </span>
          )}
          {pattern.meta?.tier !== undefined && (
            <span className="px-2.5 py-1 bg-zinc-800/50 border border-zinc-700/50 text-zinc-400 rounded-lg text-xs">
              Tier {pattern.meta.tier}: {TIER_LABELS[pattern.meta.tier] || 'Unknown'}
            </span>
          )}
        </div>
      )}

      {/* Caution Notice */}
      {pattern.meta?.caution && (
        <p className="text-xs text-red-400/80 leading-relaxed">
          ▲ {pattern.meta.caution}
        </p>
      )}

      {/* Signature */}
      {pattern.signature && pattern.signature.length > 0 && (
        <div>
          <h4 className="text-[10px] font-medium text-zinc-500 uppercase tracking-widest mb-2">
            Signature
          </h4>
          <div className="flex flex-wrap gap-1.5">
            {pattern.signature.map((sig, i) => (
              <code key={i} className="px-2.5 py-1.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs rounded-lg font-mono">
                {sig}
              </code>
            ))}
          </div>
        </div>
      )}

      {/* Mechanism */}
      {pattern.mechanism && (
        <div>
          <h4 className="text-[10px] font-medium text-zinc-500 uppercase tracking-widest mb-2">
            Mechanism
          </h4>
          <p className="text-sm text-zinc-400 leading-relaxed">
            <ParsedText text={pattern.mechanism} onPatternClick={handlePatternClick} />
          </p>
        </div>
      )}

      {/* Preconditions */}
      {pattern.preconditions && pattern.preconditions.length > 0 && (
        <div>
          <h4 className="text-[10px] font-medium text-zinc-500 uppercase tracking-widest mb-2">
            Preconditions
          </h4>
          <ul className="space-y-2">
            {pattern.preconditions.map((pre, i) => (
              <li key={i} className="text-sm text-zinc-400 pl-3 border-l-2 border-amber-600/50">
                <ParsedText text={pre} onPatternClick={handlePatternClick} />
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Postconditions */}
      {pattern.postconditions && pattern.postconditions.length > 0 && (
        <div>
          <h4 className="text-[10px] font-medium text-zinc-500 uppercase tracking-widest mb-2">
            Postconditions
          </h4>
          <ul className="space-y-2">
            {pattern.postconditions.map((post, i) => (
              <li key={i} className="text-sm text-zinc-400 pl-3 border-l-2 border-emerald-600/50">
                <ParsedText text={post} onPatternClick={handlePatternClick} />
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Invariants */}
      {pattern.invariants && pattern.invariants.length > 0 && (
        <div>
          <h4 className="text-[10px] font-medium text-zinc-500 uppercase tracking-widest mb-2">
            Invariants
          </h4>
          <ul className="space-y-2">
            {pattern.invariants.map((inv, i) => (
              <li key={i} className="text-sm text-zinc-400 pl-3 border-l-2 border-zinc-700">
                <ParsedText text={inv} onPatternClick={handlePatternClick} />
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Parameters */}
      {pattern.parameters && (Array.isArray(pattern.parameters) ? pattern.parameters.length > 0 : Object.keys(pattern.parameters).length > 0) && (
        <div>
          <h4 className="text-[10px] font-medium text-zinc-500 uppercase tracking-widest mb-2">
            Parameters
          </h4>
          <div className="space-y-1.5">
            {Array.isArray(pattern.parameters) ? (
              // Array format: either strings or objects
              pattern.parameters.map((param, i) => (
                <div key={i} className="text-sm text-zinc-400 font-mono">
                  {typeof param === 'string' ? param : `${param.name}: ${param.type}${param.range ? ` ${param.range}` : ''}`}
                </div>
              ))
            ) : (
              // Object format: {name: type}
              Object.entries(pattern.parameters).map(([name, type]) => (
                <div key={name} className="flex items-center gap-2 text-sm">
                  <span className="text-zinc-300 font-mono">{name}</span>
                  <span className="text-zinc-700">:</span>
                  <span className="text-zinc-500 font-mono">{typeof type === 'string' ? type : JSON.stringify(type)}</span>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Failure Modes */}
      {pattern.failureModes && pattern.failureModes.length > 0 && (
        <div>
          <h4 className="text-[10px] font-medium text-zinc-500 uppercase tracking-widest mb-2">
            Failure Modes
          </h4>
          <ul className="space-y-2">
            {pattern.failureModes.map((mode, i) => (
              <li key={i} className="text-sm text-zinc-400 pl-3 border-l-2 border-red-600/50">
                <ParsedText text={mode} onPatternClick={handlePatternClick} />
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Related Patterns */}
      {pattern.relatedPatterns && pattern.relatedPatterns.length > 0 && (
        <div>
          <h4 className="text-[10px] font-medium text-zinc-500 uppercase tracking-widest mb-2">
            Related Patterns
          </h4>
          <div className="flex flex-wrap gap-2">
            {pattern.relatedPatterns.map((related) => (
              <button
                key={related.id}
                type="button"
                onClick={() => handlePatternClick(related.id)}
                className="px-2.5 py-1.5 bg-zinc-800/50 hover:bg-zinc-800 border border-zinc-700/50 hover:border-zinc-600 text-zinc-300 text-xs rounded-lg transition-all"
              >
                {related.handle}
                <span className="text-zinc-600 ml-1">#{related.stub}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Dependencies */}
      {pattern.dependencies && Object.keys(pattern.dependencies).length > 0 && (
        <div>
          <h4 className="text-[10px] font-medium text-zinc-500 uppercase tracking-widest mb-2">
            Dependencies
          </h4>
          <div className="space-y-3">
            {Object.entries(pattern.dependencies).map(([relType, targets]) => (
              <div key={relType}>
                <span className="text-[10px] text-zinc-600 uppercase tracking-wider">{relType.replace('_', ' ')}</span>
                <div className="flex flex-wrap gap-1.5 mt-1.5">
                  {Object.entries(targets as Record<string, string>).map(([name, ref]) => {
                    const targetHandle = ref.split('#')[0]
                    return (
                      <button
                        key={name}
                        type="button"
                        onClick={() => handlePatternClick(targetHandle)}
                        className="px-2 py-1 bg-zinc-800/50 hover:bg-zinc-800 border border-zinc-700/50 hover:border-zinc-600 text-zinc-400 text-xs rounded-md transition-all font-mono"
                      >
                        {ref}
                      </button>
                    )
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="pt-4 flex items-center gap-4 border-t border-zinc-800/50">
        <Link
          to={`/graph?node=${patternId}`}
          className="text-sm text-emerald-400 hover:text-emerald-300 transition-colors"
        >
          View in 3D Graph →
        </Link>
        <button
          type="button"
          onClick={() => setShowJson(!showJson)}
          className="text-sm text-zinc-500 hover:text-zinc-300 transition-colors"
        >
          {showJson ? 'Hide JSON' : 'Show JSON'}
        </button>
        {showJson && (
          <button
            type="button"
            onClick={async () => {
              await navigator.clipboard.writeText(JSON.stringify(pattern, null, 2))
              setCopiedJson(true)
              setTimeout(() => setCopiedJson(false), 2000)
            }}
            className="text-sm text-zinc-500 hover:text-zinc-300 flex items-center gap-1.5 transition-colors"
          >
            {copiedJson ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-500" />
                Copied
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                Copy
              </>
            )}
          </button>
        )}
      </div>

      {/* JSON View */}
      {showJson && (
        <pre className="p-4 bg-zinc-950 border border-zinc-800/50 rounded-xl text-xs text-zinc-400 overflow-x-auto max-h-96 overflow-y-auto font-mono">
          {JSON.stringify(pattern, null, 2)}
        </pre>
      )}
    </div>
  )
}

export default HomePage;
