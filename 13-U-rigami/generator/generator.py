#!/bin/env python3

from random import choice, randrange, sample

import sys
dots = set()
with open(sys.argv[1], "r") as f:
  for y,line in enumerate(f):
   for x, char in enumerate(line):
      if char=="*":
        dots.add((x,y)) 
    
folds = []
for _ in range(10):
  axis = choice(["x", "y"])
  w = max(x for x,_ in dots)+1
  h = max(y for _,y in dots)+1
  offset = w if axis == "x" else h
  size = randrange(offset)
  grab = sample(dots, len(dots)//2)
  for x,y in grab:
    if axis == "x":
        if x > (offset-size): 
          dots.add((2*offset-x,y))
          if choice([True, True]):
            dots.remove((x,y))
    else:
        if y > (offset-size): 
          dots.add((x,2*offset-y))
          if choice([True, True]):
            dots.remove((x,y))
  folds.append((axis,offset))

for x,y in dots:
  print(f"{x},{y}")
print()
for axis,size in reversed(folds):
  print(f"fold along {axis}={size}")
