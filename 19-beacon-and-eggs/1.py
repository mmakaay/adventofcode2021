#!/bin/env python3

from sys import argv, exit
from operator import sub
from itertools import combinations, product
from math import dist


def load_scanners():
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <filename>")
        exit(1)
    scanners = []
    with open(argv[1], "r") as f:
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
        yield lambda x, y, z: (+x, +y, +z)  # 0 degrees
        yield lambda x, y, z: (-y, +x, +z)  # 90 degrees CCW
        yield lambda x, y, z: (-x, -y, +z)  # 180 degrees
        yield lambda x, y, z: (+y, -x, +z)  # 90 degrees CW

    def rotations():
        yield lambda x, y, z: (+x, +y, +z)  # 0 degrees
        yield lambda x, y, z: (-z, +y, +x)  # 90 degrees CCW over Y
        yield lambda x, y, z: (+z, +y, -x)  # 90 degrees CW over Y
        yield lambda x, y, z: (+x, -z, +y)  # 90 degrees CCW over X
        yield lambda x, y, z: (+x, +z, -y)  # 90 degrees CW over Y
        yield lambda x, y, z: (-x, +y, -z)  # 180 degrees over Y

    def make_transformation(twist, rotate):
        return lambda pos: twist(*rotate(*pos))

    return [
        make_transformation(twist, rotate)
        for twist, rotate in product(twists(), rotations())
    ]


def apply_transformations(beacons, transformations):
    for transformation in transformations:
        yield list(map(transformation, beacons))


def fingerprint(beacons):
    return set(fingerprint_beacon(beacon, beacons) for beacon in beacons)

def fingerprint_beacon(beacon, beacons):
    o = sorted((taxi_distance(beacon, other), other) for other in beacons)
    _,other1 = o[1]
    _,other2 = o[2]
    deltas = (beacon[0]-other1[0],beacon[1]-other1[1], beacon[2]-other1[2],
              other1[0]-other2[0],other1[1]-other2[1], other1[2]-other2[2])
    return hash(deltas)

def taxi_distance(a, b):
    return sum(abs(p1 - p2) for p1, p2 in zip(a, b))


scanners = load_scanners()
fixed = scanners.pop()
transformations = make_transformations()
fingerprints = list(map(fingerprint, scanners))
for mod in apply_transformations(scanners[0], transformations):
  scanners[0] = mod
  fingerprints[0] = fingerprint(mod)
  for i,j in combinations(range(len(scanners)), 2):
    overlap = fingerprints[i].intersection(fingerprints[j])
    if overlap:
      print(i,j,"overlap",len(overlap))


#stitched = scanners.pop()
#print(stitched)
#beacons = scanners[0]
#for beacons in scanners:
#    for rotated in apply_transformations(beacons, transformations):
#        print(rotated[0])
