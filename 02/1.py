#!/bin/env python3.10

from functools import reduce

f = open("input.txt", "r")
commands = [
    (c, int(a)) for c, a in
    (x.split(" ") for x in f)
]

def pilot(pos, command):
    x, y = pos
    match command:
        case ("forward", delta):
            return (x+delta, y)
        case ("up", delta):
            return (x, y-delta)
        case ("down", delta):
            return (x, y+delta)

x, y = reduce(pilot, commands, (0, 0))

print(x*y)
