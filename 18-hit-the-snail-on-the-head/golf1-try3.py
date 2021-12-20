#!/bin/env python3
from functools import *;E=enumerate
def I():
 for l in open("input.txt"):
  i=0;n,d=[],[]
  for c in map(int,l.translate({91:'-1,',93:',-3'}).split(",")):
   u=c>=0;i+=(c+2)*(c<0);n+=[c]*u;d+=[i]*u
  yield(n,d)
A=lambda a,b:R(a[0]+b[0],[x+1 for x in a[1]+b[1]])
def R(v,d):
 m=len(v)-1;f=lambda x,y:[i for i,n in E(x)if n>y]
 if p:=f(d,4):
  p=p[0];v[p-1]+=v[p]*(p>0);g=m>p+1;v[p+1+g]+=v[p+1]*g
  v[p:p+2]=[0];d[p:p+2]=[d[p]-1];return(R(v,d))
 elif p:=f(v,9):
  p=p[0];l=v[p]//2;r=v[p]-l;v[p:p+1]=[l,r];d[p:p+1]=[d[p]+1]*2;return(R(v,d))
 return(v,d)
def M(v,d):
 for i,n in E(v[:-1]):
  if d[i]==d[i+1]:
   v[i:i+2]=[3*n+2*v[i+1]];d[i:i+2]=[d[i]-1]
   return v[0]if len(v)<2 else M(v,d)
print(M(*reduce(A,list(I()))))
