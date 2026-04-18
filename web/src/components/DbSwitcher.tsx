import { Database, Check, Lock } from 'lucide-react'
import { useState } from 'react'
import { useDbs, useSwitchDb } from '@/hooks/useApi'
import { cn } from '@/lib/utils'

export function DbSwitcher() {
  const { data } = useDbs()
  const switchDb = useSwitchDb()
  const [isOpen, setIsOpen] = useState(false)

  if (!data) return null

  // Hide the switcher entirely when there's nothing to switch between.
  // No databases = nothing to show; exactly one = no meaningful choice.
  // Returning null here also lets the callsite skip its trailing divider.
  if (!data.databases || data.databases.length < 2) return null

  const active = data.databases.find((d) => d.active)
  const activeName = active ? (active.bundled ? 'default' : active.name) : '?'

  const handleSelect = (db: { path: string; bundled: boolean }) => {
    if (db.bundled) {
      switchDb.mutate({ default: true })
    } else {
      switchDb.mutate({ path: db.path })
    }
    setIsOpen(false)
  }

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          'flex items-center gap-1.5 px-2 py-1 rounded text-xs transition-colors',
          'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800',
        )}
      >
        <Database className="w-3 h-3" />
        <span className="font-mono">{activeName}</span>
      </button>

      {isOpen && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setIsOpen(false)} />
          <div className="absolute top-full left-0 mt-1 bg-zinc-900 border border-zinc-700 rounded-lg shadow-xl z-50 py-1 min-w-[260px] max-h-[400px] overflow-y-auto">
            <div className="px-3 py-1 text-[10px] text-zinc-500 uppercase tracking-wider">
              Active vocabulary
            </div>
            {data.databases.map((db) => (
              <button
                key={db.path}
                type="button"
                onClick={() => handleSelect(db)}
                disabled={!db.exists || switchDb.isPending}
                className={cn(
                  'w-full px-3 py-1.5 text-left text-xs flex items-center gap-2 transition-colors',
                  db.active
                    ? 'bg-zinc-800 text-zinc-200'
                    : 'text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200',
                  !db.exists && 'opacity-50 cursor-not-allowed',
                )}
              >
                {db.active ? (
                  <Check className="w-3 h-3 text-emerald-400 shrink-0" />
                ) : (
                  <span className="w-3 h-3 shrink-0" />
                )}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5">
                    <span className="font-mono truncate">
                      {db.bundled ? 'default' : db.name}
                    </span>
                    {db.bundled && (
                      <Lock className="w-2.5 h-2.5 text-zinc-600 shrink-0" />
                    )}
                  </div>
                  <div className="text-[10px] text-zinc-600 truncate">
                    {db.path}
                  </div>
                </div>
              </button>
            ))}
            {switchDb.isPending && (
              <div className="px-3 py-2 text-[10px] text-zinc-500 border-t border-zinc-800">
                Switching…
              </div>
            )}
            {switchDb.isError && (
              <div className="px-3 py-2 text-[10px] text-red-400 border-t border-zinc-800">
                {String(switchDb.error)}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}
