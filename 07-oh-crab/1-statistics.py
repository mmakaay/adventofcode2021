#!/bin/env python3

from statistics import median

def read_crabs_from_file(path):
  with open(path, "r") as f:
    crabs = list(map(int, next(f).split(",")))
  return crabs


crabs = read_crabs_from_file("input.txt")
best_position = int(median(crabs))
fuel = sum(abs(pos-best_position) for pos in crabs)

print(fuel)
