#!/bin/env python3
from collections import Counter as T
f=open("input.txt")
p=next(f).strip();next(f);r=dict((l[0]+l[1],l[6])for l in f)
P,E=T([p[i:i+2]for i in range(len(p)-1)]),T(p)
for i in range(40):
 for h,j in dict(P).items():
  I=r[h];P.subtract({h:j});P.update({h[0]+I:j,I+h[1]:j});E.update({I:j})
C=E.values();print(max(C)-min(C))

