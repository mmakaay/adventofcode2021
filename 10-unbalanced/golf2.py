#!/bin/env python3
M,E,H="([{<",")]}>",[]
for l in open("input.txt"):
 s,o,S="",0,0
 for c in l.strip():
  if c in M:s=E[M.index(c)]+s
  elif s[0]!=c:o+=1
  else:s=s[1:]
 if o<1:[S:=1+S*5+E.index(c)for c in s];H=sorted(H+[S])
print(H[len(H)//2])
