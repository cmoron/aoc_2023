#!/usr/bin/env python
import sys
from enum import Enum
from collections import deque
from math import lcm
from functools import reduce

MODULES = {}
CYCLES = {}

class Counter:
    lo_count = 0
    hi_count = 0
    button_count = 0

    @staticmethod
    def count_pulse(pulse):
        if pulse == Pulse.HIGH:
            Counter.hi_count += 1
        if pulse == Pulse.LOW:
            Counter.lo_count += 1

    @staticmethod
    def count_push():
        Counter.button_count += 1

    @staticmethod
    def get_count():
        return Counter.lo_count, Counter.hi_count

    def reset():
        Counter.lo_count = 0
        Counter.hi_count = 0


class Pulse(Enum):
    HIGH = 1
    LOW = 0

    def __str__(self):
        return 'low' if self == Pulse.LOW else 'high'

class Status(Enum):
    ON = 1
    OFF = 0

class Module:
    def __init__(self, name=''):
        self.outputs = []
        self.inputs = {}
        self.name = name
        self.pulse = None

    def receive(self, pulse, sender):
        pass

    def send(self):
        for output in self.outputs:
            Counter.count_pulse(self.pulse)
            # print(f'{self.name} -{self.pulse}-> {output}')
            if output == 'rx' and self.pulse == Pulse.LOW:
                print('p2:', Counter.button_count)
                sys.exit(0)
            if output in MODULES:
                MODULES[output].receive(self.pulse, self)

        for output in self.outputs:
            if output in MODULES:
                MODULES[output].send()

    def add_input(self, module):
        self.inputs[module] = Pulse.LOW

    def reset(self):
        pass

    def __str__(self):
        return f'{self.name} -> {self.outputs}'

    def __repr__(self):
        return f'{self.name} -> {self.outputs}'

class FlipFlop(Module):
    def __init__(self, name):
        super().__init__(name)
        self.status = Status.OFF
        self.buffer = deque()

    def receive(self, pulse, sender):
        if pulse == Pulse.LOW:
            if self.status == Status.OFF:
                self.status = Status.ON
                self.buffer.append(Pulse.HIGH)
            elif self.status == Status.ON:
                self.status = Status.OFF
                self.buffer.append(Pulse.LOW)

    def send(self):
        if self.buffer:
            self.pulse = self.buffer.popleft()
            super().send()

    def reset(self):
        self.buffer = deque()
        self.status = Status.OFF

class Conjunction(Module):
    def __init__(self, name):
        super().__init__(name)
        self.inputs = {}

    def receive(self, pulse, sender):
        if sender in self.inputs:
            self.inputs[sender] = pulse

        if (self.name in CYCLES.keys()):
            if all(pulse == Pulse.HIGH for pulse in self.inputs.values()):
                if pulse == Pulse.HIGH and CYCLES[self.name] == 0:
                    CYCLES[self.name] = Counter.button_count - 1

        # we need qm to send low
        # if (self.name == 'qm'):
            # if all(pulse == Pulse.HIGH for pulse in self.inputs.values()):
                # for inp in self.inputs:
                    # if inp.pulse == Pulse.HIGH:
                        # print(inp.name, Counter.button_count)
        # if (self.name == 'dd'):
            # if all(pulse == Pulse.LOW for pulse in self.inputs.values()):
                # for inp in self.inputs:
                    # print('>', inp.name, Counter.button_count)
        # if (self.name == 'ls'):
            # if any(pulse == Pulse.HIGH for pulse in self.inputs.values()):
                # for inp in self.inputs:
                    # if inp.pulse == Pulse.HIGH and inp.name == 'dd':
                        # print('>>>', inp.name, Counter.button_count)

        if all(pulse == Pulse.HIGH for pulse in self.inputs.values()):
            self.pulse = Pulse.LOW
        else:
            self.pulse = Pulse.HIGH

    def __str__(self):
        return f'{self.name} -> {self.outputs} <- {self.inputs}'

class Broadcast(Module):
    def __init__(self):
        super().__init__()
        self.name = "broadcaster"

    def receive(self, pulse, sender):
        self.pulse = pulse

class Button:
    def __init__(self, broadcast):
        self.broadcast = broadcast

    def push(self):
        # print('button -low-> broadcaster')
        Counter.count_pulse(Pulse.LOW)
        Counter.count_push()
        self.broadcast.receive(Pulse.LOW, self)
        self.broadcast.send()

FILE_NAME = sys.argv[1]

button = None
broadcast = None
conjunctions = []
with open(FILE_NAME, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        modstr, outputs = line.split(' -> ')[0], line.split(' -> ')[1].split(', ')

        if 'broadcaster' in modstr:
            broadcast = Broadcast()
            button = Button(broadcast)
            broadcast.outputs = outputs
            MODULES['broadcaster'] = broadcast
        else:
            modtype, modname = modstr[0], modstr[1:]
            if modtype == '%':
                module = FlipFlop(modname)
            elif modtype == '&':
                module = Conjunction(modname)
                conjunctions.append(modname)
            module.outputs = outputs
            MODULES[modname] = module

for c in conjunctions:
    conjunction = MODULES[c]
    for module in MODULES.values():
        if c in module.outputs:
            conjunction.add_input(module)

#p1
for _ in range(1000):
    button.push()
print('Part 1:', Counter.lo_count * Counter.hi_count)

#p2
# Reset to initial state
for module in MODULES.values():
    module.reset()
    Counter.reset()

# show inputs
for m in MODULES.values():
    for module in MODULES.values():
        if m.name in module.outputs:
            m.add_input(module)

level0 = []
level1 = []

for module in MODULES.values():
    if 'rx' in module.outputs:
        level0.append(module.name)

for inp in level0:
    for module in MODULES.values():
        if inp in module.outputs:
            level1.append(module.name)

for inp in level1:
    for module in MODULES.values():
        if inp in module.outputs:
            CYCLES[module.name] = 0

while(True):
    button.push()
    if all(val != 0 for val in CYCLES.values()):
        print('Part 2:', reduce(lcm, (c for c in CYCLES.values())))
        break
