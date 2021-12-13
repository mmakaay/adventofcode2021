#!/bin/env python3

V,P=list(open("input.txt")),["","2J","H"]
E=[(l[11]=="y",int(l[13:]))for l in V if"="in l]
for x,y in[map(int,l.split(","))for l in V if","in l]:
 for a,o in E:x,y=2*o-x if a<1 and x>o else x,2*o-y if a and y>o else y
 P+=[f"{y+1};{x+1}f*"]
print("\033[".join(P+["7;0f"]))
