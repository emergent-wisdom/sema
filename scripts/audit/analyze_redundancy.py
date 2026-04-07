#!/usr/bin/env python3
"""
Analyze Redundancy Script
Finds structural rhymes in the taxonomy to aid deduplication.
"""

import os
import sys

# Fix import path
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'orthogonal-insight-engine'))

from sema.taxonomy_graph.graph_store import GraphStore, NodeType

TAXONOMY_DB = "data/taxonomy.db"

def analyze():
    print(f"🔍 Analyzing Taxonomy Redundancy in {TAXONOMY_DB}...")
    store = GraphStore(TAXONOMY_DB)
    
    # 1. Analyze Scenarios
    scenarios = store.get_nodes_by_type(NodeType.SCENARIO)
    print(f"  Total Scenarios: {len(scenarios)}")
    
    # Check for semantic overlap between scenarios themselves
    # (This finds patterns used in similar contexts)
    print("\n  [Scenario Clusters]")
    
    # Group by simple similarity check (O(N^2) but N=30 is fine)
    # In a real app, use clustering algorithm
    
    processed = set()
    clusters = []
    
    for i, (id1, data1) in enumerate(scenarios):
        if id1 in processed: continue
        
        cluster = [(id1, data1)]
        processed.add(id1)
        
        embedding1 = store.embedding_service.get_embedding(data1['text'])
        
        for j, (id2, data2) in enumerate(scenarios):
            if i == j or id2 in processed: continue
            
            embedding2 = store.embedding_service.get_embedding(data2['text'])
            sim = store.embedding_service.cosine_similarity(embedding1, embedding2)
            
            if sim > 0.75: # Broad threshold for "Related Contexts"
                cluster.append((id2, data2))
                processed.add(id2)
        
        if len(cluster) > 1:
            clusters.append(cluster)

    # Report Clusters
    for cluster in clusters:
        print(f"  Cluster ({len(cluster)} scenarios):")
        for node_id, data in cluster:
            # Find solutions linked to this scenario
            preds = [p for p in store.graph.predecessors(node_id) 
                     if store.graph.nodes[p]['node_type'] == NodeType.SOLUTION]
            
            linked_sols = [store.graph.nodes[p]['text'] for p in preds]
            print(f"    - \"{data['text'][:80]}...\"")
            print(f"      ↳ Solved by: {', '.join(linked_sols)}")
        print("")

    # 2. Analyze Mechanism Overlap
    # (Do different patterns use very similar mechanisms?)
    print("  [Mechanism Overlap]")
    mechanisms = store.get_nodes_by_type(NodeType.MECHANISM)
    
    # Quick check for high similarity
    for i, (id1, data1) in enumerate(mechanisms):
        emb1 = store.embedding_service.get_embedding(data1['text'])
        for j, (id2, data2) in enumerate(mechanisms):
            if i >= j: continue
            
            emb2 = store.embedding_service.get_embedding(data2['text'])
            sim = store.embedding_service.cosine_similarity(emb1, emb2)
            
            if sim > 0.80:
                print(f"  ⚠️ High Similarity ({sim:.2f}):")
                print(f"     A: {data1['text'][:100]}...")
                print(f"     B: {data2['text'][:100]}...")

if __name__ == "__main__":
    analyze()
