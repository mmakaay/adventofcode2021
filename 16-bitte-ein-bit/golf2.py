#!/bin/env python3
from operator import *
from functools import reduce as r
def I(l,v=0):return I(l-1,v<<1|B())if l else v
def Z():
 V,T,L,M,O,P=I(3),I(3),6,1,0,0
 if T==4:
  while M:M=B();P=P<<4|I(4);O+=5
  return L+O,(V,T,P)
 O,P=[X,Y][B()]()
 return L+M+O,(V,T,P)
def X():
 O=15;W=I(O);A=[]
 while W:P,V=Z();O+=P;A.append(V);W-=P
 return O,A
def Y():
 O=11;W=I(O);A=[]
 while W:P,V=Z();O+=P;A.append(V);W-=1
 return O,A
def V(T):
 _,t,a=T;f=[add,mul,min,max,0,gt,lt,eq][t]
 if f:a=int(r(f,[V(arg)for arg in a]))
 return a
N=[map(int,f"{int(h,16):04b}")for h in next(open("input.txt")).strip().upper()]
B=lambda:next(b for n in N for b in n)
print(V(Z()[1]))
