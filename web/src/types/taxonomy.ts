export type NodeType =
  | 'PATTERN'
  | 'TAXONOMY_PATH'
  | 'CATEGORY'      // legacy — pre-0.2.0 DBs
  | 'LAYER'         // legacy — pre-0.2.0 DBs
  | 'INVARIANT'
  | 'PARAMETER'
  | 'PRECONDITION'
  | 'POSTCONDITION';

export type EdgeType =
  | 'REFERENCES'
  | 'HAS_INVARIANT'
  | 'IN_PATH'
  | 'PARENT_PATH'
  | 'IN_CATEGORY'   // legacy
  | 'IN_LAYER'      // legacy
  | 'HAS_PARAMETER'
  | 'HAS_PRECONDITION'
  | 'HAS_POSTCONDITION'
  | 'COMPOSES_WITH'
  | 'ACCEPTS'
  | 'YIELDS'
  | 'HAS_SIGNATURE';

export interface PatternMetadata {
  pattern?: {
    handle?: string;
    mechanism?: string;
    gloss?: string;
    sema_ref?: string;
    sema_stub?: string;
    tier?: number;
    ring?: number;
  };
  sema_layer?: string;
  sema_category?: string;
}

export interface GraphNode {
  id: string;
  text: string;
  type: NodeType;
  layer?: string;
  category?: string;
  handle?: string;
  gloss?: string;
  metadata: PatternMetadata;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: EdgeType;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface PatternMeta {
  tier?: number;
  ring?: number;
  layer?: string;
  category?: string;
  related?: string[];
  caution?: string;
}

export interface Pattern {
  id: string;
  handle: string;
  gloss: string;
  mechanism: string;
  invariants: string[];
  parameters: Record<string, string>;
  hash: string;
  stub: string;
  layer: string;
  category: string;
  // Additional fields from INSTRUCTION.md
  signature?: string[];
  preconditions?: string[];
  postconditions?: string[];
  failureModes?: string[];
  dataSchema?: Record<string, unknown>;
  derivedFrom?: string;
  meta?: PatternMeta;
}

export interface PatternWithRelated extends Pattern {
  relatedPatterns: Pattern[];
  dependencies?: Record<string, Record<string, string>>;
}

// Ring labels
export const RING_LABELS: Record<number, string> = {
  0: 'Kernel',
  1: 'Standard',
  2: 'Userland',
};

// Tier labels
export const TIER_LABELS: Record<number, string> = {
  0: 'Primitive',
  1: 'Ironclad',
  2: 'Honesty-Dependent',
  3: 'Experimental',
};

// Layer colors for visualization
export const LAYER_COLORS: Record<string, string> = {
  Physics: '#34d399',       // green
  Mind: '#a855f7',          // purple
  Society: '#f97316',       // orange
  Infrastructure: '#60a5fa', // blue
};

export const NODE_TYPE_COLORS: Record<NodeType, string> = {
  PATTERN: '#60a5fa',         // blue (default, overridden by layer)
  TAXONOMY_PATH: '#71717a',   // grey (overridden to layer color when depth=1)
  CATEGORY: '#71717a',        // grey (legacy)
  LAYER: '#e4e4e7',           // light grey (legacy)
  INVARIANT: '#fbbf24',       // yellow
  PARAMETER: '#22d3ee',       // cyan
  PRECONDITION: '#f472b6',    // pink
  POSTCONDITION: '#4ade80',   // green
};

export const EDGE_TYPE_COLORS: Record<EdgeType, string> = {
  REFERENCES: '#60a5fa',        // blue
  COMPOSES_WITH: '#34d399',     // green
  IN_PATH: '#52525b',           // grey — pattern → leaf taxonomy path
  PARENT_PATH: '#3f3f46',       // darker grey — child path → parent path
  IN_LAYER: '#52525b',          // grey (legacy)
  IN_CATEGORY: '#52525b',       // grey (legacy)
  HAS_INVARIANT: '#fbbf24',     // yellow (not shown in filter)
  HAS_PARAMETER: '#22d3ee',     // cyan (not shown in filter)
  HAS_PRECONDITION: '#f472b6',  // pink (not shown in filter)
  HAS_POSTCONDITION: '#4ade80', // green (not shown in filter)
  ACCEPTS: '#a855f7',           // purple
  YIELDS: '#fb923c',            // orange
  HAS_SIGNATURE: '#71717a',     // grey (not shown in filter)
};
