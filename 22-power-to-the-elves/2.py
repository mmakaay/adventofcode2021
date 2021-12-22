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
                turn_on = m[1] == "on"
                x1 = min(int(m[2]), int(m[3]))
                y1 = min(int(m[4]), int(m[5]))
                z1 = min(int(m[6]), int(m[7]))
                x2 = max(int(m[2]), int(m[3]))
                y2 = max(int(m[4]), int(m[5]))
                z2 = max(int(m[6]), int(m[7]))
                step = (turn_on, (x1, y1, z1), (x2, y2, z2))
                steps.append(step)
            else:
                print("Syntax error in: ", line)
    return steps


def boot_up(reactor, steps):
    while steps:
        steps, reactor = execute_next_step(steps, reactor)
    return reactor


def execute_next_step(steps, reactor):
    step, steps = steps[0], steps[1:]
    overlaps = find_overlaps(reactor, step)
    if overlaps:
        reactor = handle_overlaps(reactor, step, overlaps)
    turn_on, _, _ = step
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
    for overlapped in overlaps:
        reactor.remove(overlapped)
        splitted = split_overlapped(overlapped, step)
        reactor.update(splitted)
    return reactor


def split_overlapped(overlapped, step):
    o_on, (ox1, oy1, oz1), (ox2, oy2, oz2) = overlapped
    s_on, (sx1, sy1, sz1), (sx2, sy2, sz2) = step
    #print("Process overlapped ",overlapped)
    if ox1 < sx1 <= ox2:
        #print("input x 1", ((ox1, oy1, oz1), (ox2, oy2, oz2)))
        #print("step", step)
        keep = (o_on, (ox1, oy1, oz1), (sx1-1, oy2, oz2))
        ox1 = sx1
        yield keep
        #print("keep x 1 @", sx1, "=", keep)
        #print("remaining", ((ox1, oy1, oz1), (ox2, oy2, oz2)))
        #print()
    if ox1 <= sx2 < ox2:
        #print("input x 2", ((ox1, oy1, oz1), (ox2, oy2, oz2)))
        #print("step", step)
        keep = (o_on, (sx2+1, oy1, oz1), (ox2, oy2, oz2))
        ox2 = sx2
        yield keep
        #print("keep x 2 @", sx2, "=", keep)
        #print("remaining", ((ox1, oy1, oz1), (ox2, oy2, oz2)))
        #print()
    if oy1 < sy1 <= oy2:
        #print("input y 1", ((ox1, oy1, oz1), (ox2, oy2, oz2)))
        #print("step", step)
        keep = (o_on, (ox1, oy1, oz1), (ox2, sy1-1, oz2))
        yield keep
        oy1 = sy1
        #print("keep y 1 @", sy1, "=", keep)
        #print("remaining", ((ox1, oy1, oz1), (ox2, oy2, oz2)))
        #print()

    if oy1 <= sy2 < oy2:
        #print("input y 2", ((ox1, oy1, oz1), (ox2, oy2, oz2)))
        #print("step", step)
        keep = (o_on, (ox1, sy2+1, oz1), (ox2, oy2, oz2))
        yield keep
        oy2 = sy2
        #print("keep y 2 @", sy2, "=", keep)
        #print("remaining", ((ox1, oy1, oz1), (ox2, oy2, oz2)))
        #print()

    if oz1 < sz1 <= oz2:
        #print("input z 1", ((ox1, oy1, oz1), (ox2, oy2, oz2)))
        #print("step", step)
        keep = (o_on, (ox1, oy1, oz1), (oy1, oy2, sz2-1))
        yield keep
        oz1 = sz1
        #print("keep z 1 @", sz1, "=", keep)
        #print("remaining", ((ox1, oy1, oz1), (ox2, oy2, oz2)))
        #print()

    if oz1 <= sz2 < oz2:
        #print("input z 2", ((ox1, oy1, oz1), (ox2, oy2, oz2)))
        #print("step", step)
        keep = (o_on, (ox1, oy1, sz2+1), (ox2, oy2, oz2))
        oz2 = sz2
        yield keep
        #print("keep z 2 @", sz2, "=", keep)
        #print("remaining", ((ox1, oy1, oz1), (ox2, oy2, oz2)))
        #print()

def count_on(reactor):
    total = 0
    for turn_on, (x1,y1,z1), (x2,y2,z2) in reactor:
        if turn_on:
            subtotal = ((x2-x1+1) *(y2-y1+1) * (z2-z1+1))
            print("Sum up", ((x1,y1,z1), (x2,y2,z2)), "=", subtotal)
            total+= subtotal
    return total

steps = load_reboot_steps()
reactor = set()
reactor = boot_up(reactor, steps)
print(count_on(reactor))
#print("Must be 0:", count_on(reactor) - 2758514936282235)

