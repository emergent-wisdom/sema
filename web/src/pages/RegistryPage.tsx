import { useEffect, useState, type ReactNode } from 'react'
import { Link } from 'react-router-dom'
import type { MetaFunction } from 'react-router'
import {
  ArrowLeft,
  ArrowRight,
  Bot,
  Check,
  ChevronRight,
  CircleUserRound,
  Copy,
  ExternalLink,
  Github,
  Library,
  Link2,
  Loader2,
  Lock,
  LogOut,
  Network,
  Plus,
  ShieldCheck,
} from 'lucide-react'
import { SemaLogo } from '@/components/SemaLogo'
import { LicenseLine } from '@/components/LicenseLine'
import { cn } from '@/lib/utils'

type Screen = 'discover' | 'connect' | 'create'
type Preset = 'full' | 'standard' | 'empty'
type McpClientId = 'claude-code' | 'codex' | 'cursor' | 'vscode' | 'claude-desktop'

type GitHubUser = {
  login?: string
  name?: string | null
  avatar_url?: string | null
}

type AuthState = {
  authenticated: boolean
  user: GitHubUser | null
  github_oauth_configured: boolean
  session_configured: boolean
}

type WorkspaceSummary = {
  workspace_id: string
  label: string
  pattern_count: number
  vocabulary_root_stub: string
}

const MCP_ARGS = ['--from', 'semahash[mcp]', 'sema', 'mcp']
const AGENT_KICKOFF_PROMPT =
  'Use the Sema tools to help me build a vocabulary. First call sema_use with no arguments and report which vocabulary is active and whether it is bundled/read-only. Search existing patterns before proposing new ones. Draft and validate each new pattern, and wait for my approval before calling sema_mint.'

const MCP_SETUPS: Array<{
  id: McpClientId
  label: string
  location: string
  snippet: string
}> = [
  {
    id: 'claude-code',
    label: 'Claude Code',
    location: 'Run in a terminal',
    snippet: 'claude mcp add sema -- uvx --from "semahash[mcp]" sema mcp',
  },
  {
    id: 'codex',
    label: 'Codex',
    location: 'Run in a terminal',
    snippet: 'codex mcp add sema -- uvx --from "semahash[mcp]" sema mcp',
  },
  {
    id: 'cursor',
    label: 'Cursor',
    location: 'Add to .cursor/mcp.json',
    snippet: JSON.stringify({ mcpServers: { sema: { command: 'uvx', args: MCP_ARGS } } }, null, 2),
  },
  {
    id: 'vscode',
    label: 'VS Code',
    location: 'Add to .vscode/mcp.json',
    snippet: JSON.stringify({ servers: { sema: { type: 'stdio', command: 'uvx', args: MCP_ARGS } } }, null, 2),
  },
  {
    id: 'claude-desktop',
    label: 'Claude Desktop',
    location: 'Add to claude_desktop_config.json',
    snippet: JSON.stringify({ mcpServers: { sema: { command: 'uvx', args: MCP_ARGS } } }, null, 2),
  },
]

export const meta: MetaFunction = ({ matches }) => {
  const inherited = matches.flatMap((match) => match.meta ?? [])
  const overridden = inherited.filter(
    (entry) => !('title' in entry) && !('name' in entry && entry.name === 'description')
  )
  return [
    ...overridden,
    { title: 'Explore Sema — Patterns and Vocabularies' },
    {
      name: 'description',
      content: 'Discover public agent patterns and vocabularies, connect your agent, and create a vocabulary of your own.',
    },
  ]
}

