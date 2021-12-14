#!/bin/env python3
from collections import defaultdict as X
f,P=open("input.txt"),X(int)
S=next(f).strip();next(f);rules=dict((l[0]+l[1],l[6])for l in f)
for i in range(len(S)-1):P[S[i:i+2]]+=1
for i in range(40):
 N=X(int)
 for p,c in P.items():i=rules[p];N[p[0]+i]+=c;N[i+p[1]]+=c
 P=N
V=X(int);V[S[-1]]+=1
for p,c in P.items():V[p[0]]+=c
v=V.values()
print(max(v)-min(v))
