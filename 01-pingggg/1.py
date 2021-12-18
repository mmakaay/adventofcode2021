#!/usr/bin/env python3

with open("input.txt", "r") as f:
    depths = list(map(int, f))
    paired = zip(depths, depths[1:])
    higher = sum(b - a > 0 for a, b in paired)
print(higher)
