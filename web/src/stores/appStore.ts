import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { GraphNode, NodeType, EdgeType } from '@/types/taxonomy';

// Edge types grouped for filtering UI
export const SEMANTIC_EDGE_TYPES: EdgeType[] = ['REFERENCES', 'COMPOSES_WITH'];
export const STRUCTURAL_EDGE_TYPES: EdgeType[] = ['IN_LAYER', 'IN_CATEGORY', 'ACCEPTS', 'YIELDS'];
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

const DEFAULT_SHOW_NODE_TYPES: NodeType[] = ['PATTERN', 'CATEGORY', 'LAYER'];
// Default: all edges except REFERENCES (too many connections)
const DEFAULT_SHOW_EDGE_TYPES: EdgeType[] = ['COMPOSES_WITH', 'IN_LAYER', 'IN_CATEGORY', 'ACCEPTS', 'YIELDS'];

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
      partialize: (state) => ({
        detailsPanelOpen: state.detailsPanelOpen,
        showNodeTypes: Array.from(state.showNodeTypes),
        showEdgeTypes: Array.from(state.showEdgeTypes),
      }),
      merge: (persisted, current) => {
        const p = persisted as { showNodeTypes?: NodeType[]; showEdgeTypes?: EdgeType[] };
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
