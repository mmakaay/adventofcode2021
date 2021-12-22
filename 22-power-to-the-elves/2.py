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
    syntax = re.compile(f"(on|off) x={r},y={r},z={r}")
    with open(argv[1], "r") as f:
        for line in f:
            if m := syntax.match(line):
                onoff = m[1] == "on"
                x1 = min(int(m[2]), int(m[5]))
                y1 = min(int(m[3]), int(m[6]))
                z1 = min(int(m[4]), int(m[7]))
                x2 = max(int(m[2]), int(m[5]))
                y2 = max(int(m[3]), int(m[6]))
                z2 = max(int(m[4]), int(m[7]))
                steps.append((onoff, (x1, y1, z1), (x2, y2, z2)))
            else:
                print("Syntax error in: ", line)
    return steps


def boot_up(reactor, steps):
    while steps:
        steps, reactor = execute_next_step(steps, reactor)


def execute_next_step(steps, reactor):
    step, steps = steps[0], steps[1:]
    overlaps = find_overlaps(reactor, step)
    if overlaps:
        reactor = handle_overlaps(reactor, step, overlaps)
    print("Add step to reactor")
    reactor.add(step)
    return steps, reactor


def find_overlaps(reactor, step):
    return [existing for existing in reactor if overlapping(existing, step)]


def overlapping(a, b):
    _, (ax1, ay1, az1), (ax2, ay2, az2) = a
    _, (bx1, by1, bz1), (bx2, by2, bz2) = b
    if bx2 < ax1 or by2 < ay1 or bz2 < az1:
        return False
    if ax2 < bx1 or ay2 < by1 or az2 < bz1:
        return False
    return True


def handle_overlaps(reactor, step, overlaps):
    print("Handle", len(overlaps), "overlappings")
    for overlapped in overlaps:
        reactor.remove(overlapped)
        splitted = split_overlapped(overlapped, step)
        reactor.update(splitted)
    return reactor


def split_overlapped(overlapped, step):
    _, (ox1, oy1, oz1), (ox2, oy2, oz2) = overlapped
    _, (sx1, sy1, sz1), (sx2, sy2, sz2) = step

    print("Evaluate --", overlapped, step)
    if sx1 >= ox1 and sx1 <= ox2:
        print("Split low x plane")
    if sx2 >= ox1 and sx2 <= ox2:
        print("Split high x plane")
    if sy1 >= oy1 and sy1 <= oy2:
        print("Split low y plane")
    if sy2 >= oy1 and sy2 <= oy2:
        print("Split high y plane")
    if sz1 >= oz1 and sz1 <= oz2:
        print("Split low z plane")
    if sz2 >= oz1 and sz2 <= oz2:
        print("Split high z plane")

    return [overlapped]


steps = load_reboot_steps()
reactor = set()
reactor = boot_up(reactor, steps)
