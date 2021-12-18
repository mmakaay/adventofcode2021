#!/bin/env python3

from collections import Counter


def load_recipe(path):
    with open(path) as f:
        template = next(f).strip()
        rules = {}
        for [match, insert] in [l.strip().split(" -> ") for l in f if " -> " in l]:
            rules[match] = (insert, match[0] + insert, insert + match[1])
    return template, rules


def count_pairs_in_polymer(polymer):
    return Counter([polymer[i : i + 2] for i in range(len(polymer) - 1)])


def count_elements_in_polymer(polymer):
    return Counter(polymer)


def grow_polymer(pairs, elements, rules):
    for pair, count in dict(pairs).items():
        new_element, left_pair, right_pair = rules[pair]
        pairs.subtract({pair: count})
        pairs.update({left_pair: count, right_pair: count})
        elements.update({new_element: count})


polymer, rules = load_recipe("input.txt")
pairs = count_pairs_in_polymer(polymer)
elements = count_elements_in_polymer(polymer)
for i in range(10):
    grow_polymer(pairs, elements, rules)

ordered = elements.most_common()
print(ordered[0][1] - ordered[-1][1])
