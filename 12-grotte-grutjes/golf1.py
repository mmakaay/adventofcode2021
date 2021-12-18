#!/bin/env python3
def explore(r,c,p):
 p+=(c,)
 if c=="end":yield p
 else:
  r=r if c.isupper()else dict((C,[e for e in E if e != c])for C,E in r.items())
  for n in r[c]:yield from explore(r,n,p)
r={}
for[a,b]in([l.strip().split("-")for l in open("input.txt", "r")]):r[a]=r.get(a,[])+[b];r[b]=r.get(b,[])+[a]
print(len(list((explore(r,"start",())))))
