#!/bin/env python3

from sys import argv, exit
import re

FREE = "."
EASTBOUND = ">"
SOUTHBOUND = "v"


def load_cucumbers():
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <filename>")
        exit(1)
    with open(argv[1], "r") as f:
        return [list(line.strip()) for line in f]


def move_cucumbers(cucumbers):
    steps = 0
    while move_cucumbers_east(cucumbers) + move_cucumbers_south(cucumbers):
        steps += 1
    return steps


def move_cucumbers_east(cucumbers):
    width = len(cucumbers[0])
    moved = False
    for y, row in enumerate(cucumbers):
        movable = []
        newrow = list(row)
        for x in range(width):
            if row[x] == EASTBOUND:
                next_x = (x + 1) % width
                if row[next_x] == FREE:
                    newrow[x], newrow[next_x] = newrow[next_x], newrow[x]
                    moved = True
        if moved:
            cucumbers[y] = newrow
    return moved


def move_cucumbers_south(cucumbers):
    height = len(cucumbers)
    width = len(cucumbers[0])
    moved = False
    for x in range(width):
        movable = []
        for y in range(height):
            if cucumbers[y][x] == SOUTHBOUND:
                next_y = (y + 1) % height
                if cucumbers[next_y][x] == FREE:
                    movable.append((y, next_y))
        for y, next_y in movable:
            cucumbers[next_y][x], cucumbers[y][x] = (
                cucumbers[y][x],
                cucumbers[next_y][x],
            )
            moved = True
    return moved

cucumbers = load_cucumbers()
steps = move_cucumbers(cucumbers)

print(f"Steps: {steps}")
