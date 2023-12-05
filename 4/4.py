#!/usr/bin/env python
import sys
import math

FILE_NAME = sys.argv[1]
total_score = 0
total_cards = 0
cards = {}
with open(FILE_NAME, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        numbers = line.split(' |')[1].split()
        winning = line.split(' |')[0].split(': ')[1].split()
        card_id = int(line.split(' |')[0].split(': ')[0].split('Card ')[1])
        score = len([i for i in numbers if i in winning])
        cards[card_id] = {'copies': 1, 'score': score, 'winning': winning, 'numbers': numbers}
        total_score += math.trunc(pow(2, score -1))

    for card_id, card in cards.items():
        range_start = card_id + 1
        range_end = range_start + card['score']
        for i in range(range_start, range_end):
            cards[i]['copies'] += 1 * card['copies']
        total_cards += card['copies']

print(f'Part 1: {total_score}')
print(f'Part 2: {total_cards}')
