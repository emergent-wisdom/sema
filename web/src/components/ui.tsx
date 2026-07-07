import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { cn } from '@/lib/utils'

/**
 * Shared UI primitives — the design system, kept deliberately small.
 * Tokens live in index.css (:root). Pages compose these instead of
 * hand-rolling zinc-* class soup.
 */

/** A pattern reference (Handle#stub) — the protocol's words, always mono. */
export function RefChip({
  handle,
  stub,
  className,
}: {
  handle: string
  stub?: string
  className?: string
}) {
  return (
    <span
      className={cn(
        'ref-mono inline-flex items-baseline rounded-md bg-white/[0.04] px-1.5 py-0.5',
        'text-zinc-300',
        className
      )}
    >
      {handle}
      {stub && <span className="text-emerald-400/90">#{stub}</span>}
    </span>
  )
}

/** Quiet text navigation link — no box, weight comes from type. */
export function NavItem({
  to,
  href,
  active,
  children,
}: {
  to?: string
  href?: string
  active?: boolean
  children: ReactNode
}) {
  const cls = cn(
    'text-sm transition-colors py-1',
    active ? 'text-zinc-100' : 'text-zinc-400 hover:text-zinc-100'
  )
  if (to) {
    return (
      <Link to={to} className={cls}>
        {children}
      </Link>
    )
  }
  return (
    <a href={href} target="_blank" rel="noopener noreferrer" className={cls}>
      {children}
    </a>
  )
}

/** The one loud button per view. */
export function PrimaryLink({
  to,
  children,
  className,
}: {
  to: string
  children: ReactNode
  className?: string
}) {
  return (
    <Link
      to={to}
      className={cn(
        'inline-flex items-center gap-2 rounded-lg bg-emerald-400/10 px-4 py-2',
        'text-sm font-medium text-emerald-300 ring-1 ring-inset ring-emerald-400/25',
        'transition-colors hover:bg-emerald-400/15 hover:text-emerald-200',
        className
      )}
    >
      {children}
    </Link>
  )
}
