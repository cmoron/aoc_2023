#!/usr/bin/env python
import sys

FILE_NAME = sys.argv[1]
RED_CUBES=12
GREEN_CUBES=13
BLUE_CUBES=14

valid_ids = []
powers = 0
with open(FILE_NAME, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        game_id = int(line.split(':')[0].replace('Game ', ''))
        cube_sets = line.split(':')[1].split(';')
        valid_game = 1
        max_red, max_blue, max_green = 0, 0, 0
        for cube_set in cube_sets:
            colors = cube_set.split(', ')
            nb_red, nb_blue, nb_green = 0, 0, 0
            for color in colors:
                if ' red' in color:
                    nb_red = int(color.split(' red')[0])
                    if nb_red > max_red:
                        max_red = nb_red
                elif ' blue' in color:
                    nb_blue = int(color.split(' blue')[0])
                    if nb_blue > max_blue:
                        max_blue = nb_blue
                elif ' green' in color:
                    nb_green = int(color.split(' green')[0])
                    if nb_green > max_green:
                        max_green = nb_green
            if nb_red > RED_CUBES or nb_blue > BLUE_CUBES or nb_green > GREEN_CUBES:
                valid_game = 0

        power = max_red * max_blue * max_green
        powers += power
        if valid_game:
            valid_ids.append(game_id)

print(f'Part 1: {sum(valid_ids)}')
print(f'Part 2: {powers}')
