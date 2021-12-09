#!/bin/env python3
from functools import reduce as r
def c(l):return r(lambda x,y:x|1<<(ord(y)-97),l,0),len(l)
def q(g,x,m):h=[k for k,c in y if c==x and m&k==m][0];z[g]=h;y.remove((h,x))
s,i=0,[[list(map(c,x.split()))for x in d.split("|")] for d in open("input.txt")]
for y,e in i:
 y,z=set(y),[0]*10;q(1,2,0);q(3,5,z[1]);q(4,4,0);q(7,3,0)
 q(8,7,0);q(9,6,z[3]);q(0,6,z[1]);q(6,6,0);q(5,5,z[9]&~z[1])
 q(2,5,0);s+=int("".join(map(str,(z.index(d)for d,_ in e))))
print(s)