export function RegistryPage({ initialScreen = 'discover' }: { initialScreen?: Screen } = {}) {
  const [auth, setAuth] = useState<AuthState | null>(null)
  const [workspace, setWorkspace] = useState<WorkspaceSummary | null>(null)
  const [authLoading, setAuthLoading] = useState(true)
  const [screen, setScreen] = useState<Screen>(initialScreen)

  useEffect(() => {
    let active = true

    Promise.all([
      fetch('/api/me', { credentials: 'same-origin' }).then((response) => (
        response.ok ? response.json() as Promise<AuthState> : null
      )),
      fetch('/api/workspace').then((response) => (
        response.ok ? response.json() as Promise<WorkspaceSummary> : null
      )),
    ])
      .then(([authState, workspaceState]) => {
        if (!active) return
        setAuth(authState)
        setWorkspace(workspaceState)
      })
      .catch(() => {
        if (!active) return
        setAuth(null)
        setWorkspace(null)
      })
      .finally(() => {
        if (active) setAuthLoading(false)
      })

    return () => {
      active = false
    }
  }, [])

  const authenticated = Boolean(auth?.authenticated && auth.user?.login)
  const authReady = Boolean(auth?.github_oauth_configured && auth?.session_configured)

  const startAuth = () => {
    window.location.assign('/auth/github/start')
  }

  const openProtectedScreen = (nextScreen: Exclude<Screen, 'discover'>) => {
    if (!authenticated) {
      startAuth()
      return
    }
    setScreen(nextScreen)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <div
        className="fixed inset-0 pointer-events-none opacity-[0.018]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />

      <RegistryHeader
        authenticated={authenticated}
        authLoading={authLoading}
        authReady={authReady}
        user={auth?.user}
        setScreen={setScreen}
        startAuth={startAuth}
        openCreate={() => openProtectedScreen('create')}
      />

      {screen === 'connect' ? (
        <AgentConnection
          onBack={() => setScreen('discover')}
          onCreate={() => setScreen('create')}
        />
      ) : screen === 'create' ? (
        <VocabularyCreator
          user={auth?.user}
          onBack={() => setScreen('discover')}
          onConnect={() => setScreen('connect')}
        />
      ) : (
        <Discovery
          authenticated={authenticated}
          workspace={workspace}
          startAuth={startAuth}
          openConnect={() => openProtectedScreen('connect')}
          openCreate={() => openProtectedScreen('create')}
        />
      )}

      <footer className="relative mt-16 border-t border-zinc-800/60">
        <div className="mx-auto flex max-w-7xl flex-col justify-between gap-3 px-6 py-7 text-sm text-zinc-500 sm:flex-row sm:items-center">
          <p>Sema public registry preview</p>
          <LicenseLine />
        </div>
      </footer>
    </div>
  )
}

function RegistryHeader({
  authenticated,
  authLoading,
  authReady,
  user,
  setScreen,
  startAuth,
  openCreate,
}: {
  authenticated: boolean
  authLoading: boolean
  authReady: boolean
  user?: GitHubUser | null
  setScreen: (screen: Screen) => void
  startAuth: () => void
  openCreate: () => void
}) {
  return (
    <header className="relative z-40 border-b border-zinc-800/60 bg-zinc-950/85 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-5 px-6 py-4">
        <button
          type="button"
          onClick={() => setScreen('discover')}
          className="flex items-center gap-3 text-left"
        >
          <span className="flex h-10 w-10 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/10 text-emerald-400">
            <SemaLogo className="h-6 w-6" />
          </span>
          <span>
            <span className="block text-base font-semibold tracking-tight">Sema</span>
            <span className="block text-xs text-zinc-500">Patterns for agents</span>
          </span>
        </button>


        <div className="flex items-center gap-2">
          {authLoading ? (
            <span className="inline-flex items-center gap-2 px-3 py-2 text-sm text-zinc-500">
              <Loader2 className="h-4 w-4 animate-spin" />
              Checking account
            </span>
          ) : authenticated ? (
            <>
              <div className="hidden items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900/60 px-3 py-2 sm:flex">
                {user?.avatar_url ? (
                  <img src={user.avatar_url} alt="" className="h-5 w-5 rounded-full" />
                ) : (
                  <CircleUserRound className="h-4 w-4 text-zinc-500" />
                )}
                <span className="text-sm text-zinc-300">@{user?.login}</span>
              </div>
              <button
                type="button"
                onClick={openCreate}
                className="inline-flex items-center gap-2 rounded-lg bg-emerald-400 px-3.5 py-2 text-sm font-medium text-zinc-950 transition-colors hover:bg-emerald-300"
              >
                <Plus className="h-4 w-4" />
                <span className="hidden sm:inline">Create vocabulary</span>
                <span className="sm:hidden">Create</span>
              </button>
              <a
                href="/auth/logout"
                aria-label="Sign out"
                className="rounded-lg border border-zinc-800 p-2 text-zinc-500 transition-colors hover:text-zinc-200"
              >
                <LogOut className="h-4 w-4" />
              </a>
            </>
          ) : (
            <button
              type="button"
              onClick={startAuth}
              disabled={!authReady}
              className="inline-flex items-center gap-2 rounded-lg border border-zinc-700 bg-zinc-100 px-4 py-2 text-sm font-medium text-zinc-950 transition-colors hover:bg-white disabled:cursor-not-allowed disabled:opacity-50"
            >
              <Github className="h-4 w-4" />
              Log in
            </button>
          )}
        </div>
      </div>
    </header>
  )
}

