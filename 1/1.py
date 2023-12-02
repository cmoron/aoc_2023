#!/usr/bin/env python
import sys

dic = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5e",
    "six": "s6x",
    "seven": "s7n",
    "eight": "e8t",
    "nine": "n9e",
}

total_1 = 0
total_2 = 0

filename = sys.argv[1]
with open(filename, 'r', encoding='utf-8') as file:

    for line in file:

        p2_line = line
        for key, value in dic.items():
            p2_line = p2_line.replace(key, value)

        if line:
            number = [char for char in line if char.isdigit()]
            total_1 += int(number[0] + number[-1])

        if p2_line:
            number = [char for char in p2_line if char.isdigit()]
            total_2 += int(number[0] + number[-1])

print(f'Part 1 : {total_1}')
print(f'Part 2 : {total_2}')
print(f'Result: {total_1 + total_2}')
