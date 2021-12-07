#!/bin/env python3

from statistics import mean
from math import floor, ceil

crabs = list(map(int, next(open("input.txt")).split(",")))

# Find optimal position.
average = mean(crabs)
crabs_left = sum(True for crab in crabs if crab < average)
crabs_right = len(crabs) - crabs_left;
position = floor(average) if crabs_left > crabs_right else ceil(average)

# Compute fuel.
distances = (abs(crab - position) for crab in crabs)
fuel_costs = (d*(d+1)//2 for d in distances)
fuel_total = sum(fuel_costs)

print(fuel_total)
