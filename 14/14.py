#!/usr/bin/env python
import sys
from functools import cache

FILE_NAME = sys.argv[1]
PLATFORM = []

def transpose(matrix):
    transposed = []
    for col_i in range(len(matrix[0])):
        transposed.append([])
        for row in matrix:
            transposed[col_i].append(row[col_i])
    return transposed

def untranspose(transposed_matrix):
    original = []
    for col_i in range(len(transposed_matrix[0])):
        original.append([])
        for row in transposed_matrix:
            original[col_i].append(row[col_i])
    return original

def t_to_a(tuple_data):
    return [list(row) for row in tuple_data]

def a_to_t(array):
    return tuple(tuple(row) for row in array)

@cache
def tilt_north(tplatform):
    platform = t_to_a(tplatform)
    for row_index, line in enumerate(platform):
        for col_index, col in enumerate(line):
            if col == 'O':
                i = row_index
                while i > 0 and platform[i-1][col_index] == ".":
                    i -= 1
                if i != row_index:
                    platform[i][col_index] = 'O'
                    platform[row_index][col_index] = '.'
    return a_to_t(platform)

@cache
def tilt_west(tplatform):
    platform = transpose(tplatform)
    tplatform = tilt_north(a_to_t(platform))
    return a_to_t(untranspose(tplatform))

@cache
def tilt_east(tplatform):
    platform = transpose(t_to_a(tplatform))
    tplatform = tilt_south(a_to_t(platform))
    return a_to_t(untranspose(tplatform))

@cache
def tilt_south(tplatform):
    platform = t_to_a(tplatform)
    for row_index, line in reversed(list(enumerate(platform))):
        for col_index, col in enumerate(line):
            if col == 'O':
                i = row_index
                while i < len(platform) - 1 and platform[i+1][col_index] == ".":
                    i += 1
                if i != row_index:
                    platform[i][col_index] = 'O'
                    platform[row_index][col_index] = '.'
    return a_to_t(platform)

@cache
def cycle(tplatform):
    tplatform = tilt_north(tplatform)
    tplatform = tilt_west(tplatform)
    tplatform = tilt_south(tplatform)
    tplatform = tilt_east(tplatform)
    return tplatform

def compute_weight(platform):
    row_weight = len(platform)
    weight = 0
    for row in platform:
        weight += row.count('O') * row_weight
        row_weight -= 1
    return weight

with open(FILE_NAME, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        PLATFORM.append(list(line))

PLATFORM = t_to_a(tilt_north(a_to_t(PLATFORM)))
print('Part1:', compute_weight(PLATFORM))
cache = {}
steps = 10**9
for index in range(steps):
    tpf = cycle(a_to_t(PLATFORM))
    PLATFORM = t_to_a(tpf)
    key = hash(tpf)
    if key in cache:
        loop_size = index - cache[key]
        if (steps - index - 1) % loop_size == 0:
            break
    cache[key] = index
print('Part2:', compute_weight(PLATFORM))
