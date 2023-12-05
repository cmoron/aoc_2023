#!/usr/bin/env python
import sys

FILE_NAME = sys.argv[1]

seed_to_soil_map = []
soil_to_fertilizer_map = []
fertilizer_to_water_map = []
water_to_light_map = []
light_to_temperature_map = []
temperature_to_humidity_map = []
humidity_to_location_map = []

def reg_seed_to_soil(line):
    seed_to_soil_map.append([int(elem) for elem in line.split()])
    seed_to_soil_map.sort(key=lambda x: x[1])

def reg_soil_to_fertilizer(line):
    soil_to_fertilizer_map.append([int(elem) for elem in line.split()])
    soil_to_fertilizer_map.sort(key=lambda x: x[1])

def reg_fertilizer_to_water(line):
    fertilizer_to_water_map.append([int(elem) for elem in line.split()])
    fertilizer_to_water_map.sort(key=lambda x: x[1])

def reg_water_to_light(line):
    water_to_light_map.append([int(elem) for elem in line.split()])
    water_to_light_map.sort(key=lambda x: x[1])

def reg_light_to_temperature(line):
    light_to_temperature_map.append([int(elem) for elem in line.split()])
    light_to_temperature_map.sort(key=lambda x: x[1])

def reg_temperature_to_humidity(line):
    temperature_to_humidity_map.append([int(elem) for elem in line.split()])
    temperature_to_humidity_map.sort(key=lambda x: x[1])

def reg_humidity_to_location(line):
    humidity_to_location_map.append([int(elem) for elem in line.split()])
    humidity_to_location_map.sort(key=lambda x: x[1])

# optimized infer to use ranges for p2
def infer_optim(seed_map, ranges):
    res = []

    for start, end in ranges:
        found_mapping = False
        for target, source, length in seed_map:
            max_source = source + length
            if start < source:
                if end < source:
                    res.append([start, end])
                    found_mapping = True
                    break

                if end <= max_source:
                    res.append([start, source])
                    res.append([target, target + (end - source)])
                    found_mapping = True
                    break

                res.append([start, source])
                res.append([target, target + (max_source - source)])
                start = max_source

            elif source <= start < max_source:
                if end <= max_source:
                    res.append([target + (start - source), target + (end - source)])
                    found_mapping = True
                    break

                res.append([target + (start - source) , target + (max_source - source)])
                start = max_source

        if not found_mapping:
            res.append([start, end])
    return res

def infer_all_optim(ranges):
    soil = infer_optim(seed_to_soil_map, ranges)
    fertilizer = infer_optim(soil_to_fertilizer_map, soil)
    water = infer_optim(fertilizer_to_water_map, fertilizer)
    light = infer_optim(water_to_light_map, water)
    temperature = infer_optim(light_to_temperature_map, light)
    humidity = infer_optim(temperature_to_humidity_map, temperature)
    location = infer_optim(humidity_to_location_map, humidity)
    return location

current_state = ""
states = {
    "seed-to-soil map:": reg_seed_to_soil,
    "soil-to-fertilizer map:": reg_soil_to_fertilizer,
    "fertilizer-to-water map:": reg_fertilizer_to_water,
    "water-to-light map:": reg_water_to_light,
    "light-to-temperature map:": reg_light_to_temperature,
    "temperature-to-humidity map:": reg_temperature_to_humidity,
    "humidity-to-location map:": reg_humidity_to_location
}

with open(FILE_NAME, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()

        if line == "":
            current_state = ""

        if current_state:
            states[current_state](line)

        if line.startswith('seeds:'):
            seeds = [int(seed) for seed in line.split('seeds: ')[1].split()]
        elif line and line[0].isalpha():
            current_state = line

    p1_seeds = []
    for seed in seeds:
        # trick to use artificial ranges like p2.
        p1_seeds.append([seed, seed])

    locations = infer_all_optim(p1_seeds)
    locations.sort(key=lambda x: x[0])
    print(f'Part 1: {[start for start, _ in locations][0]}')

    p2_seeds = []
    for index, seed in enumerate(seeds):
        if index % 2 == 1:
            seed_val = seeds[index - 1]
            p2_seeds.append([seed_val, seed_val + seed])

    locations = infer_all_optim(p2_seeds)
    locations.sort(key=lambda x: x[0])
    print(f'Part 2: {[start for start, _ in locations][0]}')
