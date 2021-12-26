#!/bin/env python3
#
# This script generates valid serial numbers based on my puzzle input.
# For information on how I got to this code, see the file strategy.txt.

from itertools import product

serial = [0] * 15

p1s = [1]
p2s = [1, 2]
p3s = [8, 9]
p5s = [1, 2, 3, 4, 5, 6]
p6s = [2, 3, 4, 5, 6, 7, 8, 9]
p7s = [3, 4, 5, 6, 7, 8, 9]
p11s = [7, 8, 9]
serial_number_bases = product(p1s, p2s, p3s, p5s, p6s, p7s, p11s)

for p1, p2, p3, p5, p6, p7, p11 in serial_number_bases:
    serial[1] = p1
    serial[2] = p2
    serial[3] = p3
    serial[4] = p5 + 3
    serial[5] = p5
    serial[6] = p6
    serial[7] = p7
    serial[8] = p7 - 2
    serial[9] = p6 - 1
    serial[10] = p3 - 7
    serial[11] = p11
    serial[12] = p11 - 6
    serial[13] = p2 + 7
    serial[14] = p1 + 8
    print("".join(map(str, serial[1:])))
