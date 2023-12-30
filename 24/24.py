#!/usr/bin/env python
import sys
import z3

def z3_intersect(stones):
    x, y, z, vx, vy, vz = z3.Reals('x y z vx vy vz')
    s = z3.Solver()

    for stone in stones:
        t = z3.Real('t_{}'.format(stones.index(stone)))
        s.add(stone.x + stone.vx * t == x + vx * t)
        s.add(stone.y + stone.vy * t == y + vy * t)
        s.add(stone.z + stone.vz * t == z + vz * t)
        s.add(t >= 0)

    if s.check() == z3.sat:
        m = s.model()
        return m[x], m[y], m[z], m[vx], m[vy], m[vz]
    return None

class Hailstone:
    def __init__(self, x, y, z, vx, vy, vz):
        self.x, self.y, self.z = x, y, z
        self.vx, self.vy, self.vz = vx, vy, vz

        # compute y = ax + b
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.vx
        y2 = self.y + self.vy

        d = x2 - x1
        self.a = (y2 - y1) / d
        self.b = y1 - self.a * x1

    def intersect(self, other):
        a1, b1 = self.a, self.b
        a2, b2 = other.a, other.b

        if a1 == a2:
            return None

        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1

        # calculating the time of intersection for each stone
        t1 = (x - self.x) / self.vx
        t2 = (x - other.x) / other.vx

        if t1 >= 0 and t2 >= 0:
            return (x, y)

        return None

    def __str__(self):
        return f'{self.x}, {self.y}, {self.vx}, {self.vy}, {self.a}x + {self.b}'

stones = []
with open(sys.argv[1], 'r', encoding='utf-8') as file:
    for line in file:
        positions, velocities = line.strip().split('@')
        x, y, z = map(float, positions.split(', '))
        vx, vy, vz = map(float, velocities.split(', '))
        stones.append(Hailstone(x, y, z, vx, vy, vz))

# example
# amin, amax = 7, 27
# input
amin, amax = 200000000000000, 400000000000000

p1_res = 0

for i in range(len(stones)):
    for j in range(i + 1, len(stones)):
        # p1
        res = stones[i].intersect(stones[j])
        if res:
            x, y = res
            if amin <= x <= amax and amin <= y <= amax:
                p1_res += 1

print('Part1:', p1_res)

# p2
solution = z3_intersect(stones)
p2_res = 0
if solution:
    x_val = int(str(solution[0]))
    y_val = int(str(solution[1]))
    z_val = int(str(solution[2]))
    p2_res = x_val + y_val + z_val
print("Part2:", p2_res)
