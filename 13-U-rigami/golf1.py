#!/bin/env python3
d,f=[],open("input.txt")
while","in(l:=next(f)):d.append(list(map(int,l.split(","))))
p=[[0]*(max(x for x,_ in d)+1)for _ in range(max(y for _,y in d)+1)] 
for x,y in d:p[y][x]=1
l=next(f);a=l[11]=="x";o=int(l[13:]);p,b=[(p[:o],p[o+1:]),([l[:o]for l in p],[l[o+1:]for l in p])][a]
b=[b[::-1],[l[::-1]for l in b]][a];r,s=len(b[0]),len(b)
for X in range(r*s):p[X//r+len(p)-s][X%r+len(p[0])-r]|=b[X//r][X%r]
print(sum(x for l in p for x in l))
