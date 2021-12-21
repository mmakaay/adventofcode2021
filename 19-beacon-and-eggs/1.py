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

twist_0 = lambda x, y, z: (x, y, z)
twist_90 = lambda x, y, z: (-y, x, z)
twist_180 = lambda x, y, z: (-x, -y, z)
twist_270 = lambda x, y, z: (y, -x, z)
twists = [twist_0, twist_90, twist_180, twist_270]

rot_0 = lambda x, y, z: (x, y, z)
rot_90Yccw = lambda x, y, z: (-z, y, x)
rot_90Ycw = lambda x, y, z: (z, y, -x)
rot_90Xccw = lambda x, y, z: (x, -z, y)
rot_90Xcw = lambda x, y, z: (x, z, -y)
rot_180 = lambda x, y, z: (-x, y, -z)
rotations = [rot_0, rot_90Yccw, rot_90Ycw, rot_90Xccw, rot_90Xcw, rot_180]

def make_transformation(twist, rotate):
    return lambda pos: twist(*rotate(*pos))

transformations = [
    make_transformation(twist, rotate)
    for twist, rotate in product(twists, rotations)
]

def generate_transformations(beacons):
    for transform in transformations:
        yield list(map(transform, beacons))

def taxi_distance(a, b):
    return sum(abs(p1-p2) for p1,p2 in zip(a,b))


#def fingerprint(beacons, depth):
#    fingerprints = set()
#    for beacon in beacons:
#        o = sorted(taxi_distance(beacon, other) for other in beacons)
#        fingerprints.add((tuple(o[0:depth]), beacon))
#    return fingerprints
#        
    #beacon_distances = [(beacon, taxi_distance((0,0,0),beacon)) for beacon in beacons]
    #beacons_by_distance = [beacon for beacon,_ in sorted(beacon_distances, key=lambda x:x[1])]
    #fingerprints = set()
#
#    for i in range(len(beacons)-1):
#        pair = beacons[i:i+2]
#        fingerprints.add(taxi_distance(*pair))
#    return fingerprints


if len(argv) != 2:
    print(f"Usage: {argv[0]} <filename>")
    exit(1)

scanners = load_scanners(argv[1])
stitched = scanners.pop()
beacons = scanners[0]
for beacons in scanners:
    for rotated in generate_transformations(beacons):
        print(rotated[0])
   

