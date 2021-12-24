#!/bin/env python3

import re
from sys import argv, exit
from itertools import combinations
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
    """Implements a Beacon that can be contained by a Scanner."""

    def __init__(self, pos):
        self.orig_pos = pos
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
        Returns a tuple of (x,y,z) deltas for the Beacon positions."""
        return tuple(p1 - p2 for p1, p2 in zip(self.pos, other.pos))

    def __eq__(self, other):
        """Returns True when this Beacon has the same coordinates as the other Beacon."""
        return self.pos == other.pos

    def transform(self, transform_func):
        """Transform the coordinates for the Beacon using the provided
        transformation function."""
        self.pos = transform_func(self.pos)

    def reset(self):
        """Reset the coordinates for the Beacon to the initial state,
        from before any transformations."""
        self.pos = self.orig_pos


class Scanner:
    """Implement a Scanner that contains a set of Beacons."""

    def __init__(self, name):
        self.pos = (0, 0, 0)
        self.orig_pos = (0, 0, 0)
        self.name = name
        self.beacons = []
        self.fingerprints = None

    def add_beacon(self, beacon):
        self.beacons.append(beacon)

    def __str__(self):
        return f"<{self.name}>"

    def __repr__(self):
        return self.__str__()

    def create_fingerprints(self):
        """Creates fingerprints for all contained Beacons."""
        for beacon in self.beacons:
            beacon.set_fingerprint(self.create_beacon_fingerprint(beacon))
        self.fingerprints = set(beacon.fingerprint for beacon in self.beacons)

    def create_beacon_fingerprint(self, beacon):
        """Creates a orientation-agnostic fingerprint for a single Beacon."""
        distances = sorted(self.beacons, key=lambda b2: dist(beacon.pos, b2.pos))
        d1 = tuple(sorted(map(lambda x: abs(x), distances[1] - beacon)))
        d2 = tuple(sorted(map(lambda x: abs(x), distances[2] - beacon)))
        return (d1, d2)

    def beacons_for_fingerprint(self, fingerprint):
        """Looks up the Beacons for this Scanner, matching the given fingerprint."""
        return (beacon for beacon in self.beacons if beacon.fingerprint == fingerprint)

    def transform(self, transform_func):
        """Transform the coordinates for this Scanner and for all Beacons contained
        by this Scanner, using the provided transformation function."""
        self.pos = transform_func(self.pos)
        for beacon in self.beacons:
            beacon.transform(transform_func)

    def reset(self):
        """Resets the coordinates for this Scanner and for all Beacons contained
        by this Scanner."""
        self.pos = self.orig_pos
        for beacon in self.beacons:
            beacon.reset()


def get_reorientation_transformations():
    """Returns a list of functions that can be used to rotate 3D coordinates
    into any possible direction. See the file 'strategy.txt' for information on
    how I got to this piece of code."""
    return [
        lambda pos: (+pos[0], +pos[1], +pos[2]),
        lambda pos: (-pos[1], +pos[0], +pos[2]),
        lambda pos: (-pos[0], -pos[1], +pos[2]),
        lambda pos: (+pos[1], -pos[0], +pos[2]),
        lambda pos: (-pos[2], +pos[1], +pos[0]),
        lambda pos: (-pos[1], -pos[2], +pos[0]),
        lambda pos: (+pos[2], -pos[1], +pos[0]),
        lambda pos: (+pos[1], +pos[2], +pos[0]),
        lambda pos: (+pos[2], +pos[1], -pos[0]),
        lambda pos: (-pos[1], +pos[2], -pos[0]),
        lambda pos: (-pos[2], -pos[1], -pos[0]),
        lambda pos: (+pos[1], -pos[2], -pos[0]),
        lambda pos: (+pos[0], -pos[2], +pos[1]),
        lambda pos: (+pos[2], +pos[0], +pos[1]),
        lambda pos: (-pos[0], +pos[2], +pos[1]),
        lambda pos: (-pos[2], -pos[0], +pos[1]),
        lambda pos: (+pos[0], +pos[2], -pos[1]),
        lambda pos: (-pos[2], +pos[0], -pos[1]),
        lambda pos: (-pos[0], -pos[2], -pos[1]),
        lambda pos: (+pos[2], -pos[0], -pos[1]),
        lambda pos: (-pos[0], +pos[1], -pos[2]),
        lambda pos: (-pos[1], -pos[0], -pos[2]),
        lambda pos: (+pos[0], -pos[1], -pos[2]),
        lambda pos: (+pos[1], +pos[0], -pos[2]),
    ]


def find_scanner_shift(overlap, a, b):
    """Assuming that two scanners are oriented in the same direction,
    check if a shift transformation exists that lets at least 12 Beacons
    of the two scanners end up in the same end position."""
    if not overlap:
        return None
    shifts = Counter()
    for fingerprint in overlap:
        for ba in a.beacons_for_fingerprint(fingerprint):
            for bb in b.beacons_for_fingerprint(fingerprint):
                delta = bb - ba
                shifts.update([delta])
                if len(shifts) > 1:
                    return None
    s, c = shifts.popitem()
    if c >= 12:
        return lambda pos: (pos[0] + s[0], pos[1] + s[1], pos[2] + s[2])
    return None


def align(scanners):
    """Align the provided list of Scanners. This will transform the coordinates
    of the Scanners and their Beacons in such way, that the Beacons that are seen
    by two or more Scanners end up at the same coordinates."""
    possible_alignments = make_alignment_candidates(scanners)
    start = pick_start_scanner(possible_alignments)
    unaligned = set(scanners) ^ {start}
    unaligned = alignment_step(possible_alignments, unaligned)

    if unaligned:
        print("Alignment failed for scanner(s):")
        print("> " + "\n> ".join(map(str, unaligned)))
        exit(1)


def make_alignment_candidates(scanners):
    """Returns pairs of Scanners, ordered by the likeliness that they can be
    aligned with each other. The is determined by checking how many fingerprint
    overlaps can be found between the two related sets of Beacons."""

    def matching_fingerprints(pair):
        a, b = pair
        return (a.fingerprints & b.fingerprints, a, b)

    def by_number_of_overlaps(pair):
        matching, a, b = pair
        return len(matching)

    combis = combinations(scanners, 2)
    pairs = map(matching_fingerprints, combis)
    pairs = sorted(pairs, key=by_number_of_overlaps, reverse=True)
    return pairs


def pick_start_scanner(possible_alignments):
    """Pick the Scanner that looks like it might have the most neighbours as the
    starting point for alignment. Being the starting point means that the coordinate
    system for start Beacon will be fixated, serving as the reference coordinate
    system that all other Sensors must be aligned to."""
    connections = Counter()
    for overlap, a, b in possible_alignments:
        l = len(overlap)
        connections.update({a: l, b: l})
    start, _ = connections.most_common()[0]
    return start


def alignment_step(possible_alignments, unaligned):
    """Find the next Sensor that can be aligned with an already aligned Sensor."""
    for overlap, a, b in prepare_pairs(possible_alignments, unaligned):
        for reorient_scanner in get_reorientation_transformations():
            a.reset()
            a.transform(reorient_scanner)
            if shift_scanner := find_scanner_shift(overlap, a, b):
                a.transform(shift_scanner)
                unaligned.remove(a)
                return alignment_step(possible_alignments, unaligned)
    return unaligned


def prepare_pairs(possible_alignments, unaligned):
    """Filter and order the pairs in such way that aligning two scanners will
    only be done from an unaligned to an already aligned one. If both scanners
    are already aligned, or both are unaligned, then no alignment will be
    performed with them (yet)."""
    for overlap, a, b in possible_alignments:
        if a in unaligned and b not in unaligned:
            yield overlap, a, b
        elif b in unaligned and a not in unaligned:
            yield overlap, b, a


def get_unique_beacons(scanners):
    unique_beacons = set()
    for scanner in scanners:
        unique_beacons.update(beacon.pos for beacon in scanner.beacons)
    return unique_beacons


def get_max_scanner_distance(scanners):
    def taxi_distance(pair):
        a, b = pair
        return sum(abs(p1 - p2) for p1, p2 in zip(a.pos, b.pos))

    return max(map(taxi_distance, combinations(scanners, 2)))


scanners = load_scanners()
align(scanners)
unique_beacons = get_unique_beacons(scanners)
max_scanner_distance = get_max_scanner_distance(scanners)


print("Number of beacons:", len(unique_beacons))
print("Maximum sensor distance:", max_scanner_distance)
