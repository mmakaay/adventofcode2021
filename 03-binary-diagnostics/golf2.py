#!/bin/env python3.10
def s(d,u,c=0):
 if len(d)<2:return d[0]
 t=len(d)/2;y=sum(line[c]for line in d)>=t;b=[not y,y][u]
 return s(list(filter(lambda r:r[c]==b,d)),u,(c+1)%len(d[0]))
i=lambda x:int("".join(map(str,x)),2)
d=[list(map(int,line.strip()))for line in open("input.txt")]
print(i(s(d,1))*i(s(d,0)))
