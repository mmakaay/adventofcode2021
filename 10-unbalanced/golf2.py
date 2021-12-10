#!/bin/env python3
M,E,H="([{<",")]}>",[]
for l in open("input.txt"):
 s,o,S="",0,0
 for c in l.strip():o+=s==(s:=E[M.index(c)]+s if c in M else s[s[0]==c:])
 H=sorted(H+[S:=1+S*5+E.index(c)for c in s][-1:]*(o<1))
print(H[len(H)//2])
