#!/usr/bin/env python

import sys
import networkx as nx

adj = {}
G = nx.Graph()
with open(sys.argv[1], 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip().replace(': ', ' ')
        comp, plugs = line.split()[0], line.split()[1:]
        for plug in plugs:
            G.add_edge(comp, plug)
            G.add_edge(plug, comp)

g1, g2 = nx.stoer_wagner(G)[1]

print('Part1: ', len(g1) * len(g2))
