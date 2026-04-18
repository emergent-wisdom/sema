import { Search, Filter, X, Link } from 'lucide-react'
import { useState, useRef } from 'react'
import { useGraph, usePatterns, useSearchPatterns } from '@/hooks/useApi'
import { useAppStore, SEMANTIC_EDGE_TYPES, STRUCTURAL_EDGE_TYPES, ALL_FILTERABLE_EDGE_TYPES } from '@/stores/appStore'
import type { NodeType } from '@/types/taxonomy'
import { LAYER_COLORS, NODE_TYPE_COLORS, EDGE_TYPE_COLORS } from '@/types/taxonomy'
import { cn } from '@/lib/utils'
import { DbSwitcher } from './DbSwitcher'
import { useDbs } from '@/hooks/useApi'

const LAYERS = ['Physics', 'Mind', 'Society', 'Infrastructure']
// Node types the filter UI offers. TAXONOMY_PATH replaced the old
// LAYER + CATEGORY scaffolding in 0.2.0; legacy types are intentionally
// not exposed in the filter chips (they'd be empty on current DBs).
const NODE_TYPES: NodeType[] = ['PATTERN', 'TAXONOMY_PATH']

// Human-readable display names for node types. `TAXONOMY_PATH` is the
// internal node-type identifier; users see it as "Taxonomy" in the UI.
const NODE_TYPE_LABEL: Record<NodeType, string> = {
  PATTERN: 'Pattern',
  TAXONOMY_PATH: 'Taxonomy',
  CATEGORY: 'Category',
  LAYER: 'Layer',
  INVARIANT: 'Invariant',
  PARAMETER: 'Parameter',
  PRECONDITION: 'Precondition',
  POSTCONDITION: 'Postcondition',
}

export function TopBar() {
  const { data: graphData } = useGraph()
  const { data: patterns } = usePatterns()

  const { data: dbs } = useDbs()
  const showDbSwitcher = (dbs?.databases?.length ?? 0) >= 2

  const nodeCount = graphData?.nodes.length || 0
  const edgeCount = graphData?.edges.length || 0
  const patternCount = patterns?.length || 0

  return (
    <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-zinc-900/90 backdrop-blur-md px-4 py-2 rounded-lg border border-zinc-800 shadow-lg z-50 flex items-center gap-3">
      {/* DB Switcher — hidden when there's nothing to switch between.
          Hide the trailing divider along with it so the top bar doesn't
          start with a dangling vertical line. */}
      {showDbSwitcher && (
        <>
          <DbSwitcher />
          <div className="w-px h-4 bg-zinc-700" />
        </>
      )}

      {/* Stats */}
      <div className="flex items-center gap-3 text-xs">
        <span className="text-zinc-500">
          <strong className="text-zinc-300">{patternCount}</strong> patterns
        </span>
        <span className="text-zinc-700">|</span>
        <span className="text-zinc-500">
          <strong className="text-zinc-300">{nodeCount}</strong> nodes
        </span>
        <span className="text-zinc-500">
          <strong className="text-zinc-300">{edgeCount}</strong> edges
        </span>
      </div>

      <div className="w-px h-4 bg-zinc-700" />

      {/* Search */}
      <SearchInput />

      <div className="w-px h-4 bg-zinc-700" />

      {/* Layer Filter */}
      <LayerFilter />

      {/* Node Type Filter */}
      <NodeTypeFilter />

      {/* Edge Type Filter */}
      <EdgeTypeFilter />
    </div>
  )
}

