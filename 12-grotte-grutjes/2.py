#!/bin/env python3

from collections import defaultdict


def load_routes(path):
    routes = defaultdict(list)
    with open(path, "r") as f:
        for line in f:
            [a, b] = line.strip().split("-")
            if b != "start":
                routes[a].append(b)
            if a != "start":
                routes[b].append(a)
    return routes


def is_small_cave(cave):
    return cave.islower()


def list_small_caves(routes):
    return [c for c in routes.keys() if is_small_cave(c)]


def create_travel_plans(routes):
    small_caves = list_small_caves(routes)
    for sightseeing_cave in small_caves:
        yield dict((cave, 2 if cave == sightseeing_cave else 1) for cave in small_caves)


def apply_travel_plan(current_cave, travel_plan):
    if current_cave in travel_plan:
        if travel_plan[current_cave] == 0:
            return None
        return dict(
            (c, m - 1 if c == current_cave else m) for c, m in travel_plan.items()
        )
    return travel_plan


def explore(routes, current_cave, travel_plan, path=()):
    if travel_plan := apply_travel_plan(current_cave, travel_plan):
        path += (current_cave,)
        if current_cave == "end":
            yield path
        else:
            for next_cave in routes[current_cave]:
                yield from explore(routes, next_cave, travel_plan, path)


routes = load_routes("input.txt")
paths = set()
for travel_plan in create_travel_plans(routes):
    paths.update(explore(routes, "start", travel_plan))

print(len(paths))
