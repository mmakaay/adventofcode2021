#!/bin/env python3
d=[0]*9
for i in map(int,next(open("input.txt")).split(",")):d[i]+=1
for x in range(80):d[(x+7)%9]+=d[x%9]
print(sum(d[0:]))
