#!/bin/env python3
import sys;B,V,P=0,list(open(sys.argv[1])),["","2J","H"]
for x,y in[map(int,l.split(","))for l in V if","in l]:
 for a,o in[(l[11]=="y",int(l[13:]))for l in V if"="in l]:
  x,y=[2*o-x,x][(x<o)|a],[y,2*o-y][a*y>o]
 B=max(B,y);P+=[f"{y+1};{x+1}f*"]
print("\033[".join(P+[f"{B+1};0f"]))
