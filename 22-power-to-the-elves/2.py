#!/bin/env python3

from sys import argv, exit
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
                corner1 = (int(m[2]), int(m[4]), int(m[6]))
                corner2 = (int(m[3]), int(m[5]), int(m[7]))
                step = (turn_on, corner1, corner2)
                steps.append(step)
    return steps


def boot_up_reactor(steps, reactor=set()):
    if steps:
        step, remaining_steps = steps[0], steps[1:]
        overlaps = find_overlaps(reactor, step)
        reactor = handle_overlaps(reactor, step, overlaps)
        if is_turn_on_step(step):
            reactor.add(step)
        return boot_up_reactor(remaining_steps, reactor)
    else:
        return reactor


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
    if ox1 < sx1 <= ox2:
        yield (o_on, (ox1, oy1, oz1), (sx1 - 1, oy2, oz2))
        ox1 = sx1
    if oy1 < sy1 <= oy2:
        yield (o_on, (ox1, oy1, oz1), (ox2, sy1 - 1, oz2))
        oy1 = sy1
    if oz1 < sz1 <= oz2:
        yield (o_on, (ox1, oy1, oz1), (ox2, oy2, sz1 - 1))
        oz1 = sz1
    if ox1 <= sx2 < ox2:
        yield (o_on, (sx2 + 1, oy1, oz1), (ox2, oy2, oz2))
        ox2 = sx2
    if oy1 <= sy2 < oy2:
        yield (o_on, (ox1, sy2 + 1, oz1), (ox2, oy2, oz2))
        oy2 = sy2
    if oz1 <= sz2 < oz2:
        yield (o_on, (ox1, oy1, sz2 + 1), (ox2, oy2, oz2))
        oz2 = sz2


def is_turn_on_step(step):
    turn_on, _, _ = step
    return turn_on


def count_lit_cubes(reactor):
    def number_of_cubes_in(block):
        _, (x1, y1, z1), (x2, y2, z2) = block
        return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)

    return sum(map(number_of_cubes_in, reactor))


steps = load_reboot_steps()
reactor = boot_up_reactor(steps)
lit_cubes = count_lit_cubes(reactor)

print(lit_cubes)
