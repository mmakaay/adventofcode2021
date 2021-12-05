#!/bin/env python3.10

from functools import reduce

with open("input.txt", "r") as f:
  commands = [
    (c, int(a)) for c, a in
    (x.split(" ") for x in f)
  ]

def pilot(pos, command):
  x, y, aim = pos
  match command:
    case ("forward", delta):
      return (x+delta, y+aim*delta, aim)
    case ("up", delta):
      return (x, y, aim-delta)
    case ("down", delta):
      return (x, y, aim+delta)

x, y, _ = reduce(pilot, commands, (0, 0, 0))

print(x*y)
