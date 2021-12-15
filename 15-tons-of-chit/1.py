#!/bin/env python3

import sys
from math import inf
from heapq import heappush, heappop


def load_cave(path):
  with open(path, "r") as f:
    return [list(map(int, line.strip())) for line in f]


def get_dimensions(cave):
  w = len(cave[0])
  h = len(cave)
  return w,h


def create_adjacency_map(cave):
  w,h = get_dimensions(cave)
  start_node = (0,0)
  end_node = (w-1,h-1)
  adjacencies = {}
  for y in range(h):
    for x in range(w):
      neighbors = []
      if x < w-1: neighbors.append(((x+1,y), cave[y][x+1]))
      if y < h-1: neighbors.append(((x,y+1), cave[y+1][x]))
      if x > 0: neighbors.append(((x-1,y), cave[y][x-1]))
      if y > 0: neighbors.append(((x,y-1), cave[y-1][x]))
      adjacencies[(x,y)] = neighbors
  return adjacencies, start_node, end_node


def init_nodes_to_visit_queue(start_node):
  return [(0, start_node, [start_node])]


def init_minimum_risk_map(adjacencies):
  return dict(
    (node, 0 if node == start_node else inf)
    for node in adjacencies.keys()
  ) 


def find_safest_route(adjacencies, start_node, end_node):
  nodes_to_visit = init_nodes_to_visit_queue(start_node)
  minimum_risk = init_minimum_risk_map(adjacencies)
  visited_nodes = set()

  while nodes_to_visit:
    cost, node, path = heappop(nodes_to_visit)

    if node == end_node:
      return (cost, path)

    for neighbor,to_cost in adjacencies[node]:
      if neighbor in visited_nodes:
        continue
      
      known_risk_to_neighbour = minimum_risk[neighbor]
      risk_via_this_node = cost + to_cost
      if risk_via_this_node < known_risk_to_neighbour:
        minimum_risk[neighbor] = risk_via_this_node
        queue_node = (risk_via_this_node, neighbor, [neighbor]+path)
        heappush(nodes_to_visit, queue_node)

    visited_nodes.add(node)


cave = load_cave(sys.argv[1]) 
adjacencies, start_node, end_node = create_adjacency_map(cave)
risk_level, _ = find_safest_route(adjacencies, start_node, end_node)

print(risk_level)
