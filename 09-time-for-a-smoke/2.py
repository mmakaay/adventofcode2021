#!/bin/env python3

import math


def read_grid_from_file(path):
  with open(path, "r") as f:
    return [list(map(int, line.strip())) for line in f]


def grid_width(grid):
  return len(grid[0])


def grid_height(grid):
  return len(grid)


def value_at(grid, coordinate):
  x, y = coordinate
  return grid[y][x]


def get_surrounding(coordinate):
  x, y = coordinate
  yield (x,   y-1)
  yield (x-1, y  )
  yield (x+1, y  )
  yield (x,   y+1)


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


def is_upstream(grid, coordinate, around):
  value = value_at(grid, coordinate)
  value_around = value_at(grid, around)
  return value_around != 9 and value_around > value


def follow_upstream(grid, coordinate, basin):
  basin.add(coordinate)
  for around in within_bounds(grid, get_surrounding(coordinate)):
    if is_upstream(grid, coordinate, around):
      follow_upstream(grid, around, basin)
  return basin


def get_basin(grid, lowpoint):
  return follow_upstream(grid, lowpoint, set())


def get_basins(lowpoints):
  lowpoints = get_lowpoints(grid)
  return (get_basin(grid, lowpoint) for lowpoint in lowpoints) 


grid = read_grid_from_file("input.txt")
basins = get_basins(grid)
basins_by_size = sorted(basins, key=len, reverse=True)
biggest_three = basins_by_size[0:3]

print(math.prod(map(len, biggest_three)))
