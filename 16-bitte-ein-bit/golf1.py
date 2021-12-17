#!/bin/env python3
def I(l,v=0):return I(l-1,v<<1|B())if l else v
def Z():
 G,A,V,E,R=I(3),I(3),1,0,0
 if A-4:
  D=B();E=15-4*D;W=I(E)
  while W:J,t=Z();G+=t;E+=J;W-=[J,1][D]
 else:
  while V:V=I(5)&16;E+=5
 return 6+V+E,G
i=(b=="1"for n in(f"{int(h,16):04b}"for h in
next(open("input.txt")).strip())for b in n)
B=lambda:next(i)
print(Z()[1])
