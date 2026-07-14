import { Link } from 'react-router-dom'
import { ArrowRight, Bot } from 'lucide-react'
import { SemaLogo } from '@/components/SemaLogo'
import { LicenseLine } from '@/components/LicenseLine'
import { NavItem } from '@/components/ui'
import { HandshakeDemo } from '@/components/HandshakeDemo'

const REGISTRY_ENABLED = import.meta.env.VITE_ENABLE_WORKSPACE === 'true'

/**
 * The front door. Per docs/site-architecture.md this page has exactly
 * three jobs: state the claim, show one proof (the handshake demo),
 * and route the visitor — browse or connect. Everything else lives on
 * its own page.
 */
export function HomePage() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col">
      {/* Subtle background texture */}
      <div
        className="fixed inset-0 pointer-events-none opacity-[0.02]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />

      <div className="relative flex-1 overflow-hidden">
        {/* Background gradient mesh */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-1/2 -left-1/4 w-full h-full bg-gradient-radial from-emerald-900/20 via-transparent to-transparent blur-3xl" />
          <div className="absolute -bottom-1/2 -right-1/4 w-full h-full bg-gradient-radial from-zinc-800/30 via-transparent to-transparent blur-3xl" />
        </div>

        <div className="relative max-w-6xl mx-auto px-6 pt-12 pb-20">
          {/* Header — wordmark + quiet links */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-5 mb-20">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-emerald-500/20 to-emerald-500/5 ring-1 ring-inset ring-emerald-500/20 flex items-center justify-center text-emerald-400">
                <SemaLogo className="w-5 h-5" />
              </div>
              <h1 className="text-lg font-semibold tracking-tight">Sema</h1>
            </div>
            <nav className="flex items-center gap-5 sm:gap-7 flex-wrap sm:justify-end">
              <NavItem href="/api/paper">Paper</NavItem>
              <NavItem href="https://github.com/emergent-wisdom/sema">GitHub</NavItem>
              <NavItem href="https://discord.gg/hRhVqAuDYQ">Discord</NavItem>
              <NavItem to="/docs">Docs</NavItem>
              {REGISTRY_ENABLED && <NavItem to="/registry">Registry</NavItem>}
            </nav>
          </div>

          {/* Hero — claim + proof, side by side */}
          <div className="grid lg:grid-cols-[minmax(0,1.15fr)_minmax(0,1fr)] gap-10 lg:gap-14 items-center">
            <div className="rise-in">
              <p className="ref-mono text-emerald-400/80 mb-4 text-sm">
                word = hash(canonical(definition))
              </p>
              <h2 className="text-5xl sm:text-6xl font-light tracking-[-0.03em] text-zinc-100 leading-[1.05] mb-6">
                When the hash
                <br />
                <span className="text-emerald-400">is the word.</span>
              </h2>
              <p className="text-lg text-zinc-400 leading-relaxed max-w-lg mb-10">
                A shared vocabulary agents can verify. When two agents share
                a pattern hash, they share exact semantics — and when they
                don't, the handshake fails closed.
              </p>

              {/* The two paths */}
              <div className="flex flex-col sm:flex-row gap-3">
                {REGISTRY_ENABLED ? (
                  <>
                    <Link
                      to="/registry"
                      className="inline-flex items-center justify-center gap-2 rounded-lg bg-emerald-400 px-6 py-3 text-sm font-medium text-zinc-950 transition-colors hover:bg-emerald-300"
                    >
                      Browse vocabularies
                      <ArrowRight className="w-4 h-4" />
                    </Link>
                    <Link
                      to="/connect"
                      className="inline-flex items-center justify-center gap-2 rounded-lg border border-zinc-700 bg-zinc-900/70 px-6 py-3 text-sm font-medium text-zinc-200 transition-colors hover:border-zinc-600 hover:bg-zinc-800"
                    >
                      <Bot className="w-4 h-4" />
                      Connect my agent
                    </Link>
                  </>
                ) : (
                  <>
                    <Link
                      to="/graph"
                      className="inline-flex items-center justify-center gap-2 rounded-lg bg-emerald-400 px-6 py-3 text-sm font-medium text-zinc-950 transition-colors hover:bg-emerald-300"
                    >
                      Explore the vocabulary
                      <ArrowRight className="w-4 h-4" />
                    </Link>
                    <a
                      href="/install.md"
                      className="inline-flex items-center justify-center gap-2 rounded-lg border border-zinc-700 bg-zinc-900/70 px-6 py-3 text-sm font-medium text-zinc-200 transition-colors hover:border-zinc-600 hover:bg-zinc-800"
                    >
                      <Bot className="w-4 h-4" />
                      Connect my agent
                    </a>
                  </>
                )}
              </div>
            </div>

            <div className="rise-in flex lg:justify-end" style={{ animationDelay: '0.15s' }}>
              <HandshakeDemo />
            </div>
          </div>
        </div>
      </div>

      <footer className="relative border-t border-zinc-800/50">
        <div className="max-w-6xl mx-auto px-6 py-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <p className="text-sm text-zinc-500">
            452 patterns · MCP server · content-addressed since the first hash
          </p>
          <LicenseLine />
        </div>
      </footer>
    </div>
  )
}

export default HomePage
