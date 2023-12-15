#!/usr/bin/env python

import sys
import re

def _hash(val, char):
    return ((val + ord(char)) * 17) % 256

def hash_label(label):
    val = 0
    for c in label:
        val = _hash(val, c)
    return val

def parse_step(step):
    pattern = re.compile('([a-z]+)(.)([1-9]?)')
    match = pattern.match(step)
    label, sign, focal = match.group(1), match.group(2), None
    if sign == '=':
        focal = match.group(3)

    return label, sign, focal

FILE = sys.argv[1]
with open(FILE, 'r', encoding='utf-8') as file:
    line = file.readline().strip()

# p1
p1_res = 0
for step in line.split(','):
    p1_res += hash_label(step)

print('Part1:', p1_res)

# p2
# prepare date struct
boxes = {}
for step in line.split(','):
    label, sign, focal = parse_step(step)
    box = hash_label(label)

    if sign == '=':
        if box in boxes:
            boxes[box][label] = focal
        else:
            boxes[box] = {label: focal}
    if sign == '-':
        if box in boxes and label in boxes[box]:
            del boxes[box][label]

# compute p2
p2_res = 0
for box_index, lens in boxes.items():
    if len(lens) == 0:
        continue
    slot = 1
    box_power = 0
    for focal in lens.values():
        focal_power = box_index + 1
        focal_power *= slot * int(focal)
        box_power += focal_power
        slot += 1
    p2_res += box_power

print('Part2:', p2_res)
