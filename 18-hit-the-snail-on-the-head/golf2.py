#!/bin/env python3
import re,functools as f,itertools as i;E=enumerate
def A(a,b):return R([-1]+a+b+[-2])
def R(c,l=0):
 for p,e in E(c):
  l+=e==-1;l-=e<-1
  if l>4:
   r=[I for I,V in E(c[p+3:])if V>=0];L=[I for I,V in E(c[:p])if V>=0]
   if r:c[p+r[0]+3]+=c[p+2]
   if L:c[L[-1]]+=c[p+1]
   c[p:p+4]=[0];return R(c)
 for p,e in E(c):
  if e>9:L=c[p]//2;c[p:p+1]=[-1,L,c[p]-L,-2];return R(c)
 return c
def M(a):
 if len(a)<2:return a[0]
 for i,c in E(a):
  if c>=0 and a[i-1]>=0:a[i-2:i+2]=[3*a[i-1]+2*c];return M(a)
d=[list(map(int,l.translate({91:'-1,',93:',-2'}).split(",")))for l in open("input.txt")]
print(max(M(A(a,b)) for a,b in i.permutations(d,2)))
