#!/bin/env python3

import re


def load_instructions(path):
    dots = set()
    instructions = []
    with open(path, "r") as f:
        for line in f:
            if groups := re.match(r"(\d+),(\d+)", line):
                dots.add((int(groups[1]), int(groups[2])))
            elif groups := re.match(r"fold along (x|y)=(\d+)", line):
                instructions.append((groups[1], int(groups[2])))
    return dots, instructions


def fold(dots, axis, offset):
    for x, y in set(dots):
        if axis == "y":
            if y > offset:
                dots.add((x, 2 * offset - y))
                dots.remove((x, y))
        else:
            if x > offset:
                dots.add((2 * offset - x, y))
                dots.remove((x, y))


dots, instructions = load_instructions("input.txt")
fold(dots, *instructions[0])
print(len(dots))