function Discovery({
  authenticated,
  workspace,
  startAuth,
  openConnect,
  openCreate,
}: {
  authenticated: boolean
  workspace: WorkspaceSummary | null
  startAuth: () => void
  openConnect: () => void
  openCreate: () => void
}) {
  return (
    <main className="relative">
      <section className="overflow-hidden border-b border-zinc-800/50">
        <div className="absolute left-1/2 top-0 h-[420px] w-[900px] -translate-x-1/2 rounded-full bg-emerald-900/10 blur-3xl" />
        <div className="relative mx-auto max-w-7xl px-6 py-14 sm:py-20">
          <div className="mx-auto max-w-4xl text-center">
            <h1 className="text-4xl font-light tracking-tight text-zinc-50 sm:text-5xl">
              Public vocabularies your agent can verify.
            </h1>
            <p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-zinc-400 sm:text-lg">
              Browse published pattern collections, connect your agent to use
              them, and publish a vocabulary of your own.
            </p>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
              <button
                type="button"
                onClick={openConnect}
                className="inline-flex items-center gap-2 rounded-lg bg-emerald-400 px-5 py-2.5 text-sm font-medium text-zinc-950 transition-colors hover:bg-emerald-300"
              >
                <Bot className="h-4 w-4" />
                Connect my agent
              </button>
              <button
                type="button"
                onClick={authenticated ? openCreate : startAuth}
                className="inline-flex items-center gap-2 rounded-lg border border-zinc-700 bg-zinc-900/70 px-5 py-2.5 text-sm font-medium text-zinc-200 transition-colors hover:border-zinc-600 hover:bg-zinc-800"
              >
                <Github className="h-4 w-4" />
                {authenticated ? 'Create a vocabulary' : 'Log in to create'}
              </button>
            </div>
          </div>
        </div>
      </section>

      <section className="border-y border-zinc-800/60 bg-zinc-900/20">
        <div className="mx-auto max-w-7xl px-6 py-14">
          <SectionHeading
            kicker="Vocabularies"
            title="Public vocabularies"
            body="Browse stable, published collections your agent can use. Community publishing is the next registry milestone."
          />
          <div className="mt-7 grid gap-4 lg:grid-cols-[minmax(0,1.25fr)_minmax(320px,.75fr)]">
            <VocabularyCard workspace={workspace} openConnect={openConnect} />
            <button
              type="button"
              onClick={openCreate}
              className="group flex min-h-64 flex-col items-start justify-between rounded-2xl border border-dashed border-zinc-700 bg-zinc-950/30 p-6 text-left transition-colors hover:border-emerald-500/40 hover:bg-emerald-500/[0.03]"
            >
              <span className="flex h-11 w-11 items-center justify-center rounded-xl border border-zinc-700 bg-zinc-900 text-zinc-400 transition-colors group-hover:border-emerald-500/30 group-hover:text-emerald-300">
                <Plus className="h-5 w-5" />
              </span>
              <span>
                <span className="block text-lg font-medium text-zinc-200">Publish your vocabulary</span>
                <span className="mt-2 block max-w-sm text-sm leading-6 text-zinc-500">
                  Log in, create a vocabulary, then connect an agent to work on it with you.
                </span>
              </span>
              <span className="inline-flex items-center gap-2 text-sm font-medium text-emerald-300">
                {authenticated ? 'Start creating' : 'Log in to start'}
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </span>
            </button>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-14">
        <SectionHeading
          kicker="Your path"
          title="Explore first. Create when you are ready."
          body="Account setup should follow value, not block it."
        />
        <div className="mt-7 grid gap-4 md:grid-cols-3">
          <JourneyStep
            number="01"
            icon={Github}
            title="Log in"
            body="Use GitHub as your identity when you want to save or publish. Browsing remains public."
            action={authenticated ? 'You are signed in' : 'Log in with GitHub'}
            onClick={authenticated ? undefined : startAuth}
            complete={authenticated}
          />
          <JourneyStep
            number="02"
            icon={Library}
            title="Create your own"
            body="Start from the public library, a smaller preset, or an empty vocabulary."
            action="Create vocabulary"
            onClick={openCreate}
          />
          <JourneyStep
            number="03"
            icon={Bot}
            title="Connect your agent"
            body="Choose your MCP client and connect it to the vocabulary you selected."
            action="Connect agent"
            onClick={openConnect}
          />
        </div>
      </section>
    </main>
  )
}

