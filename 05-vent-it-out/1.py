#!/bin/env python3

import re
from itertools import chain

# Read data.
with open("input.txt") as f:
  data = [list(map(int, re.split(',| -> ', line))) for line in f]

# Use only horizontal and vertical vent lines.
data = [(x1,y1,x2,y2) for x1,y1,x2,y2 in data if x1==x2 or y1==y2]

# Initialize a grid that can hold all data points.
max_x = max(max(x1,x2) for x1,_,x2,_ in data)
max_y = max(max(y1,y2) for _,y1,_,y2 in data)
grid = [[0]*(max_x+1) for _ in range(max_y+1)]

# Draw in all vent lines.
for x1,y1,x2,y2 in data:
  steps = max(abs(x1-x2), abs(y1-y2))
  d_x = (x2-x1) // steps
  d_y = (y2-y1) // steps
  for i in range(steps+1):
    x = x1 + i*d_x 
    y = y1 + i*d_y 
    grid[y][x] += 1

print(sum(p>=2 for p in chain(*grid)))
