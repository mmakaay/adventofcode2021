#!/bin/env python3
O,C,e= "([{<",")]}>",0
for l in open("input.txt"):
 s=""
 for c in l.strip():
  if c in O:s+=C[O.index(c)]
  elif s[-1]!=c:e+=[1,19,399,8379][C.index(c)]*3;break
  else:s=s[:-1]
print(e)  
