import { ExternalLink } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'
import { SemaLogo } from '@/components/SemaLogo'
import { cn } from '@/lib/utils'

// The local view has two destinations of its own. Documentation and the
// public library registry live on semahash.org.
const NAV_ITEMS = [
  { label: 'Vocabulary', to: '/', matches: (path: string) => path === '/' },
  { label: 'Graph', to: '/graph', matches: (path: string) => path.startsWith('/graph') },
]

const EXTERNAL_LINK_CLASS =
  'inline-flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm text-zinc-400 transition-colors hover:bg-zinc-900/60 hover:text-zinc-100'

export function LocalHeader({ maxWidthClass = 'max-w-[1400px]' }: { maxWidthClass?: string }) {
  const location = useLocation()

  return (
    <header className="sticky top-0 z-50 border-b border-zinc-800/60 bg-zinc-950/90 backdrop-blur-xl">
      <div className={cn('mx-auto flex min-h-16 items-center justify-between gap-4 px-4 sm:px-6', maxWidthClass)}>
        <Link to="/" className="flex shrink-0 items-center gap-3">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/10 text-emerald-400">
            <SemaLogo className="h-5 w-5" />
          </span>
          <span className="hidden sm:block">
            <span className="block text-sm font-semibold tracking-tight text-zinc-100">Sema</span>
            <span className="block text-[11px] text-zinc-500">Local view</span>
          </span>
        </Link>

        <nav className="flex items-center gap-1" aria-label="Primary navigation">
          {NAV_ITEMS.map((item) => {
            const active = item.matches(location.pathname)
            return (
              <Link
                key={item.to}
                to={item.to}
                aria-current={active ? 'page' : undefined}
                className={cn(
                  'rounded-lg px-3 py-2 text-sm transition-colors',
                  active ? 'bg-zinc-900 text-zinc-100' : 'text-zinc-400 hover:bg-zinc-900/60 hover:text-zinc-100',
                )}
              >
                {item.label}
              </Link>
            )
          })}
        </nav>

        <div className="flex shrink-0 items-center gap-1">
          <a
            href="https://semahash.org/docs"
            target="_blank"
            rel="noopener noreferrer"
            className={cn(EXTERNAL_LINK_CLASS, 'hidden sm:inline-flex')}
          >
            Docs
            <ExternalLink className="h-3.5 w-3.5 text-zinc-600" aria-hidden="true" />
          </a>
          <a
            href="https://semahash.org/registry"
            target="_blank"
            rel="noopener noreferrer"
            className={EXTERNAL_LINK_CLASS}
            title="Libraries published on semahash.org"
          >
            semahash.org
            <ExternalLink className="h-3.5 w-3.5 text-zinc-600" aria-hidden="true" />
          </a>
        </div>
      </div>
    </header>
  )
}
