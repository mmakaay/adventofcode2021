#!/bin/env python3

from collections import defaultdict


def load_routes(path):
    routes = defaultdict(list)
    with open(path, "r") as f:
        for line in f:
            [a, b] = line.strip().split("-")
            routes[a].append(b)
            routes[b].append(a)
    return routes


def is_small_cave(cave):
    return cave.islower()


def routes_after_vising_cave(routes, current_cave):
    if is_small_cave(current_cave):
        routes = dict(
            (cave, [e for e in exits if e != current_cave])
            for cave, exits in routes.items()
        )
    return routes


def explore(routes, current_cave, path=()):
    path += (current_cave,)
    if current_cave == "end":
        yield path
    else:
        routes = routes_after_vising_cave(routes, current_cave)
        for next_cave in routes[current_cave]:
            yield from explore(routes, next_cave, path)


routes = load_routes("input.txt")
paths = list(explore(routes, "start"))

print(len(paths))
