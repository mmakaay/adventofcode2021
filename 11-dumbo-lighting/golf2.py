#!/bin/env python3
o,G,f=ord,[l.strip() for l in open("input.txt")],[]
A,H,R,G=0,len(G[0]),len(G),"".join(G)
while len(f)!=H*R:
 A,f,G=A+1,[],[chr(o(x)+1)for x in G]
 while X:=[j for j,x in enumerate(G)if o(x)>57 and j not in f]:
  for n in X:
   f,a,b,c,d=f+[n],n%H>0,(n+1)%H>0,n//H>0,n//H<R-1
   r=[p for p in[n-1]*a+[n-H-1]*a*c+[n+H-1]*a*d+[n+1]*b+[n-H]*c+[n-H+1]*c*b+[n+H]*d+[n+H+1]*d*b]
   for p in r:G[p]=chr(o(G[p])+1)
 for m in f:G[m]='0'
print(A)
