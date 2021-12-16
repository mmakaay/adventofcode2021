#!/bin/env python3
def I(l,v=0):return I(l-1,v<<1|B())if l else v
def Z():
 G,A,T,V,E,R=I(3),I(3),6,1,0,0
 if A==4:
  while V:V=I(5)&16;E+=5
 else:E,R=X(B())
 return(G,A,R),T+V+E
def X(D):
 E=15-4*D;W,A=I(E),[]
 while W:G,R=Z();E+=R;A+=[G];W-=[R,1][D]
 return E,A
def G(t,A=0):v,t,a=t;return A+(sum(map(G,a))if t!=4 else 0)+v
i=(b=="1"for n in(f"{int(h,16):04b}"for h in
next(open("input.txt")).strip())for b in n)
B=lambda:next(i);print(G(Z()[0]))
