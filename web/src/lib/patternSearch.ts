import type { Pattern } from '@/types/taxonomy'

const STOP_WORDS = new Set([
  'a',
  'an',
  'and',
  'between',
  'by',
  'for',
  'from',
  'in',
  'of',
  'on',
  'or',
  'the',
  'to',
  'with',
])

export interface RankedPattern {
  pattern: Pattern
  score: number
}

function searchableHandle(pattern: Pattern): string {
  return `${pattern.id} ${pattern.handle.split('#')[0]}`
    .replace(/([a-z0-9])([A-Z])/g, '$1 $2')
    .toLowerCase()
}

export function rankPatterns(patterns: Pattern[], rawQuery: string): RankedPattern[] {
  const query = rawQuery.trim().toLowerCase().replace(/\s+/g, ' ')
  if (query.length < 2) return []

  const rawTerms = query.split(' ').filter((term) => term.length >= 2)
  const meaningfulTerms = rawTerms.filter((term) => !STOP_WORDS.has(term))
  const terms = meaningfulTerms.length > 0 ? meaningfulTerms : rawTerms

  return patterns
    .map((pattern) => {
      const handle = searchableHandle(pattern)
      const compactQuery = query.replace(/\s+/g, '')
      const compactHandles = [pattern.id, pattern.handle.split('#')[0]].map((value) =>
        value.toLowerCase().replace(/\s+/g, ''),
      )
      const signature = (pattern.signature ?? []).join(' ').toLowerCase()
      const gloss = (pattern.gloss ?? '').toLowerCase()
      const category = (pattern.category ?? '').toLowerCase()
      const mechanism = (pattern.mechanism ?? '').toLowerCase()
      const layer = (pattern.layer ?? '').toLowerCase()

      let score = 0
      let matchedTerms = 0

      for (const term of terms) {
        const compactTerm = term.replace(/\s+/g, '')
        const termScore = Math.max(
          handle.includes(term) || compactHandles.some((value) => value.includes(compactTerm))
            ? 120
            : 0,
          signature.includes(term) ? 80 : 0,
          gloss.includes(term) ? 70 : 0,
          category.includes(term) ? 50 : 0,
          mechanism.includes(term) ? 40 : 0,
          layer.includes(term) ? 30 : 0,
        )
        if (termScore > 0) {
          score += termScore
          matchedTerms += 1
        }
      }

      if (matchedTerms === 0) return null

      const exactHandle = compactHandles.some((value) => value === compactQuery)
      const handlePrefix = compactHandles.some((value) => value.startsWith(compactQuery))
      const phraseMatch = [handle, signature, gloss, mechanism].some((field) =>
        field.includes(query),
      )
      const coverage = matchedTerms / Math.max(terms.length, 1)

      score += coverage * 200
      if (phraseMatch) score += 250
      if (handlePrefix) score += 500
      if (exactHandle) score += 500

      return { pattern, score }
    })
    .filter((result): result is RankedPattern => result !== null)
    .sort(
      (a, b) =>
        b.score - a.score || a.pattern.handle.localeCompare(b.pattern.handle),
    )
}
