#!/usr/bin/env python3

with open("input.txt", "r") as f:
  data = list(map(int, f))
  paired = zip([data[0]]+data, data)
  higher = sum(b-a > 0 for a,b in paired)
print(higher)
