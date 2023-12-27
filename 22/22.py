#!/usr/bin/env python3

import sys

def overlaps(a, b):
    ax1, ay1, ax2, ay2 = a[0], a[1], a[3], a[4]
    bx1, by1, bx2, by2 = b[0], b[1], b[3], b[4]
    return not (ax2 < bx1 or bx2 < ax1 or ay2 < by1 or by2 < ay1)

bricks = []
with open(sys.argv[1], 'r', encoding='utf-8') as file:
    for line in file:
        bricks.append([int(x) for x in line.strip().replace('~', ',').split(',')])

bricks.sort(key=lambda x:x[2])

floor = [[0, 0, 0, 9, 9, 0]]
supports = {}
supported = {}

for i, b in enumerate(bricks):
    ok = False
    h = b[5] - b[2]
    supports[i] = set()
    supported[i] = set()
    for a in reversed(floor):
        if overlaps(a, b):
            ok = True
            b[2] = a[5] + 1
            b[5] = b[2] + h
            floor.append(b)
            floor.sort(key=lambda x:x[5])
            break

bricks.sort(key=lambda x:x[2])

for i, b in enumerate(bricks[:-1]):
    for j, a in enumerate(bricks[i + 1:]):
        j = j + i + 1
        if a[2] - b[5] > 1:
            break
        if overlaps(a, b):
            supports[i].add(j)
            supported[j].add(i)

p1_res = 0

for lo in supports.keys():
    if all(len(supported[up]) > 1 for up in supports[lo]):
        p1_res += 1

print('Part 1:', p1_res)

def chain(up, breaked, supports, supported):
    if len(supports[up]) == 0:
        return
    for dwn in supports[up]:
        if all(elem in breaked for elem in supported[dwn]):
            breaked.append(dwn)
            chain(dwn, breaked, supports, supported)
        else:
            continue

p2_res = 0
for dwn in supports.keys():
    breaked = [dwn]
    chain(dwn, breaked, supports, supported)
    p2_res += len(breaked) - 1

print('Part 2:', p2_res)
