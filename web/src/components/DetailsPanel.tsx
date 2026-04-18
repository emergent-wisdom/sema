import { X, Copy, Check, ExternalLink, Layers, FolderOpen } from 'lucide-react'
import { useState, useMemo, type ReactNode } from 'react'
import { usePattern, usePatterns, useGraph, usePatternsByCategory, usePatternsByLayer } from '@/hooks/useApi'
import { useAppStore } from '@/stores/appStore'
import { LAYER_COLORS, RING_LABELS, TIER_LABELS } from '@/types/taxonomy'
import type { PatternMeta, Pattern, GraphNode } from '@/types/taxonomy'
import { cn } from '@/lib/utils'

export function DetailsPanel() {
  const { selectedNodeId, detailsPanelOpen, setDetailsPanelOpen, selectNode } =
    useAppStore()
  const { data: graphData } = useGraph()

  // Find the selected node to determine its type
  const selectedNode = useMemo(() => {
    if (!graphData || !selectedNodeId) return null
    return graphData.nodes.find((n) => n.id === selectedNodeId) || null
  }, [graphData, selectedNodeId])

  const nodeType = selectedNode?.type

  if (!detailsPanelOpen || !selectedNodeId) {
    return null
  }

  const getTitle = () => {
    switch (nodeType) {
      case 'TAXONOMY_PATH':
        return 'Taxonomy'
      case 'CATEGORY':
        return 'Category'
      case 'LAYER':
        return 'Layer'
      default:
        return 'Pattern Details'
    }
  }

  return (
    <div className="absolute top-0 right-0 h-full w-[400px] bg-zinc-900/95 backdrop-blur-md border-l border-zinc-800 shadow-xl z-50 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800">
        <h2 className="text-sm font-medium text-zinc-300">{getTitle()}</h2>
        <button
          type="button"
          onClick={() => {
            setDetailsPanelOpen(false)
            selectNode(null)
          }}
          className="p-1 rounded hover:bg-zinc-800 text-zinc-500 hover:text-zinc-300 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {nodeType === 'TAXONOMY_PATH' && selectedNode ? (
          <TaxonomyPathDetails node={selectedNode} />
        ) : nodeType === 'CATEGORY' && selectedNode ? (
          <CategoryDetails node={selectedNode} />
        ) : nodeType === 'LAYER' && selectedNode ? (
          <LayerDetails node={selectedNode} />
        ) : nodeType === 'PATTERN' && selectedNodeId ? (
          <PatternDetailsLoader patternId={selectedNodeId} />
        ) : (
          <div className="p-4 text-zinc-500 text-sm">Select a node</div>
        )}
      </div>
    </div>
  )
}

// Separate component to only fetch pattern when we know it's a PATTERN node
function PatternDetailsLoader({ patternId }: { patternId: string }) {
  const { data: pattern, isLoading } = usePattern(patternId)

  if (isLoading) {
    return <div className="p-4 text-zinc-500 text-sm">Loading...</div>
  }

  if (!pattern) {
    return <div className="p-4 text-zinc-500 text-sm">Pattern not found</div>
  }

  return <PatternDetails pattern={pattern} />
}

// Parse text with PatternName#stub references and make them clickable
// Exported for reuse in HomePage
export function ParsedText({ text, onPatternClick }: { text: string; onPatternClick: (handle: string) => void }) {
  const { data: patterns } = usePatterns()

  const patternMap = useMemo(() => {
    if (!patterns) return new Map<string, { id: string; handle: string; stub: string }>()
    const map = new Map<string, { id: string; handle: string; stub: string }>()
    for (const p of patterns) {
      // Index by lowercase handle (without stub)
      const baseHandle = p.handle.split('#')[0].toLowerCase()
      map.set(baseHandle, { id: p.id, handle: p.handle, stub: p.stub })
    }
    return map
  }, [patterns])

  const parts = useMemo(() => {
    // Match PatternName#stub references (with optional surrounding quotes)
    // PatternName must start with uppercase letter, followed by word chars
    const regex = /'?([A-Z][a-zA-Z0-9_]*)#([a-f0-9]{4})'?/g
    const result: ReactNode[] = []
    let lastIndex = 0
    let match

    while ((match = regex.exec(text)) !== null) {
      // Add text before the match
      if (match.index > lastIndex) {
        result.push(text.slice(lastIndex, match.index))
      }

      const patternRef = match[1]
      const displayText = `${match[1]}#${match[2]}`

      // Check if this pattern exists (case-insensitive)
      const patternInfo = patternMap.get(patternRef.toLowerCase())

      if (patternInfo) {
        // Clickable pattern link
        result.push(
          <button
            key={match.index}
            type="button"
            onClick={() => onPatternClick(patternInfo.id)}
            className="text-blue-400 hover:text-blue-300 hover:underline font-medium"
          >
            {displayText}
          </button>
        )
      } else {
        // Unknown pattern - show as styled but not clickable
        result.push(
          <span key={match.index} className="text-zinc-500 font-mono text-xs">
            {displayText}
          </span>
        )
      }

      lastIndex = match.index + match[0].length
    }

    // Add remaining text
    if (lastIndex < text.length) {
      result.push(text.slice(lastIndex))
    }

    return result
  }, [text, patternMap, onPatternClick])

  return <>{parts}</>
}

