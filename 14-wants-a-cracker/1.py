#!/bin/env python3

from collections import deque, Counter, defaultdict

def load_recipe(path):
  with open(path) as f:
    template = next(f).strip()
    rules = defaultdict(dict)
    for [match, insert] in [l.strip().split(" -> ") for l in f if " -> " in l]:
      rules[match[0]][match[1]] = insert
  return template, rules

template, rules = load_recipe("input.txt")
string = deque(template)

for _ in range(10):
  end = len(string)
  i, insert = 0, None
  while (i < end):
    elt = string[i]
    if insert is not None:
        if elt in insert:
          string.insert(i, insert[elt])
          i += 1
          end += 1
    insert = rules[elt] if elt in rules else None
    i += 1

counter = Counter(string)
ordered = sorted(counter.items(), key=lambda x:x[1])
print(ordered[-1][1]-ordered[0][1])
