#!/bin/env python3

from sys import argv, exit
from collections import defaultdict
import re


def load_reboot_steps():
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <filename>")
        exit(1)

    steps = []
    r = r"(-?\d+)\.\.(-?\d+)"
    syntax = re.compile(f'(on|off) x={r},y={r},z={r}')
    with open(argv[1], "r") as f:
        for line in f:
            if m := syntax.match(line):
                steps.append(list(
                    (m[1] == "on", x,y,z)
                    for x in range(max(-50, int(m[2])), min(50,int(m[3]))+1)
                    for y in range(max(-50, int(m[4])), min(50,int(m[5]))+1)
                    for z in range(max(-50, int(m[6])), min(50,int(m[7]))+1)
                ))
            else:
                print("Syntax error in: ", line)
    return steps


steps = load_reboot_steps()
reactor = defaultdict(lambda: defaultdict(lambda: defaultdict(bool)))

for step in steps:
    for onoff, x, y, z in step:
        if -50<=x<=50 and -50<=y<=50 and -50<=z<=50:
            reactor[x][y][z] = onoff

print(sum(onoff for x in reactor.keys() for y in reactor[x].keys() for onoff in reactor[x][y].values()))
