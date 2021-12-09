#!/bin/env python3

def read_grid_from_file(path):
  with open(path, "r") as f:
    return [list(map(int, line.strip())) for line in f]


def get_surrounding(coordinate):
  x, y = coordinate
  yield (x,   y-1)
  yield (x-1, y  )
  yield (x+1, y  )
  yield (x,   y+1)


def grid_width(grid):
  return len(grid[0])


def grid_height(grid):
  return len(grid)


def value_at(grid, coordinate):
  x, y = coordinate
  return grid[y][x]


def coordinates(grid):
  for x in range(grid_width(grid)):  
    for y in range(grid_height(grid)):
      yield (x, y)


def within_bounds(grid, coordinates):
  return (
    (x, y) for x, y in coordinates if 
    x >= 0 and y >= 0 and x < grid_width(grid) and y < grid_height(grid)
  )


def is_lowpoint(grid, coordinate):
  return all(
    value_at(grid, around) > value_at(grid, coordinate)
    for around in within_bounds(grid, get_surrounding(coordinate))
  )


def get_lowpoints(grid):
  for coordinate in coordinates(grid):
    if is_lowpoint(grid, coordinate):
      yield coordinate


def get_risklevel(grid, lowpoint):
  return value_at(grid, lowpoint) + 1


grid = read_grid_from_file("input.txt")
lowpoints = get_lowpoints(grid)
risk_levels = (get_risklevel(grid, lowpoint) for lowpoint in lowpoints)

print(sum(risk_levels))

