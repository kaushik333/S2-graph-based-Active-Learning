#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 09:59:58 2019

@author: Kaushik Koneripalli
"""

import networkx as nx
import matplotlib.pyplot as plt
from itertools import product
import random
import numpy as np

class S2(object):
    def __init__(self, nr = 8, nc = 8, ratio = 0.5, budget=15):
        self.pos_list=[]
        self.neg_list=[]
        self.pos_list_coarse=[]
        self.neg_list_coarse=[]
        self.queried_pts={}
        self.label_prop={}
        self.queried_pts_coarse={}
        self.shortest2_path=[]
        self.budget=budget
        self.nr = nr
        self.nc = nc
        self.ratio = ratio
        self.G = None
        self.Gc = None
        self.create_graph()
        self.draw_binary_grid_graph()
        
    def create_graph(self, N_c=0, N_r=0):
        if(N_c==0 and N_r==0):
            (N_c, N_r) = (self.nc, self.nr)
        
        self.G=nx.grid_2d_graph(N_c, N_r)
        self.labels = dict( ((i, j), i * N_r + j) for i, j in self.G.nodes() )
        for (i,j) in self.labels:
            self.G.node[(i,j)]['id'] = self.labels[(i,j)]
            
        list1 = range(int(N_c*self.ratio))
        list2 = range(N_r)
        tot_list = []
        tot_list.append(list1)
        tot_list.append(list2)
        self.class_1 = list(product(*tot_list))
        for (i,j) in self.class_1:
            self.G.node[(i,j)]['label'] = 1
            
        list1 = range(int(N_c*self.ratio),N_c)
        list2 = range(N_r)
        tot_list = []
        tot_list.append(list1)
        tot_list.append(list2)
        self.class_2 = list(product(*tot_list))
        for (i,j) in self.class_2:
            self.G.node[(i,j)]['label'] = 0
            
    def draw_binary_grid_graph(self, fig_num=0, coarsen=False, c1='y', c2='g'):
        
        if not coarsen:
            
            pos = dict( (n, n) for n in self.G.nodes() )    
                
            plt.figure()
            nx.draw_networkx_nodes(self.G, pos=pos, nodelist=self.class_1, node_size=50, node_color=c1)
            nx.draw_networkx_nodes(self.G, pos=pos, nodelist=self.class_2, node_size=50, node_color=c2)
            
            if self.queried_pts != {}:
                nx.draw_networkx_nodes(self.G, pos=pos, nodelist=list(self.queried_pts.keys()), node_size=50, node_color='b')
            
            # draw edges and the corresponding labels
            print(len(self.G.edges()))
            nx.draw_networkx_edges(self.G, pos=pos)
#            nx.draw_networkx_labels(self.G, pos=pos, labels=self.labels, font_size=7)
            
            plt.axis('off')
            plt.text(2, 10, s="Budget: "+str(len(self.queried_pts))+" Total Budget: "+str(self.budget), fontsize=20)
            plt.savefig('S2_progress_'+str(fig_num)+'.png')
        
        if self.Gc and coarsen:
            pos = dict( (n, n) for n in self.Gc.nodes() )    
            
            list1 = range(self.nc_coars)
            list2 = range(self.nr_coars)
            tot_list = []
            tot_list.append(list1)
            tot_list.append(list2)
            self.coars_list = list(product(*tot_list))
            
            plt.figure()
            nx.draw_networkx_nodes(self.Gc, pos=pos, nodelist=self.coars_list, node_size=50, node_color='b')
            
            nx.draw_networkx_edges(self.Gc, pos=pos)
            
            plt.axis('off')
            
    def sample_graph(self):
        self.sampling_graph = list(self.Gc.node())
        (prev_len_pos, prev_len_neg) = (len(self.pos_list), len(self.neg_list))
        print(prev_len_pos, prev_len_neg)
        while(prev_len_pos>=len(self.pos_list) or prev_len_neg>=len(self.neg_list)):
            z = random.choice(self.sampling_graph)
            if self.Gc.node[z]['label']==1:
                self.pos_list.append(self.Gc.node[z]['parent'])
                self.pos_list_coarse.append(z)
                self.queried_pts[self.Gc.node[z]['parent']]=1
                self.queried_pts_coarse[z]=1
                print(len(self.pos_list))
            else:
                self.neg_list.append(self.Gc.node[z]['parent'])
                self.neg_list_coarse.append(z)
                self.queried_pts[self.Gc.node[z]['parent']]=0
                self.queried_pts_coarse[z]=0
                print(len(self.neg_list))
            self.sampling_graph.remove(z)
            
    def find_shortest2_path(self):        
        shortest_paths = []
        try:
            if len(self.neg_list_coarse) < len(self.pos_list_coarse):
                for i in range(len(self.pos_list)):
                    shortest_paths.append(nx.shortest_path(self.Gc, source=self.pos_list_coarse[i], target=self.neg_list_coarse[-1]))
            else:
                for i in range(len(self.neg_list)):
                    shortest_paths.append(nx.shortest_path(self.Gc, source=self.pos_list_coarse[-1], target=self.neg_list_coarse[i]))
        
            shortest2_path_index = min([(len(shortest_paths[i]),i) for i in range(len(shortest_paths))], key=lambda t: t[0])[1] 
            self.shortest2_path = shortest_paths[shortest2_path_index]  
        except:
            self.shortest2_path = None
            
    def find_cut_edge(self, graph):
        while(len(self.shortest2_path)!=2 and len(self.queried_pts_coarse)<self.budget):
            if graph.node[self.shortest2_path[int(len(self.shortest2_path)/2)]]['label']==1:
                z = self.shortest2_path[int(len(self.shortest2_path)/2)]
                if graph==self.Gc:
                    self.queried_pts_coarse[z]=1
                    self.queried_pts[graph.node[z]['parent']]=1
                else:
                    self.queried_pts[z]=1
                self.shortest2_path = self.shortest2_path[int(len(self.shortest2_path)/2):]
            else:
                z = self.shortest2_path[int(len(self.shortest2_path)/2)]
                if graph==self.Gc:
                    self.queried_pts_coarse[z]=0
                    self.queried_pts[graph.node[z]['parent']]=0
                else:
                    self.queried_pts[z]=0
                self.shortest2_path = self.shortest2_path[:int(len(self.shortest2_path)/2)+1]
        
        if len(self.queried_pts)==self.budget:
            self.budget_flag=True
        else:
            print("Cut edge : {}".format(self.shortest2_path))
            graph.remove_edge(*tuple(self.shortest2_path))
        if graph==self.Gc:
            self.pos_list_coarse = [self.shortest2_path[0]]
            self.neg_list_coarse = [self.shortest2_path[1]]
            self.shortest2_path = nx.shortest_path(self.G, source=self.Gc.node[self.shortest2_path[0]]['parent'], target=self.Gc.node[self.shortest2_path[1]]['parent'])
            self.find_cut_edge(graph=self.G)
        else:
            self.pos_list = [self.shortest2_path[0]]
            self.neg_list = [self.shortest2_path[1]]
            
    def perform_S2(self):
        i=1
        self.budget_flag=False
        while(len(self.queried_pts)<=self.budget):
            self.find_shortest2_path()
            sp = self.shortest2_path
            print("SP is {}".format(sp))
            if (sp is not None) and (not self.budget_flag):
                self.find_cut_edge(graph=self.Gc)
#                self.draw_binary_grid_graph(fig_num=i, coarsen=True)
                i+=1
            else:
                if (sp is None):
                    self.budget_flag=False
                    break
                break
        self.draw_binary_grid_graph(fig_num=i, coarsen=False)
            
        if(self.budget_flag):
            print("Ran out of budget !!!")
        else:
            print("Found all cut edges!!!")
            
    def coarsen(self, level=1):
        if self.nc%(2**level)==0:
            self.nc_coars = self.nc//(2**level)
        else:
            self.nc_coars = self.nc//(2**level) + 1
            
        if self.nr%(2**level)==0:
            self.nr_coars = self.nr//(2**level)
        else:
            self.nr_coars = self.nr//(2**level) + 1
            
        self.Gc = nx.grid_2d_graph(self.nc_coars, self.nr_coars)
        
        l1=[]
        for i in range(0,self.nc,2**level):
            l1.append(i)
            
        l2=[]
        for i in range(0,self.nr,2**level):
            l2.append(i)
            
        self.l = list(product(*[l1,l2]))
        
        self.Gclabels = dict( ((i, j), i * self.nr_coars + j) for i, j in self.Gc.nodes() )
        k=0
        for (i,j) in self.Gclabels:
            self.Gc.node[(i,j)]['id'] = self.Gclabels[(i,j)]
            self.Gc.node[(i,j)]['parent'] = self.l[k]
            self.Gc.node[(i,j)]['label'] = self.G.node[self.l[k]]['label']
            k+=1       
            
    def label_completion(self):
        wt = nx.adjacency_matrix(self.G)
        wt = wt.todense()
        self.weight = np.zeros((self.nc*self.nr, self.nc*self.nr))
        queried_id = [self.G.nodes[iden]['id'] for iden in self.queried_pts]
        queried_labels = np.array([self.queried_pts[iden] for iden in self.queried_pts])
        tot = list(range(self.nc*self.nr))
        non_queried = list(set(tot) - set(queried_id))
        
        # W_ll
        rows = np.array(queried_id)
        cols = np.array(queried_id)
        self.weight[0:len(queried_id), 0:len(queried_id)] = wt[rows[:,None],cols]
        
        # W_lu
        rows = np.array(queried_id)
        cols = np.array(non_queried)
        self.weight[0:len(queried_id), len(queried_id):] = wt[rows[:,None],cols]
        
        # W_ul
        rows = np.array(non_queried)
        cols = np.array(queried_id)
        self.weight[len(queried_id):, 0:len(queried_id)] = wt[rows[:,None],cols]
        
        # W_uu
        rows = np.array(non_queried)
        cols = np.array(non_queried)
        self.weight[len(queried_id):, len(queried_id):] = wt[rows[:,None],cols]
        
        # Z-L-G algorithm
        d_vec = np.sum(self.weight,axis=1)
        D_inv = np.diag(1./d_vec)
        
        P = np.matmul(D_inv, self.weight)
        
        I = np.eye(len(non_queried))
        v1 = np.linalg.inv(I - P[len(queried_id):, len(queried_id):])
        v2 = np.matmul(P[len(queried_id):, 0:len(queried_id)], queried_labels)
        f_u = np.matmul(v1, v2)
        f_u[np.where(f_u>=0.5)]=1
        f_u[np.where(f_u<0.5)]=0
        
        # Visualize the results after applying Z-L-G
        
        for i in range(len(non_queried)):
            nq = (int(non_queried[i]/self.nr), non_queried[i]%self.nr)
            self.label_prop[nq] = f_u[i]
            
        self.class_1 = []
        self.class_2 = []
        for key in self.label_prop:
            if self.label_prop[key]==1:
                self.class_1.append(key)
            else:
                self.class_2.append(key)
        
        self.draw_binary_grid_graph(coarsen=False, c1='r', c2='c')
        
        
        
        
S2_model = S2(nr=30, nc=60, ratio=0.5, budget=20)
S2_model.coarsen(level=3) # set level=0 for normal S2 and >0 to coarsen it. 
S2_model.sample_graph()
S2_model.perform_S2()
S2_model.label_completion()
