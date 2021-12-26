#!/bin/env python3

from alu import *
from sys import argv, exit
from itertools import combinations_with_replacement


def load_program():
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <filename>")
        exit(1)
    with open(argv[1], "r") as f:
        return list(f)


src = load_program()

digit_src = []
lines = None
for line in src:
    if "inp" in line:
        lines = ["inp w", "inp x", "inp y", "inp z"]
        digit_src.append(lines)
    else:
        lines.append(line.strip())

possible_input = set([(0,0,0)])
for i,src in enumerate(digit_src):
    if i < 13:
        continue
    print("-------- digit",i, "----------")
    print("\n".join(src))
    program = ALUCompiler().compile(src)
    for input_vars in list(possible_input):
        possible_input = set()
        for w in range(10):
            W,X,Y,Z = program.run(w, *input_vars)
            possible_input.add((X,Y,Z))
            print("input=", input_vars, "w=",w,"OUT=",W,X,Y,Z)
        print("Next possible input:", possible_input)

