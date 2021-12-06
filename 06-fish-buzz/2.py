#!/bin/env python3

from collections import Counter

def read_data():
  with open("input.txt") as f:
    return list(map(int, next(f).split(",")))

def group_fish_by_age(data):
  return dict(Counter(data))

def age_school_one_day(school):
  return dict(((k-1, v) for k,v in school.items()))

def handle_births(school):
  try:
    births = school.pop(-1)
    school[8] = births
    school[6] = school[6]+births if 6 in school else births
  except KeyError:
    pass
  return school

data = read_data()
school = group_fish_by_age(data)
for day in range(256):
  school = age_school_one_day(school)
  school = handle_births(school)

print(sum(school.values()))
