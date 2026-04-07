import json
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from sema.taxonomy_graph.graph_store import EdgeType, GraphStore, NodeType


def audit_rigor():
    db_path = "data/taxonomy.db"
    store = GraphStore(db_path)
    
    solutions = store.get_nodes_by_type(NodeType.SOLUTION)
    
    stats = {
        'total': len(solutions),
        'with_invariants': 0,
        'with_preconditions': 0,
        'with_postconditions': 0,
        'fully_rigorous': 0,  # Has all 3
        'naked': 0            # Has none
    }
    
    # Categories of naked patterns (guess based on name)
    naked_examples = []
    
    for sol_id, data in solutions:
        has_inv = False
        has_pre = False
        has_post = False
        
        # Check edges
        for succ in store.graph.successors(sol_id):
            edge_data = store.graph.get_edge_data(sol_id, succ)
            edge_type = edge_data.get('edge_type')
            
            if edge_type == EdgeType.HAS_INVARIANT: has_inv = True
            if edge_type == EdgeType.HAS_PRECONDITION: has_pre = True
            if edge_type == EdgeType.HAS_POSTCONDITION: has_post = True
            
        if has_inv: stats['with_invariants'] += 1
        if has_pre: stats['with_preconditions'] += 1
        if has_post: stats['with_postconditions'] += 1
        
        if has_inv and has_pre and has_post:
            stats['fully_rigorous'] += 1
            
        if not (has_inv or has_pre or has_post):
            stats['naked'] += 1
            if len(naked_examples) < 15:
                naked_examples.append(data['text'])
                
    print(json.dumps(stats, indent=2))
    print("\nSample 'Naked' Patterns (No strict logic):")
    for ex in naked_examples:
        print(f"- {ex}")

if __name__ == "__main__":
    audit_rigor()
