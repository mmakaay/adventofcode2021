#!/bin/env python3

OPENERS = "([{<"
CLOSERS = ")]}>"
SCORES  = [3, 57, 1197, 25137]


def load_program(path):
 with open(path, "r") as f:
   return list(map(str.strip, f))

def is_opener(char):
  return char in OPENERS


def closer_for(char):
  return CLOSERS[OPENERS.index(char)]


def find_error_in_line(line):
  stack = []
  for char in line:
    if is_opener(char):
      stack.append(closer_for(char))
    else:
      if not stack:
        return char
      expected_char = stack.pop()
      if expected_char != char:
        return char
  return None


def find_errors_in_program(program):
  return map(find_error_in_line, program)


def score_for_error(error):
    return SCORES[CLOSERS.index(error)] if error is not None else 0


def compute_score_for_errors(errors):
  return sum(map(score_for_error, errors))


program = load_program("input.txt")
errors = find_errors_in_program(program)
score = compute_score_for_errors(errors)

print(score)  
