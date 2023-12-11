#!/usr/bin/env python
import sys
import itertools

FILE_NAME = sys.argv[1]
SKY = []
GALAXY='#'
GALAXIES = {}
COUPLES = []
EMPTY_ROWS = []
EMPTY_COLS = []
P2_MULT = 999999

def dist(g1, g2, p2 = False):

    g1_x, g1_y = GALAXIES[g1][0], GALAXIES[g1][1]
    g2_x, g2_y = GALAXIES[g2][0], GALAXIES[g2][1]
    empty_rows = 0
    empty_cols = 0
    mult = 1
    if p2:
        mult = P2_MULT

    for row in EMPTY_ROWS:
        if g1_x < row < g2_x:
            empty_rows += 1
        elif g2_x < row < g1_x:
            empty_rows += 1

    for col in EMPTY_COLS:
        if g1_y < col < g2_y:
            empty_cols += 1
        elif g2_y < col < g1_y:
            empty_cols += 1

    x = abs(g1_x - g2_x)
    y = abs(g1_y - g2_y)

    x += empty_cols * mult
    y += empty_rows * mult

    return x + y

with open(FILE_NAME, 'r', encoding='utf-8') as file:
    matrix = []
    for index, line in enumerate(file):
        line = line.strip()
        if GALAXY not in line:
            EMPTY_ROWS.append(index)
        matrix.append(list(line))

    for col in range(len(matrix[0])):
        if GALAXY not in [line[col] for line in matrix]:
            EMPTY_COLS.append(col)

    res = [(i, j) for i, row in enumerate(matrix) for j, val in enumerate(row) if val == GALAXY]
    for index, g in enumerate(res):
        GALAXIES[index] = g

    COUPLES = list(itertools.combinations(GALAXIES.keys(), 2))

    p1_res = 0
    for couple in COUPLES:
        p1_res += dist(couple[0], couple[1])

    print(f'Part 1: {p1_res}')

    p2_res = 0
    for couple in COUPLES:
        p2_res += dist(couple[0], couple[1], True)
    print(f'Part 2: {p2_res}')
