import { useEffect, useRef, useState, type ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { useDocs, useAllDocs } from '@/hooks/useApi'
import { cn } from '@/lib/utils'
import { SemaLogo } from '@/components/SemaLogo'

export function DocsPage() {
  const { data: docList, isLoading: isLoadingList } = useDocs()
  const { data: allDocs, isLoading: isLoadingDocs } = useAllDocs()
  const [activeSlug, setActiveSlug] = useState<string | null>(null)
  const sectionRefs = useRef<Map<string, HTMLElement>>(new Map())
  const tocRef = useRef<HTMLElement>(null)

  // Intersection observer for scroll spy
  useEffect(() => {
    if (!allDocs || allDocs.length === 0) return

    const observer = new IntersectionObserver(
      (entries) => {
        // Find the most visible section
        const visibleEntries = entries.filter(e => e.isIntersecting)
        if (visibleEntries.length > 0) {
          // Prefer the one closest to the top
          const sorted = visibleEntries.sort((a, b) => {
            return a.boundingClientRect.top - b.boundingClientRect.top
          })
          const topEntry = sorted.find(e => e.boundingClientRect.top >= -100) || sorted[0]
          if (topEntry) {
            setActiveSlug(topEntry.target.id)
          }
        }
      },
      {
        rootMargin: '-80px 0px -60% 0px',
        threshold: [0, 0.1, 0.5],
      }
    )

    sectionRefs.current.forEach((el) => {
      observer.observe(el)
    })

    return () => observer.disconnect()
  }, [allDocs])

  const scrollToSection = (slug: string) => {
    const el = sectionRefs.current.get(slug)
    if (el) {
      const yOffset = -100
      const y = el.getBoundingClientRect().top + window.scrollY + yOffset
      window.scrollTo({ top: y, behavior: 'smooth' })
    }
  }

  const isLoading = isLoadingList || isLoadingDocs

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      {/* Subtle grain texture overlay */}
      <div
        className="fixed inset-0 pointer-events-none opacity-[0.015] z-50"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Floating header */}
      <header className="fixed top-0 left-0 right-0 z-40 bg-zinc-950/80 backdrop-blur-xl border-b border-zinc-800/50">
        <div className="max-w-[1400px] mx-auto px-8 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-4 group">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500/20 to-emerald-500/5 border border-emerald-500/20 flex items-center justify-center text-emerald-400 group-hover:from-emerald-500/30 group-hover:to-emerald-500/10 transition-colors">
              <SemaLogo className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-lg font-medium tracking-tight">Documentation</h1>
              <p className="text-xs text-zinc-500">Sema Protocol Specification</p>
            </div>
          </Link>
          <Link
            to="/"
            className="flex items-center gap-2 text-sm text-zinc-500 hover:text-zinc-200 transition-colors group"
          >
            <ArrowLeft className="w-4 h-4 transition-transform group-hover:-translate-x-0.5" />
            Patterns
          </Link>
        </div>
      </header>

      <div className="flex">
        {/* Sticky TOC sidebar */}
        <aside
          ref={tocRef}
          className="fixed left-0 top-0 bottom-0 w-64 pt-24 pb-8 px-6 border-r border-zinc-800/50 hidden lg:block overflow-y-auto"
        >
          <nav className="space-y-1">
            <p className="text-[10px] uppercase tracking-widest text-zinc-600 mb-4 font-medium">Contents</p>
            {docList?.map((doc, index) => {
              const isActive = activeSlug === doc.slug
              return (
                <button
                  key={doc.slug}
                  type="button"
                  onClick={() => scrollToSection(doc.slug)}
                  className={cn(
                    'w-full text-left px-3 py-2 rounded-lg text-sm transition-all duration-300 flex items-start gap-3 group',
                    isActive
                      ? 'bg-zinc-800/80 text-zinc-100'
                      : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/40'
                  )}
                >
                  <span className={cn(
                    'text-[10px] font-mono mt-0.5 transition-colors',
                    isActive ? 'text-emerald-400' : 'text-zinc-600 group-hover:text-zinc-500'
                  )}>
                    {String(index + 1).padStart(2, '0')}
                  </span>
                  <span className="leading-snug">{doc.title}</span>
                </button>
              )
            })}
          </nav>

          {/* Progress indicator */}
          <div className="absolute bottom-8 left-6 right-6">
            <div className="h-px bg-zinc-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-emerald-500/50 to-emerald-400/50 transition-all duration-300"
                style={{
                  width: docList && activeSlug
                    ? `${((docList.findIndex(d => d.slug === activeSlug) + 1) / docList.length) * 100}%`
                    : '0%'
                }}
              />
            </div>
            <p className="text-[10px] text-zinc-600 mt-2 text-center">
              {docList && activeSlug && (
                <>{docList.findIndex(d => d.slug === activeSlug) + 1} of {docList.length}</>
              )}
            </p>
          </div>
        </aside>

        {/* Main content */}
        <main className="flex-1 lg:ml-64 pt-24 pb-32">
          {isLoading ? (
            <div className="max-w-3xl mx-auto px-8">
              <div className="space-y-4">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="animate-pulse">
                    <div className="h-8 bg-zinc-800/50 rounded w-1/3 mb-4" />
                    <div className="h-4 bg-zinc-800/30 rounded w-full mb-2" />
                    <div className="h-4 bg-zinc-800/30 rounded w-5/6" />
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="max-w-3xl mx-auto px-8">
              {allDocs?.map((doc, index) => (
                <section
                  key={doc.slug}
                  id={doc.slug}
                  ref={(el) => {
                    if (el) sectionRefs.current.set(doc.slug, el)
                  }}
                  className={cn(
                    'scroll-mt-28',
                    index > 0 && 'mt-24 pt-16 border-t border-zinc-800/50'
                  )}
                >
                  {/* Section header */}
                  <div className="mb-10">
                    <div className="flex items-center gap-4 mb-4">
                      <span className="text-xs font-mono text-emerald-500/70 bg-emerald-500/5 px-2 py-1 rounded border border-emerald-500/10">
                        {String(index + 1).padStart(2, '0')}
                      </span>
                      <div className="flex-1 h-px bg-gradient-to-r from-zinc-800 to-transparent" />
                    </div>
                    <h2 className="text-3xl font-semibold tracking-tight text-zinc-100">
                      {doc.title}
                    </h2>
                  </div>

                  {/* Document content */}
                  <article className="docs-content">
                    <MarkdownContent content={doc.content} onNavigate={scrollToSection} />
                  </article>
                </section>
              ))}

              {/* End marker */}
              <div className="mt-32 pt-16 border-t border-zinc-800/50 text-center">
                <div className="inline-flex items-center gap-3 text-zinc-600">
                  <div className="w-8 h-px bg-zinc-800" />
                  <span className="text-xs uppercase tracking-widest">End of Documentation</span>
                  <div className="w-8 h-px bg-zinc-800" />
                </div>
                <div className="mt-6">
                  <Link
                    to="/"
                    className="inline-flex items-center gap-2 text-sm text-zinc-500 hover:text-emerald-400 transition-colors"
                  >
                    <ArrowLeft className="w-4 h-4" />
                    Back to Pattern Library
                  </Link>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Mobile TOC toggle - floating pill */}
      <div className="fixed bottom-6 left-1/2 -translate-x-1/2 lg:hidden z-50">
        <div className="bg-zinc-900/95 backdrop-blur-xl border border-zinc-700/50 rounded-full px-4 py-2 shadow-2xl shadow-black/50">
          <div className="flex items-center gap-3 text-sm">
            <span className="text-zinc-500">Reading:</span>
            <span className="text-zinc-200 font-medium">
              {docList?.find(d => d.slug === activeSlug)?.title || 'Documentation'}
            </span>
          </div>
        </div>
      </div>

      {/* Custom styles for docs content */}
      <style>{`
        .docs-content h1 {
          font-size: 1.875rem;
          font-weight: 600;
          margin-top: 2.5rem;
          margin-bottom: 1rem;
          color: rgb(244 244 245);
          letter-spacing: -0.025em;
        }
        .docs-content h2 {
          font-size: 1.5rem;
          font-weight: 600;
          margin-top: 2.5rem;
          margin-bottom: 0.75rem;
          color: rgb(228 228 231);
          letter-spacing: -0.015em;
        }
        .docs-content h3 {
          font-size: 1.25rem;
          font-weight: 500;
          margin-top: 2rem;
          margin-bottom: 0.5rem;
          color: rgb(212 212 216);
        }
        .docs-content h4 {
          font-size: 1.125rem;
          font-weight: 500;
          margin-top: 1.5rem;
          margin-bottom: 0.5rem;
          color: rgb(161 161 170);
        }
        .docs-content p {
          color: rgb(161 161 170);
          line-height: 1.75;
          margin: 1rem 0;
        }
        .docs-content li {
          color: rgb(161 161 170);
          line-height: 1.75;
          margin-left: 1.5rem;
        }
        .docs-content blockquote {
          border-left: 2px solid rgb(39 39 42);
          padding-left: 1rem;
          margin: 1.5rem 0;
          color: rgb(113 113 122);
          font-style: italic;
        }
        .docs-content pre {
          background: rgb(24 24 27);
          border: 1px solid rgb(39 39 42);
          border-radius: 0.5rem;
          padding: 1rem;
          overflow-x: auto;
          margin: 1.5rem 0;
        }
        .docs-content code {
          font-family: 'JetBrains Mono', 'Fira Code', monospace;
          font-size: 0.875rem;
        }
        .docs-content :not(pre) > code {
          background: transparent;
          padding: 0;
          font-size: 0.875em;
          color: rgb(52 211 153);
        }
        .docs-content table {
          width: 100%;
          border-collapse: collapse;
          margin: 1.5rem 0;
        }
        .docs-content th {
          text-align: left;
          padding: 0.75rem 1rem;
          border-bottom: 1px solid rgb(63 63 70);
          color: rgb(212 212 216);
          font-weight: 500;
          font-size: 0.875rem;
        }
        .docs-content td {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid rgb(39 39 42);
          color: rgb(161 161 170);
          font-size: 0.875rem;
        }
        .docs-content hr {
          border: none;
          border-top: 1px solid rgb(39 39 42);
          margin: 2.5rem 0;
        }
        .docs-content a {
          color: rgb(52 211 153);
          text-decoration: none;
          transition: color 0.15s;
        }
        .docs-content a:hover {
          color: rgb(110 231 183);
        }
      `}</style>
    </div>
  )
}

