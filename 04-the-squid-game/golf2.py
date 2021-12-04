#!/bin/env python3
def w(board):return any(all(f<0 for f in board[i*5:i*5+5])or all(f<0 for f in board[i::5])for i in range(5))
k,*l="".join(open("input.txt")).split("\n\n")
n,b=list(map(int,k.split(","))),[list(map(int,"".join(y).split()))for y in l]
for v in n:
 for o in b:
  if v in o:o[o.index(v)]=-1
 if len(b)>1:b=[b for b in b if not w(b)]
 elif w(b[0]):break
print(sum(n for n in b[0]if n>0)*v)

