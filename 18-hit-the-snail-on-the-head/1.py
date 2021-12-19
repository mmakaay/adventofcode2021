#!/bin/env python3

from sys import argv, exit
from functools import reduce
from operator import add
from snail_tree import *


if len(argv) != 2:
    print(f"Usage: {argv[0]} <path to sum file>")
    exit(1)

with open(argv[1], "r") as f:
    snails = [parse_snail_code(line.strip()) for line in f]

summed = reduce(add, snails)

print("Sum:", summed)
print("Magnitude:", summed.magnitude())
