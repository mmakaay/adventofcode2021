#!/bin/env python3
k,*l="".join(open("input.txt")).split("\n\n")
e,n,b=1,list(map(int,k.split(","))),[list(map(int,"".join(y).split())) for y in l]
for v in n:
 for w in b:
  if v in w:w[w.index(v)]=-1
  for i in range(5):
   if(all(f<0 for f in w[i*5:i*5+5])or all(f<0 for f in w[i::5]))and e:print(sum(n for n in w if n>0)*v);e=0
