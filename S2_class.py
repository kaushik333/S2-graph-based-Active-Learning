#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 13:37:42 2019

@author: Kaushik Koneripalli
"""
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product
import random

class S2(object):
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
            

    def find_shortest2_path(self):        
        shortest_paths = []
        try:
            if len(self.neg_list) < len(self.pos_list):
                for i in range(len(self.pos_list)):
                    shortest_paths.append(nx.shortest_path(self.G, source=self.pos_list[i], target=self.neg_list[-1]))
            else:
                for i in range(len(self.neg_list)):
                    shortest_paths.append(nx.shortest_path(self.G, source=self.pos_list[-1], target=self.neg_list[i]))
        
            shortest2_path_index = min([(len(shortest_paths[i]),i) for i in range(len(shortest_paths))], key=lambda t: t[0])[1] 
            self.shortest2_path = shortest_paths[shortest2_path_index]  
        except:
            self.shortest2_path = None
            
    
    def find_cut_edge(self):
        while(len(self.shortest2_path)!=2 and len(self.queried_pts)<self.budget):
            if self.G.node[self.shortest2_path[int(len(self.shortest2_path)/2)]]['label']==1:
                self.queried_pts[self.shortest2_path[int(len(self.shortest2_path)/2)]]=1
                self.shortest2_path = self.shortest2_path[int(len(self.shortest2_path)/2):]
            else:
                self.queried_pts[self.shortest2_path[int(len(self.shortest2_path)/2)]]=0
                self.shortest2_path = self.shortest2_path[:int(len(self.shortest2_path)/2)+1]
        if len(self.queried_pts)==self.budget:
            self.budget_flag=True
        else:
            self.G.remove_edge(*tuple(self.shortest2_path))
        
    def perform_S2(self):
        i=1
        self.budget_flag=False
        while(len(self.queried_pts)<=self.budget):
            self.find_shortest2_path()
            sp = self.shortest2_path
            if (sp is not None) and (not self.budget_flag):
                self.find_cut_edge()
                self.draw_binary_grid_graph(fig_num=i)
                i+=1
                self.pos_list = [self.shortest2_path[0]]
                self.neg_list = [self.shortest2_path[1]]
            else:
                self.budget_flag=False
                break
            
        if(self.budget_flag):
            print("Ran out of budget !!!")
        else:
            print("Found all cut edges!!!")
        
S2_model = S2(nr=10, nc=25, ratio=0.5, budget=20)
S2_model.sample_graph()
S2_model.perform_S2()
