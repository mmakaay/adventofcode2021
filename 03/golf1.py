#!/bin/env python3.10

d=[map(int,l.strip())for l in open("input.txt")]
g,e,t=0,0,len(d)/2
c = list(zip(*d))
for values in c:
    add_gamma = sum(values) > t
    g = (g << 1) | add_gamma
    e = (e << 1) | (not add_gamma)

print(g*e)
