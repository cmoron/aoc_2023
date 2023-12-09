#!/usr/bin/env python
import sys

def gen_diff(values):
    res = []
    for index in range(len(values) - 1):
        res.append(values[index + 1] - values[index])
    return res

def main():
    file_path = sys.argv[1]
    with open(file_path, 'r', encoding='utf-8') as file:
        p1_res = 0
        p2_res = 0
        for line in file:
            line = line.strip()
            report = [int(n) for n in line.split()]
            sequences = []
            sequences.append(report)

            while not all(val == 0 for val in report):
                report = gen_diff(report)
                sequences.append(report)

            ex_val = 0
            h_val = 0
            for sequence in reversed(sequences):
                # extrapolate
                sequence.append(sequence[-1] + ex_val)
                sequence.insert(0, sequence[0] - h_val)
                ex_val = sequence[-1]
                h_val = sequence[0]

            p1_res += sequences[0][-1]
            p2_res += sequences[0][0]
        print(f'Part 1: {p1_res}')
        print(f'Part 2: {p2_res}')

if __name__ == '__main__':
    main()