// Simple markdown renderer
function MarkdownContent({ content, onNavigate }: { content: string; onNavigate?: (slug: string) => void }) {
  // Parse markdown to HTML-like structure
  const lines = content.split('\n')
  const elements: ReactNode[] = []
  let inCodeBlock = false
  let codeContent: string[] = []
  let codeLanguage = ''
  let inTable = false
  let tableRows: string[][] = []
  let tableHeader: string[] = []

  const processInlineFormatting = (text: string): ReactNode => {
    // Handle inline code, bold, italic, and links
    const parts: ReactNode[] = []
    let remaining = text
    let key = 0

    while (remaining.length > 0) {
      // Inline code
      const codeMatch = remaining.match(/`([^`]+)`/)
      // Bold
      const boldMatch = remaining.match(/\*\*([^*]+)\*\*/)
      // Italic
      const italicMatch = remaining.match(/\*([^*]+)\*/)
      // Links
      const linkMatch = remaining.match(/\[([^\]]+)\]\(([^)]+)\)/)

      const matches = [
        codeMatch && { type: 'code', match: codeMatch, index: codeMatch.index! },
        boldMatch && { type: 'bold', match: boldMatch, index: boldMatch.index! },
        italicMatch && { type: 'italic', match: italicMatch, index: italicMatch.index! },
        linkMatch && { type: 'link', match: linkMatch, index: linkMatch.index! },
      ].filter(Boolean).sort((a, b) => a!.index - b!.index)

      if (matches.length === 0) {
        parts.push(remaining)
        break
      }

      const first = matches[0]!
      if (first.index > 0) {
        parts.push(remaining.slice(0, first.index))
      }

      if (first.type === 'code') {
        parts.push(<code key={key++}>{first.match[1]}</code>)
      } else if (first.type === 'bold') {
        parts.push(<strong key={key++}>{processInlineFormatting(first.match[1])}</strong>)
      } else if (first.type === 'italic') {
        parts.push(<em key={key++}>{processInlineFormatting(first.match[1])}</em>)
      } else if (first.type === 'link') {
        const href = first.match[2]
        const linkText = first.match[1]

        // Check if it's an internal doc link (ends with .md)
        if (href.endsWith('.md') && onNavigate) {
          // Convert path like "core/philosophy.md" to slug "core__philosophy"
          const slug = href.replace(/\.md$/, '').replace(/\//g, '__')
          parts.push(
            <button
              key={key++}
              type="button"
              onClick={() => onNavigate(slug)}
              className="text-zinc-300 hover:text-emerald-400 transition-colors cursor-pointer"
            >
              {linkText}
            </button>
          )
        } else {
          parts.push(<a key={key++} href={href}>{linkText}</a>)
        }
      }

      remaining = remaining.slice(first.index + first.match[0].length)
    }

    return <>{parts}</>
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]

    // Code blocks
    if (line.startsWith('```')) {
      if (inCodeBlock) {
        elements.push(
          <pre key={i}>
            <code className={`language-${codeLanguage}`}>{codeContent.join('\n')}</code>
          </pre>
        )
        codeContent = []
        inCodeBlock = false
      } else {
        inCodeBlock = true
        codeLanguage = line.slice(3).trim()
      }
      continue
    }

    if (inCodeBlock) {
      codeContent.push(line)
      continue
    }

    // Tables
    if (line.includes('|') && line.trim().startsWith('|')) {
      const cells = line.split('|').filter(c => c.trim()).map(c => c.trim())

      if (!inTable) {
        inTable = true
        tableHeader = cells
      } else if (line.match(/^\|[\s:|-]+\|$/)) {
        // Separator row, skip
      } else {
        tableRows.push(cells)
      }

      // Check if next line is not a table
      if (i + 1 >= lines.length || !lines[i + 1].includes('|')) {
        elements.push(
          <div key={i} className="overflow-x-auto">
            <table>
              <thead>
                <tr>
                  {tableHeader.map((h, j) => (
                    <th key={j}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {tableRows.map((row, ri) => (
                  <tr key={ri}>
                    {row.map((cell, ci) => (
                      <td key={ci}>{processInlineFormatting(cell)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
        inTable = false
        tableRows = []
        tableHeader = []
      }
      continue
    }

    // Skip the first h1 (it's the doc title which we show in section header)
    if (line.startsWith('# ') && elements.length === 0) {
      continue
    }

    // Headers
    if (line.startsWith('# ')) {
      elements.push(<h1 key={i}>{processInlineFormatting(line.slice(2))}</h1>)
    } else if (line.startsWith('## ')) {
      elements.push(<h2 key={i}>{processInlineFormatting(line.slice(3))}</h2>)
    } else if (line.startsWith('### ')) {
      elements.push(<h3 key={i}>{processInlineFormatting(line.slice(4))}</h3>)
    } else if (line.startsWith('#### ')) {
      elements.push(<h4 key={i}>{processInlineFormatting(line.slice(5))}</h4>)
    }
    // Blockquotes
    else if (line.startsWith('> ')) {
      elements.push(
        <blockquote key={i}>
          {processInlineFormatting(line.slice(2))}
        </blockquote>
      )
    }
    // Unordered lists
    else if (line.match(/^[\*\-]\s/)) {
      elements.push(
        <li key={i} className="list-disc">
          {processInlineFormatting(line.slice(2))}
        </li>
      )
    }
    // Ordered lists
    else if (line.match(/^\d+\.\s/)) {
      const content = line.replace(/^\d+\.\s/, '')
      elements.push(
        <li key={i} className="list-decimal">
          {processInlineFormatting(content)}
        </li>
      )
    }
    // Horizontal rule
    else if (line.match(/^---+$/)) {
      elements.push(<hr key={i} />)
    }
    // Empty lines
    else if (line.trim() === '') {
      // Skip empty lines (spacing handled by CSS)
    }
    // Regular paragraphs
    else {
      elements.push(<p key={i}>{processInlineFormatting(line)}</p>)
    }
  }

  return <>{elements}</>
}
