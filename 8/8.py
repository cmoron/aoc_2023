#!/usr/bin/env python
import sys
import math

FILE_NAME = sys.argv[1]
with open(FILE_NAME, 'r', encoding='utf-8') as file:
    instructions = list(file.readline().strip())
    network = {}
    for l in file:
        if l.strip():
            line = l.strip()
            node = line.split(" = ")[0]
            left = line.split(" = ")[1].split(', ')[0][1:]
            right = line.split(" = ")[1].split(', ')[1][:-1]
            network[node] = {'L': left, 'R': right}

    dest = "AAA"
    if dest in network:
        index = 0
        steps = 0
        while dest != "ZZZ":
            instruction = instructions[index]
            index = (index + 1) % len(instructions)
            dest = network[dest][instruction]
            steps += 1

        print(f'Part 1: {steps}')

    sim_dest = []
    for key in network:
        if key[-1] == 'A':
            sim_dest.append(key)

    instruction_index = 0
    steps = 0
    founds = []
    for dest in sim_dest:
        index = 0
        steps = 0
        while dest[-1] != "Z":
            instruction = instructions[index]
            index = (index + 1) % len(instructions)
            dest = network[dest][instruction]
            steps += 1
        founds.append(steps)

    lcm = founds[0]
    for index in range(1, len(founds)):
        lcm = lcm * founds[index] // math.gcd(lcm, founds[index])

    print(f'Part 2: {lcm}')
