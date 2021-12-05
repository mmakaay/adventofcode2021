#!/bin/env python3
import re
o,q=max,list(map(int,re.split(',| -> |\n',"".join(open("input.txt")).strip())));m=1000;g=[0]*m*m
for a,b,c,d in [q[i:i+4]for i in range(0,len(q),4)]:
 s=o(abs(a-c),abs(b-d))
 for i in range(s+1):g[(b+i*(d-b)//s)*m+(a+i*(c-a)//s)]+=1
print(sum(p>=2 for p in g))
