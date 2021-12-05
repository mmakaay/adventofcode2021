#!/usr/bin/env python3.10
d=list(map(int,open("input.txt")))
s=[sum(d[i:i+3])for i in range(len(d)-2)]
print(sum(b-a>0 for a,b in zip([s[0]]+s,s)))
