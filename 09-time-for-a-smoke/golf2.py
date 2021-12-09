#!/bin/env python3
M,E,H=map,len,range;G=[list(M(int,line.strip()))for line in open("input.txt")];w,o=E(G[0]),E(G)
def W(J,E,M,I,G):return(J[G][I]<9)*(J[G][I]>J[M][E])
def O(M,G):return[(M,G-1)]*(G>0)+[(M-1,G)]*(M>0)+[(M+1,G)]*(M<w-1)+[(M,G+1)]*(G<o-1)
def T(B,A,H):H.add(A);[T(B,n,H)for n in O(*A)if W(B,*A,*n)];return H
b=(T(G,H,set())for H in((a,b)for b in H(o)for a in H(w)if all(G[y][x]>G[b][a]for x,y in O(a,b))))
q=sorted(b,key=E,reverse=1);print(E(q[0])*E(q[1])*E(q[2]))
