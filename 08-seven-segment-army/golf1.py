#!/bin/env python3
print(sum(x<5 or x>6for o in[map(len,l.split("|")[1].split())for l in open("input.txt")]for x in o))