function SearchInput() {
  const { searchQuery, setSearchQuery, selectNodeAndFly } = useAppStore()
  const { data: searchResults, isLoading: isSearching } = useSearchPatterns(searchQuery)
  const [isFocused, setIsFocused] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  // Use search results directly (already limited by API)
  const suggestions = searchResults?.slice(0, 8) || []

  const handleSelect = (id: string) => {
    selectNodeAndFly(id)
    setSearchQuery('')
    inputRef.current?.blur()
  }

  return (
    <div className="relative">
      <div className="flex items-center gap-2">
        <Search className="w-3.5 h-3.5 text-zinc-500" />
        <input
          ref={inputRef}
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setTimeout(() => setIsFocused(false), 200)}
          placeholder="Search patterns..."
          className="bg-transparent text-sm text-zinc-300 placeholder:text-zinc-600 outline-none w-40"
        />
        {searchQuery && (
          <button
            type="button"
            onClick={() => setSearchQuery('')}
            className="text-zinc-500 hover:text-zinc-300"
          >
            <X className="w-3 h-3" />
          </button>
        )}
      </div>

      {/* Suggestions Dropdown */}
      {isFocused && searchQuery.length >= 2 && (
        <div className="absolute top-full left-0 mt-2 w-72 bg-zinc-900 border border-zinc-700 rounded-lg shadow-xl overflow-hidden">
          {isSearching ? (
            <div className="px-3 py-2 text-xs text-zinc-500">Searching...</div>
          ) : suggestions.length === 0 ? (
            <div className="px-3 py-2 text-xs text-zinc-500">No results</div>
          ) : (
            suggestions.map((pattern) => {
              // Extract ID from handle (e.g., "SpectralTune#76ac" -> "SpectralTune")
              const patternId = pattern.handle.split('#')[0]
              return (
                <button
                  key={pattern.handle}
                  type="button"
                  onClick={() => handleSelect(patternId)}
                  className="w-full text-left px-3 py-2 hover:bg-zinc-800 transition-colors"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-zinc-200">{pattern.handle}</span>
                    {pattern.score !== undefined && pattern.score < 1 && (
                      <span className="text-[10px] text-zinc-600">
                        {Math.round(pattern.score * 100)}%
                      </span>
                    )}
                  </div>
                  <div className="text-xs text-zinc-500 line-clamp-1">
                    {pattern.gloss}
                  </div>
                </button>
              )
            })
          )}
        </div>
      )}
    </div>
  )
}

function LayerFilter() {
  const { filterByLayer, setFilterByLayer } = useAppStore()
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          'flex items-center gap-1.5 px-2 py-1 rounded text-xs transition-colors',
          filterByLayer
            ? 'bg-zinc-800 text-zinc-200'
            : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800',
        )}
      >
        <Filter className="w-3 h-3" />
        {filterByLayer || 'Layer'}
        {filterByLayer && (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation()
              setFilterByLayer(null)
            }}
            className="ml-1 hover:text-zinc-100"
          >
            <X className="w-3 h-3" />
          </button>
        )}
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute top-full left-0 mt-1 bg-zinc-900 border border-zinc-700 rounded-lg shadow-xl z-50 py-1 min-w-[140px]">
            {LAYERS.map((layer) => (
              <button
                key={layer}
                type="button"
                onClick={() => {
                  setFilterByLayer(layer === filterByLayer ? null : layer)
                  setIsOpen(false)
                }}
                className={cn(
                  'w-full px-3 py-1.5 text-left text-xs flex items-center gap-2 transition-colors',
                  layer === filterByLayer
                    ? 'bg-zinc-800 text-zinc-200'
                    : 'text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200',
                )}
              >
                <span
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: LAYER_COLORS[layer] }}
                />
                {layer}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

function NodeTypeFilter() {
  const { showNodeTypes, toggleNodeType } = useAppStore()
  const [isOpen, setIsOpen] = useState(false)

  const activeCount = showNodeTypes.size

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          'flex items-center gap-1.5 px-2 py-1 rounded text-xs transition-colors',
          activeCount < NODE_TYPES.length
            ? 'bg-zinc-800 text-zinc-200'
            : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800',
        )}
      >
        Types
        {activeCount < NODE_TYPES.length && (
          <span className="bg-zinc-700 text-zinc-300 text-[10px] px-1 rounded">
            {activeCount}
          </span>
        )}
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute top-full right-0 mt-1 bg-zinc-900 border border-zinc-700 rounded-lg shadow-xl z-50 py-1 min-w-[140px]">
            {NODE_TYPES.map((type) => {
              const isActive = showNodeTypes.has(type)
              return (
                <button
                  key={type}
                  type="button"
                  onClick={() => toggleNodeType(type)}
                  className="w-full px-3 py-1.5 text-left text-xs flex items-center gap-2 hover:bg-zinc-800 transition-colors"
                >
                  <span
                    className="w-2.5 h-2.5 rounded-full"
                    style={{
                      backgroundColor: isActive
                        ? NODE_TYPE_COLORS[type]
                        : 'transparent',
                      border: isActive
                        ? 'none'
                        : `1px solid ${NODE_TYPE_COLORS[type]}`,
                    }}
                  />
                  <span
                    className={cn(
                      isActive ? 'text-zinc-200' : 'text-zinc-500 line-through',
                    )}
                  >
                    {NODE_TYPE_LABEL[type] ?? type}
                  </span>
                </button>
              )
            })}
          </div>
        </>
      )}
    </div>
  )
}

