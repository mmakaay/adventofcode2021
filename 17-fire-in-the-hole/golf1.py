#!/bin/env python3
s=int(next(open("example.txt")).split("y=-")[1].split(".")[0])
print(s*(s+1)//2)
