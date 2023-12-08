#!/usr/bin/env python
import sys

class Card:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_value(self):
        values = {"A": 14, "K": 13, "Q": 12,"T": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2, "J": 1}
        return values[self.symbol]

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"{self.symbol}"

class Hand:
    def __init__(self, cards_generator, bid):
        self.cards = list(cards_generator)
        self.cards_dict = {}
        self.bid = bid
        self.j_count = 0
        for card in self.cards:
            if card.symbol == 'J':
                self.j_count += 1
            if card.symbol in self.cards_dict:
                self.cards_dict[card.symbol] += 1
            else:
                self.cards_dict[card.symbol] = 1

    def get_value(self):
        values = sorted(self.cards_dict.values(), reverse=True)

        if len(values) > 1 and self.j_count > 0:
            if self.j_count == 1:
                values[0] += 1
                values[-1] = 0
            elif self.j_count == 2:
                if values[0] == 3:
                    values[0] += 2
                    values[1] = 0
                elif values[0] == 2 and values[1] == 2:
                    values[0] += 2
                    values[1] = 0
                else:
                    values[0] = 3
                    values[-1] = 0
            elif self.j_count == 3:
                if values[1] == 2:
                    values[0] += 2
                    values[1] = 0
                else:
                    values[0] += 1
                    values[-1] = 0
            else:
                values[0] = 0
                values[1] += self.j_count

        if values[0] == 5 and len(values) > 1:
            values[1] = 0

        values = sorted(values, reverse=True)

        total = 0
        comb_factor = 10**10
        one_factor = 15**4

        # combinations
        for value in values:
            total += (value) * comb_factor
            comb_factor //= 10

        # high card
        for card in self.cards:
            total += card.get_value() * one_factor
            one_factor //= 15

        return total

    def __str__(self):
        res = ""
        for c in self.cards:
            res += c.symbol
        # return str(self.cards)
        return res

    def __repr__(self):
        return f"Hand('{self.cards}', {self.bid}, {self.get_value()})"


FILE_NAME = sys.argv[1]
with open(FILE_NAME, 'r', encoding='utf-8') as file:
    hands = []
    for line in file:
        line = line.strip()
        cards_in = line.split()[0]
        bid = int(line.split()[1])
        hands.append(Hand((Card(c) for c in cards_in), bid))

    hands.sort(key=lambda hand: hand.get_value())

    p2 = 0
    for index, hand in enumerate(hands):
        p2 += hand.bid * (index + 1)

    print(f'Part 2: {p2}')