function EdgeTypeFilter() {
  const { showEdgeTypes, toggleEdgeType } = useAppStore()
  const [isOpen, setIsOpen] = useState(false)

  const activeCount = showEdgeTypes.size
  const totalCount = ALL_FILTERABLE_EDGE_TYPES.length

  const formatEdgeType = (type: string) => {
    return type.toLowerCase().replace(/_/g, ' ')
  }

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          'flex items-center gap-1.5 px-2 py-1 rounded text-xs transition-colors',
          activeCount < totalCount
            ? 'bg-zinc-800 text-zinc-200'
            : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800',
        )}
      >
        <Link className="w-3 h-3" />
        Edges
        {activeCount < totalCount && (
          <span className="bg-zinc-700 text-zinc-300 text-[10px] px-1 rounded">
            {activeCount}
          </span>
        )}
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute top-full right-0 mt-1 bg-zinc-900 border border-zinc-700 rounded-lg shadow-xl z-50 py-1 min-w-[180px] max-h-[300px] overflow-y-auto">
            {/* Semantic edge types */}
            <div className="px-3 py-1 text-[10px] text-zinc-500 uppercase tracking-wider">
              Semantic
            </div>
            {SEMANTIC_EDGE_TYPES.map((type) => {
              const isActive = showEdgeTypes.has(type)
              return (
                <button
                  key={type}
                  type="button"
                  onClick={() => toggleEdgeType(type)}
                  className="w-full px-3 py-1.5 text-left text-xs flex items-center gap-2 hover:bg-zinc-800 transition-colors"
                >
                  <span
                    className="w-2.5 h-2.5 rounded-full"
                    style={{
                      backgroundColor: isActive
                        ? EDGE_TYPE_COLORS[type]
                        : 'transparent',
                      border: isActive
                        ? 'none'
                        : `1px solid ${EDGE_TYPE_COLORS[type]}`,
                    }}
                  />
                  <span
                    className={cn(
                      'capitalize',
                      isActive ? 'text-zinc-200' : 'text-zinc-500 line-through',
                    )}
                  >
                    {formatEdgeType(type)}
                  </span>
                </button>
              )
            })}

            {/* Structural edge types */}
            <div className="px-3 py-1 mt-1 text-[10px] text-zinc-500 uppercase tracking-wider border-t border-zinc-800">
              Structural
            </div>
            {STRUCTURAL_EDGE_TYPES.map((type) => {
              const isActive = showEdgeTypes.has(type)
              return (
                <button
                  key={type}
                  type="button"
                  onClick={() => toggleEdgeType(type)}
                  className="w-full px-3 py-1.5 text-left text-xs flex items-center gap-2 hover:bg-zinc-800 transition-colors"
                >
                  <span
                    className="w-2.5 h-2.5 rounded-full"
                    style={{
                      backgroundColor: isActive
                        ? EDGE_TYPE_COLORS[type]
                        : 'transparent',
                      border: isActive
                        ? 'none'
                        : `1px solid ${EDGE_TYPE_COLORS[type]}`,
                    }}
                  />
                  <span
                    className={cn(
                      'capitalize',
                      isActive ? 'text-zinc-200' : 'text-zinc-500 line-through',
                    )}
                  >
                    {formatEdgeType(type)}
                  </span>
                </button>
              )
            })}
          </div>
        </>
      )}
    </div>
  )
}
