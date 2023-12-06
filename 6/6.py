#!/usr/bin/env python
import sys

FILE_NAME = sys.argv[1]

def compute_distance(time, max_time):
    if time in (0, max_time):
        return 0
    speed = time
    return speed * (max_time - time)

def find_start_offset(offset_min, offset_max, max_time, distance):
    offset = (offset_min + offset_max) // 2
    score = compute_distance(offset, max_time)
    if offset_max - offset_min <= 2:
        if score <= distance:
            return offset + 1
        return offset

    if score >= distance:
        return find_start_offset(offset_min, offset, max_time, distance)
    return find_start_offset(offset, offset_max, max_time, distance)

def compute_score(max_time, distance):

    start_win_offset = find_start_offset(1, max_time // 2, max_time, distance)
    end_win_offset = max_time - start_win_offset

    return end_win_offset - start_win_offset + 1

with open(FILE_NAME, 'r', encoding='utf-8') as file:

    l1 = file.readline().strip()
    l2 = file.readline().strip()

    # p1
    times = [int(d) for d in l1.split(":")[1].split()]
    distances = [int(t) for t in l2.split(":")[1].split()]
    data = zip(times, distances)

    p1_total = 1
    for p1_time, p1_distance in data:
        p1_total *= compute_score(p1_time, p1_distance)

    print(f'Part1: {p1_total}')

    # p2
    p2_distance = int(''.join(str(d) for d in distances))
    p2_time = int(''.join(str(t) for t in times))
    print(f'Part2: {compute_score(p2_time, p2_distance)}')
