#!/bin/env python3

from sys import argv, exit
from operator import sub
from itertools import combinations, product
from collections import Counter
from math import dist


def load_scanners():
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <filename>")
        exit(1)
    scanners = []
    with open(argv[1], "r") as f:
        for line in f:
            if "scanner" in line:
                scanner = Scanner()
                scanners.append(scanner)
            elif "," in line:
                pos = tuple(map(int, line.strip().split(",")))
                beacon = Beacon(pos)
                scanner.append(beacon)
    for scanner in scanners:
        scanner.create_fingerprints()
    return scanners


class Beacon:
    """Implements a single set of beacon coordinates for a Scanner."""

    def __init__(self, pos):
        self.pos = pos
        self.fingerprint = None

    def set_fingerprint(self, fingerprint):
        """Sets the fingerprint for this Beacon. The fingerprint is used for
        comparing this Beacon against Beacons of other Scanners, without
        having to know the relative positions of the two Scanners.
        The actual creation of the fingerprint is handled by the containing
        Scanner, because this depends on the surrounding Beacons that the
        Scanner knows about."""
        self.fingerprint = fingerprint

    def __sub__(self, other):
        """Makes it possible to subtract two Beacon objects from each other.
        Returns a tuple of x,y,z deltas."""
        x, y, z = self.pos
        x2, y2, z2 = other.pos
        return (x - x2, y - y2, z - z2)

    def transform(self, transform_func):
        """Transform the coordinates for the Beacon using the provided
        transformation function."""
        self.pos = transform_func(self.pos) 
        self.fingerprint = None

class Scanner(list):
    """Implements a list of Beacons."""

    def __init__(self):
        self.fingerprints = None

    def create_fingerprints(self):
        """Creates fingerprints for all contained Beacons."""
        for beacon in self:
            beacon.set_fingerprint(self.create_beacon_fingerprint(beacon))
        self.fingerprints = set(beacon.fingerprint for beacon in self)

    def create_beacon_fingerprint(self, beacon):
        """Creates a fingerprint for a single contained Beacon."""
        distances = sorted((dist(beacon.pos, b2.pos), b2) for b2 in self)[1:]
        closest_delta = beacon - distances[0][1]
        fingerprint = closest_delta
        return fingerprint

    def beacons_for_fingerprint(self, fingerprint):
        """Yields the Beacons for this Scanner, matching the given fingerprint."""
        return (beacon for beacon in self if beacon.fingerprint == fingerprint)

    def transform(self, transform_func):
        """Transform the coordinates for all Beacons contained by this Scanner,
        using the provided transformation function."""
        for beacon in self:
            beacon.transform(transform_func)
        self.create_fingerprints()


def make_transformations():
    """Returns a list of functions that can be used to rotate 3D coordinates
    in any possible direction. See the file 'strategy.txt' for information on
    how I got to this code."""

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


def get_pairing_candidates(scanners):
    """Returns sets of Scanners that can possible be matched with each other.
    A possible match is detected by checking how many equal fingerprints can
    be found between two sets of Beacons. We know that there must be at least
    12 matching Beacons to be able to be sure that two Scanners are next to
    each other. Therefore, here we want to find the Beacons with 12 or more
    fingerprint matches."""

    def overlapping_fingerprints(a, b):
        return (a.fingerprints & b.fingerprints, a, b)

    def nr_of_overlaps(x):
        overlap, a, b = x
        return len(overlap)

    overlaps = (overlapping_fingerprints(a, b) for a, b in combinations(scanners, 2))
    big_overlaps = filter(lambda x: nr_of_overlaps(x) >= 12, overlaps)
    candidates = sorted(big_overlaps, key=nr_of_overlaps, reverse=True)
    return candidates

def guess_shift_for_matching_two_scanners(overlap, a, b):
    dX, dY, dZ = Counter(),Counter(),Counter() 
    for fingerprint in list(overlap):
        for b1 in a.beacons_for_fingerprint(fingerprint):
            for b2 in b.beacons_for_fingerprint(fingerprint):
                xa,ya,za = b1.pos
                xb,yb,zb = b2.pos
                dX.update([xb-xa])
                dY.update([yb-ya])
                dZ.update([zb-za])
    tX = dX.most_common()[0][0]
    tY = dY.most_common()[0][0]
    tZ = dZ.most_common()[0][0]
    return lambda pos: (pos[0]+tX, pos[1]+tY, pos[2]+tZ)


scanners = load_scanners()
candidates = get_pairing_candidates(scanners)

for overlap, a, b in candidates:
    shift_it = guess_shift_for_matching_two_scanners(overlap, a, b)
    b.transform(shift_it)



# print(scanners)
# fixed = scanners.pop()
# transformations = make_transformations()

# fingerprints = list(map(fingerprint, scanners))
# for mod in apply_transformations(scanners[0], transformations):
#    scanners[0] = mod
#    fingerprints[0] = fingerprint(mod)
#    for i, j in combinations(range(len(scanners)), 2):
#        overlap = fingerprints[i].intersection(fingerprints[j])
#        if len(overlap) >= 12:
#            print(i, j, "overlap", len(overlap))
#

# stitched = scanners.pop()
# print(stitched)
# beacons = scanners[0]
# for beacons in scanners:
#    for rotated in apply_transformations(beacons, transformations):
#        print(rotated[0])