function VocabularyCard({
  workspace,
  openConnect,
}: {
  workspace: WorkspaceSummary | null
  openConnect: () => void
}) {
  return (
    <article className="relative overflow-hidden rounded-2xl border border-emerald-500/20 bg-gradient-to-br from-emerald-500/[0.08] via-zinc-900/70 to-zinc-950 p-6">
      <div className="absolute right-0 top-0 h-52 w-52 rounded-full bg-emerald-500/5 blur-3xl" />
      <div className="relative flex h-full min-h-64 flex-col justify-between gap-8">
        <div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-start">
          <div className="flex items-start gap-4">
            <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/10 text-emerald-300">
              <SemaLogo className="h-7 w-7" />
            </span>
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h3 className="text-xl font-medium text-zinc-50">Sema Bootstrap</h3>
                <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-2 py-0.5 text-[11px] font-medium text-emerald-300">Official</span>
              </div>
              <p className="mt-1 text-sm text-zinc-500">emergent-wisdom/sema</p>
            </div>
          </div>
          <span className="inline-flex w-fit items-center gap-1.5 rounded-full border border-zinc-700 bg-zinc-950/50 px-3 py-1.5 text-xs text-zinc-400">
            <ShieldCheck className="h-3.5 w-3.5 text-emerald-400" />
            Public & verified
          </span>
        </div>
        <p className="max-w-2xl text-sm leading-6 text-zinc-400">
          The shared starting vocabulary for agent reasoning, coordination, verification, and infrastructure.
        </p>
        <div className="grid gap-3 sm:grid-cols-3">
          <VocabularyFact label="Patterns" value={String(workspace?.pattern_count ?? 452)} />
          <VocabularyFact label="Root" value={workspace?.vocabulary_root_stub ?? '46e651aeeb832fdc'} mono />
          <VocabularyFact label="License" value="CC BY 4.0" />
        </div>
        <div className="flex flex-wrap gap-3">
          <Link
            to="/vocabularies/bootstrap"
            className="inline-flex items-center gap-2 rounded-lg bg-zinc-100 px-4 py-2.5 text-sm font-medium text-zinc-950 transition-colors hover:bg-white"
          >
            Browse vocabulary
            <ExternalLink className="h-4 w-4" />
          </Link>
          <button
            type="button"
            onClick={openConnect}
            className="inline-flex items-center gap-2 rounded-lg border border-zinc-700 bg-zinc-900/70 px-4 py-2.5 text-sm font-medium text-zinc-200 transition-colors hover:border-zinc-600 hover:bg-zinc-800"
          >
            <Bot className="h-4 w-4" />
            Connect agent
          </button>
        </div>
      </div>
    </article>
  )
}

