import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import ForceGraph3D from 'react-force-graph-3d'
import { useGraph } from '@/hooks/useApi'
import { useAppStore } from '@/stores/appStore'
import { useLiveStore, useRecentArrivalIds } from '@/hooks/useLiveAdditions'
import type { GraphNode, GraphEdge, NodeType, EdgeType } from '@/types/taxonomy'
import { LAYER_COLORS, NODE_TYPE_COLORS, EDGE_TYPE_COLORS } from '@/types/taxonomy'

const DEFAULT_COLOR = '#71717a'
const ARRIVAL_COLOR = '#a7f3d0'
// How long a newly minted pattern stays highlighted in the graph.
const ARRIVAL_HIGHLIGHT_MS = 20000

interface Node3D {
  id: string
  name: string
  color: string
  type: NodeType
  layer?: string
  /** Size for the renderer, computed while the node's metadata is at hand. */
  val: number
  x?: number
  y?: number
  z?: number
}

interface Link3D {
  source: string | Node3D
  target: string | Node3D
  type: EdgeType
  id: string
}

function getNodeColor(node: GraphNode): string {
  if (node.type === 'PATTERN' && node.layer) {
    return LAYER_COLORS[node.layer] || NODE_TYPE_COLORS.PATTERN
  }
  // Taxonomy paths are structural scaffolding, not content. Keep them
  // visually neutral (grey) so they read as hubs/anchors without competing
  // with pattern nodes for attention.
  if (node.type === 'TAXONOMY_PATH') {
    return NODE_TYPE_COLORS.TAXONOMY_PATH
  }
  // Legacy node types
  if (node.type === 'CATEGORY' && node.layer) {
    return LAYER_COLORS[node.layer] || NODE_TYPE_COLORS.CATEGORY
  }
  return NODE_TYPE_COLORS[node.type] || DEFAULT_COLOR
}

function getNodeSize(node: GraphNode): number {
  if (node.type === 'TAXONOMY_PATH') {
    // Root (layer) = 8, child paths progressively smaller.
    const depth = (node.metadata as Record<string, unknown>)?.depth
    if (typeof depth === 'number') {
      return Math.max(4, 10 - 2 * depth)
    }
    return 6
  }
  switch (node.type) {
    case 'LAYER':
      return 8
    case 'CATEGORY':
      return 6
    case 'PATTERN':
      return 4
    default:
      return 3
  }
}

