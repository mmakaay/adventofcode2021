#!/bin/env python3.10
import itertools as i,functools as f
@f.cache
def T(S,t,g,h):
 if t<1 or S<1:return[0,S==0 and h==g][t<1]
 if(s:=S-h)>=21:return 0 
 return sum(f*T(s,t-1,g,(h-S-1)%10+1)for f,S in zip([1,3,6,7,6,3,1],R(3,10)))
[p1,p2]=[int(line.split(": ")[1])for line in open("input.txt")]
R=range;e=R(1,11);G=list(i.product(e,e,R(21,31),e,R(3,21)))
W=lambda a,b,w:sum(T(y,t,[a,b][w],x)*T(u,t-(1-w),[b,a][w],z)for t,x,y,z,u in G)
print(max(W(p1,p2,0),W(p1,p2,1)))
