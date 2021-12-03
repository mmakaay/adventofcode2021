#!/usr/bin/env python3

with open("input.txt", "r") as f:
  data = list(map(int, f))
  sums = [sum(data[i:i+3]) for i in range(len(data)-2)]
  paired = zip([sums[0]]+sums, sums)
  higher = sum(b-a > 0 for a,b in paired)
print(higher)