function TaxonomyPathDetails({ node }: { node: GraphNode }) {
  const { selectNodeAndFly } = useAppStore()
  const { data: patterns, isLoading } = usePatterns()

  // Pull segments from node.metadata (set by the graph_store). Fall back
  // to splitting node.text on '/' for defensive compat.
  const segments: string[] = useMemo(() => {
    const meta = node.metadata as Record<string, unknown> | undefined
    const segs = meta?.segments
    if (Array.isArray(segs) && segs.every((s) => typeof s === 'string')) {
      return segs as string[]
    }
    return (node.text || '').split('/').filter(Boolean)
  }, [node])

  const layer = segments[0]
  const layerColor = (layer && LAYER_COLORS[layer]) || '#71717a'

  // Patterns whose path starts with this node's segments.
  // Current schema has depth=2 everywhere, so we match on
  // layer (segments[0]) and, if present, category (segments[1]).
  const matched = useMemo(() => {
    if (!patterns) return [] as Pattern[]
    return patterns.filter((p) => {
      if (segments[0] && p.layer !== segments[0]) return false
      if (segments[1] && p.category !== segments[1]) return false
      return true
    })
  }, [patterns, segments])

  return (
    <div className="p-4 space-y-4">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div
          className="p-2 rounded-lg"
          style={{ backgroundColor: layerColor + '20' }}
        >
          <Layers className="w-5 h-5" style={{ color: layerColor }} />
        </div>
        <div>
          {/* Path breadcrumb */}
          <h3 className="text-lg font-semibold text-zinc-100 flex flex-wrap items-center gap-1">
            {segments.map((seg, i) => (
              <span key={`${seg}-${i}`} className="flex items-center gap-1">
                {i > 0 && <span className="text-zinc-600">/</span>}
                <span>{seg}</span>
              </span>
            ))}
          </h3>
          <p className="text-xs text-zinc-500">
            Taxonomy · depth {segments.length} · structural node
          </p>
        </div>
      </div>

      {/* Pattern list — filtered by path prefix */}
      <div>
        <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
          Patterns under this path ({matched.length})
        </h4>
        {isLoading ? (
          <div className="text-sm text-zinc-500">Loading...</div>
        ) : matched.length > 0 ? (
          <div className="space-y-2">
            {matched.map((p) => (
              <button
                key={p.id}
                type="button"
                onClick={() => selectNodeAndFly(p.id)}
                className="w-full text-left p-2 rounded bg-zinc-800/50 hover:bg-zinc-800 transition-colors group"
              >
                <div className="flex items-center gap-2">
                  <span
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: LAYER_COLORS[p.layer] || '#71717a' }}
                  />
                  <span className="text-sm text-zinc-200 group-hover:text-zinc-100">
                    {p.handle}
                  </span>
                  <span className="text-xs text-zinc-600 font-mono">#{p.stub}</span>
                  <ExternalLink className="w-3 h-3 text-zinc-600 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
                {p.gloss && (
                  <p className="text-xs text-zinc-500 mt-1 line-clamp-1">{p.gloss}</p>
                )}
              </button>
            ))}
          </div>
        ) : (
          <div className="text-sm text-zinc-500">No patterns under this path</div>
        )}
      </div>
    </div>
  )
}


