#!/usr/bin/env python
import sys

memo = {}
def count(rec, arr):

    if not rec and not arr:
        return 1
    if not rec and arr:
        return 0
    if not arr and '#' in rec:
        return 0

    if (rec, arr) in memo:
        return memo[(rec, arr)]

    res = 0
    first = rec[0]
    rest = rec[1:]

    if first == '.':
        res = count(rest, arr)
    elif first == '#':
        if arr[0] > 1 and len(rec) > 1 and rec[1] == '.':
            res = 0
        else:
            if arr[0] == 1:
                if len(arr) > 1 and rest and rest[0] == '?':
                    res = count('.' + rest[1:], arr[1:])
                elif len(arr) > 1 and rest and rest[0] == '#':
                    res = 0
                else:
                    res = count(rest, arr[1:])
            else:
                if rest and rest[0] == '?':
                    res = count('#' + rest[1:], (arr[0] - 1,) + arr[1:])
                else:
                    res = count(rest, (arr[0] - 1,) + arr[1:])

    else:
        res += count('#' + rest, arr)
        res += count('.' + rest, arr)

    memo[(rec, arr)] = res
    return res

p1_res = 0
p2_res = 0
with open(sys.argv[1], 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        rec, arr = line.split()
        arr = tuple(map(int, arr.split(',')))
        p1_res += count(rec, arr)

        rec = ((rec + '?') * 5)[:-1]
        arr = arr * 5
        p2_res += count(rec, arr)


print('Part 1:', p1_res)
print('Part 2:', p2_res)
