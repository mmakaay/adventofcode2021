#!/bin/env python3

from sys import argv, exit


def load_starting_positions(path):
    with open(path) as f:
        return tuple(int(line.split(": ")[1]) for line in f)


def turn_throw_generator():
    turn = 0
    previous_scores = 0
    while True:
        turn += 1
        score = (turn * 3 * (turn * 3 + 1) // 2 - previous_scores) % 100
        previous_scores += score
        yield turn, score


def play(game, throw):
    start1, start2 = game
    player1 = (0, start1)
    player2 = (0, start2)
    players = (player1, player2)

    while not game_over(players):
        players, turn = one_turn(players, throw)
    return verdict(players, turn)


def one_turn(players, throw):
    player1, player2 = players
    turn, player1 = progress_player(player1, throw)
    return (player2, player1), turn


def progress_player(player, throw):
    score, pos = player
    turn, points = next(throw)
    new_pos = 1 + ((pos + points) - 1) % 10
    return turn, (score + new_pos, new_pos)


def game_over(players):
    player1, player2 = players
    score1, _ = player1
    score2, _ = player2
    return score1 >= 1000 or score2 >= 1000


def verdict(players, turn):
    player1, player2 = players
    score1, _ = player1
    score2, _ = player2
    winner = max(score1, score2)
    loser = min(score1, score2)
    return winner, loser, turn


if len(argv) != 2:
    print(f"Usage: {argv[0]} <filename>")
    exit(1)

game = load_starting_positions(argv[1])
throw = turn_throw_generator()
winner, loser, turn = play(game, throw)

throws = turn * 3
result = throws * loser
print(result)
