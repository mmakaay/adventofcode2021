#!/bin/env python3
from operator import *
from functools import reduce as r
def I(l,v=0):return I(l-1,v<<1|B())if l else v
def Z():
 I(3);T,L,M,O,P=I(3),6,1,0,0
 if T==4:
  while M:M=B();P=P<<4|I(4);O+=5
 else:O,P=X(B())
 return(T,P),L+M+O
def X(D):
 O=15-4*D;W,A=I(O),[]
 while W:V,P=Z();O+=P;A.append(V);W-=[P,1][D]
 return O,A
def V(T):
 t,a=T;f=[add,mul,min,max,0,gt,lt,eq][t]
 if f:a=int(r(f,map(V,a)))
 return a
i=(b=="1"for n in(f"{int(h,16):04b}"for h in
next(open("input.txt")).strip())for b in n)
B=lambda:next(i);print(V(Z()[0]))
