#!/bin/env python3

from functools import reduce


OPENERS = "([{<"
CLOSERS = ")]}>"
SCORES = [1, 2, 3, 4]

OK = 0
CORRUPT = 1
INCOMPLETE = 2


def load_program(path):
    with open(path, "r") as f:
        return list(map(str.strip, f))


def is_opener(char):
    return char in OPENERS


def closer_for(char):
    return CLOSERS[OPENERS.index(char)]


def preprocess_line(line):
    stack = []
    for char in line:
        if is_opener(char):
            stack.append(closer_for(char))
        else:
            if not stack:
                return line, CORRUPT, char
            expected_char = stack.pop()
            if expected_char != char:
                return line, CORRUPT, char
    return line, INCOMPLETE if stack else OK, list(reversed(stack))


def remove_corrupted_lines(preprocessed):
    is_not_corrupted = lambda p: p[1] != CORRUPT
    return filter(is_not_corrupted, preprocessed)


def autocomplete_incomplete_lines(preprocessed):
    for line, state, missing_closers in preprocessed:
        yield line + "".join(missing_closers), missing_closers


def score_for_autocomplete(autocomplete):
    _, missing_closers = autocomplete

    def score(score, closer):
        return score * 5 + SCORES[CLOSERS.index(closer)]

    return reduce(score, missing_closers, 0)


def compute_score_for_autocompleted(autocompleted):
    scores = list(sorted(map(score_for_autocomplete, autocompleted)))
    middle_score = scores[(len(scores) - 1) // 2]
    return middle_score


program = load_program("input.txt")
preprocessed = list(map(preprocess_line, program))
decorruptified = remove_corrupted_lines(preprocessed)
autocompleted = autocomplete_incomplete_lines(decorruptified)
score = compute_score_for_autocompleted(autocompleted)

print(score)
