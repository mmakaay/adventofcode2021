#!/bin/env python3

import json

def read_data(path):
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
    row = board[i*5:i*5+5]
    col = board[i::5]
    if all(f is None for f in row) or all(f is None for f in col):
      return True
  return False

def is_losing(board):
    return not is_winning(board)

def remove_winners(boards):
  return list(filter(is_losing, boards))


numbers, boards = read_data("input.txt")
for number in numbers:
  flag_number_on_boards(boards, number)
  if len(boards) > 1:
    boards = remove_winners(boards)
  elif is_winning(boards[0]):
    break

remaining = [n for n in boards[0] if n is not None]
print(sum(remaining) * number)
