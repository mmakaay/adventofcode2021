#!/bin/env python3

from sys import argv, exit
from operator import sub
from itertools import combinations,product


def load_scanners(path):
    scanners = []
    scanner = None
    with open(path) as f:
        for line in f:
            if "scanner" in line:
                scanner = []
                scanners.append(scanner)
            elif "," in line:
                beacon = tuple(map(int, line.strip().split(",")))
                scanner.append(beacon)
    return scanners            


def make_transformations():
    def twists():
        yield lambda x, y, z: (x, y, z)
        yield lambda x, y, z: (-y, x, z)
        yield lambda x, y, z: (-x, -y, z)
        yield lambda x, y, z: (y, -x, z)
    def rotations():
        yield lambda x, y, z: (x, y, z)
        yield lambda x, y, z: (-z, y, x)
        yield lambda x, y, z: (z, y, -x)
        yield lambda x, y, z: (x, -z, y)
        yield lambda x, y, z: (x, z, -y)
        yield lambda x, y, z: (-x, y, -z)
    def make_transformation(twist, rotate):
        return lambda pos: twist(*rotate(*pos))
    return [
        make_transformation(twist, rotate)
        for twist, rotate in product(twists(), rotations())
    ]


def apply_transformations(beacons, transformations):
    for transformation in transformations:
        yield list(map(transformation, beacons))


def taxi_distance(a, b):
    return sum(abs(p1-p2) for p1,p2 in zip(a,b))


if len(argv) != 2:
    print(f"Usage: {argv[0]} <filename>")
    exit(1)

scanners = load_scanners(argv[1])
stitched = scanners.pop()
beacons = scanners[0]
transformations = make_transformations()
for beacons in scanners:
    for rotated in apply_transformations(beacons, transformations):
        print(rotated[0])
   

