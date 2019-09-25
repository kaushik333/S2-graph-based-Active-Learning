#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 22:11:08 2019

@author: kaushik
"""

import S2         
from defineGraph import Graph
import coarsen


org_graph = Graph(nr=50, nc=50, ratio=0.5, budget=80)
org_graph.draw_binary_grid_graph()

coarse_graph, coarse_flag = coarsen.coarsen_graph(org_graph,level=1)
coarse_graph.draw_binary_grid_graph()

sample_flag = S2.S2(coarse_graph,org_graph,coarse_flag=coarse_flag)
coarse_graph.draw_binary_grid_graph()

if not sample_flag:
    sample_flag = S2.S2(org_graph,org_graph,coarse_flag=coarse_flag)

if not sample_flag:   
    S2.label_completion(org_graph)