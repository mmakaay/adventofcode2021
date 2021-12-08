#!/bin/env python3
#
# Not the most optimal algorithm, but it was fun writing it this way.

from itertools import permutations

DIGITS = [
  "abcefg",
  "cf",
  "acdeg",
  "acdfg",
  "bcdf",  
  "abdfg",
  "abdefg",
  "acf",
  "abcdefg",
  "abcdfg"
]
LENGHTS = [len(x) for x in DIGITS]
UNIQUE = [x for x in LENGHTS if LENGHTS.count(x) == 1]


def read_data(path):
  with open(path, "r") as f:
    return [[x.split() for x in line.split("|")] for line in f]
       

def digits_with_same_length(pattern):
  return [x for x in DIGITS if len(x) == len(pattern)]


def sort_patterns(patterns):
  """Sort the patterns for an optimal route through the algorithm.
     The patterns that have a unique amount of segments are moved
     to the start of the list, to cut down the number of recursion
     routes as much as possible."""
  def sort_key(pattern):
    return (len(pattern) in UNIQUE, len(pattern))
  return sorted(patterns, key=sort_key, reverse=True)


def generate_rewiring_options(pattern, option, rewiring):
  new_in_pattern = "".join(x for x in pattern if x not in rewiring.keys())
  new_in_option = "".join(x for x in option if x not in rewiring.values())
  for option_permutation in permutations(new_in_option):
    new_rewiring = rewiring
    for i,p in enumerate(new_in_pattern):
      new_rewiring[p] = option_permutation[i]
    yield new_rewiring


def build_rewirer(rewiring):
  translation = str.maketrans(rewiring)
  def rewire_(pattern):
    rewired = pattern.translate(translation)
    return "".join(sorted(rewired))
  return rewire_


def is_valid_rewiring(rewired):
  return rewired in DIGITS


def find_required_rewiring_recurse(patterns, idx, rewiring):
  pattern = patterns[idx]
  for option in digits_with_same_length(pattern):
    for rewiring in generate_rewiring_options(pattern, option, rewiring):
      rewire = build_rewirer(rewiring) 
      if is_valid_rewiring(rewire(pattern)):
        if idx == len(patterns)-1:
          return rewire
        result = find_required_rewiring_recurse(patterns, idx+1, rewiring)
        if result:
          return result
  

def find_required_rewiring(patterns):
  patterns = sort_patterns(patterns)
  result = find_required_rewiring_recurse(patterns, 0, {})
  return result


def render_display(rewire, display):
  descrambled = [rewire(scrambled) for scrambled in display]
  digits = [DIGITS.index(rewire(scrambled)) for scrambled in display]
  return "".join(map(str, digits))


sum = 0
for patterns, display in read_data("input.txt"):
  rewire = find_required_rewiring(patterns)
  rendered = render_display(rewire, display)
  sum += int(rendered)

print(sum)
