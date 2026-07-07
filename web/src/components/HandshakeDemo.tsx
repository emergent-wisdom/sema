/**
 * The hero demo: three handshake lines that "run" on page load.
 * Shows the fail-closed protocol doing its job instead of describing it —
 * two agents agree, a drifted third gets HALTed.
 */
export function HandshakeDemo() {
  return (
    <div
      className="w-full max-w-md rounded-xl bg-[--ink-raise] ring-1 ring-white/[0.06] shadow-2xl shadow-black/40"
      aria-label="Example: sema handshake catching semantic drift"
    >
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-white/[0.06]">
        <span className="ref-mono text-zinc-500">sema_handshake</span>
        <span className="flex gap-1.5">
          <i className="w-2.5 h-2.5 rounded-full bg-white/10" />
          <i className="w-2.5 h-2.5 rounded-full bg-white/10" />
        </span>
      </div>

      <div className="ref-mono px-4 py-4 space-y-2.5 text-[13px] leading-relaxed">
        <Line delay={0}>
          <span className="text-zinc-500">agent-a›</span>{' '}
          <span className="text-zinc-300">
            handshake(<span className="text-zinc-100">"StateLock"</span>, "7cd8")
          </span>
        </Line>
        <Line delay={0.55}>
          <span className="text-emerald-400">✓ PROCEED</span>
          <span className="text-zinc-500"> — semantic alignment confirmed</span>
        </Line>

        <Line delay={1.3}>
          <span className="text-zinc-500">agent-b›</span>{' '}
          <span className="text-zinc-300">
            handshake(<span className="text-zinc-100">"StateLock"</span>, "91f2")
          </span>
        </Line>
        <Line delay={1.85} halt>
          <span className="text-red-400">■ HALT</span>
          <span className="text-zinc-500"> — drift detected, do not coordinate</span>
        </Line>
      </div>
    </div>
  )
}

function Line({
  children,
  delay,
  halt,
}: {
  children: React.ReactNode
  delay: number
  halt?: boolean
}) {
  return (
    <div
      className="rounded px-1 -mx-1"
      style={{
        animation: halt
          ? `verdict-in 0.9s ${delay}s both, halt-flash 1.4s ${delay}s both`
          : `verdict-in 0.9s ${delay}s both`,
      }}
    >
      {children}
    </div>
  )
}
