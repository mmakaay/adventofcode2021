#!/bin/env python3.10

from functools import reduce


def load_diagnostics_from_file(path):
  with open("input.txt", "r") as f:
    data = [list(map(int, line.strip())) for line in f]
  return data


def shakedown(data, use_most_common, column=0):
  if len(data) == 1:
    return data[0]

  threshold = len(data) / 2
  most_common = sum(line[column] for line in data) >= threshold
  filter_bit = most_common if use_most_common else not most_common
  filtered = list(filter(lambda row: row[column] == filter_bit, data))
  max_column = len(data[0]) - 1
  next_column = 0 if column == max_column else column+1
  return shakedown(filtered, use_most_common, next_column)


def row2int(row):
  value = 0
  for bit in row:
    value = (value << 1) | bit
  return value


data = load_diagnostics_from_file("input.txt")
o2generator = row2int(shakedown(data, use_most_common=True))
co2scrubber = row2int(shakedown(data, use_most_common=False))

print(o2generator, "*", co2scrubber, " = ", o2generator*co2scrubber)
