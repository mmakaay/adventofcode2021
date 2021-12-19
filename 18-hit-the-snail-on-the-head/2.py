#!/bin/env python3

from sys import argv, exit
from itertools import permutations
from snail_tree import *


if len(argv) != 2:
    print(f"Usage: {argv[0]} <path to sum file>")
    exit(1)

with open(argv[1], "r") as f:
    snails = [line.strip() for line in f]

max_magnitude = 0
for a, b in permutations(snails, 2):
    c = parse_snail_code(a) + parse_snail_code(b)
    max_magnitude = max(max_magnitude, c.magnitude())

print("Max possible magnitude:", max_magnitude)
