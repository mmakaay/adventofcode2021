#!/bin/env python3
import re
from functools import *
def D(c):return c.isdigit()
def S(a,s,d):
 while 0<s<len(a)-1 and not D(a[s]):s+=d;e=s
 if D(a[s]):
  while D(a[e+d]):e+=d
  [s,e]=sorted([s,e]);return(s,e,N(a,s,e+1))
 return(0,0,0)
def N(a,s,e):
 return int("".join(a[s:e]))
def sum(a,b):
 a = ["["]+list(a)+[","]+list(b)+["]"]
 while True:
  i,e,s,d,n=0,-1,-1,0,-1
  for c in a:y=D(c);u=n>0>s and y;s=[s,i-1][u];n=[-1,n][u];n=[n,i][y and n<0>s];d+=(c=='[')-(c==']');e=[e,i][d>4 and e<0];i+=1
  if e<0 and s<0:break 
  if e>0:
   p=e;f=a.index;e=f(']',p);c=f(',',p);L=N(a,p+1,c);R=N(a,c+1,e)
   k,l,m=S(a,p,-1);s,t,u=S(a,e,1)
   if s:a[s:t+1]=list(str(u+R))
   a[p:e+1]="0"
   if k:a[k:l+1]=list(str(m+L))
  elif s>0:
   t=s+1
   while D(a[t]):t+=1
   v=N(a,s,t);l=v//2;r=v-l
   a[s:t]=["["]+list(str(l))+[","]+list(str(r))+["]"]
 return "".join(a)
def magnitude(a):
 R=re.compile('\[(\d+),(\d+)\]')
 while R.search(a):
  a = R.sub(lambda x:str(3*int(x[1])+2*int(x[2])),a)
 return a
c=reduce(sum,(l.strip() for l in open("input.txt")))
print(magnitude(c))
