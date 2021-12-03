#!/bin/env python3.10

f = open("input.txt", "r")
data = [map(int, line.strip()) for line in f]

gamma, epsilon = 0, 0
threshold = len(data) / 2
columns = list(zip(*data))

for values in columns:
    add_gamma = sum(values) > threshold
    gamma = (gamma << 1) | add_gamma
    epsilon = (epsilon << 1) | (not add_gamma)

print(gamma*epsilon)
