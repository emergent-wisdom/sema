import { useEffect, useRef, useState } from 'react'
import { create } from 'zustand'
import { usePatterns, useWorkspace } from '@/hooks/useApi'

export type Arrival = {
  id: string
  stub: string
  gloss: string
  layer: string
  at: number
}

type LiveState = {
  arrivals: Arrival[]
  /** Fly the graph camera to each new pattern as it arrives. */
  follow: boolean
  record: (items: Arrival[]) => void
  reset: () => void
  setFollow: (follow: boolean) => void
}

const MAX_ARRIVALS = 50

// Patterns that appeared while this view was open. The database keeps no
// creation time, so "new" means new since the page loaded, never a guess.
export const useLiveStore = create<LiveState>()((set) => ({
  arrivals: [],
  follow: false,
  record: (items) =>
    set((state) => ({ arrivals: [...items, ...state.arrivals].slice(0, MAX_ARRIVALS) })),
  reset: () => set({ arrivals: [] }),
  setFollow: (follow) => set({ follow }),
}))

/**
 * Compare each poll of the pattern list with the last one and record the
 * patterns that were not there before. Mount once, near the root, so the
 * record survives moving between the vocabulary page and the graph.
 */
export function LiveAdditionsTracker() {
  const { data: patterns } = usePatterns()
  const { data: workspace } = useWorkspace()
  const known = useRef<Set<string> | null>(null)
  const knownDb = useRef<string | null>(null)
  const record = useLiveStore((state) => state.record)
  const reset = useLiveStore((state) => state.reset)
  const dbPath = workspace?.db_path ?? null

  useEffect(() => {
    if (!patterns || dbPath === null) return
    // Another vocabulary is a fresh start, not a burst of new patterns.
    if (known.current === null || knownDb.current !== dbPath) {
      known.current = new Set(patterns.map((pattern) => pattern.id))
      knownDb.current = dbPath
      reset()
      return
    }
    const seen = known.current
    const fresh = patterns.filter((pattern) => !seen.has(pattern.id))
    if (fresh.length === 0) return
    const now = Date.now()
    for (const pattern of fresh) seen.add(pattern.id)
    record(
      fresh.map((pattern) => ({
        id: pattern.id,
        stub: pattern.stub,
        gloss: pattern.gloss,
        layer: pattern.layer,
        at: now,
      })),
    )
  }, [patterns, dbPath, record, reset])

  return null
}

/** Ids of the patterns that arrived within the last `windowMs`, refreshed every second. */
export function useRecentArrivalIds(windowMs: number): Set<string> {
  const arrivals = useLiveStore((state) => state.arrivals)
  const [now, setNow] = useState(() => Date.now())
  const newest = arrivals[0]?.at ?? 0

  // Tick only while the newest arrival is still inside the window.
  useEffect(() => {
    if (!newest) return
    setNow(Date.now())
    const timer = window.setInterval(() => {
      const current = Date.now()
      setNow(current)
      if (current - newest >= windowMs) window.clearInterval(timer)
    }, 1000)
    return () => window.clearInterval(timer)
  }, [newest, windowMs])

  const ids = new Set<string>()
  for (const arrival of arrivals) {
    if (now - arrival.at < windowMs) ids.add(arrival.id)
  }
  return ids
}
