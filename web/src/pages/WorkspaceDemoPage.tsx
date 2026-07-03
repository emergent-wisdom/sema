import { useMemo, useState, type ReactNode } from 'react'
import { Link } from 'react-router-dom'
import {
  ArrowLeft,
  Check,
  ChevronRight,
  Circle,
  Copy,
  GitBranch,
  Github,
  Globe2,
  Library,
  Lock,
  Mail,
  Network,
  Plus,
  Rocket,
  Search,
  ShieldCheck,
  Users,
} from 'lucide-react'
import { SemaLogo } from '@/components/SemaLogo'
import { cn } from '@/lib/utils'

type StepId = 'connect' | 'library' | 'team' | 'publish'
type Visibility = 'Private' | 'Team' | 'Public'
type Collaborator = {
  email: string
  name: string
  role: string
  status: string
}

const steps: Array<{ id: StepId; label: string; icon: typeof Github }> = [
  { id: 'connect', label: 'GitHub', icon: Github },
  { id: 'library', label: 'Library', icon: Library },
  { id: 'team', label: 'Team', icon: Users },
  { id: 'publish', label: 'Publish', icon: Rocket },
]

const starterPatterns = [
  { handle: 'Claim', stub: 'c391', layer: 'Reasoning', state: 'Published' },
  { handle: 'Evidence', stub: '8aa2', layer: 'Verification', state: 'Published' },
  { handle: 'ReviewLoop', stub: '41db', layer: 'Coordination', state: 'Draft' },
  { handle: 'DecisionRecord', stub: '91e6', layer: 'Governance', state: 'Draft' },
]

const activity = [
  'Created workspace root',
  'Linked source repository',
  'Prepared collaborator invitations',
  'Generated staged MCP endpoint',
]

const initialCollaborators: Collaborator[] = [
  {
    email: 'henrik.westeberg@emergentwisdom.org',
    name: 'Henrik Westerberg',
    role: 'Owner',
    status: 'Active',
  },
  {
    email: 'researcher@example.com',
    name: 'Research Partner',
    role: 'Editor',
    status: 'Invited',
  },
]

