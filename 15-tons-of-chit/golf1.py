#!/bin/env python3
from heapq import* 
C=[list(map(int,line.strip()))for line in open("input.txt")]
w,h,V,R,D=len(C[0])-1,len(C)-1,[(0,0,0)],{},set()
while V:
 r,x,y=heappop(V);D.add((x,y))
 for N in[x for x in[(x-1,y)]*x+[(x,y-1)]*y+[(x+1,y)]*(x<w)+[(x,y+1)]*(y<h)if x not in D]:
  k,l=N;u,y=C[l][k],R.get(N,2**99);t=r+u
  if t<y:R[N]=t;heappush(V,(t,k,l))
print(R[h,w])
