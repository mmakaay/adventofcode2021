#!/bin/env python3
d,f=set(),open("input.txt")
while","in(l:=next(f)):d.add(tuple(map(int,l.split(","))))
l=next(f);a=l[11]=="y";o=int(l[13:])
for x,y in set(d):
 if a and y>o:d.add((x, 2*o-y));d.remove((x,y))
 if a<1 and x>o:d.add((2*o-x, y));d.remove((x,y))
print(len(d))