export function WorkspaceDemoPage() {
  const [activeStep, setActiveStep] = useState<StepId>('connect')
  const [githubConnected, setGithubConnected] = useState(false)
  const [libraryName, setLibraryName] = useState('Civic Intelligence Library')
  const [repo, setRepo] = useState('henrikwesterberg/civic-intelligence')
  const [visibility, setVisibility] = useState<Visibility>('Private')
  const [inviteEmail, setInviteEmail] = useState('claude@example.com')
  const [collaborators, setCollaborators] = useState(initialCollaborators)
  const [published, setPublished] = useState(false)
  const [copied, setCopied] = useState(false)

  const repoName = repo.split('/').filter(Boolean).pop() || 'workspace'
  const endpoint = `https://sema-web-production.up.railway.app/mcp/${repoName.toLowerCase()}`
  const currentStepIndex = steps.findIndex((step) => step.id === activeStep)

  const completed = useMemo<Record<StepId, boolean>>(
    () => ({
      connect: githubConnected,
      library: libraryName.trim().length > 0 && repo.includes('/'),
      team: collaborators.length > 1,
      publish: published,
    }),
    [collaborators.length, githubConnected, libraryName, published, repo]
  )

  const graphHealth = published ? 'Published' : 'Ready'

  const nextStep = () => {
    const next = steps[Math.min(currentStepIndex + 1, steps.length - 1)]
    setActiveStep(next.id)
  }

  const addCollaborator = () => {
    const normalized = inviteEmail.trim().toLowerCase()
    if (!normalized || collaborators.some((member) => member.email === normalized)) return

    const name = normalized
      .split('@')[0]
      .split(/[._-]/)
      .filter(Boolean)
      .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
      .join(' ')

    setCollaborators((current) => [
      ...current,
      {
        email: normalized,
        name: name || normalized,
        role: 'Reviewer',
        status: 'Invited',
      },
    ])
    setInviteEmail('')
  }

  const copyEndpoint = async () => {
    await navigator.clipboard.writeText(endpoint)
    setCopied(true)
    setTimeout(() => setCopied(false), 1800)
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <div
        className="fixed inset-0 pointer-events-none opacity-[0.018]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />

      <header className="sticky top-0 z-40 border-b border-zinc-800/60 bg-zinc-950/85 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-4">
          <div className="flex items-center gap-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg border border-emerald-500/20 bg-emerald-500/10 text-emerald-400">
              <SemaLogo className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center gap-3">
                <h1 className="text-lg font-semibold tracking-tight">Sema Workspace</h1>
                <span className="rounded-md border border-emerald-500/20 bg-emerald-500/10 px-2 py-1 text-[11px] font-medium text-emerald-300">
                  Staging rehearsal
                </span>
              </div>
              <p className="text-xs text-zinc-500">{repo || 'No repository selected'}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Link
              to="/"
              className="inline-flex items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900/70 px-3 py-2 text-sm text-zinc-400 transition-colors hover:border-zinc-700 hover:text-zinc-100"
            >
              <ArrowLeft className="h-4 w-4" />
              Patterns
            </Link>
          </div>
        </div>
      </header>

      <main className="mx-auto grid max-w-7xl gap-6 px-6 py-6 lg:grid-cols-[280px_minmax(0,1fr)]">
        <aside className="space-y-4">
          <nav className="rounded-lg border border-zinc-800/70 bg-zinc-900/45 p-3">
            {steps.map((step, index) => {
              const Icon = step.icon
              const isActive = step.id === activeStep
              const isComplete = completed[step.id]
              return (
                <button
                  key={step.id}
                  type="button"
                  onClick={() => setActiveStep(step.id)}
                  className={cn(
                    'flex w-full items-center justify-between rounded-lg px-3 py-3 text-left transition-all',
                    isActive
                      ? 'bg-zinc-800 text-zinc-100'
                      : 'text-zinc-500 hover:bg-zinc-800/50 hover:text-zinc-200'
                  )}
                >
                  <span className="flex items-center gap-3">
                    <span
                      className={cn(
                        'flex h-8 w-8 items-center justify-center rounded-lg border',
                        isActive
                          ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300'
                          : 'border-zinc-800 bg-zinc-950/50 text-zinc-500'
                      )}
                    >
                      <Icon className="h-4 w-4" />
                    </span>
                    <span>
                      <span className="block text-sm font-medium">{step.label}</span>
                      <span className="block text-xs text-zinc-600">Step {index + 1}</span>
                    </span>
                  </span>
                  {isComplete ? (
                    <Check className="h-4 w-4 text-emerald-400" />
                  ) : (
                    <Circle className="h-3 w-3 text-zinc-700" />
                  )}
                </button>
              )
            })}
          </nav>

          <section className="rounded-lg border border-zinc-800/70 bg-zinc-900/45 p-4">
            <div className="mb-4 flex items-center gap-2 text-sm font-medium text-zinc-200">
              <ShieldCheck className="h-4 w-4 text-emerald-400" />
              Workspace State
            </div>
            <div className="space-y-3 text-sm">
              <StatusRow label="Source" value={githubConnected ? 'GitHub linked' : 'Not linked'} />
              <StatusRow label="Access" value={visibility} />
              <StatusRow label="Root" value="39ca671a4dcb3075" />
              <StatusRow label="Graph" value={graphHealth} />
            </div>
          </section>
        </aside>

        <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_360px]">
          <section className="rounded-lg border border-zinc-800/70 bg-zinc-900/45 p-5">
            <StepPanel
              activeStep={activeStep}
              githubConnected={githubConnected}
              setGithubConnected={setGithubConnected}
              libraryName={libraryName}
              setLibraryName={setLibraryName}
              repo={repo}
              setRepo={setRepo}
              visibility={visibility}
              setVisibility={setVisibility}
              inviteEmail={inviteEmail}
              setInviteEmail={setInviteEmail}
              collaborators={collaborators}
              addCollaborator={addCollaborator}
              published={published}
              setPublished={setPublished}
              endpoint={endpoint}
              copied={copied}
              copyEndpoint={copyEndpoint}
              nextStep={nextStep}
            />
          </section>

          <aside className="space-y-6">
            <section className="rounded-lg border border-zinc-800/70 bg-zinc-900/45 p-5">
              <div className="mb-4 flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-widest text-zinc-600">Workspace</p>
                  <h2 className="mt-1 text-lg font-medium text-zinc-100">{libraryName}</h2>
                </div>
                <div className="flex h-10 w-10 items-center justify-center rounded-lg border border-emerald-500/20 bg-emerald-500/10 text-emerald-300">
                  <Network className="h-5 w-5" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <Metric label="Patterns" value="24" />
                <Metric label="Drafts" value="4" />
                <Metric label="Members" value={String(collaborators.length)} />
                <Metric label="Proposals" value="3" />
              </div>
            </section>

            <section className="rounded-lg border border-zinc-800/70 bg-zinc-900/45 p-5">
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-sm font-medium text-zinc-200">Library Outline</h2>
                <Search className="h-4 w-4 text-zinc-600" />
              </div>
              <div className="space-y-2">
                {starterPatterns.map((pattern) => (
                  <div
                    key={pattern.handle}
                    className="flex items-center justify-between rounded-lg border border-zinc-800/70 bg-zinc-950/35 px-3 py-2"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium text-zinc-200">{pattern.handle}</span>
                        <code className="rounded bg-zinc-800 px-1.5 py-0.5 text-[10px] text-zinc-500">
                          #{pattern.stub}
                        </code>
                      </div>
                      <p className="mt-1 text-xs text-zinc-600">{pattern.layer}</p>
                    </div>
                    <span
                      className={cn(
                        'rounded-md px-2 py-1 text-[11px] font-medium',
                        pattern.state === 'Published'
                          ? 'bg-emerald-500/10 text-emerald-300'
                          : 'bg-amber-500/10 text-amber-300'
                      )}
                    >
                      {pattern.state}
                    </span>
                  </div>
                ))}
              </div>
            </section>

            <section className="rounded-lg border border-zinc-800/70 bg-zinc-900/45 p-5">
              <h2 className="mb-4 text-sm font-medium text-zinc-200">Recent Activity</h2>
              <div className="space-y-3">
                {activity.map((item) => (
                  <div key={item} className="flex gap-3 text-sm">
                    <div className="mt-1 h-2 w-2 rounded-full bg-emerald-400" />
                    <span className="text-zinc-500">{item}</span>
                  </div>
                ))}
              </div>
            </section>
          </aside>
        </div>
      </main>
    </div>
  )
}

