#!/bin/env python3

def read_grid_from_file(path):
  with open(path, "r") as f:
    return [list(map(int, line.strip())) for line in f]


def get_surrounding(x, y):
  yield (x-1, y-1)
  yield (x, y-1)
  yield (x+1, y-1)
  yield (x-1, y)
  yield (x+1, y)
  yield (x-1, y+1)
  yield (x, y+1)
  yield (x+1, y+1)


def within_bounds(grid, options):
  return (
    (x, y, grid[y][x]) for x,y in options if 
    x >= 0 and y >= 0 and x < len(grid[0]) and y < len(grid)
  )


def is_lowpoint(grid, x, y):
  return all(
    grid[y][x] < value
    for _,_,value in within_bounds(grid, get_surrounding(x, y))
  )


def get_lowpoints(grid):
  for x in range(len(grid[0])):  
    for y in range(len(grid)):
      if is_lowpoint(grid, x,y):
        yield (x, y, grid[y][x])


def get_risklevel(lowpoint):
  _, _, value = lowpoint
  return value + 1


grid = read_grid_from_file("example2.txt")
lowpoints = list(get_lowpoints(grid))
risk_level = sum(map(get_risklevel, lowpoints))

print(risk_level)
