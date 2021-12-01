#!/usr/bin/env python3

f = open("input.txt", "r")
data = list(map(int, f))
paired = zip([data[0]]+data, data)
higher = sum(b-a > 0 for a,b in paired)
print(higher)
