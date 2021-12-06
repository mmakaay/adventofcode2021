#!/bin/env python3
d=[0]*10
for i in map(int,next(open("input.txt")).split(",")):d[i+1]+=1
for x in range(720):
 c=x%9;d[c]=d[c+1]
 if c>7:d[0],d[9],d[7]=0,d[0],d[7]+d[0]
print(sum(d))
