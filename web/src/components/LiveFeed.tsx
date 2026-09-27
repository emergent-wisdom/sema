import { useEffect, useRef, useState } from 'react'
import { LAYER_COLORS } from '@/types/taxonomy'
import { useIsLocal } from '@/hooks/useApi'
import { useLiveStore } from '@/hooks/useLiveAdditions'
import { useAppStore } from '@/stores/appStore'

function ago(ms: number): string {
  const seconds = Math.max(0, Math.round(ms / 1000))
  if (seconds < 60) return `${seconds} s ago`
  const minutes = Math.round(seconds / 60)
  if (minutes < 60) return `${minutes} min ago`
  return `${Math.round(minutes / 60)} h ago`
}

/**
 * The patterns an agent minted while this view was open, newest first. The
 * same patterns light up in the graph; follow mode flies to each one.
 */
export function LiveFeed() {
  const isLocal = useIsLocal()
  const arrivals = useLiveStore((state) => state.arrivals)
  const selectNodeAndFly = useAppStore((state) => state.selectNodeAndFly)
  const follow = useLiveStore((state) => state.follow)
  const setFollow = useLiveStore((state) => state.setFollow)
  const [now, setNow] = useState(() => Date.now())
  const lastFollowed = useRef<string | null>(null)
  const newest = arrivals[0]

  useEffect(() => {
    if (arrivals.length === 0) return
    setNow(Date.now())
    const timer = window.setInterval(() => setNow(Date.now()), 5000)
    return () => window.clearInterval(timer)
  }, [arrivals])

  // Give the layout a moment to place the new node before flying to it.
  useEffect(() => {
    if (!follow || !newest || lastFollowed.current === newest.id) return
    lastFollowed.current = newest.id
    const timer = window.setTimeout(() => selectNodeAndFly(newest.id), 1500)
    return () => window.clearTimeout(timer)
  }, [follow, newest, selectNodeAndFly])

  if (!isLocal) return null

  return (
    <aside
      aria-label="Patterns added while this view is open"
      className="absolute bottom-4 left-4 z-40 hidden w-72 rounded-xl border border-zinc-800 bg-zinc-900/90 p-3 shadow-lg backdrop-blur-md sm:block"
    >
      <div className="flex items-center justify-between gap-2">
        <p className="flex items-center gap-2 text-xs font-medium text-zinc-300">
          <span className="live-dot h-1.5 w-1.5 rounded-full bg-emerald-400" aria-hidden="true" />
          Live
        </p>
        <label className="flex cursor-pointer items-center gap-1.5 text-[11px] text-zinc-400">
          <input
            type="checkbox"
            checked={follow}
            onChange={(event) => setFollow(event.target.checked)}
            className="accent-emerald-400"
          />
          Follow new patterns
        </label>
      </div>
      {arrivals.length === 0 ? (
        <p className="mt-2 text-xs leading-5 text-zinc-500">
          Patterns your agent mints appear here and light up in the graph.
        </p>
      ) : (
        <ul className="mt-2 space-y-0.5" aria-live="polite">
          {arrivals.slice(0, 6).map((arrival) => (
            <li key={arrival.id}>
              <button
                type="button"
                onClick={() => selectNodeAndFly(arrival.id)}
                className="flex w-full items-center gap-2 rounded-md px-1.5 py-1 text-left transition-colors hover:bg-zinc-800/70"
              >
                <span
                  className="h-1.5 w-1.5 shrink-0 rounded-full"
                  style={{ backgroundColor: LAYER_COLORS[arrival.layer] || '#71717a' }}
                  aria-hidden="true"
                />
                <span className="min-w-0 flex-1 truncate text-xs text-zinc-200">
                  {arrival.id}
                  <span className="ref-mono text-emerald-400/70">#{arrival.stub}</span>
                </span>
                <span className="shrink-0 text-[10px] tabular-nums text-zinc-500">
                  {ago(now - arrival.at)}
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </aside>
  )
}
