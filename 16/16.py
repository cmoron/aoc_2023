#!/usr/bin/env python
import sys

sys.setrecursionlimit(2**12)

class Solve:

    def __init__(self, env):
        self.env = env
        self.log = set()

    def hash_key(self, state):
        r, c, d = state
        return (r, c, d, frozenset(self.log))

    def move(self, r, c, d):
        if d == 'N':
            return r - 1, c, d
        if d == 'S':
            return r + 1, c, d
        if d == 'E':
            return r, c + 1, d
        return r, c - 1, d # west

    def run(self, state):
        r, c, d = state

        if r < 0 or c < 0 or r >= len(self.env) or c >= len(self.env) or state in self.log:
            return set()

        self.log.add(state)
        enlight = {(r, c)}
        next_state = self.move(r, c, d)

        if self.env[r][c] == '.':
            enlight.update(self.run(next_state))
        elif d in 'NS' and self.env[r][c] == '|':
            enlight.update(self.run(self.move(r, c, d)))
        elif d in 'EW' and self.env[r][c] == '|':
            enlight.update(self.run(self.move(r, c, 'N')))
            enlight.update(self.run(self.move(r, c, 'S')))
        elif d in 'EW' and self.env[r][c] == '-':
            enlight.update(self.run(self.move(r, c, d)))
        elif d in 'NS' and self.env[r][c] == '-':
            enlight.update(self.run(self.move(r, c, 'W')))
            enlight.update(self.run(self.move(r, c, 'E')))
        elif self.env[r][c] == '/':
            if d == 'N':
                enlight.update(self.run(self.move(r, c, 'E')))
            elif d == 'S':
                enlight.update(self.run(self.move(r, c, 'W')))
            elif d == 'E':
                enlight.update(self.run(self.move(r, c, 'N')))
            elif d == 'W':
                enlight.update(self.run(self.move(r, c, 'S')))
        elif self.env[r][c] == '\\':
            if d == 'N':
                enlight.update(self.run(self.move(r, c, 'W')))
            elif d == 'S':
                enlight.update(self.run(self.move(r, c, 'E')))
            elif d == 'E':
                enlight.update(self.run(self.move(r, c, 'S')))
            elif d == 'W':
                enlight.update(self.run(self.move(r, c, 'N')))

        return enlight

    def solve_p1(self):
        return len(self.run((0, 0, 'E')))

    def solve_p2(self):
        R = len(self.env)
        C = len(self.env[0])
        res = []

        for r in range(R):
            self.log = set() # reset logs
            res.append(len(self.run((r, 0, 'E'))))

        for r in range(R):
            self.log = set() # reset logs
            res.append(len(self.run((r, C - 1, 'W'))))

        for c in range(C):
            self.log = set() # reset logs
            res.append(len(self.run((0, c, 'S'))))

        for c in range(C):
            self.log = set() # reset logs
            res.append(len(self.run((C - 1, c, 'N'))))

        return max(res)

def main():
    FILE_NAME = sys.argv[1]
    env = []
    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            env.append(list(line))

    solver = Solve(env)

    # p1
    print('Part1:', solver.solve_p1())

    # p2
    print('Part2:', solver.solve_p2())

if __name__ == "__main__":
    main()
