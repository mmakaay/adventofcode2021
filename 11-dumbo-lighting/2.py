#!/bin/env python3

def load_octopi(path):
  with open(path) as f:
    return [list(map(int, line.strip())) for line in f]


def get_surrounding(pos):
  x, y = pos
  yield (x-1, y-1)
  yield (x,   y-1)
  yield (x+1, y-1)
  yield (x-1, y  )
  yield (x+1, y  )
  yield (x-1, y+1)
  yield (x,   y+1)
  yield (x+1, y+1)


def grid_width(grid):
  return len(grid[0])


def grid_height(grid):
  return len(grid)


def value_at(grid, pos):
  x, y = pos
  return grid[y][x]


def positions(grid):
  return (
    (x, y)
    for y in range(grid_height(grid))
    for x in range(grid_width(grid))
  )


def within_bounds(grid, positions):
  return (
    (x, y) for x, y in positions if 
    x >= 0 and y >= 0 and x < grid_width(grid) and y < grid_height(grid)
  )


def increase_energy_level_at_pos(octopi, pos):
  x,y = pos
  octopi[y][x] += 1


def increase_energy_level(octopi):
  for pos in positions(octopi):
    increase_energy_level_at_pos(octopi, pos)


def deplete_energy_at_pos(octopi, pos):
  x,y = pos
  octopi[y][x] = 0


def deplete_energy_at_positions(octopi, positions):
  for pos in positions:
    deplete_energy_at_pos(octopi, pos)


def find_flash_positions(octopi): 
  for pos in positions(octopi):
    if value_at(octopi, pos) > 9:
      yield pos


def flash(octopi, flashed=[]): 
  new_flash_positions = list(
    pos for pos in find_flash_positions(octopi)
    if pos not in flashed
  )
  if new_flash_positions:
    for flash_pos in new_flash_positions:
      for around in within_bounds(octopi, get_surrounding(flash_pos)):
        increase_energy_level_at_pos(octopi, around)
    return flash(octopi, flashed + new_flash_positions)
  return flashed


def cycle_octopi(octopi):
  increase_energy_level(octopi)
  flashed = flash(octopi)
  deplete_energy_at_positions(octopi, flashed)
  return flashed


octopi = load_octopi("input.txt") 
number_of_octopi = grid_width(octopi) * grid_height(octopi)
step = 1
while step:
  flashed = cycle_octopi(octopi)
  if len(flashed) == number_of_octopi:
      break;
  step += 1

print(step)
