#!/bin/env python3

import re
from alu import *
from sys import argv, exit


def load_program():
    with open("serial_checksum.alu", "r") as f:
        src = list(f)
    return ALUCompiler().compile(src)


def get_serial_to_check():
    serial = argv[1]
    if not re.match(r"^[1-9]{14}$", serial):
        print("Malformed serial number!")
        exit(2)
    return list(map(int, serial))

    
if len(argv) != 2:
    print(f"Usage: {argv[0]} <serial>")
    exit(1)

serial = get_serial_to_check()
checksum_computer = load_program()
_, _, _, checksum = checksum_computer.run(*serial)

if checksum == 0:
    print("Valid serial number")
    exit(0)
else:
    print("Invalid serial number")
    exit(3)

