import { useQuery } from '@tanstack/react-query';
import type { GraphData, Pattern, PatternWithRelated } from '@/types/taxonomy';

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch ${url}: ${res.statusText}`);
  }
  return res.json();
}

export const queryKeys = {
  graph: ['graph'] as const,
  patterns: ['patterns'] as const,
  pattern: (id: string) => ['pattern', id] as const,
  search: (query: string) => ['patterns', 'search', query] as const,
  patternsByCategory: (category: string) => ['patterns', 'category', category] as const,
  patternsByLayer: (layer: string) => ['patterns', 'layer', layer] as const,
};

export function useGraph() {
  return useQuery({
    queryKey: queryKeys.graph,
    queryFn: () => fetchJson<GraphData>('/api/graph'),
    staleTime: 30000,
  });
}

export function usePatterns() {
  return useQuery({
    queryKey: queryKeys.patterns,
    queryFn: () => fetchJson<Pattern[]>('/api/patterns'),
    staleTime: 30000,
  });
}

export function usePattern(id: string | null) {
  return useQuery({
    queryKey: queryKeys.pattern(id || ''),
    queryFn: () => fetchJson<PatternWithRelated>(`/api/patterns/${id}`),
    enabled: !!id,
    staleTime: 30000,
  });
}

export interface SearchResult {
  handle: string;
  gloss: string;
  mechanism: string;
  category: string;
  layer: string;
  sema_ref: string;
  source: 'keyword' | 'semantic';
  score: number;
}

export function useSearchPatterns(query: string) {
  return useQuery({
    queryKey: queryKeys.search(query),
    queryFn: () => fetchJson<SearchResult[]>(`/api/search?q=${encodeURIComponent(query)}`),
    enabled: query.length >= 2,
    staleTime: 10000,
  });
}

export function usePatternsByCategory(category: string | null) {
  return useQuery({
    queryKey: queryKeys.patternsByCategory(category || ''),
    queryFn: () => fetchJson<Pattern[]>(`/api/patterns/by-category/${encodeURIComponent(category!)}`),
    enabled: !!category,
    staleTime: 30000,
  });
}

export function usePatternsByLayer(layer: string | null) {
  return useQuery({
    queryKey: queryKeys.patternsByLayer(layer || ''),
    queryFn: () => fetchJson<Pattern[]>(`/api/patterns/by-layer/${encodeURIComponent(layer!)}`),
    enabled: !!layer,
    staleTime: 30000,
  });
}

// Documentation
export interface DocSummary {
  slug: string;
  title: string;
  filename: string;
}

export interface DocContent {
  slug: string;
  title: string;
  content: string;
}

export function useDocs() {
  return useQuery({
    queryKey: ['docs'],
    queryFn: () => fetchJson<DocSummary[]>('/api/docs'),
    staleTime: 60000,
  });
}

export function useDoc(slug: string | null) {
  return useQuery({
    queryKey: ['docs', slug],
    queryFn: () => fetchJson<DocContent>(`/api/docs/${slug}`),
    enabled: !!slug,
    staleTime: 60000,
  });
}

export function useAllDocs() {
  const { data: docList } = useDocs();

  return useQuery({
    queryKey: ['docs', 'all'],
    queryFn: async () => {
      if (!docList) return [];
      const docs = await Promise.all(
        docList.map(d => fetchJson<DocContent>(`/api/docs/${d.slug}`))
      );
      return docs;
    },
    enabled: !!docList && docList.length > 0,
    staleTime: 60000,
  });
}
