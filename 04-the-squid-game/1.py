#!/bin/env python3


def load_bingo_data_from_file(path):
    with open(path) as f:
        numbers = list(map(int, next(f).split(",")))
        boards = []
        for line in f:
            if line.strip() == "":
                boards.append([])
            else:
                boards[-1].extend(list(map(int, line.split())))
    return numbers, boards


def flag_number_on_boards(boards, number):
    for board in boards:
        try:
            i = board.index(number)
            board[i] = None
        except ValueError:
            pass


def is_winning(board):
    for i in range(5):
        row = board[i * 5 : i * 5 + 5]
        col = board[i::5]
        if all(f is None for f in row) or all(f is None for f in col):
            return True
    return False


def find_winners(boards):
    return list(filter(is_winning, boards))


numbers, boards = load_bingo_data_from_file("input.txt")
for number in numbers:
    flag_number_on_boards(boards, number)
    winners = find_winners(boards)
    if any(winners):
        break

for winner in winners:
    remaining = [n for n in winner if n is not None]
    print(sum(remaining) * number)
