import { lazy, Suspense } from 'react'

const GraphPage = lazy(() => import('./GraphPage'))

export default function GraphPageLazy({ showBackButton = true }: { showBackButton?: boolean }) {
  return (
    <Suspense fallback={<div className="flex items-center justify-center h-screen bg-background text-muted-foreground">Loading graph...</div>}>
      <GraphPage showBackButton={showBackButton} />
    </Suspense>
  )
}
