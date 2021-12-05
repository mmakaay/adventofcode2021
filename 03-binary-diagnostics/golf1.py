#!/bin/env python3.10
d=[map(int,l.strip())for l in open("input.txt")]
g,e,t,c=0,0,len(d)/2,list(zip(*d))
for v in c:a=sum(v)>t;g=g<<1|a;e=e<<1|(not a)
print(g*e)
