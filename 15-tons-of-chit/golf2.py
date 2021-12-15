#!/bin/env python3
from heapq import*;C=[list(map(int,line.strip()))for line in open("input.txt")]
o,p,V,R,D=len(C[0]),len(C),[(0,0,0)],{},set();w,h=o*5,p*5;U=[[0]*w for _ in range(h)]
for i in range(h*w):f,g=i//w,i%w;U[f][g]=1+(C[f%p][g%o]+g//o+f//p-1)%9 
while V:
 r,x,y=heappop(V);D.add((x,y))
 for N in[x for x in [(x-1,y)]*(x>0)+[(x,y-1)]*(y>0)+[(x+1,y)]*(x<(w-1))+[(x,y+1)]*(y<(h-1))if x not in D]:
  k,l=N;u,y=U[l][k],R.get(N,2**99);t=r+u
  if t<y:R[N]=t;heappush(V,(t,k,l))
print(R[h-1,w-1])
