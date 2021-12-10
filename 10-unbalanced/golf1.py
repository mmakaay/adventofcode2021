#!/bin/env python3
M,E,H="([{<",")]}>",0
for l in open("input.txt"):
 s=""
 for c in l.strip():
  if c in M:s+=E[M.index(c)]
  elif s[-1]!=c:H+=[1,19,399,8379][E.index(c)]*3;break
  else:s=s[:-1]
print(H)  
