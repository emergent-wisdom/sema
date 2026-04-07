import glob
import json
import os
from collections import defaultdict


def get_dependencies_handles(p):
    """
    Return set of Handles that this pattern depends on.
    """
    deps = set()
    d = p.get('dependencies', {})
    
    # Categorized
    for cat in ['accepts', 'yields', 'composes_with', 'references']:
        if cat in d and isinstance(d[cat], dict):
            for val in d[cat].values():
                # Extract handle from sema:Handle#hash or just Handle
                s = val.replace("sema:", "").split('#')[0].strip()
                if s: deps.add(s)
    
    return deps

def find_sccs(graph):
    """
    Tarjan's algorithm for finding SCCs.
    """
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    result = []
    
    def strongconnect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        
        try:
            successors = graph.get(node, [])
            for successor in successors:
                if successor not in index:
                    strongconnect(successor)
                    lowlink[node] = min(lowlink[node], lowlink[successor])
                elif successor in stack:
                    lowlink[node] = min(lowlink[node], index[successor])
        except RecursionError:
            # Deep recursion fallback or ignore
            pass

        if lowlink[node] == index[node]:
            connected_component = []
            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node: break
            result.append(connected_component)
    
    for node in graph:
        if node not in index:
            strongconnect(node)
            
    return result

def main():
    vocab_dir = "nextvocabulary"
    files = glob.glob(os.path.join(vocab_dir, "*.json"))
    
    patterns = {}
    for f in files:
        try:
            with open(f) as fp:
                data = json.load(fp)
                handle = data.get('handle')
                if handle:
                    patterns[handle] = data
        except:
            pass
            
    # Build Graph
    graph = defaultdict(list)
    for handle, p in patterns.items():
        deps = get_dependencies_handles(p)
        for d in deps:
            if d in patterns: # Only internal edges
                graph[handle].append(d)
                
    # Find SCCs
    sccs = find_sccs(graph)
    
    # Filter for cycles (SCC size > 1 or self loop)
    cycles = []
    for scc in sccs:
        if len(scc) > 1:
            cycles.append(scc)
        elif len(scc) == 1:
            node = scc[0]
            if node in graph.get(node, []):
                cycles.append(scc)
                
    print(f"Found {len(cycles)} cycles (Strongly Connected Components).")
    
    for i, cycle in enumerate(cycles):
        print(f"\nCycle {i+1} (Size {len(cycle)}):")
        print(f"Members: {', '.join(cycle)}")
        
        # Print internal edges to help visualization
        print("Internal Edges:")
        cycle_set = set(cycle)
        for u in cycle:
            for v in graph[u]:
                if v in cycle_set:
                    print(f"  {u} -> {v}")

if __name__ == "__main__":
    main()
