#!/bin/env python3
def s(x,y):return[]+[(x,y-1)]*(y>0)+[(x-1,y)]*(x>0)+[(x+1,y)]*(x<w-1)+[(x,y+1)]*(y<h-1)
g=[list(map(int,line.strip()))for line in open("input.txt")];w,h=len(g[0]),len(g)
print(sum(g[b][a]+1 for b in range(h)for a in range(w)if all(g[y][x]>g[b][a]for x,y in s(a,b))))
