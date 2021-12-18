#!/bin/env python3
#
# For an explanation, see the file "strategy.txt".

import re


def load_target_area(path):
    with open(path, "r") as f:
        match = re.match(r".*x=(\d+)\.\.(\d+).*y=([-\d]+)\.\.([-\d]+)", next(f))
        return dict(zip(("x_min", "x_max", "y_min", "y_max"), map(int, match.groups())))


def get_max_start_speed(target):
    return -1 * target["y_min"] - 1


def get_max_height_for_start_speed(speed):
    return (speed * speed + speed) // 2


target = load_target_area("input.txt")
max_y_speed = get_max_start_speed(target)
max_height = get_max_height_for_start_speed(max_y_speed)

print(f"speed {max_y_speed}, height = {max_height}")
