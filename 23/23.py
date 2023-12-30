#!/usr/bin/env python3
import sys
from aoc.utils import get_neighbors

sys.setrecursionlimit(2**14)

def dir_possible(direction, char):
    if char == '#':
        return False
    if char == '^' and direction != 'N':
        return False
    if char == '>' and direction != 'E':
        return False
    if char == 'v' and direction != 'S':
        return False
    if char == '<' and direction != 'W':
        return False
    return True

def dfs(matrix, position, visited, max_length, current_length=0, p2 = False):
    row, col = int(-position.imag), int(position.real)

    if position == END:
        max_length.append(current_length)
        return

    visited.add((row, col))

    neighbors = get_neighbors(matrix, row, col)
    for d, cell in neighbors.items():
        if p2:
            if cell == '#':
                continue
        else:
            if not dir_possible(d, cell):
                continue

        new_direction = DIR[d]
        new_position = position + new_direction
        new_row, new_col = int(-new_position.imag), int(new_position.real)

        if (new_row, new_col) not in visited:
            dfs(matrix, new_position, visited, max_length, current_length + 1, p2)

    visited.remove((row, col))

env = []
with open(sys.argv[1], 'r', encoding='utf-8') as file:
    for line in file:
        print(line.strip())
        env.append(list(line.strip()))

R, C = len(env), len(env[0])
DIR = {'N': 0 + 1j, 'E': 1 + 0j, 'S': 0 - 1j, 'W': -1 + 0j}
START = 1 + 0j
END = complex(C - 2, (R - 1) * - 1)

visited = set()
max_length = []

dfs(env, START, visited, max_length)

print("Part1:", max(max_length))

max_length = []
visited = set()
dfs(env, START, visited, max_length, p2 = True)
print("Part2:", max(max_length))
