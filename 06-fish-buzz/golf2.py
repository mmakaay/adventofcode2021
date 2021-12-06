#!/bin/env python3
d=[0]*10
for i in map(int,next(open("input.txt")).split(",")):d[i+1]+=1
for x in range(256):d=d[1:]+[0];d[9],d[7]=d[0],d[7]+d[0]
print(sum(d[1:]))
