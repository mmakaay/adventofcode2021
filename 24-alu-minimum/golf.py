#!/bin/env python3
import itertools as i
S,r,Z=[0]*15,range,[0]
for N in i.product([1],[1,2],[8,9],Z,r(1,7),r(2,10),r(3,10),Z,Z,Z,[7,8,9],Z,Z,Z):
 N=list(N)
 for a,b,c in[(3,4,3),(7,6,-2),(8,5,-1),(9,2,-7),(11,10,-6),(12,1,7),(13,0,8)]:N[a]=N[b]+c
 print("".join(map(str,N)))
