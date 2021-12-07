#!/bin/env python3
c=list(map(int,next(open("input.txt")).split(",")))
print(min(sum(abs(c-p)*(abs(c-p)+1)//2 for c in c) for p in range(max(c))))
