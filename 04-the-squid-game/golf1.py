#!/bin/env python3
k,*l="".join(open("input.txt").readlines()).split("\n\n")
n,b=list(map(int,k.split(","))),[list(map(int,"".join(y).split())) for y in l]
for v in n:
 for w in b:
  if v in w:w[w.index(v)]=-1
  for i in range(5):
   if all(f==-1 for f in w[i*5:i*5+5]) or all(f==-1 for f in w[i::5]):
    print(sum(n for n in w if n>0)*v)
    import sys
    sys.exit()
