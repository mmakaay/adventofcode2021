#!/bin/env python3.10
x,y,m=0,0,{"f":(1,0),"u":(0,-1),"d":(0,1)}
for q,r,a in((*m[c[0]],int(a))for c,a in(x.split(" ")for x in open("input.txt"))):x+=q*a;y+=r*a
print(x*y)
