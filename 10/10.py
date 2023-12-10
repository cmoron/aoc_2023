#!/usr/bin/env python
import sys

TILES = ['|' ,'-' ,'L' ,'J' ,'7' ,'F']
S_ROW = 0
S_COL = 0
S_TYPE = 'S'
LOOP = []

def get_neighbors(matrix, row, col):
    rows, cols = len(matrix), len(matrix[0])
    directions = {"N": (-1, 0), "NE": (-1, 1), "E": (0, 1), "SE": (1, 1),
                  "S": (1, 0), "SW": (1, -1), "W": (0, -1), "NW": (-1, -1)
    }

    neighbors = {}
    for direction, (d_row, d_col) in directions.items():
        n_row, n_col = row + d_row, col + d_col
        if 0 <= n_row < rows and 0 <= n_col < cols:
            neighbors[direction] = matrix[n_row][n_col]

    return neighbors

def in_path(tile, neighbors):
    if tile == '|':
        if not 'N' in neighbors or not 'S' in neighbors:
            return False
        if 'N' in neighbors:
            if not neighbors['N'] in ['|', '7', 'F', 'S']:
                return False
        if 'S' in neighbors:
            if not neighbors['S'] in ['|', 'L', 'J', 'S']:
                return False
    if tile == '-':
        if not 'W' in neighbors or not 'E' in neighbors:
            return False
        if 'W' in neighbors:
            if not neighbors['W'] in ['-', 'L', 'F', 'S']:
                return False
        if 'E' in neighbors:
            if not neighbors['E'] in ['-', '7', 'J', 'S']:
                return False
    if tile == 'L':
        if not 'N' in neighbors or not 'E' in neighbors:
            return False
        if 'N' in neighbors:
            if not neighbors['N'] in ['|', '7', 'F', 'S']:
                return False
        if 'E' in neighbors:
            if not neighbors['E'] in ['-', '7', 'J', 'S']:
                return False
    if tile == 'J':
        if not 'N' in neighbors or not 'W' in neighbors:
            return False
        if 'N' in neighbors:
            if not neighbors['N'] in ['|', '7', 'F', 'S']:
                return False
        if 'W' in neighbors:
            if not neighbors['W'] in ['-', 'L', 'F', 'S']:
                return False
    if tile == '7':
        if not 'S' in neighbors or not 'W' in neighbors:
            return False
        if 'S' in neighbors:
            if not neighbors['S'] in ['|', 'L', 'J', 'S']:
                return False
        if 'W' in neighbors:
            if not neighbors['W'] in ['-', 'L', 'F', 'S']:
                return False
    return True

def find_s_type(matrix, row, col):
    neighbors = get_neighbors(matrix, row, col)
    for tile in TILES:
        if in_path(tile, neighbors):
            return tile
    return 'S'

def run_pipe(env, row, col):
    next_tile = ''
    run_from = ''
    steps = 0
    LOOP.clear()

    # ['|' ,'-' ,'L' ,'J' ,'7' ,'F']
    if S_TYPE in ['|' ,'J' ,'L']:
        next_tile = get_neighbors(env, row, col)['N']
        run_from = 'S'
        row -= 1
    elif S_TYPE == '7':
        next_tile = get_neighbors(env, row, col)['S']
        run_from = 'N'
        row += 1
    else:
        next_tile = get_neighbors(env, row, col)['E']
        run_from = 'W'
        col += 1
    LOOP.append((row, col))

    while next_tile != 'S':
        tile = next_tile
        steps += 1

        if tile == '|' and run_from == 'S':
            next_tile = get_neighbors(env, row, col)['N']
            row -= 1
        elif tile == '|' and run_from == 'N':
            next_tile = get_neighbors(env, row, col)['S']
            row += 1
        if tile == '-' and run_from == 'W':
            next_tile = get_neighbors(env, row, col)['E']
            col += 1
        elif tile == '-' and run_from == 'E':
            next_tile = get_neighbors(env, row, col)['W']
            col -= 1
        if tile == 'L' and run_from == 'N':
            next_tile = get_neighbors(env, row, col)['E']
            run_from = 'W'
            col += 1
        elif tile == 'L' and run_from == 'E':
            next_tile = get_neighbors(env, row, col)['N']
            run_from = 'S'
            row -= 1
        if tile == 'J' and run_from == 'N':
            next_tile = get_neighbors(env, row, col)['W']
            run_from = 'E'
            col -= 1
        elif tile == 'J' and run_from == 'W':
            next_tile = get_neighbors(env, row, col)['N']
            run_from = 'S'
            row -= 1
        if tile == '7' and run_from == 'S':
            next_tile = get_neighbors(env, row, col)['W']
            run_from = 'E'
            col -= 1
        elif tile == '7' and run_from == 'W':
            next_tile = get_neighbors(env, row, col)['S']
            run_from = 'N'
            row += 1
        if tile == 'F' and run_from == 'S':
            next_tile = get_neighbors(env, row, col)['E']
            run_from = 'W'
            col += 1
        elif tile == 'F' and run_from == 'E':
            next_tile = get_neighbors(env, row, col)['S']
            run_from = 'N'
            row += 1
        LOOP.append((row, col))

    if steps % 2:
        return steps // 2 + 1
    return steps // 2

def replace_out(env):
    for row_index, row in enumerate(env):
        for col_index, _ in enumerate(row):
            if not (row_index, col_index) in LOOP:
                env[row_index][col_index] = '.'

def detect_leak(env):
    # count walls
    env[S_ROW][S_COL] = S_TYPE
    for row_index, row in enumerate(env):
        walls = 0
        l = False
        f = False
        for col_index, _ in enumerate(row):
            if (row_index, col_index) in LOOP:
                if env[row_index][col_index] == '|':
                    walls += 1
                    l, f = False, False
                if env[row_index][col_index] == 'L':
                    l = True
                    f = False
                if l and env[row_index][col_index] == '7':
                    walls += 1
                    l = False
                if env[row_index][col_index] == 'F':
                    f = True
                    l = False
                if f and env[row_index][col_index] == 'J':
                    walls += 1
                    f = False
            else:
                if walls % 2 == 0:
                    env[row_index][col_index] = 'O'
                else:
                    env[row_index][col_index] = 'I'

    count = 0
    for row in env:
        count += row.count('I')
    return count

FILE_NAME = sys.argv[1]
with open(FILE_NAME, 'r', encoding='utf-8') as file:
    env = []
    for row_index, line in enumerate(file):
        row = []
        for col_index, c in enumerate(line.strip()):
            if c == 'S':
                S_ROW, S_COL = row_index, col_index
            row.append(c)
        env.append(row)

    S_TYPE = find_s_type(env, S_ROW, S_COL)
    max_dist = run_pipe(env, S_ROW, S_COL)
    print(f'Part1: {max_dist}')
    replace_out(env)
    print(f'Part2: {detect_leak(env)}')
