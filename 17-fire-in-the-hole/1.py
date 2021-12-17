#!/bin/env python3

import re


def load_target_area(path):
  with open(path, "r") as f:
    match = re.match(r".*x=(\d+)\.\.(\d+).*y=([-\d]+)\.\.([-\d]+)", next(f))
    x1,x2,y1,y2 = tuple(map(int, match.groups()))
    return x1,x2,y1,y2


def find_y_speed_options(y_min, y_max):
  y_speed_range = list(range(0, (abs(y_min))))
  for start_speed in y_speed_range:
    speed = start_speed
    y = 0
    while y >= y_min:
      if y <= y_max:
        yield (start_speed, y)
      speed += 1
      y -= speed 


def get_max_start_speed(options):
  return max(start_speed for start_speed,_ in options)


def get_max_height_for_start_speed(speed):
  max_height = 0
  for s in range(speed+1):
    max_height += s 
  return max_height


x_min,x_max,y_min,y_max = load_target_area("input.txt")
speed_options = find_y_speed_options(y_min, y_max)
max_y_speed = get_max_start_speed(speed_options)
max_height = get_max_height_for_start_speed(max_y_speed)

print(f"speed {max_y_speed}, height = {max_height}")
