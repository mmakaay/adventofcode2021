#!/bin/env python3
import re
q=list(map(int,re.split(',| -> |\n',"".join(open("input.txt")).strip())))
m,n=max(q[0::2])+1,max(q[1::2])+1
g,c=[0]*m*n,[q[i:i+4]for i in range(0,len(q),4)]
for a,b,c,d in c:
 if a==c or b==d:
  s=max(abs(a-c),abs(b-d))
  d,e=(c-a)//s,(d-b)//s
  for i in range(s+1):g[(b+i*e)*m+(a+i*d)]+=1
print(sum(p>=2 for p in g))