function CategoryDetails({ node }: { node: GraphNode }) {
  const { selectNodeAndFly } = useAppStore()
  const categoryName = node.text || node.handle || ''
  const { data: patterns, isLoading } = usePatternsByCategory(categoryName)

  return (
    <div className="p-4 space-y-4">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-lg bg-zinc-800">
          <FolderOpen className="w-5 h-5 text-zinc-400" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-zinc-100">{categoryName}</h3>
          <p className="text-xs text-zinc-500">Category</p>
        </div>
      </div>

      {/* Pattern List */}
      <div>
        <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
          Patterns ({patterns?.length || 0})
        </h4>
        {isLoading ? (
          <div className="text-sm text-zinc-500">Loading...</div>
        ) : patterns && patterns.length > 0 ? (
          <div className="space-y-2">
            {patterns.map((p) => (
              <button
                key={p.id}
                type="button"
                onClick={() => selectNodeAndFly(p.id)}
                className="w-full text-left p-2 rounded bg-zinc-800/50 hover:bg-zinc-800 transition-colors group"
              >
                <div className="flex items-center gap-2">
                  <span
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: LAYER_COLORS[p.layer] || '#71717a' }}
                  />
                  <span className="text-sm text-zinc-200 group-hover:text-zinc-100">
                    {p.handle}
                  </span>
                  <span className="text-xs text-zinc-600 font-mono">#{p.stub}</span>
                  <ExternalLink className="w-3 h-3 text-zinc-600 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
                {p.gloss && (
                  <p className="text-xs text-zinc-500 mt-1 line-clamp-1">{p.gloss}</p>
                )}
              </button>
            ))}
          </div>
        ) : (
          <div className="text-sm text-zinc-500">No patterns in this category</div>
        )}
      </div>
    </div>
  )
}

function LayerDetails({ node }: { node: GraphNode }) {
  const { selectNodeAndFly } = useAppStore()
  const layerName = node.text || node.handle || ''
  const { data: patterns, isLoading } = usePatternsByLayer(layerName)
  const layerColor = LAYER_COLORS[layerName] || '#71717a'

  // Group patterns by category
  const patternsByCategory = useMemo(() => {
    if (!patterns) return new Map<string, Pattern[]>()
    const map = new Map<string, Pattern[]>()
    for (const p of patterns) {
      const cat = p.category || 'Uncategorized'
      const existing = map.get(cat) || []
      existing.push(p)
      map.set(cat, existing)
    }
    return map
  }, [patterns])

  return (
    <div className="p-4 space-y-4">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div
          className="p-2 rounded-lg"
          style={{ backgroundColor: layerColor + '20' }}
        >
          <Layers className="w-5 h-5" style={{ color: layerColor }} />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-zinc-100">{layerName}</h3>
          <p className="text-xs text-zinc-500">Layer</p>
        </div>
      </div>

      {/* Stats */}
      <div className="flex items-center gap-4 text-sm">
        <span className="text-zinc-500">
          <strong className="text-zinc-300">{patterns?.length || 0}</strong> patterns
        </span>
        <span className="text-zinc-500">
          <strong className="text-zinc-300">{patternsByCategory.size}</strong> categories
        </span>
      </div>

      {/* Pattern List by Category */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="text-sm text-zinc-500">Loading...</div>
        ) : patternsByCategory.size > 0 ? (
          Array.from(patternsByCategory.entries()).map(([category, categoryPatterns]) => (
            <div key={category}>
              <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
                {category} ({categoryPatterns.length})
              </h4>
              <div className="space-y-1">
                {categoryPatterns.map((p) => (
                  <button
                    key={p.id}
                    type="button"
                    onClick={() => selectNodeAndFly(p.id)}
                    className="w-full text-left px-2 py-1.5 rounded hover:bg-zinc-800 transition-colors group flex items-center gap-2"
                  >
                    <span className="text-sm text-zinc-300 group-hover:text-zinc-100">
                      {p.handle}
                    </span>
                    <span className="text-xs text-zinc-600 font-mono">#{p.stub}</span>
                    <ExternalLink className="w-3 h-3 text-zinc-600 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
                  </button>
                ))}
              </div>
            </div>
          ))
        ) : (
          <div className="text-sm text-zinc-500">No patterns in this layer</div>
        )}
      </div>
    </div>
  )
}

