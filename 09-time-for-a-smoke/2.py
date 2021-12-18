#!/bin/env python3

import math


def load_grid_from_file(path):
    with open(path, "r") as f:
        return [list(map(int, line.strip())) for line in f]


def grid_width(grid):
    return len(grid[0])


def grid_height(grid):
    return len(grid)


def value_at(grid, pos):
    x, y = pos
    return grid[y][x]


def get_surrounding(pos):
    x, y = pos
    yield (x, y - 1)
    yield (x - 1, y)
    yield (x + 1, y)
    yield (x, y + 1)


def positions(grid):
    return ((x, y) for y in range(grid_height(grid)) for x in range(grid_width(grid)))


def within_bounds(grid, positions):
    return (
        (x, y)
        for x, y in positions
        if x >= 0 and y >= 0 and x < grid_width(grid) and y < grid_height(grid)
    )


def is_lowpoint(grid, pos):
    return all(
        value_at(grid, around) > value_at(grid, pos)
        for around in within_bounds(grid, get_surrounding(pos))
    )


def get_lowpoints(grid):
    return (pos for pos in positions(grid) if is_lowpoint(grid, pos))


def is_upstream(grid, pos, around):
    value = value_at(grid, pos)
    value_around = value_at(grid, around)
    return value_around != 9 and value_around > value


def follow_upstream(grid, pos, basin):
    basin.add(pos)
    for around in within_bounds(grid, get_surrounding(pos)):
        if is_upstream(grid, pos, around):
            follow_upstream(grid, around, basin)
    return basin


def get_basin(grid, lowpoint):
    return follow_upstream(grid, lowpoint, set())


def get_basins(lowpoints):
    lowpoints = get_lowpoints(grid)
    return (get_basin(grid, lowpoint) for lowpoint in lowpoints)


grid = load_grid_from_file("input.txt")
basins = get_basins(grid)
basins_by_size = sorted(basins, key=len, reverse=True)
biggest_three = basins_by_size[0:3]

print(math.prod(map(len, biggest_three)))
