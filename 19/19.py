#!/usr/bin/env python
import sys
from copy import deepcopy

class Rule:
    def __init__(self, condition, dest):
        self.condition = condition
        self.dest = dest

    def eval(self, obj):
        if not self.condition:
            return self.dest

        x, m, a, s = obj['x'], obj['m'], obj['a'], obj['s']

        if eval(self.condition):
            return self.dest
        return None

    def __str__(self):
        return f'{self.condition} -> {self.dest}'

    def __repr__(self):
        return f'{self.condition} -> {self.dest}' if self.condition else f'{self.dest}'

class Workflow:
    def __init__(self, ident, rules):
        self.ident = ident
        self.rules = rules

    def eval(self, obj):
        for rule in self.rules:
            res = rule.eval(obj)
            if res:
                return res
        return None

    def __str__(self):
        return f'{self.ident}: {self.rules}'

    def __repr__(self):
        return f'{self.ident}: {self.rules}'

FILE_NAME = sys.argv[1]
WF = {}
OBJS = []

# parse
with open(FILE_NAME, 'r', encoding='utf-8') as file:
    workflows, objs = file.read().split("\n\n")

    for wf in workflows.splitlines():
        wfid, rules_line = wf[:-1].split('{')
        rules = []
        for rule in rules_line.split(','):
            comp = rule.split(':')
            rules.append(Rule(comp[0], comp[1]) if len(comp) > 1 else Rule(None, rule))
        wf = Workflow(wfid, rules)
        WF[wf.ident] = wf

    for obj_line in objs.splitlines():
        obj = {}
        for attr in obj_line[1:-1].split(','):
            obj[attr.split('=')[0]] = int(attr.split('=')[1])
        OBJS.append(obj)

# p1
p1_res = 0
for obj in OBJS:
    res = 'in'
    while res not in ['A', 'R']:
        res = WF[res].eval(obj)
    if res == 'A':
        p1_res += sum(obj[i] for i in 'xmas')
print('Part 1:', p1_res)

# p2

def calc(ranges):
    comb = 1
    for _, val in ranges.items():
        lo, hi= val[0], val[1]
        comb *= hi - lo + 1
    return comb

def eval_(wf, ranges):
    combs = 0
    r = ranges
    for rule in wf.rules:

        if not rule.condition:
            if rule.dest == 'A':
                return combs + calc(r)
            if rule.dest == 'R':
                return combs
            return combs + eval_(WF[rule.dest], deepcopy(r))

        key = rule.condition[0]
        sign = rule.condition[1]
        n = int(rule.condition[2:])
        hi, lo = r[key][1], r[key][0]

        # process the rule
        if sign == '>':
            r[key] = (max(lo, n + 1), hi)
        if sign == '<':
            r[key] = (lo, min(hi, n - 1))

        if rule.dest == 'A':
            combs += calc(r)
        elif rule.dest == 'R':
            combs += 0
        else:
            combs += eval_(WF[rule.dest], deepcopy(r))

        # condition to go to next rule
        if sign == '>':
            r[key] = (lo, n)
        if sign == '<':
            r[key] = (n, hi)

    return combs

ranges = {key: (1, 4000) for key in 'xmas'}
print('Part 2:', eval_(WF["in"], ranges))
