#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 23:27:39 2019

@author: kaushik
"""

import networkx as nx
import random
import numpy as np

def S2(graph,org_graph,coarse_flag=True):
    
    while True:
        
        graph,sample_flag = sample_graph(graph)
#        print("Inside S2",len(graph.queried_pts),sample_flag,coarse_flag)
        
        if not sample_flag:
            return sample_flag
        
        while True:
            
            if coarse_flag:
                if len({**org_graph.queried_pts, **graph.queried_pts}) >= graph.budget: #len(graph.queried_pts)
                    org_graph.queried_pts = {**org_graph.queried_pts, **graph.queried_pts}
                    label_completion(org_graph)
                    return sample_flag
            else:
                if len(graph.queried_pts) >= graph.budget:
                    label_completion(graph)
                    return sample_flag
            
            qp = graph.queried_pts.keys()
            for node1 in qp:
                for node2 in qp:
                    if node1 in graph.G.neighbors(node2):
                        if graph.queried_pts[node1] + graph.queried_pts[node2] == 1: # check for oppositely labelled points being connected
                            
                            graph.G.remove_edge(node1, node2)
                            if coarse_flag:
                                if graph.G.node[node1]['label']==1:
                                    bisect_sp(org_graph,node1,node2)
                                else:
                                    bisect_sp(org_graph,node2,node1)
            
            graph, ret_mssp = mssp(graph) 
            
            if ret_mssp is None:
                break           


def sample_graph(graph):
    
    sampling_graph = list(set(graph.G.node()) - set(graph.queried_pts.keys()))
    
    try:
        z = random.choice(sampling_graph)
        if graph.G.node[z]['label']==1:
            graph.pos_list.append(z)
            graph.queried_pts[z]=1
        else:
            graph.neg_list.append(z)
            graph.queried_pts[z]=0
        
        return graph,True
    
    except:
        return graph,False
               
            
def mssp(graph):
    
    shortest_paths=[]
    
    if len(graph.pos_list)==0 or len(graph.neg_list)==0: # if no oppositely paired pts exist, u cant do S2
        return graph, None
    
    try:
        for i in range(len(graph.neg_list)):
            for j in range(len(graph.pos_list)):
                shortest_paths.append(nx.shortest_path(graph.G, source=graph.pos_list[j], target=graph.neg_list[i]))
    except:
        return graph, None
    
    shortest2_path_index = min([(len(shortest_paths[i]),i) for i in range(len(shortest_paths))], key=lambda t: t[0])[1] 
    shortest2_path = shortest_paths[shortest2_path_index] 
    
    mid_pt = shortest2_path[int(len(shortest2_path)/2)]
    if graph.G.node[mid_pt]['label']==1:
        graph.queried_pts[mid_pt]=1
        graph.pos_list.append(mid_pt)
    else:
        graph.queried_pts[mid_pt]=0
        graph.neg_list.append(mid_pt)
    
    return graph, True

def bisect_sp(org_graph, node1, node2):
    
    sp = nx.shortest_path(org_graph.G, source=node1, target=node2)
    
    if len(org_graph.queried_pts)>org_graph.budget:
        return
    
    while(len(sp)!=2 and len(org_graph.queried_pts)<org_graph.budget):
        if org_graph.G.node[sp[int(len(sp)/2)]]['label']==1:
            org_graph.queried_pts[sp[int(len(sp)/2)]]=1
            sp = sp[int(len(sp)/2):]
        else:
            org_graph.queried_pts[sp[int(len(sp)/2)]]=0
            sp = sp[:int(len(sp)/2)+1]
    print(sp)
    org_graph.G.remove_edge(*tuple(sp))

def label_completion(graph):
    wt = nx.adjacency_matrix(graph.G)
    wt = wt.todense()
    graph.weight = np.zeros((graph.nc*graph.nr, graph.nc*graph.nr))
    queried_id = [graph.G.nodes[iden]['id'] for iden in graph.queried_pts]
    queried_labels = np.array([graph.queried_pts[iden] for iden in graph.queried_pts])
    tot = list(range(graph.nc*graph.nr))
    
    non_queried = list(set(tot) - set(queried_id))
    
    if non_queried != []:
    
        # W_ll
        rows = np.array(queried_id)
        cols = np.array(queried_id)
        graph.weight[0:len(queried_id), 0:len(queried_id)] = wt[rows[:,None],cols]
        
        # W_lu
        rows = np.array(queried_id)
        cols = np.array(non_queried)
        graph.weight[0:len(queried_id), len(queried_id):] = wt[rows[:,None],cols]
        
        # W_ul
        rows = np.array(non_queried)
        cols = np.array(queried_id)
        graph.weight[len(queried_id):, 0:len(queried_id)] = wt[rows[:,None],cols]
        
        # W_uu
        rows = np.array(non_queried)
        cols = np.array(non_queried)
        graph.weight[len(queried_id):, len(queried_id):] = wt[rows[:,None],cols]
        
    else:
        # W_ll
        rows = np.array(queried_id)
        cols = np.array(queried_id)
        graph.weight[0:len(queried_id), 0:len(queried_id)] = wt[rows[:,None],cols]
    
    # Z-L-G algorithm
    d_vec = np.sum(graph.weight,axis=1)
    D_inv = np.diag(1./d_vec)
    
    P = np.matmul(D_inv, graph.weight)
    
    I = np.eye(len(non_queried))
    v1 = np.linalg.inv(I - P[len(queried_id):, len(queried_id):])
    v2 = np.matmul(P[len(queried_id):, 0:len(queried_id)], queried_labels)
    f_u = np.matmul(v1, v2)
    f_u[np.where(f_u>=0.5)]=1
    f_u[np.where(f_u<0.5)]=0
    
    # Visualize the results after applying Z-L-G
    
    for i in range(len(non_queried)):
        nq = (int(non_queried[i]/graph.nr), non_queried[i]%graph.nr)
        graph.label_prop[nq] = f_u[i]
        
    graph.class1 = []
    graph.class2 = []
    for key in graph.label_prop:
        if graph.label_prop[key]==1:
            graph.class1.append(key)
        else:
            graph.class2.append(key)
    
    graph.draw_binary_grid_graph(c1='r', c2='c')