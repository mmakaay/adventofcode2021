#!/bin/env python3

from functools import reduce


def load_octopi(path):
    with open(path) as f:
        return [list(map(int, line.strip())) for line in f]


def get_surrounding(pos):
    x, y = pos
    yield (x - 1, y - 1)
    yield (x, y - 1)
    yield (x + 1, y - 1)
    yield (x - 1, y)
    yield (x + 1, y)
    yield (x - 1, y + 1)
    yield (x, y + 1)
    yield (x + 1, y + 1)


def grid_width(grid):
    return len(grid[0])


def grid_height(grid):
    return len(grid)


def value_at(grid, pos):
    x, y = pos
    return grid[y][x]


def positions(grid):
    return ((x, y) for y in range(grid_height(grid)) for x in range(grid_width(grid)))


def within_bounds(grid, positions):
    return list(
        (x, y)
        for x, y in positions
        if x >= 0 and y >= 0 and x < grid_width(grid) and y < grid_height(grid)
    )


def increase_energy_level_at(octopi, at_positions):
    return [
        [value + 1 if (x, y) in at_positions else value for x, value in enumerate(row)]
        for y, row in enumerate(octopi)
    ]


def increase_all_energy_levels(octopi):
    return increase_energy_level_at(octopi, positions(octopi))


def deplete_energy_level_at(octopi, at_positions):
    return [
        [0 if (x, y) in at_positions else value for x, value in enumerate(row)]
        for y, row in enumerate(octopi)
    ]


def find_flash_positions(octopi):
    for pos in positions(octopi):
        if value_at(octopi, pos) > 9:
            yield pos


def flash(octopi, flashed=[]):
    new_flash_positions = list(
        pos for pos in find_flash_positions(octopi) if pos not in flashed
    )
    if new_flash_positions:
        for flash_pos in new_flash_positions:
            surrounding = within_bounds(octopi, get_surrounding(flash_pos))
            octopi = increase_energy_level_at(octopi, surrounding)
        return flash(octopi, flashed + new_flash_positions)
    return octopi, flashed


def cycle_octopi(octopi, flashed=[]):
    octopi = increase_all_energy_levels(octopi)
    octopi, new_flashed = flash(octopi)
    octopi = deplete_energy_level_at(octopi, new_flashed)
    return octopi, flashed + new_flashed


octopi = load_octopi("input.txt")
number_of_flashes = 0
for _ in range(100):
    octopi, flashed = cycle_octopi(octopi)
    number_of_flashes += len(flashed)

print(number_of_flashes)
