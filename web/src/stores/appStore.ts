import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { GraphNode, NodeType, EdgeType } from '@/types/taxonomy';

// Edge types grouped for filtering UI. Legacy IN_LAYER / IN_CATEGORY
// are intentionally excluded — they don't exist in 0.2.0+ DBs.
export const SEMANTIC_EDGE_TYPES: EdgeType[] = ['REFERENCES', 'COMPOSES_WITH'];
export const STRUCTURAL_EDGE_TYPES: EdgeType[] = [
  'IN_PATH',
  'PARENT_PATH',
  'ACCEPTS',
  'YIELDS',
];
export const ALL_FILTERABLE_EDGE_TYPES: EdgeType[] = [...SEMANTIC_EDGE_TYPES, ...STRUCTURAL_EDGE_TYPES];

interface AppState {
  // Selection
  selectedNodeId: string | null;
  hoveredNode: GraphNode | null;
  pendingFlyToNodeId: string | null;

  // Filters
  filterByLayer: string | null;
  filterByCategory: string | null;
  showNodeTypes: Set<NodeType>;
  showEdgeTypes: Set<EdgeType>;
  searchQuery: string;

  // UI State
  detailsPanelOpen: boolean;

  // Actions
  selectNode: (id: string | null) => void;
  selectNodeAndFly: (id: string) => void;
  setHoveredNode: (node: GraphNode | null) => void;
  setFilterByLayer: (layer: string | null) => void;
  setFilterByCategory: (category: string | null) => void;
  toggleNodeType: (type: NodeType) => void;
  toggleEdgeType: (type: EdgeType) => void;
  setSearchQuery: (query: string) => void;
  setDetailsPanelOpen: (open: boolean) => void;
  clearPendingFly: () => void;
}

const DEFAULT_SHOW_NODE_TYPES: NodeType[] = ['PATTERN', 'TAXONOMY_PATH'];
// Show everything on load — the dense interconnection IS the graph's
// story. Primitives get hundreds of incoming REFERENCES; hiding those
// by default made the library look sparser than it actually is. Users
// who find it too busy can toggle REFERENCES off.
const DEFAULT_SHOW_EDGE_TYPES: EdgeType[] = [
  'REFERENCES',
  'COMPOSES_WITH',
  'IN_PATH',
  'PARENT_PATH',
  'ACCEPTS',
  'YIELDS',
];

// Bump this when DEFAULT_SHOW_* changes so persisted state is invalidated.
// Merge logic rehydrates defaults when the saved version is stale — so users
// with old filter selections picked up new node/edge types automatically
// instead of staring at an empty graph after a schema migration.
const APP_STORE_VERSION = 4;

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      selectedNodeId: null,
      hoveredNode: null,
      pendingFlyToNodeId: null,
      filterByLayer: null,
      filterByCategory: null,
      showNodeTypes: new Set(DEFAULT_SHOW_NODE_TYPES),
      showEdgeTypes: new Set(DEFAULT_SHOW_EDGE_TYPES),
      searchQuery: '',
      detailsPanelOpen: true,

      selectNode: (id) =>
        set({
          selectedNodeId: id,
          detailsPanelOpen: id !== null,
        }),

      selectNodeAndFly: (id) =>
        set({
          selectedNodeId: id,
          pendingFlyToNodeId: id,
          detailsPanelOpen: true,
        }),

      setHoveredNode: (node) => set({ hoveredNode: node }),

      setFilterByLayer: (layer) => set({ filterByLayer: layer }),

      setFilterByCategory: (category) => set({ filterByCategory: category }),

      toggleNodeType: (type) =>
        set((state) => {
          const newSet = new Set(state.showNodeTypes);
          if (newSet.has(type)) {
            newSet.delete(type);
          } else {
            newSet.add(type);
          }
          return { showNodeTypes: newSet };
        }),

      toggleEdgeType: (type) =>
        set((state) => {
          const newSet = new Set(state.showEdgeTypes);
          if (newSet.has(type)) {
            newSet.delete(type);
          } else {
            newSet.add(type);
          }
          return { showEdgeTypes: newSet };
        }),

      setSearchQuery: (query) => set({ searchQuery: query }),

      setDetailsPanelOpen: (open) => set({ detailsPanelOpen: open }),

      clearPendingFly: () => set({ pendingFlyToNodeId: null }),
    }),
    {
      name: 'sema-app-store',
      version: APP_STORE_VERSION,
      partialize: (state) => ({
        detailsPanelOpen: state.detailsPanelOpen,
        showNodeTypes: Array.from(state.showNodeTypes),
        showEdgeTypes: Array.from(state.showEdgeTypes),
      }),
      merge: (persisted, current) => {
        const p = persisted as {
          showNodeTypes?: NodeType[];
          showEdgeTypes?: EdgeType[];
          version?: number;
        };
        // Stale persisted state — discard filter selections so new default
        // types (e.g. TAXONOMY_PATH after the path-based migration) are
        // visible immediately without a manual toggle.
        if (!p?.version || p.version < APP_STORE_VERSION) {
          return { ...current };
        }
        return {
          ...current,
          showNodeTypes: p?.showNodeTypes
            ? new Set(p.showNodeTypes)
            : current.showNodeTypes,
          showEdgeTypes: p?.showEdgeTypes
            ? new Set(p.showEdgeTypes)
            : current.showEdgeTypes,
        };
      },
    }
  )
);
