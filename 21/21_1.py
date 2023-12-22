#!/usr/bin/env python

import sys

D = { 'W': (0, -1), 'N': (-1, 0), 'E': (0, 1), 'S': (1, 0)}

env = []
with open(sys.argv[1], 'r', encoding='utf-8') as file:
    r = 0
    start = None
    for line in file:
        line = list(line.strip())
        if 'S' in line:
            start = (r, line.index('S'))
        env.append(line)
        r += 1

R, C = len(env), len(env[0])  # Dimensions de la grille de base

# p1
valid_neighbors = {}
for r in range(R):
    for c in range(C):
        if env[r][c] != '#':
            valid_neighbors[(r, c)] = [((r + D[d][0]) % R, (c + D[d][1]) % C)
                                       for d in D
                                       if env[(r + D[d][0]) % R][(c + D[d][1]) % C] != '#']

next_pos = set([start])
steps = 64
for _ in range(steps):
    new_next_pos = set()
    for plot in next_pos:
        new_next_pos.update(valid_neighbors.get(plot, []))
    next_pos = new_next_pos

print('Part1:', len(next_pos))
