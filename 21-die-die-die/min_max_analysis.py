#!/bin/env python3

import math

possible_steps_per_turn = [3,4,5,6,7,8,9]
game_starting_positions = [1,2,3,4,5,6,7,8,9,10]

games = [(pos,0) for pos in game_starting_positions]
turn = 0

def is_winning(game):
    pos, score = game
    return score >= 21

def one_turn(games):
    new_games = []
    for pos,score in games:
        for steps in possible_steps_per_turn:
            new_pos = ((pos + steps) - 1) % 10 + 1
            new_score = score + new_pos
            new_games.append((new_pos, new_score))
    return new_games

min_score = None
max_score = None

# First search for the minimum number of turns to reach 21.
while True:
    turn += 1
    min_score = min(s for _,s in games)
    games = one_turn(games)
    winners = list(filter(is_winning, games))
    if winners:
        max_score = max(s for _,s in games)
        print()
        print(f"We got the first {len(winners)} winners after {turn} turns")
        print(f"Total turns with other player included is {2*turn - 1} turns")
        print(f"Minimum score: {min_score}")
        print(f"Maximum score: {max_score}")
        break

# Continue searching for the maximum number of turns to reach 21.
while True:
    max_score = max(s for _,s in games)
    games = list(filter(lambda game: not is_winning(game), games))
    if not games:
        print()
        print(f"We got the last winners after {turn} turns")
        print(f"Total turns with other player included is {2*turn - 1} turns")
        print(f"Minimum score: {min_score}")
        print(f"Maximum score: {max_score}")
        break
    turn += 1
    games = one_turn(games)

print()

