#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 10:01:53 2019

@author: labuser
"""

import networkx as nx
import random
from defineGraph import Graph
     
def coarsen_graph(graph, level=1):
    
    if level==0:
        return graph,False
    
    V = set(list(graph.G.nodes))
    V_tilde = set()
    U_tilde = set()
    
    updated_set = V
    while bool(updated_set):
        rand_vertex = random.sample(updated_set, k=1)[0]
        V_tilde.add(rand_vertex)
        neighbors = list(nx.single_source_shortest_path_length(graph.G, rand_vertex, cutoff=level).keys())
        for i in neighbors:
            U_tilde.add(i)
            
        updated_set = updated_set - V_tilde - U_tilde
    
    remove_nodes = V - V_tilde
    
    # define edges for coarsened graph
    edge_list = []
    for i in V_tilde:
        n1 = set(nx.single_source_shortest_path_length(graph.G, i, cutoff=level).keys())
        for j in V_tilde-set(i):
            n2 = set(nx.single_source_shortest_path_length(graph.G, j, cutoff=level).keys())
            val = set.intersection(n1,n2)
            if bool(val):
                edge_list.append((i, j))
    
    coarse_graph = Graph(nr=graph.nr, nc=graph.nc, ratio=graph.ratio, budget=graph.budget)
    coarse_graph.G = nx.create_empty_copy(coarse_graph.G)
    coarse_graph.G.update(edges=edge_list)
    
    for n in remove_nodes:
        coarse_graph.G.remove_node(n)
    
    coarse_graph.class1=[]
    coarse_graph.class2=[]
    for (i,j) in coarse_graph.G.nodes:
       if coarse_graph.G.node[(i,j)]['label']==1:
           coarse_graph.class1.append((i,j))
       else:
           coarse_graph.class2.append((i,j))
    
    return coarse_graph,True
