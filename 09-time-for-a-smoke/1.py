#!/bin/env python3


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


def get_risklevel(grid, lowpoint):
    return value_at(grid, lowpoint) + 1


grid = load_grid_from_file("input.txt")
lowpoints = get_lowpoints(grid)
risk_levels = (get_risklevel(grid, lowpoint) for lowpoint in lowpoints)

print(sum(risk_levels))
