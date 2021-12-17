#!/bin/env python3

import re
from itertools import groupby


def load_target_area(path):
  with open(path, "r") as f:
    match = re.match(r".*x=(\d+)\.\.(\d+).*y=([-\d]+)\.\.([-\d]+)", next(f))
    x1,x2,y1,y2 = tuple(map(int, match.groups()))
    return x1,x2,y1,y2


def find_y_speed_options(y_min, y_max):
  speed_range = range(y_min, (abs(y_min)))
  for start_speed in speed_range:
    speed = start_speed
    y = 0
    step = 0
    while y >= y_min:
      if y <= y_max:
        yield (start_speed, step)
      step += 1
      y += speed 
      speed = speed-1


def find_x_speed_options(x_min, x_max, max_steps):
  speed_range = range(x_max+1)
  for start_speed in speed_range:
    speed = start_speed
    x = 0
    step = 0
    while step<=max_steps and x <= x_max:
      if x >= x_min:
        yield (start_speed, step)
      x += speed 
      step += 1
      speed = speed-1 if speed > 0 else 0


def get_possible_starting_velocities(x_options, y_options):
  x_options = group_by_step(x_options)
  y_options = group_by_step(y_options)
  for step, x_values in x_options.items():
    if step in y_options:
      y_values = y_options[step]
      for x in x_values:
        for y in y_values:
          yield (x,y)


def group_by_step(options):
  def by_step(option):
    value, step = option
    return step
  sorted_options = sorted(options, key=by_step)
  grouped_options = groupby(sorted_options, key=by_step)
  return dict(
    (step, [o for o,_ in options])
    for step,options in grouped_options
  ) 


x_min,x_max,y_min,y_max = load_target_area("input.txt")
y_options = list(find_y_speed_options(y_min, y_max))
max_steps = max(step for _,step in y_options)
x_options = find_x_speed_options(x_min, x_max, max_steps)
velocities = set(get_possible_starting_velocities(x_options, y_options))

print(len(velocities))
