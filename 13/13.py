#!/usr/bin/env python

import sys
import numpy as np

FILE = sys.argv[1]
PATTERNS = []

def transpose(pattern):
    transposed = []
    for col_i in range(len(pattern[0])):
        transposed.append([])
        for row in pattern:
            transposed[col_i].append(row[col_i])
    return transposed

def find_mirror(pattern, fixed):
    for pivot in range(len(pattern) -1):
        if is_mirrored(pattern, pivot, fixed):
            return pivot + 1
    return 0

def is_mirrored(pattern, pivot, fixed):
    before = pattern[:pivot + 1]
    after = pattern[pivot + 1:]
    mirrored_len = min(len(before), len(after))

    # rotate
    before = before[-mirrored_len:]
    after = after[:mirrored_len][::-1]

    if fixed:
        return before == after
    return np.sum(np.array(before) != np.array(after)) == 1

with open(FILE,'r', encoding = 'utf-8') as file:
    pattern = []
    for line in file:
        line = line.strip()
        if line == "":
            PATTERNS.append(pattern)
            pattern = []
        else:
            pattern.append(list(line))
    PATTERNS.append(pattern)

p1_res, p2_res = 0, 0
for pattern_id, pattern in enumerate(PATTERNS):

    h_pattern = pattern
    v_pattern = transpose(pattern)

    ## p1
    p1_res += 100 * find_mirror(h_pattern, True)
    p1_res += find_mirror(v_pattern, True)

    ## p2
    p2_res += 100 * find_mirror(h_pattern, False)
    p2_res += find_mirror(v_pattern, False)


print('Part1: ', p1_res)
print('Part2: ', p2_res)
