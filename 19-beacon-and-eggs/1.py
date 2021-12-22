#!/bin/env python3

import re
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
                groups = re.match("-+\s+(scanner \d+)\s+-+", line)
                scanner = Scanner(groups[1])
                scanners.append(scanner)
            elif "," in line:
                pos = tuple(map(int, line.strip().split(",")))
                beacon = Beacon(pos)
                scanner.add_beacon(beacon)
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

    def __eq__(self, other):
        """Returns True when this Beacon has the same coordinates as the other Beacon."""
        return self.pos == other.pos

    def transform(self, transform_func):
        """Transform the coordinates for the Beacon using the provided
        transformation function."""
        self.pos = transform_func(self.pos) 
        self.fingerprint = None

class Scanner:
    """Implements a list of Beacons."""

    def __init__(self, name):
        self.name = name
        self.beacons = []
        self.fingerprints = None
        self.matched_up_with = set()
        self.transformations = make_transformations()
       
    def add_beacon(self, beacon):
        self.beacons.append(beacon)

    def __str__(self):
        return f"<{self.name}>"

    def __repr__(self):
        return self.__str__()

    def __and__(self, other):
        """Returns the Beacons that also exist in the other Scanner."""
        return [b1 for b1 in self.beacons for b2 in other.beacons if b1 == b2]

    def create_fingerprints(self):
        """Creates fingerprints for all contained Beacons."""
        for beacon in self.beacons:
            beacon.set_fingerprint(self.create_beacon_fingerprint(beacon))
        self.fingerprints = set(beacon.fingerprint for beacon in self.beacons)

    def create_beacon_fingerprint(self, beacon):
        """Creates a fingerprint for a single contained Beacon."""
        distances = sorted((dist(beacon.pos, b2.pos), b2) for b2 in self.beacons)[1:]
        closest_delta = beacon - distances[0][1]
        fingerprint = closest_delta
        return fingerprint

    def beacons_for_fingerprint(self, fingerprint):
        """Yields the Beacons for this Scanner, matching the given fingerprint."""
        return (beacon for beacon in self.beacons if beacon.fingerprint == fingerprint)

    def transform(self, transform_func):
        """Transform the coordinates for all Beacons contained by this Scanner,
        using the provided transformation function."""
        for beacon in self.beacons:
            beacon.transform(transform_func)
        self.create_fingerprints()

    def match_up_with(self, other):
        """Returns True when the Beacons from this Scanner match up with the
        Beacons from the other Scanner. Also keeps track of the two Scanners
        matching.
        Scanners match up if they have at least 12 matching Beacons in the
        same coordinate reference system."""
        if matched_up := len(self & other) >= 12:
            self.matched_up_with.add(other)
            other.matched_up_with.add(self)
        return matched_up

    def is_matched_up_with(self, other):
        return self in other.matched_up_with

    def has_match(self):
        return bool(self.matched_up_with)

    def can_reorientate(self):
        return self.transformations and not self.matched_up_with

    def reorientate(self):
        reorientate, self.transformations = self.transformations[0], self.transformations[1:]
        self.transform(reorientate)


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

    def enough_overlaps(x):
        overlap, a, b = x
        print("overlap",a,b,"=",len(overlap))
        return len(overlap) >= 12

    def only_new_matches(x):
        _, a, b = x
        return not a.is_matched_up_with(b)

    def only_append_to_already_matched(x):
        _, a, b = x
        return (
            all(not s.has_match() for s in scanners) or
            a.has_match() or b.has_match()
        )

    candidates = (overlapping_fingerprints(a, b) for a, b in combinations(scanners, 2))
    candidates = filter(enough_overlaps, candidates)
    candidates = filter(only_new_matches, candidates)
    candidates = filter(only_append_to_already_matched, candidates)
    return candidates

def unmatched_scanners(scanners):
    return [s for s in scanners if not s.matched_up_with]

def guess_shift_for_matching_two_scanners(overlap, a, b):
    dX, dY, dZ = Counter(),Counter(),Counter() 
    for fingerprint in list(overlap):
        for b1 in a.beacons_for_fingerprint(fingerprint):
            for b2 in b.beacons_for_fingerprint(fingerprint):
                xa,ya,za = b1.pos
                xb,yb,zb = b2.pos
                dX.update([xa-xb])
                dY.update([ya-yb])
                dZ.update([za-zb])
    tX = dX.most_common()[0][0]
    tY = dY.most_common()[0][0]
    tZ = dZ.most_common()[0][0]
    return lambda pos: (pos[0]+tX, pos[1]+tY, pos[2]+tZ)

def pair(scanners):
    # Check for possible matches in current orientation.
    for overlap, a, b in get_pairing_candidates(scanners):
        print("Check",a,b)
        shift_it = guess_shift_for_matching_two_scanners(overlap, a, b)
        b.transform(shift_it)
        if (a.match_up_with(b)):
            print("Paired",a,"to",b)
            return pair(scanners)
    # No matches found. If transformations are still available, try those.
    for scanner in unmatched_scanners(scanners):
        if scanner.can_reorientate():
            print("Reorientate",scanner)
            scanner.reorientate()
            return pair(scanners)
    return False


scanners = load_scanners()
pair(scanners)
print("--restart--")
for s in scanners: s.transformations = make_transformations()
pair(scanners)
print("Unmatched:", unmatched_scanners(scanners))


