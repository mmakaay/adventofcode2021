#!/bin/env python3
from operator import *
from functools import reduce as r
def I(l,v=0):return I(l-1,v<<1|B())if l else v
def Z():
 V,T,L,M,O,P=I(3),I(3),6,1,0,0
 if T==4:
  while M:M=B();P=P<<4|I(4);O+=5
  return L+O,(V,T,P)
 O,P=X(B())
 return L+M+O,(V,T,P)
def X(D):
 O=15-4*D;W,A=I(O),[]
 while W:P,V=Z();O+=P;A.append(V);W-=1 if D else P
 return O,A
def V(T):
 _,t,a=T;f=[add,mul,min,max,0,gt,lt,eq][t]
 if f:a=int(r(f,[V(x)for x in a]))
 return a
N=[map(int,f"{int(h,16):04b}")for h in next(open("input.txt")).strip().upper()]
B=lambda:next(b for n in N for b in n)
print(V(Z()[1]))
