#!/bin/env python3.10

import re
from sys import argv, exit
from itertools import product
from functools import cache


def load_players():
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <filename>")
        exit(1)
    playerinfo = re.compile("(.+) starting position: (\d+)")
    players = []
    with open(argv[1]) as f:
        for line in f:
            if groups := playerinfo.match(line):
                name = groups[1]
                starting_pos = int(groups[2])
                players.append((name, starting_pos))
    return tuple(players)


def play_all_games(players):
    player1, player2 = players
    wins1 = find_all_games_with_winner(players, player1)
    wins2 = find_all_games_with_winner(players, player2)
    return (player1, wins1), (player2, wins2)


def find_all_games_with_winner(players, winner):
    """Count the number of split off universes in which a player will win."""

    player1, player2 = players
    (_, player1_pos) = player1
    (_, player2_pos) = player2

    # Get the starting points of the winner and loser.
    wstart_pos = player1_pos if player1 == winner else player2_pos
    lstart_pos = player2_pos if player1 == winner else player1_pos

    total_routes = 0
    for turns, wpos, wscore, lpos, lscore in generate_winning_game_states():
        # Player 1 starts the game, so when player 1 wins the game, then 
        # Player 2 will have one less turn. When Player 2 wins the game, then
        # both will have had the same number of turns.
        wturns = turns
        lturns = turns - (1 if winner == player1 else 0)

        # Count the number of routes in which the current winner and loser
        # game states can be reached.
        routes_winner = find_routes_to(wscore, wturns, wstart_pos, wpos)
        routes_loser = find_routes_to(lscore, lturns, lstart_pos, lpos)

        # Combine these to fine the total number of possible routes through
        # which the current game end state can be reached.
        total_routes += routes_winner * routes_loser
    return total_routes


def generate_winning_game_states():
    """Generate all the possible end states of a game.
    See strategy.txt for information on the numbers used here."""
    turns = range(3, 11)
    winner_positions = range(1, 11)
    winner_scores = range(21, 31)
    loser_positions = range(1, 11)
    loser_scores = range(3, 21)
    yield from product(
        turns, winner_positions, winner_scores, loser_positions, loser_scores
    )


def get_dirac_distribution():
    """Get the possible scores for a single turn and their frequency distribution.
    See strategy.txt for information on the numbers used here."""
    return [(1, 3), (3, 4), (6, 5), (7, 6), (6, 7), (3, 8), (1, 9)]


@cache
def find_routes_to(score, nr_of_turns, start_pos, end_pos):
    """Find the number of routes that lead to the provided game state: a score
    that can be reached in the number of turns, starting and ending at the
    given positions."""

    # When the number of turns is 0, a valid route is found if the score is
    # 0 and the player position matches the starting position of the player.
    # Otherwise, the route was not valid.
    if nr_of_turns == 0:
        if score == 0 and end_pos == start_pos:
            return 1
        else:
            return 0

    # When the score drops below zero, then this is not a valid route.
    if score <= 0:
        return 0

    # More turns are available. Find out how many routes there are to
    # get into the current game state.
    routes = 0

    # The previous score can be found by subtracing the current end_pos, since that
    # is what brought the score to its current level in the previous turn.
    prev_score = score - end_pos

    # Only use the previous score when it is below 21 (the minimum winning score).
    # Since for example 25 is a possible winning score, there are various scores
    # (1, 2, 3, 4) that cannot have been the previous step in the game (since the
    # winner would then have won earlier).
    if prev_score >= 21:
        return 0 

    prev_nr_of_turns = nr_of_turns - 1

    # In the previous turn, one of the possible scores (3 - 9) has gotten the player
    # to the end position in this turn. So to backtrack, all the possible scores are
    # applied here.
    for freq, score in get_dirac_distribution():
        prev_end_pos = (end_pos - score - 1) % 10 + 1
        routes += freq * find_routes_to(
            prev_score, prev_nr_of_turns, start_pos, prev_end_pos
        )
    return routes


players = load_players()
results = play_all_games(players)
for (name, start_pos), wins in results:
    print(f"{name} on start pos {start_pos} wins {wins} times")
