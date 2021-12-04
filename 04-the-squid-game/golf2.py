#!/bin/env python3
def w(b):return all(any(f>=0 for f in b[i*5:i*5+5])and any(f>=0 for f in b[i::5])for i in range(5))
j="".join
k,*l=j(open("input.txt")).split("\n\n")
n,b=list(map(int,k.split(","))),[list(map(int,j(y).split()))for y in l]
for v in n:
 for o in b:
  if v in o:o[o.index(v)]=-1
 if len(b)>1:b=list(filter(w,b))
 elif not w(b[0]):break
print(sum(n for n in b[0]if n>0)*v)

