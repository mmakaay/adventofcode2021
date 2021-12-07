#!/bin/env python3

def read_crabs_from_file(path):
  with open(path, "r") as f:
    crabs = list(map(int, next(f).split(",")))
  return crabs


def get_fuel_for_position(crabs, position):
  distances = (abs(crab - position) for crab in crabs)
  fuel_total = sum(distances)
  return fuel_total


def build_options(crabs):
  positions = list(range(min(crabs), max(crabs)+1))
  for position in positions:
    fuel_total = get_fuel_for_position(crabs, position)
    yield position, fuel_total


def sort_by_fuel_use(options):
  return sorted(options, key=lambda o: o[1])


crabs = read_crabs_from_file("input.txt")
options = build_options(crabs)
options = sort_by_fuel_use(options)
best_position, fuel = options[0]

print(f"best position = {best_position}, fuel = {fuel}")
