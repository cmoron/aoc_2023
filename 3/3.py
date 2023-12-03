#!/usr/bin/env python
import sys
import re

FILE_NAME = sys.argv[1]
engine_schematic = []
gears = {}
total = 0

def register_gear(line_index, index, number):
    key = (line_index, index)
    if key in gears:
        gears[key].append(number)
    else:
        gears[key] = [number]

def detect_symbol(line_index, start, end, number):
    if start > 0:
        start -= 1

    if end < len(engine_schematic[line_index]) - 1:
        end += 1

    lines = {}
    lines[line_index] = engine_schematic[line_index]
    if line_index > 0:
        lines[line_index - 1] = engine_schematic[line_index - 1]
    if line_index < len(engine_schematic) - 1:
        lines[line_index + 1] = engine_schematic[line_index + 1]

    for line_id, line in lines.items():
        match = re.match(r'.*[^a-zA-Z0-9\.].*', line[start:end])
        if match:
            if '*' in match.string:
                index = line[start:end].find("*") + start
                register_gear(line_id, index, number)
            return True
    return False

def compute_gears():
    gear = 0
    for values in gears.values():
        if len(values) == 2:
            gear += int(values[0]) * int(values[1])

    return gear

with open(FILE_NAME, 'r', encoding='utf-8') as file:
    for line in file:
        engine_schematic.append(line.strip())

    for index, line in enumerate(engine_schematic):
        for match in re.finditer(r'\d+', line):
            number = match[0]
            start = match.start()
            end = match.end()
            if detect_symbol(index, start, end, number):
                total += int(number)

print(f'Part1 : {total}')
print(f'Part2 : {compute_gears()}')
