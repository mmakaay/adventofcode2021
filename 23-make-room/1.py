#!/bin/env python3

from sys import argv, exit
import re

# Amphipod types.
A = 0
B = 1
C = 2
D = 3

# Energy use of amphipods.
ENERGY = { A: 1, B: 10, C: 100, D: 1000 } 

# The number of positions in a room
ROOM_SIZE=4

def load_burrow():
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <filename>")
        exit(1)

    hallway = [None] * 11
    rooms = [[], [], [], []]

    amphipods = re.compile("([ABCD])")
    with open(argv[1], "r") as f:
        for line in f:
            if m := amphipods.findall(line):
                for i, a in enumerate(m):
                    # Align amphipod types A,B,C,D with their room id's.
                    # "A" => 0, "B" => 1, etc.
                    # This makes it easy to see if an amphipod is in
                    # its own room.
                    rooms[i].append(ord(a)-ord('A'))

    burrow = (hallway, rooms)
    return burrow


i = 0; # TMP
def find_solution_with_least_energy(burrow, least_energy = 0):
    global i # TMP
    if (i:=i+1) > 10: # TMP
        print("Going too deep (temp for dev)") # TMP
        return None # TMP
    if all_are_home(burrow):
        return least_energy
    for move, new_burrow in possible_moves(burrow):
        find_solution_with_least_energy(new_burrow, least_energy)


def possible_moves(burrow):
    hallway, rooms = burrow
    yield from possible_moves_from_room_to_hallway(burrow)


def possible_moves_from_room_to_hallway(burrow):
    hallway, rooms = burrow 
    for room_nr, room in enumerate(rooms):
        if move_pos := movable_amphipod_from_room(room, room_nr):
            print(room_nr, room, move_pos)
            yield (), burrow
        
       
def movable_amphipod_from_room(room, room_nr):
    occupation_level = room_occupation_level(room)

    # Not occupied? Then we can't do anything.
    if occupation_level == 0:
        return

    if occupation_level == 1:
        # When the single amphipod belongs in this room, it won't budge.
        if room[BOTTOM] == room_nr:
            return
        else:
            return BOTTOM

    if occupation_level == 2:
        # Are both positions in the room already taken by the amphipods
        # that live here? Then these won't be moved anymore.
        if room[TOP] == room_nr and room[BOTTOM] == room_nr:
            return

        # When the top amphipod is in the wrong room, then it must be moved.
        # Also, when the bottom amphipod is in the wrong room, then the top
        # one must be moved to free the bottom one. So conclusion is:
        # the top amphipod must move.
        return TOP


def room_occupation_level(room):
    return sum(pos is not None for pos in room)
   

def all_are_home(burrow):
    hallway, rooms = burrow
    return rooms == [[0, 0],[1, 1],[2, 2],[3,3]]


def dump(burrow):
    hallway, rooms = burrow
    def render(x):
        return " " if x is None else str(x)
    flipped = list(zip(*rooms))
    print(".-----------.")
    print("|" + "".join(map(render, hallway)) + "|")
    print("'-." + "|".join(map(render, flipped[0])) + ".-'")
    print("  |" + "|".join(map(render, flipped[1])) + "|  ")
    print("  `-+-+-+-'")


burrow = load_burrow()
dump(burrow)
least_energy = find_solution_with_least_energy(burrow)

print(least_energy)
