#!/bin/env python3
from operator import *
from functools import *
def I(l,v=0):return I(l-1,v<<1|B())if l else v
def Z():
 T,L,M,O,P=I(6)&7,6,1,0,0
 if T-4:
  D=B();O=15-4*D;W,P=I(O),[]
  while W:R,Q=Z();O+=Q;P+=[R];W-=[Q,1][D]
 else:
  while M:M=B();P=P<<4|I(4);O+=5
 return(T,P),L+M+O
def V(T):
 t,a=T;f=[add,mul,min,max,0,gt,lt,eq][t]
 if f:a=int(reduce(f,map(V,a)))
 return a
i=(b=="1"for n in(f"{int(h,16):04b}"for h in
next(open("input.txt")).strip())for b in n)
B=lambda:next(i);print(V(Z()[0]))
