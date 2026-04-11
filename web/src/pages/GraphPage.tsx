import { useEffect, useRef } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { GraphCanvas } from '@/components/GraphCanvas'
import { DetailsPanel } from '@/components/DetailsPanel'
import { TopBar } from '@/components/TopBar'
import { useAppStore } from '@/stores/appStore'
import { useGraph } from '@/hooks/useApi'

export function GraphPage() {
  const [searchParams] = useSearchParams()
  const nodeId = searchParams.get('node')
  const { selectNodeAndFly, selectNode, setDetailsPanelOpen } = useAppStore()
  const { data: graphData } = useGraph()
  const didFlyToNode = useRef(false)

  // If there's a node param, wait for graph to load then fly to it
  useEffect(() => {
    if (nodeId && graphData && graphData.nodes.length > 0 && !didFlyToNode.current) {
      didFlyToNode.current = true
      // Select node immediately to open panel
      selectNode(nodeId)
      setDetailsPanelOpen(true)
      // Delay fly-to so graph has time to position nodes
      const timer = setTimeout(() => {
        selectNodeAndFly(nodeId)
      }, 1500)
      return () => clearTimeout(timer)
    }
  }, [nodeId, graphData, selectNodeAndFly, selectNode, setDetailsPanelOpen])

  return (
    <div className="h-screen w-screen overflow-hidden bg-zinc-950">
      <GraphCanvas />
      <div className="hidden sm:block">
        <TopBar />
      </div>
      <div className="hidden sm:block">
        <DetailsPanel />
      </div>

      {/* Back button */}
      <Link
        to="/"
        className="absolute top-4 left-4 z-50 flex items-center gap-2 px-2 py-1.5 sm:px-3 sm:py-2 bg-zinc-900/90 backdrop-blur-md border border-zinc-800 rounded-lg text-xs sm:text-sm text-zinc-300 hover:text-zinc-100 hover:bg-zinc-800 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span className="hidden sm:inline">Back to List</span>
      </Link>
    </div>
  )
}

export default GraphPage;
