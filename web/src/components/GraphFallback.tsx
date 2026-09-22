import { Component, type ReactNode } from 'react'
import { Link } from 'react-router-dom'

export function supportsWebGL(): boolean {
  try {
    const canvas = document.createElement('canvas')
    return Boolean(canvas.getContext('webgl2') || canvas.getContext('webgl'))
  } catch {
    return false
  }
}

export function NoGraph() {
  return (
    <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 px-6 text-center">
      <p className="max-w-sm text-sm leading-6 text-zinc-400">
        The interactive graph needs WebGL, which this browser did not provide.
      </p>
      <Link
        to="/"
        className="text-sm font-medium text-emerald-400 transition-colors hover:text-emerald-300"
      >
        Browse the patterns as a list instead
      </Link>
    </div>
  )
}

// A failing 3D renderer must not take the whole page down with it.
export class GraphBoundary extends Component<
  { fallback: ReactNode; children: ReactNode },
  { failed: boolean }
> {
  state = { failed: false }

  static getDerivedStateFromError() {
    return { failed: true }
  }

  componentDidCatch(error: unknown) {
    console.warn('Graph unavailable', error)
  }

  render() {
    return this.state.failed ? this.props.fallback : this.props.children
  }
}
