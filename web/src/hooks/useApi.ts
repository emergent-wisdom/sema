import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import type { GraphData, Pattern, PatternWithRelated } from '@/types/taxonomy';

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch ${url}: ${res.statusText}`);
  }
  return res.json();
}

async function postJson<T>(url: string, body: unknown): Promise<T> {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json();
}

export interface DbInfo {
  name: string;
  path: string;
  active: boolean;
  bundled: boolean;
  exists: boolean;
}

export interface DbList {
  current: string;
  databases: DbInfo[];
}

export function useDbs() {
  return useQuery({
    queryKey: ['dbs'],
    queryFn: async () => {
      const res = await fetch('/api/dbs');
      if (res.status === 404) return null;  // Production deploy — DB management disabled
      if (!res.ok) throw new Error(`Failed to fetch /api/dbs: ${res.statusText}`);
      return res.json() as Promise<DbList>;
    },
    staleTime: 5000,
    retry: false,
    refetchInterval: 5000,
  });
}

// True when the server has DB management enabled (local mode).
// Used to gate live-refresh polling.
export function useIsLocal(): boolean {
  const { data } = useDbs();
  return data !== null && data !== undefined;
}

const LOCAL_POLL_MS = 5000;

function pollIfLocal(isLocal: boolean): number | false {
  return isLocal ? LOCAL_POLL_MS : false;
}

export function useSwitchDb() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: { path?: string; default?: boolean }) =>
      postJson<{ success: boolean; db_path: string; total_patterns: number }>('/api/use', payload),
    onSuccess: () => {
      // Invalidate everything that depends on the active DB
      qc.invalidateQueries({ queryKey: ['dbs'] });
      qc.invalidateQueries({ queryKey: ['graph'] });
      qc.invalidateQueries({ queryKey: ['patterns'] });
      qc.invalidateQueries({ queryKey: ['pattern'] });
    },
  });
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
  const isLocal = useIsLocal();
  return useQuery({
    queryKey: queryKeys.graph,
    queryFn: () => fetchJson<GraphData>('/api/graph'),
    staleTime: isLocal ? 1000 : 30000,
    refetchInterval: pollIfLocal(isLocal),
    refetchIntervalInBackground: false,
  });
}

export function usePatterns() {
  const isLocal = useIsLocal();
  return useQuery({
    queryKey: queryKeys.patterns,
    queryFn: () => fetchJson<Pattern[]>('/api/patterns'),
    staleTime: isLocal ? 1000 : 30000,
    refetchInterval: pollIfLocal(isLocal),
    refetchIntervalInBackground: false,
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