function StepPanel({
  activeStep,
  githubConnected,
  setGithubConnected,
  libraryName,
  setLibraryName,
  repo,
  setRepo,
  visibility,
  setVisibility,
  inviteEmail,
  setInviteEmail,
  collaborators,
  addCollaborator,
  published,
  setPublished,
  endpoint,
  copied,
  copyEndpoint,
  nextStep,
}: {
  activeStep: StepId
  githubConnected: boolean
  setGithubConnected: (value: boolean) => void
  libraryName: string
  setLibraryName: (value: string) => void
  repo: string
  setRepo: (value: string) => void
  visibility: Visibility
  setVisibility: (value: Visibility) => void
  inviteEmail: string
  setInviteEmail: (value: string) => void
  collaborators: Collaborator[]
  addCollaborator: () => void
  published: boolean
  setPublished: (value: boolean) => void
  endpoint: string
  copied: boolean
  copyEndpoint: () => void
  nextStep: () => void
}) {
  if (activeStep === 'connect') {
    return (
      <div>
        <StepHeader
          icon={Github}
          kicker="Account"
          title="Continue with GitHub"
          body="Use your GitHub identity as the owner of a Sema workspace."
        />
        <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_260px]">
          <div className="rounded-lg border border-zinc-800 bg-zinc-950/35 p-4">
            <button
              type="button"
              onClick={() => setGithubConnected(true)}
              className="inline-flex items-center gap-2 rounded-lg border border-zinc-700 bg-zinc-100 px-4 py-2.5 text-sm font-medium text-zinc-950 transition-colors hover:bg-white"
            >
              {githubConnected ? <Check className="h-4 w-4" /> : <Github className="h-4 w-4" />}
              {githubConnected ? 'Connected as Henrik' : 'Continue with GitHub'}
            </button>
            <div className="mt-5 grid gap-3 sm:grid-cols-3">
              <IdentityFact label="Account" value={githubConnected ? '@henrikwesterberg' : 'Waiting'} />
              <IdentityFact label="Scope" value="Repo install" />
              <IdentityFact label="Owner" value="Personal" />
            </div>
          </div>
          <div className="rounded-lg border border-zinc-800 bg-zinc-950/35 p-4">
            <p className="text-sm font-medium text-zinc-200">Install target</p>
            <p className="mt-2 text-sm leading-6 text-zinc-500">
              emergent-wisdom/sema-starter
            </p>
            <div className="mt-4 flex items-center gap-2 text-xs text-emerald-300">
              <ShieldCheck className="h-4 w-4" />
              Repository-scoped access
            </div>
          </div>
        </div>
        <StepActions onNext={nextStep} nextLabel="Create library" />
      </div>
    )
  }

  if (activeStep === 'library') {
    return (
      <div>
        <StepHeader
          icon={Library}
          kicker="Library"
          title="Name the graph"
          body="Choose the workspace name, GitHub source, and access level."
        />
        <div className="grid gap-4 md:grid-cols-2">
          <Field label="Library name">
            <input
              value={libraryName}
              onChange={(event) => setLibraryName(event.target.value)}
              className="w-full rounded-lg border border-zinc-800 bg-zinc-950/70 px-3 py-2.5 text-sm text-zinc-100 outline-none transition-colors placeholder:text-zinc-700 focus:border-zinc-600"
            />
          </Field>
          <Field label="GitHub repository">
            <div className="flex items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-950/70 px-3 py-2.5">
              <GitBranch className="h-4 w-4 text-zinc-600" />
              <input
                value={repo}
                onChange={(event) => setRepo(event.target.value)}
                className="w-full bg-transparent text-sm text-zinc-100 outline-none placeholder:text-zinc-700"
              />
            </div>
          </Field>
        </div>
        <div className="mt-4">
          <p className="mb-2 text-sm font-medium text-zinc-300">Visibility</p>
          <div className="grid gap-2 sm:grid-cols-3">
            {(['Private', 'Team', 'Public'] as Visibility[]).map((option) => {
              const isSelected = option === visibility
              const Icon = option === 'Private' ? Lock : option === 'Team' ? Users : Globe2
              return (
                <button
                  key={option}
                  type="button"
                  onClick={() => setVisibility(option)}
                  className={cn(
                    'flex items-center gap-3 rounded-lg border px-3 py-3 text-left transition-colors',
                    isSelected
                      ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200'
                      : 'border-zinc-800 bg-zinc-950/35 text-zinc-500 hover:border-zinc-700 hover:text-zinc-200'
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span className="text-sm font-medium">{option}</span>
                </button>
              )
            })}
          </div>
        </div>
        <StepActions onNext={nextStep} nextLabel="Invite team" />
      </div>
    )
  }

  if (activeStep === 'team') {
    return (
      <div>
        <StepHeader
          icon={Users}
          kicker="Team"
          title="Invite collaborators"
          body="Give reviewers and editors a place to propose graph changes."
        />
        <div className="flex flex-col gap-3 sm:flex-row">
          <div className="flex flex-1 items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-950/70 px-3 py-2.5">
            <Mail className="h-4 w-4 text-zinc-600" />
            <input
              value={inviteEmail}
              onChange={(event) => setInviteEmail(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter') addCollaborator()
              }}
              placeholder="name@example.com"
              className="w-full bg-transparent text-sm text-zinc-100 outline-none placeholder:text-zinc-700"
            />
          </div>
          <button
            type="button"
            onClick={addCollaborator}
            className="inline-flex items-center justify-center gap-2 rounded-lg border border-zinc-700 bg-zinc-100 px-4 py-2.5 text-sm font-medium text-zinc-950 transition-colors hover:bg-white"
          >
            <Plus className="h-4 w-4" />
            Invite
          </button>
        </div>
        <div className="mt-5 divide-y divide-zinc-800 overflow-hidden rounded-lg border border-zinc-800">
          {collaborators.map((member) => (
            <div key={member.email} className="flex items-center justify-between gap-4 bg-zinc-950/35 px-4 py-3">
              <div>
                <p className="text-sm font-medium text-zinc-200">{member.name}</p>
                <p className="text-xs text-zinc-600">{member.email}</p>
              </div>
              <div className="flex items-center gap-2">
                <span className="rounded-md border border-zinc-800 px-2 py-1 text-xs text-zinc-400">
                  {member.role}
                </span>
                <span className="rounded-md bg-emerald-500/10 px-2 py-1 text-xs font-medium text-emerald-300">
                  {member.status}
                </span>
              </div>
            </div>
          ))}
        </div>
        <StepActions onNext={nextStep} nextLabel="Prepare publish" />
      </div>
    )
  }

  return (
    <div>
      <StepHeader
        icon={Rocket}
        kicker="Publish"
        title="Publish the workspace"
        body="Create a stable graph root and expose the team workspace to agents."
      />
      <div className="rounded-lg border border-zinc-800 bg-zinc-950/35 p-4">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm font-medium text-zinc-200">Vocabulary root</p>
            <code className="mt-2 block break-all text-xs text-zinc-500">
              sema:root#mh:SHA-256:39ca671a4dcb3075855cb293380d1796105e2eca0de49b0537279b798b675ee6
            </code>
          </div>
          <button
            type="button"
            onClick={() => setPublished(true)}
            className={cn(
              'inline-flex items-center justify-center gap-2 rounded-lg border px-4 py-2.5 text-sm font-medium transition-colors',
              published
                ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200'
                : 'border-zinc-700 bg-zinc-100 text-zinc-950 hover:bg-white'
            )}
          >
            {published ? <Check className="h-4 w-4" /> : <Rocket className="h-4 w-4" />}
            {published ? 'Published' : 'Publish snapshot'}
          </button>
        </div>
      </div>
      <div className="mt-4 rounded-lg border border-zinc-800 bg-zinc-950/35 p-4">
        <p className="text-sm font-medium text-zinc-200">MCP endpoint</p>
        <div className="mt-3 flex flex-col gap-3 md:flex-row">
          <code className="flex-1 rounded-lg border border-zinc-800 bg-zinc-950 px-3 py-2.5 text-xs text-zinc-500">
            {endpoint}
          </code>
          <button
            type="button"
            onClick={copyEndpoint}
            className="inline-flex items-center justify-center gap-2 rounded-lg border border-zinc-800 px-3 py-2.5 text-sm text-zinc-300 transition-colors hover:border-zinc-700 hover:text-zinc-100"
          >
            {copied ? <Check className="h-4 w-4 text-emerald-400" /> : <Copy className="h-4 w-4" />}
            {copied ? 'Copied' : 'Copy'}
          </button>
        </div>
      </div>
    </div>
  )
}

function StepHeader({
  icon: Icon,
  kicker,
  title,
  body,
}: {
  icon: typeof Github
  kicker: string
  title: string
  body: string
}) {
  return (
    <div className="mb-6 flex gap-4">
      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border border-emerald-500/20 bg-emerald-500/10 text-emerald-300">
        <Icon className="h-5 w-5" />
      </div>
      <div>
        <p className="text-xs uppercase tracking-widest text-zinc-600">{kicker}</p>
        <h2 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">{title}</h2>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-500">{body}</p>
      </div>
    </div>
  )
}

function StepActions({ onNext, nextLabel }: { onNext: () => void; nextLabel: string }) {
  return (
    <div className="mt-6 flex justify-end">
      <button
        type="button"
        onClick={onNext}
        className="inline-flex items-center gap-2 rounded-lg border border-emerald-500/20 bg-emerald-500/10 px-4 py-2.5 text-sm font-medium text-emerald-300 transition-colors hover:bg-emerald-500/15 hover:text-emerald-200"
      >
        {nextLabel}
        <ChevronRight className="h-4 w-4" />
      </button>
    </div>
  )
}

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm font-medium text-zinc-300">{label}</span>
      {children}
    </label>
  )
}

function IdentityFact({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950/45 px-3 py-3">
      <p className="text-xs text-zinc-600">{label}</p>
      <p className="mt-1 text-sm font-medium text-zinc-200">{value}</p>
    </div>
  )
}

function StatusRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-4">
      <span className="text-zinc-600">{label}</span>
      <span className="truncate text-right font-medium text-zinc-300">{value}</span>
    </div>
  )
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950/35 p-3">
      <p className="text-xs text-zinc-600">{label}</p>
      <p className="mt-2 text-2xl font-light tabular-nums text-zinc-200">{value}</p>
    </div>
  )
}
