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
        self.G = None
        self.add_pos = False
        self.add_neg = False
        self.draw_binary_grid_graph()
        
    def draw_binary_grid_graph(self, fig_num=0):
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
        nx.draw_networkx_nodes(self.G, pos=pos, nodelist=class_1, node_size=50, node_color='y')
        
        list1 = range(int(N_c*self.ratio),N_c)
        list2 = range(N_r)
        tot_list = []
        tot_list.append(list1)
        tot_list.append(list2)
        class_2 = list(product(*tot_list))
        for (i,j) in class_2:
            self.G.node[(i,j)]['label'] = 0
        nx.draw_networkx_nodes(self.G, pos=pos, nodelist=class_2, node_size=50, node_color='g')
        
        if self.queried_pts != {}:
            nx.draw_networkx_nodes(self.G, pos=pos, nodelist=list(self.queried_pts.keys()), node_size=50, node_color='b')
        
        # draw edges and the corresponding labels
        print(len(self.G.edges()))
        nx.draw_networkx_edges(self.G, pos=pos)
#        nx.draw_networkx_labels(self.G, pos=pos, labels=labels, font_size=7)
        
        plt.axis('off')
        plt.text(2, 10, s="Budget: "+str(len(self.queried_pts))+" Total Budget: "+str(self.budget), fontsize=20)
        plt.savefig('S2_progress_'+str(fig_num)+'.png')
        
    def sample_graph(self):
        self.sampling_graph = list(self.G.node())
        (prev_len_pos, prev_len_neg) = (len(self.pos_list), len(self.neg_list))
        while(prev_len_pos>=len(self.pos_list) or prev_len_neg>=len(self.neg_list)):
            z = random.choice(self.sampling_graph)
            if self.G.node[z]['label']==1:
                self.pos_list.append(z)
                self.queried_pts[z]=1
            else:
                self.neg_list.append(z)
                self.queried_pts[z]=0
            self.sampling_graph.remove(z)

def S2(graph, init=False):
    
    shortest_paths = []
    
    try:
#        if init:
#            for i in range(len(graph.neg_list)):
#                for j in range(len(graph.pos_list)):
#                    graph.shortest_paths.append(nx.shortest_path(graph.G, source=graph.pos_list[j], target=graph.neg_list[i]))
#        else:
#            if graph.add_pos:
#                for j in range(len(graph.neg_list)):
#                    graph.shortest_paths.append(nx.shortest_path(graph.G, source=graph.pos_list[-1], target=graph.neg_list[j]))
#            else:
#                for j in range(len(graph.pos_list)):
#                    graph.shortest_paths.append(nx.shortest_path(graph.G, source=graph.pos_list[j], target=graph.neg_list[-1]))
        
        for i in range(len(graph.neg_list)):
                for j in range(len(graph.pos_list)):
                    shortest_paths.append(nx.shortest_path(graph.G, source=graph.pos_list[j], target=graph.neg_list[i]))
            
    except:
        graph.shortest2_path = None
        return graph
            
    graph.shortest_paths = shortest_paths
    
    shortest2_path_index = min([(len(graph.shortest_paths[i]),i) for i in range(len(graph.shortest_paths))], key=lambda t: t[0])[1] 
    graph.shortest2_path = graph.shortest_paths[shortest2_path_index] 
        
    
    mid_pt = graph.shortest2_path[int(len(graph.shortest2_path)/2)]
    if graph.G.node[mid_pt]['label']==1:
        graph.queried_pts[mid_pt]=1
        graph.add_pos = True
        graph.add_neg = False
        graph.pos_list.append(mid_pt)
    else:
        graph.queried_pts[mid_pt]=0
        graph.neg_list.append(mid_pt)
        graph.add_neg = True
        graph.add_pos = False
    
    return graph


S2Graph = S2_graph(nr=40, nc=100, ratio=0.5, budget=40)
S2Graph.sample_graph()
S2Graph.draw_binary_grid_graph()

S2Graph = S2(S2Graph, init=True)

while len(S2Graph.queried_pts) <= S2Graph.budget and S2Graph.shortest2_path is not None:
    
    S2Graph = S2(S2Graph)
    
    # finds cut edge
    try:
        while len(S2Graph.queried_pts) <= S2Graph.budget and len(S2Graph.shortest2_path)>2:
            S2Graph = S2(S2Graph)
            print(len(S2Graph.G.edges()))
            
        S2Graph.G.remove_edge(*tuple(S2Graph.shortest2_path))
    except:
        break
    
S2Graph.draw_binary_grid_graph()

    



