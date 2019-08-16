#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 19:40:23 2019

@author: labuser
"""

import networkx as nx
from matplotlib import pyplot as plt
from itertools import product
import random
import numpy as np

class S2_graph(object):
    
    def __init__(self, nr = 8, nc = 8, ratio = 0.5, budget=15):
        self.pos_list=[]
        self.neg_list=[]
        self.queried_pts={}
        self.shortest2_path=[]
        self.budget=budget
        self.nr = nr
        self.nc = nc
        self.ratio = ratio
        self.label_prop={}
        self.G = None
        self.add_pos = False
        self.add_neg = False
        self.draw_binary_grid_graph()
        
    def draw_binary_grid_graph(self, fig_num=0, c1='y', c2='g'):
        (N_c, N_r) = (self.nc, self.nr)
        if self.G is None:
            self.G=nx.grid_2d_graph(N_c, N_r)
        pos = dict( (n, n) for n in self.G.nodes() )
        labels = dict( ((i, j), i * N_r + j) for i, j in self.G.nodes() )
        for (i,j) in labels:
            self.G.node[(i,j)]['id'] = labels[(i,j)]
        
        # draw nodes with diff colors according to classes
        plt.figure()
        list1 = range(int(N_c*self.ratio))
        list2 = range(N_r)
        tot_list = []
        tot_list.append(list1)
        tot_list.append(list2)
        class_1 = list(product(*tot_list))
        for (i,j) in class_1:
            self.G.node[(i,j)]['label'] = 1
        nx.draw_networkx_nodes(self.G, pos=pos, nodelist=class_1, node_size=50, node_color=c1)
        
        list1 = range(int(N_c*self.ratio),N_c)
        list2 = range(N_r)
        tot_list = []
        tot_list.append(list1)
        tot_list.append(list2)
        class_2 = list(product(*tot_list))
        for (i,j) in class_2:
            self.G.node[(i,j)]['label'] = 0
        nx.draw_networkx_nodes(self.G, pos=pos, nodelist=class_2, node_size=50, node_color=c2)
        
        if self.queried_pts != {}:
            nx.draw_networkx_nodes(self.G, pos=pos, nodelist=list(self.queried_pts.keys()), node_size=50, node_color='b')
        
        # draw edges and the corresponding labels
        print(len(self.G.edges()))
        nx.draw_networkx_edges(self.G, pos=pos)
#        nx.draw_networkx_labels(self.G, pos=pos, labels=labels, font_size=7)
        
        plt.axis('off')
        plt.text(2, 10, s="Budget: "+str(len(self.queried_pts))+" Total Budget: "+str(self.budget), fontsize=20)
        plt.savefig('S2_progress_'+str(fig_num)+'.png')
    
    
def sample_graph(graph):
    
    sampling_graph = list(set(graph.G.node()) - set(graph.queried_pts.keys()))
    
    z = random.choice(sampling_graph)
    if graph.G.node[z]['label']==1:
        graph.pos_list.append(z)
        graph.queried_pts[z]=1
    else:
        graph.neg_list.append(z)
        graph.queried_pts[z]=0
        
    return graph
        
def S2_new(graph):
    
    while True:
        graph = sample_graph(graph)
        
        while True:
            for node1 in graph.queried_pts.keys():
                for node2 in graph.queried_pts.keys():
                    if node1 in graph.G.neighbors(node2):
                        if graph.queried_pts[node1] + graph.queried_pts[node2] == 1: # check for oppositely labelled points being connected
                            graph.G.remove_edge(node1, node2)
                        
            if len(graph.queried_pts) >= graph.budget:
                label_completion(graph)
                return
            
            graph, ret_mssp = mssp(graph) 
            
            if ret_mssp is None:
                break           
            
def mssp(graph):
    
    shortest_paths=[]
    
    if len(graph.pos_list)==0 or len(graph.neg_list)==0: # if no oppositely paired pts exist, u cant do S2
        return graph, None
    
    try:
        for i in range(len(graph.neg_list)):
            for j in range(len(graph.pos_list)):
                shortest_paths.append(nx.shortest_path(graph.G, source=graph.pos_list[j], target=graph.neg_list[i]))
    except:
        # when no SP exist or u have only + or only - queried pts
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
    
    

def label_completion(graph):
        wt = nx.adjacency_matrix(graph.G)
        wt = wt.todense()
        graph.weight = np.zeros((graph.nc*graph.nr, graph.nc*graph.nr))
        queried_id = [graph.G.nodes[iden]['id'] for iden in graph.queried_pts]
        queried_labels = np.array([graph.queried_pts[iden] for iden in graph.queried_pts])
        tot = list(range(graph.nc*graph.nr))
        non_queried = list(set(tot) - set(queried_id))
        
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
            
        graph.class_1 = []
        graph.class_2 = []
        for key in graph.label_prop:
            if graph.label_prop[key]==1:
                graph.class_1.append(key)
            else:
                graph.class_2.append(key)
        
        graph.draw_binary_grid_graph(c1='r', c2='c')


S2Graph = S2_graph(nr=50, nc=50, ratio=0.8, budget=40)
S2_new(S2Graph)
