#!/usr/bin/env python
import sys
import re

def picks_theorem(area, boundaries):
    """
    A = i + b/2 -1

    A the area of the polygon
    i the interior points
    b the boundary points

    -> i = A - b/2 + 1
    """
    return area - boundaries / 2 + 1

def shoelace_formula(vertex):
    """
    A = 1/2 * (SUM xi * (y_i+1 - y_i-1) for i = 1 to n)

    A the area of the polygon
    n the number of vertex
    """
    n = len(vertex)
    area = 0
    for i in range(n):
        x = vertex[i][0]
        j = (i + 1) % n
        area += x * (vertex[i-1][1] - vertex[j][1])
    return abs(area) // 2

D = { 'L': [0, -1], 'U': [-1, 0], 'R': [0, 1], 'D': [1, 0] }
DD = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}

# parse input
FILE_NAME = sys.argv[1]
grid = []
instructions = []
corrected_inst = [] # p2
with open(FILE_NAME, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        arr = line.split()
        instructions.append((arr[0], int(arr[1]), arr[2]))

# p1
vertex = []
boundaries = 0
x, y = 0, 0
for d, r, _ in instructions:
    vertex.append((x, y))
    for j in range(r):
        x += D[d][0]
        y += D[d][1]
        boundaries += 1

print('Part1: ', int(picks_theorem(shoelace_formula(vertex), boundaries) + boundaries))

# p2
vertex = []
boundaries = 0
x, y = 0, 0
for _, _, c in instructions:
    m = re.search(r'(\w{5})(\d)', c)
    d = DD[int(m.group(2))]
    r = int(m.group(1), 16)

    vertex.append((x, y))
    for j in range(r):
        x += D[d][0]
        y += D[d][1]
        boundaries += 1

print('Part2: ', int(picks_theorem(shoelace_formula(vertex), boundaries) + boundaries))