function AgentConnection({ onBack, onCreate }: { onBack: () => void; onCreate: () => void }) {
  const [copied, setCopied] = useState(false)
  const [copiedPrompt, setCopiedPrompt] = useState(false)
  const [clientId, setClientId] = useState<McpClientId>('claude-code')
  const selectedSetup = MCP_SETUPS.find((setup) => setup.id === clientId) ?? MCP_SETUPS[0]

  const copyCommand = async () => {
    await navigator.clipboard.writeText(selectedSetup.snippet)
    setCopied(true)
    setTimeout(() => setCopied(false), 1800)
  }

  const copyPrompt = async () => {
    await navigator.clipboard.writeText(AGENT_KICKOFF_PROMPT)
    setCopiedPrompt(true)
    setTimeout(() => setCopiedPrompt(false), 1800)
  }

  return (
    <main className="relative mx-auto max-w-5xl px-6 py-12">
      <BackButton onClick={onBack}>Back to explore</BackButton>
      <div className="mt-8 grid gap-6 lg:grid-cols-[minmax(0,1fr)_300px]">
        <section className="rounded-2xl border border-zinc-800 bg-zinc-900/45 p-6 sm:p-8">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/10 text-emerald-300">
            <Bot className="h-6 w-6" />
          </div>
          <p className="mt-7 text-xs font-medium uppercase tracking-[0.2em] text-emerald-400">Step 3</p>
          <h1 className="mt-2 text-3xl font-light tracking-tight text-zinc-50">Connect an MCP-compatible agent</h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-zinc-400">
            MCP standardizes the server protocol, while each agent has its own setup format. Choose your client below; every option starts the same local Sema stdio server.
          </p>
          <p className="mt-3 text-sm text-zinc-500">
            Prerequisite: install{' '}
            <a
              href="https://docs.astral.sh/uv/getting-started/installation/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-emerald-300 underline decoration-emerald-500/30 underline-offset-4 hover:text-emerald-200"
            >
              uv
            </a>{' '}
            once so the <code className="text-zinc-300">uvx</code> command is available.
          </p>

          <div className="mt-8">
            <p className="text-xs font-medium uppercase tracking-wider text-zinc-500">Choose your client</p>
            <div className="mt-3 flex flex-wrap gap-2">
              {MCP_SETUPS.map((setup) => (
                <button
                  key={setup.id}
                  type="button"
                  onClick={() => {
                    setClientId(setup.id)
                    setCopied(false)
                  }}
                  className={cn(
                    'rounded-lg border px-3 py-2 text-sm transition-colors',
                    clientId === setup.id
                      ? 'border-emerald-500/40 bg-emerald-500/10 text-emerald-200'
                      : 'border-zinc-800 bg-zinc-950/35 text-zinc-400 hover:border-zinc-700 hover:text-zinc-200'
                  )}
                >
                  {setup.label}
                </button>
              ))}
            </div>
          </div>

          <div className="mt-8 rounded-xl border border-zinc-800 bg-zinc-950/80 p-4">
            <div className="mb-3 flex items-center justify-between gap-3">
              <span className="text-xs font-medium uppercase tracking-wider text-zinc-500">{selectedSetup.location}</span>
              <button
                type="button"
                onClick={copyCommand}
                className="inline-flex items-center gap-1.5 text-xs text-zinc-400 hover:text-zinc-100"
              >
                {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                {copied ? 'Copied' : 'Copy'}
              </button>
            </div>
            <pre className="overflow-x-auto whitespace-pre text-sm leading-6 text-emerald-300">{selectedSetup.snippet}</pre>
          </div>

          <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-950/35 p-4">
            <div className="flex items-center justify-between gap-3">
              <p className="text-sm font-medium text-zinc-200">Start the working session</p>
              <button type="button" onClick={copyPrompt} className="inline-flex items-center gap-1.5 text-xs text-zinc-400 hover:text-zinc-100">
                {copiedPrompt ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                {copiedPrompt ? 'Copied' : 'Copy prompt'}
              </button>
            </div>
            <p className="mt-2 text-sm text-zinc-500">After Sema appears in your client's tool list, send:</p>
            <blockquote className="mt-3 border-l-2 border-emerald-500/40 pl-4 text-sm text-zinc-300">
              {AGENT_KICKOFF_PROMPT}
            </blockquote>
          </div>

          <div className="mt-8 flex flex-wrap gap-3">
            <button
              type="button"
              onClick={onCreate}
              className="inline-flex items-center gap-2 rounded-lg bg-emerald-400 px-5 py-2.5 text-sm font-medium text-zinc-950 hover:bg-emerald-300"
            >
              Create a vocabulary first
              <ArrowRight className="h-4 w-4" />
            </button>
            <Link
              to="/docs"
              className="inline-flex items-center gap-2 rounded-lg border border-zinc-700 px-5 py-2.5 text-sm text-zinc-300 hover:border-zinc-600"
            >
              Full installation guide
              <ExternalLink className="h-4 w-4" />
            </Link>
          </div>
        </section>

        <aside className="space-y-4">
          <InfoCard icon={Check} title="No account required" body="Local MCP setup works without signing in. GitHub login is only needed to save or publish a vocabulary." tone="success" />
          <InfoCard icon={Link2} title="One server, many clients" body="Claude Code, Codex, Cursor, VS Code, and Claude Desktop all launch the same Sema stdio server." />
          <InfoCard icon={ShieldCheck} title="The agent gets instructions" body="Sema supplies workflow guidance and detailed tool descriptions during MCP initialization; the kickoff prompt makes the writable-vocabulary check explicit." />
          <InfoCard icon={Network} title="Hosted endpoint next" body="A workspace-specific hosted MCP URL will arrive with the GitHub import and publishing backend." />
        </aside>
      </div>
    </main>
  )
}

function VocabularyCreator({
  user,
  onBack,
  onConnect,
}: {
  user?: GitHubUser | null
  onBack: () => void
  onConnect: () => void
}) {
  const [name, setName] = useState('')
  const [preset, setPreset] = useState<Preset>('full')
  const [copied, setCopied] = useState(false)
  const slug = slugify(name) || 'my-vocabulary'
  const createCommand = `uvx --from "semahash[mcp]" sema build ${slug}.db --preset ${preset}`
  const useCommand = `uvx --from "semahash[mcp]" sema use ${slug}.db`

  const copyCommand = async () => {
    await navigator.clipboard.writeText(`${createCommand}\n${useCommand}`)
    setCopied(true)
    setTimeout(() => setCopied(false), 1800)
  }

  return (
    <main className="relative mx-auto max-w-5xl px-6 py-12">
      <BackButton onClick={onBack}>Back to explore</BackButton>
      <div className="mt-8 grid gap-6 lg:grid-cols-[minmax(0,1fr)_300px]">
        <section className="rounded-2xl border border-zinc-800 bg-zinc-900/45 p-6 sm:p-8">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/10 text-emerald-300">
            <Library className="h-6 w-6" />
          </div>
          <p className="mt-7 text-xs font-medium uppercase tracking-[0.2em] text-emerald-400">Step 2</p>
          <h1 className="mt-2 text-3xl font-light tracking-tight text-zinc-50">Create your vocabulary</h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-zinc-400">
            Choose a name and a starting point. The commands below create a real local vocabulary your agent can use after you connect it.
          </p>
          <p className="mt-3 text-sm text-zinc-500">
            These commands use <code className="text-zinc-300">uvx</code>. If it is not installed,{' '}
            <a
              href="https://docs.astral.sh/uv/getting-started/installation/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-emerald-300 underline decoration-emerald-500/30 underline-offset-4 hover:text-emerald-200"
            >
              install uv first
            </a>.
          </p>

          <label className="mt-8 block">
            <span className="text-sm font-medium text-zinc-300">Vocabulary name</span>
            <input
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder={user?.login ? `${user.login}'s vocabulary` : 'My vocabulary'}
              className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950/70 px-4 py-3 text-sm text-zinc-100 outline-none placeholder:text-zinc-700 focus:border-emerald-500/40"
            />
          </label>

          <fieldset className="mt-6">
            <legend className="text-sm font-medium text-zinc-300">Starting point</legend>
            <div className="mt-3 grid gap-3 sm:grid-cols-3">
              <PresetOption value="full" selected={preset} setSelected={setPreset} title="Full" body="All 452 patterns" />
              <PresetOption value="standard" selected={preset} setSelected={setPreset} title="Standard" body="Curated essentials" />
              <PresetOption value="empty" selected={preset} setSelected={setPreset} title="Empty" body="Start from zero" />
            </div>
          </fieldset>

          <div className="mt-8 rounded-xl border border-zinc-800 bg-zinc-950/80 p-4">
            <div className="mb-3 flex items-center justify-between gap-3">
              <span className="text-xs font-medium uppercase tracking-wider text-zinc-500">Create locally</span>
              <button type="button" onClick={copyCommand} className="inline-flex items-center gap-1.5 text-xs text-zinc-400 hover:text-zinc-100">
                {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                {copied ? 'Copied' : 'Copy commands'}
              </button>
            </div>
            <code className="block overflow-x-auto whitespace-nowrap text-sm text-emerald-300">{createCommand}</code>
            <code className="mt-2 block overflow-x-auto whitespace-nowrap text-sm text-emerald-300">{useCommand}</code>
            <p className="mt-3 text-xs leading-5 text-zinc-500">Run both commands before connecting. If Sema is already connected, restart the MCP server so it opens the selected vocabulary.</p>
          </div>

          <div className="mt-8 flex flex-wrap gap-3">
            <button
              type="button"
              onClick={onConnect}
              className="inline-flex items-center gap-2 rounded-lg border border-zinc-700 px-5 py-2.5 text-sm text-zinc-300 hover:border-zinc-600"
            >
              <Bot className="h-4 w-4" />
              Continue to agent connection
            </button>
            <Link
              to="/docs"
              className="inline-flex items-center gap-2 rounded-lg border border-zinc-700 px-5 py-2.5 text-sm text-zinc-300 hover:border-zinc-600"
            >
              Creation guide
              <ExternalLink className="h-4 w-4" />
            </Link>
          </div>
        </section>

        <aside className="space-y-4">
          <InfoCard
            icon={CircleUserRound}
            title={user?.login ? `Signed in as @${user.login}` : 'Local vocabulary'}
            body={user?.login
              ? 'This identity will own hosted vocabularies once publishing is enabled.'
              : 'This vocabulary lives on your computer. GitHub login will only matter when hosted publishing is enabled.'}
            tone={user?.login ? 'success' : undefined}
          />
          <InfoCard icon={Lock} title="Nothing fake is saved" body="This staging screen generates working local commands. It does not pretend a hosted vocabulary was created." />
          <InfoCard icon={Github} title="Publishing is not live yet" body="GitHub App installation, repository import, and the public registry record are the next backend milestone." />
        </aside>
      </div>
    </main>
  )
}

function PresetOption({
  value,
  selected,
  setSelected,
  title,
  body,
}: {
  value: Preset
  selected: Preset
  setSelected: (value: Preset) => void
  title: string
  body: string
}) {
  const active = value === selected
  return (
    <button
      type="button"
      onClick={() => setSelected(value)}
      className={cn(
        'rounded-xl border p-4 text-left transition-colors',
        active
          ? 'border-emerald-500/40 bg-emerald-500/10'
          : 'border-zinc-800 bg-zinc-950/35 hover:border-zinc-700'
      )}
    >
      <span className={cn('block text-sm font-medium', active ? 'text-emerald-200' : 'text-zinc-200')}>{title}</span>
      <span className="mt-1 block text-xs text-zinc-500">{body}</span>
    </button>
  )
}

function JourneyStep({
  number,
  icon: Icon,
  title,
  body,
  action,
  onClick,
  complete = false,
}: {
  number: string
  icon: typeof Github
  title: string
  body: string
  action: string
  onClick?: () => void
  complete?: boolean
}) {
  return (
    <article className="flex min-h-64 flex-col rounded-xl border border-zinc-800/80 bg-zinc-900/35 p-6">
      <div className="flex items-center justify-between">
        <span className="flex h-10 w-10 items-center justify-center rounded-lg border border-zinc-800 bg-zinc-950/60 text-zinc-400">
          {complete ? <Check className="h-5 w-5 text-emerald-400" /> : <Icon className="h-5 w-5" />}
        </span>
        <span className="text-xs font-medium text-zinc-700">{number}</span>
      </div>
      <h3 className="mt-6 text-lg font-medium text-zinc-100">{title}</h3>
      <p className="mt-2 flex-1 text-sm leading-6 text-zinc-500">{body}</p>
      <button
        type="button"
        onClick={onClick}
        disabled={!onClick}
        className={cn(
          'mt-6 inline-flex w-fit items-center gap-2 text-sm font-medium',
          complete ? 'text-emerald-300' : 'text-zinc-300 hover:text-emerald-300',
          !onClick && !complete && 'cursor-default text-zinc-600'
        )}
      >
        {action}
        {complete ? null : <ChevronRight className="h-4 w-4" />}
      </button>
    </article>
  )
}

function InfoCard({
  icon: Icon,
  title,
  body,
  tone = 'neutral',
}: {
  icon: typeof Github
  title: string
  body: string
  tone?: 'neutral' | 'success'
}) {
  return (
    <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
      <Icon className={cn('h-4 w-4', tone === 'success' ? 'text-emerald-400' : 'text-zinc-500')} />
      <h2 className="mt-3 text-sm font-medium text-zinc-200">{title}</h2>
      <p className="mt-2 text-xs leading-5 text-zinc-500">{body}</p>
    </section>
  )
}

function BackButton({ onClick, children }: { onClick: () => void; children: ReactNode }) {
  return (
    <button type="button" onClick={onClick} className="inline-flex items-center gap-2 text-sm text-zinc-500 hover:text-zinc-200">
      <ArrowLeft className="h-4 w-4" />
      {children}
    </button>
  )
}

function SectionHeading({
  kicker,
  title,
  body,
  action,
}: {
  kicker: string
  title: string
  body: string
  action?: ReactNode
}) {
  return (
    <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
      <div>
        <p className="text-xs font-medium uppercase tracking-[0.2em] text-emerald-400">{kicker}</p>
        <h2 className="mt-2 text-2xl font-light tracking-tight text-zinc-100 sm:text-3xl">{title}</h2>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-500">{body}</p>
      </div>
      {action}
    </div>
  )
}

function VocabularyFact({ label, value, mono = false }: { label: string; value: string; mono?: boolean }) {
  return (
    <div className="rounded-lg border border-zinc-800/80 bg-zinc-950/35 px-3 py-3">
      <span className="block text-[11px] uppercase tracking-wider text-zinc-600">{label}</span>
      <span className={cn('mt-1 block truncate text-sm text-zinc-300', mono && 'font-mono text-xs')}>{value}</span>
    </div>
  )
}

function slugify(value: string) {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

export default RegistryPage
