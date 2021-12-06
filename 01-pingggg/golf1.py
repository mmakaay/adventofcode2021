#!/usr/bin/env python3
d=list(map(int,open("input.txt")))
print(sum(b-a>0 for a,b in zip(d,d[1:])))
