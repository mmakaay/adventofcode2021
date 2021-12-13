#!/bin/env python3
d,f,E=set(),open("input.txt"),"\033["
while","in(l:=next(f)):d.add(tuple(map(int,l.split(","))))
for l in f: 
 a=l[11]=="y";o=int(l[13:])
 for x,y in set(d):
  if a and y>o:d.add((x,2*o-y));d.remove((x,y))
  if a<1 and x>o:d.add((2*o-x, y));d.remove((x,y))
print("".join([f"{E}2J{E}H"]+[f"{E}{y+1};{x+1}f*" for x,y in d]+[f"{E}7;0f"]))

