#!/bin/env python3
s=int(next(open("input.txt")).split("y=")[1].split(".")[0])
print(s*s+s>>1)
