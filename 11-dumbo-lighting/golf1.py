#!/bin/env python3
o,G=ord,[l.strip() for l in open("input.txt")]
A,H,R,G=0,len(G[0]),len(G),"".join(G)
for n in range(100):
 f,G=[],[chr(o(x)+1)for x in G]
 while X:=[j for j,x in enumerate(G)if o(x)>57 and j not in f]:
  for n in X:
   A,G[n],f,a,b,c,d=A+1,'0',f+[n],n%H>0,(n+1)%H>0,n//H>0,n//H<R-1;r=[p for p in[n-1]*a+[n-H-1]*a*c+[n+H-1]*a*d+[n+1]*b+[n-H]*c+[n-H+1]*c*b+[n+H]*d+[n+H+1]*d*b]
   for p in r:G[p]=chr(o(G[p])+1*(p not in f))
print(A)
