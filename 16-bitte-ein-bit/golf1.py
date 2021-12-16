#!/bin/env python3
def I(l,v=0):return I(l-1,v<<1|B())if l else v
def Z():
 V,T,L,M,O,P=I(3),I(3),6,1,0,0
 if T==4:
  while M:M=I(5)&16;O+=5
 else:O,P=X(B())
 return(V,T,P),L+M+O
def X(D):
 O=15-4*D;W,A=I(O),[]
 while W:V,P=Z();O+=P;A.append(V);W-=[P,1][D]
 return O,A
def V(t,T=0):v,t,a=t;return T+(sum(map(V,a))if t!=4 else 0)+v
i=(b=="1"for n in(f"{int(h,16):04b}"for h in
next(open("input.txt")).strip())for b in n)
B=lambda:next(i);print(V(Z()[0]))
