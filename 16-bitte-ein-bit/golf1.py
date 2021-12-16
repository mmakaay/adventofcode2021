#!/bin/env python3
def I(l,v=0):return I(l-1,v<<1|B())if l else v
def Z():
 V,T,L,M,O,P=I(3),I(3),6,1,0,0
 if T==4:
  while M:M=B();P=P<<4|I(4);O+=5
  return(V,T,P),L+O
 O,P=X(B())
 return(V,T,P),L+M+O
def X(D):
 O=15-4*D;W,A=I(O),[]
 while W:V,P=Z();O+=P;A.append(V);W-=[P,1][D]
 return O,A
def V(t,T=0):v,t,a=t;return T+(sum(map(V,a))if t!=4 else 0)+v
N=[map(int,f"{int(h,16):04b}")for h in next(open("input.txt")).strip().upper()]
B=lambda:next(b for n in N for b in n)
print(V(Z()[0]))
