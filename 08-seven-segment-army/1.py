#!/bin/env python3


def load_data(path):
    with open(path, "r") as f:
        return [[x.split() for x in line.split("|")] for line in f]


data = load_data("input.txt")
all_outputs = (d for i, o in data for d in o)
only_unique = [d for d in all_outputs if len(d) in [2, 3, 4, 7]]
print(len(only_unique))