export function GraphCanvas() {
  // biome-ignore lint/suspicious/noExplicitAny: ForceGraph ref types are complex
  const fgRef = useRef<any>(null)
  const {
    selectNode,
    setHoveredNode,
    showNodeTypes,
    showEdgeTypes,
    filterByLayer,
    filterByCategory,
    pendingFlyToNodeId,
    clearPendingFly,
  } = useAppStore()
  const { data: apiData, isLoading } = useGraph()
  const recentArrivals = useRecentArrivalIds(ARRIVAL_HIGHLIGHT_MS)
  const following = useLiveStore((state) => state.follow)

  // Reuse node objects between polls. The renderer stores each node's position
  // on the object itself, so reusing it lets the graph grow in place while an
  // agent mints, instead of laying the whole vocabulary out again.
  const nodeCache = useRef(new Map<string, Node3D>())

  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null)
  const [hoveredEdgeId, setHoveredEdgeId] = useState<string | null>(null)

  const [dimensions, setDimensions] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  })

  useEffect(() => {
    const handleResize = () => {
      setDimensions({ width: window.innerWidth, height: window.innerHeight })
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const cameraAngle = useRef({ theta: 0, phi: Math.PI / 2, distance: 500 })
  // Once the person moves the camera themselves, growth no longer reframes it.
  const userMovedCamera = useRef(false)

  const updateCamera = useCallback(
    (angle: { theta: number; phi: number; distance: number }) => {
      const fg = fgRef.current
      if (!fg) return
      const x = angle.distance * Math.sin(angle.phi) * Math.sin(angle.theta)
      const y = angle.distance * Math.cos(angle.phi)
      const z = angle.distance * Math.sin(angle.phi) * Math.cos(angle.theta)
      fg.cameraPosition({ x, y, z }, { x: 0, y: 0, z: 0 }, 0)
    },
    [],
  )

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (
        e.target instanceof HTMLInputElement ||
        e.target instanceof HTMLTextAreaElement
      ) {
        return
      }

      const fg = fgRef.current
      if (!fg) return

      const angle = cameraAngle.current
      const rotateSpeed = 0.1
      if (['=', '+', '-', '_', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
        userMovedCamera.current = true
      }

      switch (e.key) {
        case '=':
        case '+':
          angle.distance = Math.max(50, angle.distance * 0.9)
          updateCamera(angle)
          break
        case '-':
        case '_':
          angle.distance = angle.distance * 1.1
          updateCamera(angle)
          break
        case 'r':
        case 'R':
          fg.zoomToFit(400, 50)
          break
        case 'Escape':
          selectNode(null)
          setHoveredNode(null)
          break
        case 'ArrowLeft':
          e.preventDefault()
          angle.theta -= rotateSpeed
          updateCamera(angle)
          break
        case 'ArrowRight':
          e.preventDefault()
          angle.theta += rotateSpeed
          updateCamera(angle)
          break
        case 'ArrowUp':
          e.preventDefault()
          angle.phi = Math.max(0.1, angle.phi - rotateSpeed)
          updateCamera(angle)
          break
        case 'ArrowDown':
          e.preventDefault()
          angle.phi = Math.min(Math.PI - 0.1, angle.phi + rotateSpeed)
          updateCamera(angle)
          break
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [selectNode, setHoveredNode, updateCamera])

  const graphData = useMemo(() => {
    let nodes = apiData?.nodes || []
    let edges = apiData?.edges || []

    // Filter by node type
    nodes = nodes.filter((n) => showNodeTypes.has(n.type))

    // Filter by layer
    if (filterByLayer) {
      nodes = nodes.filter((n) => {
        if (n.type === 'LAYER') return n.text === filterByLayer
        if (n.type === 'TAXONOMY_PATH') {
          const segs = (n.metadata as Record<string, unknown>)?.segments
          return Array.isArray(segs) && segs[0] === filterByLayer
        }
        return n.layer === filterByLayer
      })
    }

    // Filter by category
    if (filterByCategory) {
      nodes = nodes.filter((n) => {
        if (n.type === 'CATEGORY') return n.text === filterByCategory
        if (n.type === 'TAXONOMY_PATH') {
          const segs = (n.metadata as Record<string, unknown>)?.segments
          return (
            Array.isArray(segs) &&
            segs.length >= 2 &&
            segs[segs.length - 1] === filterByCategory
          )
        }
        return n.category === filterByCategory
      })
    }

    // Note: searchQuery is NOT used to filter the graph - it's only for the
    // search dropdown autocomplete. Filtering by search would cause the graph
    // to re-render and reset positions when selecting a result.

    const visibleNodeIds = new Set(nodes.map((n) => n.id))

    // Filter edges by type AND by visible nodes
    edges = edges.filter(
      (e) =>
        showEdgeTypes.has(e.type) &&
        visibleNodeIds.has(e.source) &&
        visibleNodeIds.has(e.target),
    )

    // Taxonomy node hover labels: show only the LEAF segment so users see
    // the categorization name ("Primitives") rather than the full path
    // ("Physics/Primitives"). The parent-layer context is already conveyed
    // by the node's position in the graph (patterns cluster under it).
    const nodeLabel = (n: GraphNode): string => {
      if (n.type === 'TAXONOMY_PATH') {
        const segs = (n.metadata as Record<string, unknown>)?.segments
        if (Array.isArray(segs) && segs.length > 0) {
          return String(segs[segs.length - 1])
        }
        const text = n.text || ''
        return text.includes('/') ? text.split('/').pop() || text : text
      }
      return n.handle || n.text
    }

    const cache = nodeCache.current
    const presentIds = new Set((apiData?.nodes || []).map((n) => n.id))
    for (const id of cache.keys()) {
      if (!presentIds.has(id)) cache.delete(id)
    }
    const graphNodes = nodes.map((n) => {
      const fields = {
        id: n.id,
        name: nodeLabel(n),
        color: getNodeColor(n),
        type: n.type,
        layer: n.layer,
        val: getNodeSize(n),
      }
      const existing = cache.get(n.id)
      if (existing) return Object.assign(existing, fields)
      cache.set(n.id, fields)
      return fields
    })

    // A node that arrives after the first layout starts beside a neighbour
    // that already has a position, so it grows out of the graph rather than
    // flying in from the origin.
    for (const e of edges) {
      const source = cache.get(e.source)
      const target = cache.get(e.target)
      const pairs: Array<[Node3D | undefined, Node3D | undefined]> = [
        [source, target],
        [target, source],
      ]
      for (const [fresh, anchor] of pairs) {
        if (fresh && anchor && fresh.x === undefined && anchor.x !== undefined) {
          fresh.x = anchor.x + (Math.random() - 0.5) * 20
          fresh.y = (anchor.y ?? 0) + (Math.random() - 0.5) * 20
          fresh.z = (anchor.z ?? 0) + (Math.random() - 0.5) * 20
        }
      }
    }

    return {
      nodes: graphNodes,
      links: edges.map((e) => ({
        source: e.source,
        target: e.target,
        type: e.type,
        id: e.id,
      })),
    }
  }, [apiData, showNodeTypes, showEdgeTypes, filterByLayer, filterByCategory])

  // Zoom to fit when data first loads
  const hasData = graphData.nodes.length > 0
  const nodeCount = graphData.nodes.length
  const didInitialZoom = useRef(false)
  const framedCount = useRef(0)
  useEffect(() => {
    if (hasData && !didInitialZoom.current && fgRef.current) {
      didInitialZoom.current = true
      framedCount.current = nodeCount
      setTimeout(() => {
        fgRef.current?.zoomToFit(400, 50)
      }, 500)
    }
  }, [hasData])

  // Keep a growing graph in frame while an agent adds patterns, until the
  // person moves the camera or follows new patterns instead. Wait for the
  // layout to place the new nodes first.
  useEffect(() => {
    if (!didInitialZoom.current || userMovedCamera.current || following) return
    if (nodeCount <= framedCount.current) return
    framedCount.current = nodeCount
    const timer = setTimeout(() => {
      if (!userMovedCamera.current) fgRef.current?.zoomToFit(800, 50)
    }, 1500)
    return () => clearTimeout(timer)
  }, [nodeCount, following])

  // Fly to node when pendingFlyToNodeId changes
  useEffect(() => {
    if (!pendingFlyToNodeId || !fgRef.current) return

    // Find the node in the graph to get its position
    const fg = fgRef.current
    const graphNodes = fg.graphData?.()?.nodes || graphData.nodes
    const targetNode = graphNodes.find(
      (n: Node3D) => n.id === pendingFlyToNodeId,
    )

    if (targetNode && targetNode.x !== undefined) {
      const distance = 150
      fg.cameraPosition(
        { x: targetNode.x, y: targetNode.y, z: (targetNode.z || 0) + distance },
        { x: targetNode.x, y: targetNode.y, z: targetNode.z || 0 },
        1000,
      )
    }

    clearPendingFly()
  }, [pendingFlyToNodeId, clearPendingFly, graphData.nodes])

  const handleNodeClick = useCallback(
    (node: Node3D) => {
      selectNode(node.id)
      if (fgRef.current && node.x !== undefined) {
        const distance = 150
        fgRef.current.cameraPosition(
          { x: node.x, y: node.y, z: (node.z || 0) + distance },
          { x: node.x, y: node.y, z: node.z || 0 },
          1000,
        )
      }
    },
    [selectNode],
  )

  const handleNodeHover = useCallback(
    (node: Node3D | null) => {
      setHoveredNodeId(node?.id || null)
      setHoveredEdgeId(null)
      const originalNode = apiData?.nodes.find((n) => n.id === node?.id)
      if (node && originalNode) {
        setHoveredNode(originalNode)
      } else {
        setHoveredNode(null)
      }
      document.body.style.cursor = node ? 'pointer' : 'default'
    },
    [setHoveredNode, apiData?.nodes],
  )

  const handleLinkClick = useCallback(
    (link: Link3D) => {
      // When clicking an edge, select the target node
      const targetId = typeof link.target === 'string' ? link.target : link.target?.id
      if (targetId) {
        selectNode(targetId)
        // Also fly to the target node
        const fg = fgRef.current
        if (fg) {
          const graphNodes = fg.graphData?.()?.nodes || []
          const targetNode = graphNodes.find((n: Node3D) => n.id === targetId)
          if (targetNode && targetNode.x !== undefined) {
            const distance = 150
            fg.cameraPosition(
              { x: targetNode.x, y: targetNode.y, z: (targetNode.z || 0) + distance },
              { x: targetNode.x, y: targetNode.y, z: targetNode.z || 0 },
              1000,
            )
          }
        }
      }
    },
    [selectNode],
  )

  const handleLinkHover = useCallback(
    (link: Link3D | null) => {
      setHoveredEdgeId(link?.id || null)
      setHoveredNodeId(null)
      setHoveredNode(null)
      document.body.style.cursor = link ? 'pointer' : 'default'
    },
    [setHoveredNode],
  )

  if (isLoading) {
    return (
      <div className="absolute inset-0 bg-zinc-950 flex items-center justify-center">
        <div className="text-zinc-400">Loading taxonomy...</div>
      </div>
    )
  }

  return (
    <div
      className="absolute inset-0 bg-zinc-950"
      onPointerDown={() => {
        userMovedCamera.current = true
      }}
      onWheel={() => {
        userMovedCamera.current = true
      }}
    >
      <ForceGraph3D
        ref={fgRef}
        width={dimensions.width}
        height={dimensions.height}
        graphData={graphData}
        nodeId="id"
        nodeLabel="name"
        nodeColor={(node: Node3D) =>
          node.id === hoveredNodeId
            ? '#ffffff'
            : recentArrivals.has(node.id)
              ? ARRIVAL_COLOR
              : node.color
        }
        nodeRelSize={3}
        nodeVal={(node: Node3D) => (recentArrivals.has(node.id) ? node.val * 3 : node.val)}
        nodeThreeObject={undefined}
        nodeThreeObjectExtend={false}
        linkColor={(link: Link3D) => {
          // Highlight hovered edge
          if (link.id === hoveredEdgeId) return '#ffffff'
          // Highlight edges connected to hovered node
          if (hoveredNodeId) {
            const sourceId =
              typeof link.source === 'string' ? link.source : link.source?.id
            const targetId =
              typeof link.target === 'string' ? link.target : link.target?.id
            if (sourceId === hoveredNodeId || targetId === hoveredNodeId) {
              return '#818cf8'
            }
          }
          return EDGE_TYPE_COLORS[link.type] || '#3f3f46'
        }}
        linkWidth={(link: Link3D) => {
          if (link.id === hoveredEdgeId) return 3
          if (hoveredNodeId) {
            const sourceId =
              typeof link.source === 'string' ? link.source : link.source?.id
            const targetId =
              typeof link.target === 'string' ? link.target : link.target?.id
            if (sourceId === hoveredNodeId || targetId === hoveredNodeId) {
              return 2
            }
          }
          return 0.5
        }}
        linkOpacity={0.6}
        linkHoverPrecision={4}
        linkDirectionalArrowLength={4}
        linkDirectionalArrowRelPos={1}
        linkDirectionalArrowColor={() => '#52525b'}
        onNodeClick={handleNodeClick}
        onNodeHover={handleNodeHover}
        onLinkClick={handleLinkClick}
        onLinkHover={handleLinkHover}
        enableNodeDrag={true}
        enableNavigationControls={true}
        cooldownTime={3000}
        warmupTicks={50}
        backgroundColor="#09090b"
        showNavInfo={false}
        controlType="orbit"
      />

      <HoverTooltip hoveredEdgeId={hoveredEdgeId} edges={apiData?.edges || []} nodes={apiData?.nodes || []} />
    </div>
  )
}

function HoverTooltip({
  hoveredEdgeId,
  edges,
  nodes
}: {
  hoveredEdgeId: string | null
  edges: GraphEdge[]
  nodes: GraphNode[]
}) {
  const hoveredNode = useAppStore((s) => s.hoveredNode)

  // Show edge tooltip
  if (hoveredEdgeId) {
    const edge = edges.find(e => e.id === hoveredEdgeId)
    if (edge) {
      const sourceNode = nodes.find(n => n.id === edge.source)
      const targetNode = nodes.find(n => n.id === edge.target)
      const edgeColor = EDGE_TYPE_COLORS[edge.type] || '#71717a'

      return (
        <div
          className="absolute bottom-20 left-1/2 -translate-x-1/2 bg-zinc-900/95 backdrop-blur-md border border-zinc-700 p-3 rounded-lg max-w-[400px] shadow-lg pointer-events-none z-[100]"
          style={{ borderLeftColor: edgeColor, borderLeftWidth: 3 }}
        >
          <div className="flex items-center gap-2 mb-2">
            <span
              className="px-1.5 py-0.5 rounded text-[10px] font-medium uppercase"
              style={{ backgroundColor: edgeColor + '20', color: edgeColor }}
            >
              {edge.type.replace(/_/g, ' ')}
            </span>
          </div>
          <div className="text-sm text-zinc-300">
            <span className="text-zinc-100 font-medium">{sourceNode?.handle || sourceNode?.text}</span>
            <span className="text-zinc-500 mx-2">→</span>
            <span className="text-zinc-100 font-medium">{targetNode?.handle || targetNode?.text}</span>
          </div>
        </div>
      )
    }
  }

  if (!hoveredNode) return null

  const layerColor = hoveredNode.layer
    ? LAYER_COLORS[hoveredNode.layer]
    : NODE_TYPE_COLORS[hoveredNode.type]

  return (
    <div
      className="absolute bottom-20 left-1/2 -translate-x-1/2 bg-zinc-900/95 backdrop-blur-md border border-zinc-700 p-3 rounded-lg max-w-[320px] shadow-lg pointer-events-none z-[100]"
      style={{ borderLeftColor: layerColor, borderLeftWidth: 3 }}
    >
      <div className="flex items-center gap-2 mb-1">
        <span
          className="px-1.5 py-0.5 rounded text-[10px] font-medium uppercase"
          style={{ backgroundColor: layerColor + '20', color: layerColor }}
        >
          {hoveredNode.type}
        </span>
        {hoveredNode.layer && (
          <span className="text-[10px] text-zinc-500">{hoveredNode.layer}</span>
        )}
      </div>
      <h4 className="text-sm font-medium text-zinc-100 mb-1">
        {hoveredNode.handle || hoveredNode.text}
      </h4>
      {hoveredNode.gloss && (
        <p className="text-xs text-zinc-400 leading-relaxed">
          {hoveredNode.gloss}
        </p>
      )}
    </div>
  )
}
