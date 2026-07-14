import { Link, useParams } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import GraphPageLazy from './GraphPageLazy'

/**
 * The graph view of one vocabulary. Same data, different lens — reached
 * from the vocabulary page's view switch. Reuses the existing 3D graph
 * (which renders the active vocabulary) with a way back.
 */
export default function VocabularyGraphRoute() {
  const { slug } = useParams()
  return (
    <div className="min-h-screen bg-zinc-950">
      <div className="fixed bottom-4 left-4 z-[60]">
        <Link
          to={`/vocabularies/${slug}`}
          className="inline-flex items-center gap-2 rounded-lg border border-zinc-700 bg-zinc-900/90 px-3 py-2 text-sm text-zinc-300 backdrop-blur transition-colors hover:border-zinc-600 hover:text-zinc-100"
        >
          <ArrowLeft className="h-4 w-4" />
          Patterns
        </Link>
      </div>
      <GraphPageLazy showBackButton={false} />
    </div>
  )
}
