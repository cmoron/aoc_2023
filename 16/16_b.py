#!/usr/bin/env python
import sys
from pprint import pprint
# from functools import cache

sys.setrecursionlimit(10000)
ENV = []
log = []
enlight = set()
count = 0

# @cache
def run(state):
    global count
    count += 1
    r, c, d = state

    if r < 0 or c < 0 or state in log:
        return
    if r >= len(ENV) or c >= len(ENV):
        return

    log.append(state)
    enlight.add((r, c))

    if ENV[r][c] == '.':
        if d == 'N':
            run((r - 1, c, d))
        elif d == 'S':
            run((r + 1, c, d))
        elif d == 'E':
            run((r, c + 1, d))
        elif d == 'W':
            run((r, c - 1, d))
    elif ENV[r][c] == '|':
        if d == 'N':
            run((r - 1, c, d))
        elif d == 'S':
            run((r + 1, c, d))
        elif d == 'E' or d == 'W':
            run((r - 1, c, 'N'))
            run((r + 1, c, 'S'))
    elif ENV[r][c] == '-':
        if d == 'N' or d == 'S':
            run((r, c - 1, 'W'))
            run((r, c + 1, 'E'))
        elif d == 'E':
            run((r, c + 1, d))
        elif d == 'W':
            run((r, c - 1, d))
    elif ENV[r][c] == '/':
        if d == 'N':
            run((r, c + 1, 'E'))
        elif d == 'S':
            run((r, c - 1, 'W'))
        elif d == 'E':
            run((r - 1, c, 'N'))
        elif d == 'W':
            run((r + 1, c, 'S'))
    elif ENV[r][c] == '\\':
        if d == 'N':
            run((r, c - 1, 'W'))
        elif d == 'S':
            run((r, c + 1, 'E'))
        elif d == 'E':
            run((r + 1, c, 'S'))
        elif d == 'W':
            run((r - 1, c, 'N'))

def main():
    global enlight
    global log
    FILE_NAME = sys.argv[1]
    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            # print(line)
            ENV.append(list(line))

    run((0, 0, 'E'))
    res = len(enlight)
    print('Part1:', res)

    sys.exit(0)

    res = []
    log = []
    enlight = set()
    print('run', 0, 0, 'S')
    run((0, 0, 'S'))
    for index in range(len(ENV)):
        log = []
        enlight = set()
        run((index, 0, 'E'))
        print('run', index, 0, 'E', len(enlight))
        res.append(len(enlight))

    log = []
    enlight = set()
    print('run', 0, len(ENV[0]) - 1, 'S')
    run((0, len(ENV[0]) - 1, 'S'))
    for index in range(len(ENV)):
        log = []
        enlight = set()
        run((index, len(ENV[0]) - 1, 'W'))
        print('run', index, len(ENV[0]) -1, 'W', len(enlight))
        res.append(len(enlight))

    log = []
    enlight = set()
    print('run', len(ENV[0]) - 1, 0, 'N')
    run((len(ENV[0]) - 1, 0, 'N'))
    for index in range(len(ENV[0])):
        log = []
        enlight = set()
        run((0, index, 'S'))
        print('run', 0, index, 'S', len(enlight))
        res.append(len(enlight))

    log = []
    enlight = set()
    print('run', len(ENV[0]) - 1, len(ENV[0]) - 1 , 'E')
    run((len(ENV[0]) - 1, len(ENV[0]) - 1, 'E'))
    for index in range(len(ENV[0])):
        log = []
        enlight = set()
        run((len(ENV[0]) - 1, index, 'N'))
        print('run', len(ENV) - 1, index, 'N', len(enlight))
        res.append(len(enlight))

    print(res)
    print(max(res))

if __name__ == "__main__":
    main()
