#!/bin/env python3

from statistics import median

crabs = list(map(int, next(open("input.txt")).split(",")))
best_position = int(median(crabs))
fuel = sum(abs(pos-best_position) for pos in crabs)
print(fuel)
