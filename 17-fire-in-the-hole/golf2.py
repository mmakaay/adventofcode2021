#!/bin/env python3
import re,itertools as i
X,Y={},{};a,b,c,d=tuple(map(int,re.findall('(-?\d+)',next(open("input.txt")))))
for w in range(c,-c):
 l,y,s=w,0,0
 while y>=c:Y[s]=Y.get(s,[])+[[w],[]][y>d];s+=1;y+=l;l=l-1
for w in range(b+1):
 l,x,s=w,0,0
 while s<=max(Y)and x<=b:X[s]=X.get(s,[])+[[w],[]][x<a];s+=1;x+=l;l=max(l-1,0)
print(len(set(V for C in(i.product(r,e)for r,e in((X[g],Y[g])for
g in X for h in Y if g==h))for V in C)))
