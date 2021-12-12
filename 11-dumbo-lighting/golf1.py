#!/bin/env python3
i,G=100,[l.strip() for l in open("input.txt")];A,H,R,G=0,len(G[0]),len(G),"".join(G)
while i:
 i,f,G=i-1,[],[chr(ord(x)+1)for x in G]
 while X:=[j for j,x in enumerate(G)if ord(x)>57 and j not in f]:
  for n in X:
   A,G[n],f,a,b=A+1,'0',f+[n],n%H>0,(n+1)%H>0;r=[p for p in[n-1]*a+[n-H-1]*a+[n+H-1]*a+[n+1]*b+[n-H+1]*b+[n+H+1]*b+[n-H,n+H]if H*R>p>=0]
   for p in r:G[p]=chr(ord(G[p])+1*(p not in f))
print(A)
