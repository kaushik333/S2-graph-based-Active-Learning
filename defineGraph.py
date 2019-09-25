#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 23:29:57 2019

@author: kaushik
"""
import networkx as nx
from matplotlib import pyplot as plt
from itertools import product

class Graph(object):
    
    def __init__(self, nr = 8, nc = 8, ratio = 0.5, budget=15):

        self.shortest2_path=[]
        self.budget=budget
        self.nr = nr
        self.nc = nc
        self.ratio = ratio
        self.label_prop={}
        
        self.create_graph()
        
        self.add_pos = False
        self.add_neg = False
        
        self.queried_pts = {}
        self.pos_list=[]
        self.neg_list=[]
        
    def create_graph(self):
        (N_c, N_r) = (self.nc, self.nr)
        self.G = nx.grid_2d_graph(self.nc, self.nr)
        
        labels = dict( ((i, j), i * N_r + j) for i, j in self.G.nodes() )
        for (i,j) in labels:
            self.G.node[(i,j)]['id'] = labels[(i,j)]
        
        # draw nodes with diff colors according to classes
       
#        list1 = range(int(N_c*self.ratio))
#        list2 = range(N_r)
        
        list1 = range(int(N_c*0.3),int(N_c*0.8))
        list2 = range(int(N_r*0.3),int(N_r*0.8))
        tot_list = []
        tot_list.append(list1)
        tot_list.append(list2)
        self.class1 = list(product(*tot_list))
        for (i,j) in self.class1:
            self.G.node[(i,j)]['label'] = 1
            
        
#        list1 = range(int(N_c*self.ratio),N_c)
#        list2 = range(N_r)
            
        list3 = range(N_c)
        list4 = range(N_r)
        tot_list = []
        tot_list.append(list3)
        tot_list.append(list4)
        self.class2 = list(set(list(product(*tot_list))) - set(self.class1))
        for (i,j) in self.class2:
            self.G.node[(i,j)]['label'] = 0
        
        
    def draw_binary_grid_graph(self, fig_num=0, c1='y', c2='g'):
            
        pos = dict( (n, n) for n in self.G.nodes() )
            
        plt.figure()
        nx.draw_networkx_nodes(self.G, pos=pos, nodelist=self.class1, node_size=50, node_color=c1)            
        nx.draw_networkx_nodes(self.G, pos=pos, nodelist=self.class2, node_size=50, node_color=c2)
        
        if self.queried_pts != {}:
            nx.draw_networkx_nodes(self.G, pos=pos, nodelist=list(self.queried_pts.keys()), node_size=50, node_color='b')
        
        # draw edges and the corresponding labels

        nx.draw_networkx_edges(self.G, pos=pos)

#        nx.draw_networkx_labels(self.G, pos=pos, labels=labels, font_size=7)
        
        plt.axis('off')
        plt.text(2, 10, s="Budget: "+str(len(self.queried_pts))+" Total Budget: "+str(self.budget), fontsize=20)
        plt.savefig('S2_progress_'+str(fig_num)+'.png')
    