function PatternDetails({
  pattern,
}: {
  pattern: {
    id: string
    handle: string
    gloss: string
    mechanism: string
    invariants: string[]
    parameters: Record<string, string>
    hash: string
    stub: string
    layer: string
    category: string
    // Additional fields
    signature?: string[]
    preconditions?: string[]
    postconditions?: string[]
    failureModes?: string[]
    dataSchema?: Record<string, unknown>
    derivedFrom?: string
    meta?: PatternMeta
    relatedPatterns?: Array<{
      id: string
      handle: string
      gloss: string
      stub: string
    }>
    dependencies?: Record<string, Record<string, string>>
  }
}) {
  const { selectNodeAndFly } = useAppStore()
  const [copiedRef, setCopiedRef] = useState(false)
  const [copiedHash, setCopiedHash] = useState(false)
  const [copiedJson, setCopiedJson] = useState(false)
  const [showJson, setShowJson] = useState(false)

  const layerColor = LAYER_COLORS[pattern.layer] || '#71717a'
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

  const handlePatternClick = (patternId: string) => {
    selectNodeAndFly(patternId)
  }

  return (
    <div className="p-4 space-y-4">
      {/* Handle and Stub */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <button
            type="button"
            onClick={() => selectNodeAndFly(pattern.id)}
            className="text-lg font-semibold text-zinc-100 hover:text-white transition-colors"
            title="Center on node"
          >
            {pattern.handle}
          </button>
          <button
            type="button"
            onClick={handleCopyRef}
            className="p-1 rounded hover:bg-zinc-800 text-zinc-500 hover:text-zinc-300 transition-colors"
            title="Copy reference"
          >
            {copiedRef ? (
              <Check className="w-3.5 h-3.5 text-green-500" />
            ) : (
              <Copy className="w-3.5 h-3.5" />
            )}
          </button>
        </div>

        {/* Layer and Category badges */}
        <div className="flex flex-wrap items-center gap-2">
          {pattern.layer && (
            <span
              className="px-2 py-0.5 rounded text-xs font-medium"
              style={{
                backgroundColor: layerColor + '20',
                color: layerColor,
              }}
            >
              {pattern.layer}
            </span>
          )}
          {pattern.category && (
            <span className="px-2 py-0.5 bg-zinc-800 text-zinc-400 rounded text-xs">
              {pattern.category}
            </span>
          )}
          {pattern.meta?.ring !== undefined && (
            <span className="px-2 py-0.5 bg-zinc-800 text-zinc-500 rounded text-xs">
              Ring {pattern.meta.ring}: {RING_LABELS[pattern.meta.ring] || 'Unknown'}
            </span>
          )}
          {pattern.meta?.tier !== undefined && (
            <span className="px-2 py-0.5 bg-zinc-800 text-zinc-500 rounded text-xs">
              Tier {pattern.meta.tier}: {TIER_LABELS[pattern.meta.tier] || 'Unknown'}
            </span>
          )}
        </div>
      </div>

      {/* Caution Notice */}
      {pattern.meta?.caution && (
        <p className="text-xs text-red-400/80 leading-relaxed">
          ▲ {pattern.meta.caution}
        </p>
      )}

      {/* Signature */}
      {pattern.signature && pattern.signature.length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
            Signature
          </h4>
          <div className="flex flex-wrap gap-1">
            {pattern.signature.map((sig, i) => (
              <code key={i} className="px-2 py-1 bg-zinc-800 text-blue-400 text-xs rounded font-mono">
                {sig}
              </code>
            ))}
          </div>
        </div>
      )}

      {/* Gloss */}
      {pattern.gloss && (
        <div>
          <p className="text-sm text-zinc-300 leading-relaxed">
            <ParsedText text={pattern.gloss} onPatternClick={handlePatternClick} />
          </p>
        </div>
      )}

      {/* Mechanism */}
      {pattern.mechanism && (
        <div>
          <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
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
          <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
            Preconditions
          </h4>
          <ul className="space-y-1.5">
            {pattern.preconditions.map((pre, i) => (
              <li
                key={i}
                className="text-sm text-zinc-400 pl-3 border-l-2 border-yellow-700"
              >
                <ParsedText text={pre} onPatternClick={handlePatternClick} />
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Postconditions */}
      {pattern.postconditions && pattern.postconditions.length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
            Postconditions
          </h4>
          <ul className="space-y-1.5">
            {pattern.postconditions.map((post, i) => (
              <li
                key={i}
                className="text-sm text-zinc-400 pl-3 border-l-2 border-green-700"
              >
                <ParsedText text={post} onPatternClick={handlePatternClick} />
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Invariants */}
      {pattern.invariants && pattern.invariants.length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
            Invariants
          </h4>
          <ul className="space-y-1.5">
            {pattern.invariants.map((inv, i) => (
              <li
                key={i}
                className="text-sm text-zinc-400 pl-3 border-l-2 border-zinc-700"
              >
                <ParsedText text={inv} onPatternClick={handlePatternClick} />
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Parameters */}
      {pattern.parameters && (Array.isArray(pattern.parameters) ? pattern.parameters.length > 0 : Object.keys(pattern.parameters).length > 0) && (
        <div>
          <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
            Parameters
          </h4>
          <div className="space-y-1">
            {Array.isArray(pattern.parameters) ? (
              pattern.parameters.map((param, i) => (
                <div key={i} className="text-sm text-zinc-400 font-mono">
                  {typeof param === 'string' ? param : `${param.name}: ${param.type}${param.range ? ` ${param.range}` : ''}`}
                </div>
              ))
            ) : (
              Object.entries(pattern.parameters).map(([name, type]) => (
                <div key={name} className="flex items-center gap-2 text-sm">
                  <span className="text-zinc-300 font-mono">{name}</span>
                  <span className="text-zinc-600">:</span>
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
          <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
            Failure Modes
          </h4>
          <ul className="space-y-1.5">
            {pattern.failureModes.map((mode, i) => (
              <li
                key={i}
                className="text-sm text-zinc-400 pl-3 border-l-2 border-red-700"
              >
                <ParsedText text={mode} onPatternClick={handlePatternClick} />
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Data Schema */}
      {pattern.dataSchema && Object.keys(pattern.dataSchema).length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
            Data Schema
          </h4>
          <pre className="p-2 bg-zinc-800 rounded text-xs text-zinc-400 overflow-x-auto">
            {JSON.stringify(pattern.dataSchema, null, 2)}
          </pre>
        </div>
      )}

      {/* Dependencies */}
      {pattern.dependencies && Object.keys(pattern.dependencies).length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
            Dependencies
          </h4>
          <div className="space-y-3">
            {Object.entries(pattern.dependencies).map(([relType, targets]) => (
              <div key={relType}>
                <span className="text-xs text-zinc-600 uppercase">{relType.replace(/_/g, ' ')}</span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {Object.entries(targets).map(([name, ref]) => {
                    const targetHandle = ref.split('#')[0]
                    return (
                      <button
                        key={name}
                        type="button"
                        onClick={() => selectNodeAndFly(targetHandle)}
                        className="px-2 py-0.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-400 text-xs rounded transition-colors font-mono"
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

      {/* Related Patterns */}
      {pattern.relatedPatterns && pattern.relatedPatterns.length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
            Related Patterns
          </h4>
          <div className="space-y-2">
            {pattern.relatedPatterns.map((related) => (
              <button
                key={related.id}
                type="button"
                onClick={() => selectNodeAndFly(related.id)}
                className="w-full text-left p-2 rounded bg-zinc-800/50 hover:bg-zinc-800 transition-colors group"
              >
                <div className="flex items-center gap-2">
                  <span className="text-sm text-zinc-200 group-hover:text-zinc-100 font-mono">
                    {related.handle}
                  </span>
                  <ExternalLink className="w-3 h-3 text-zinc-600 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
                {related.gloss && (
                  <p className="text-xs text-zinc-500 mt-1 line-clamp-1">
                    {related.gloss}
                  </p>
                )}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Hash */}
      <div>
        <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">
          Hash
        </h4>
        <button
          type="button"
          onClick={handleCopyHash}
          className="text-xs text-zinc-600 hover:text-zinc-400 font-mono break-all text-left transition-colors cursor-pointer"
          title="Click to copy"
        >
          {copiedHash ? (
            <span className="text-green-500">Copied!</span>
          ) : (
            pattern.hash
          )}
        </button>
      </div>

      {/* JSON Toggle */}
      <div className="pt-2 border-t border-zinc-800">
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setShowJson(!showJson)}
            className={cn(
              'text-xs px-2 py-1 rounded transition-colors',
              showJson
                ? 'bg-zinc-800 text-zinc-300'
                : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800',
            )}
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
              className="text-xs px-2 py-1 rounded text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 transition-colors flex items-center gap-1"
            >
              {copiedJson ? (
                <>
                  <Check className="w-3 h-3 text-green-500" />
                  Copied
                </>
              ) : (
                <>
                  <Copy className="w-3 h-3" />
                  Copy
                </>
              )}
            </button>
          )}
        </div>
        {showJson && (
          <pre className="mt-2 p-3 bg-zinc-950 rounded text-xs text-zinc-400 overflow-x-auto">
            {JSON.stringify(pattern, null, 2)}
          </pre>
        )}
      </div>
    </div>
  )
}
