#!/bin/env python3

from functools import reduce
import operator


def file_to_hexstream(path):
  with open(path, "r") as f:
    for line in f:
      yield from line.strip().upper()


def hexstream_to_bitstream(hexstream):
  HEXMAP = {
    "0": (0,0,0,0), "1": (0,0,0,1), "2": (0,0,1,0), "3": (0,0,1,1),
    "4": (0,1,0,0), "5": (0,1,0,1), "6": (0,1,1,0), "7": (0,1,1,1),
    "8": (1,0,0,0), "9": (1,0,0,1), "A": (1,0,1,0), "B": (1,0,1,1),
    "C": (1,1,0,0), "D": (1,1,0,1), "E": (1,1,1,0), "F": (1,1,1,1),
  }
  for hexchar in hexstream:
    yield from HEXMAP[hexchar] 


def parse_bitstream(bits):
  _, ast = parse_packet(bits)
  return ast


TYPE_SUM     = 0
TYPE_PRODUCT = 1
TYPE_MIN     = 2
TYPE_MAX     = 3
TYPE_LITERAL = 4
TYPE_GT      = 5
TYPE_LT      = 6
TYPE_EQ      = 7


def parse_packet(bits):
  version = parse_int_value(bits, 3)
  packet_type = parse_int_value(bits, 3)
  bitlen = 6
  if packet_type == TYPE_LITERAL:
    lit_bitlen, lit_value = parse_literal(bits)
    return bitlen+lit_bitlen, (version, packet_type, lit_value)
  else:
    op_bitlen, op_value = parse_operator(bits)
    return bitlen+op_bitlen, (version, packet_type, op_value)


def parse_int_value(bits, bitlen):
  value = 0
  for _ in range(bitlen):
    value = value<<1 | next(bits) 
  return value


def parse_literal(bits):
  bitlen = 0
  value = 0
  while True:
    there_is_more = next(bits)
    value = value<<4 | parse_int_value(bits, 4)
    bitlen += 5
    if not there_is_more:
      return bitlen, value


def parse_operator(bits):
  bitlen = 1
  length_type = next(bits)
  if length_type == 0:
    op_bitlen, op_value = parse_operator_args_by_bitlen(bits)
  elif length_type == 1:
    op_bitlen, op_value = parse_operator_args_by_nr_of_args(bits)
  return bitlen+op_bitlen, op_value


def parse_operator_args_by_bitlen(bits):
  bitlen = 15
  expected_bits = parse_int_value(bits, bitlen)
  args = []
  while expected_bits > 0:
    packet_bitlen, packet_value = parse_packet(bits)
    bitlen += packet_bitlen
    args.append(packet_value)
    expected_bits -= packet_bitlen
  return bitlen, args


def parse_operator_args_by_nr_of_args(bits):
  bitlen = 11
  expected_args = parse_int_value(bits, bitlen)
  args = []
  while expected_args > 0:
    packet_bitlen, packet_value = parse_packet(bits)
    bitlen += packet_bitlen
    args.append(packet_value)
    expected_args -= 1
  return bitlen, args
    

def operator_func_for_packet_type(packet_type):
  OPERATOR_FUNCS = {
    TYPE_SUM     : operator.add,
    TYPE_PRODUCT : operator.mul,
    TYPE_MIN     : min,
    TYPE_MAX     : max,
    TYPE_GT      : operator.gt,
    TYPE_LT      : operator.lt,
    TYPE_EQ      : operator.eq
  }
  return OPERATOR_FUNCS[packet_type]


def evaluate(ast):
  version, packet_type, args = ast
  if packet_type == TYPE_LITERAL:
    result = args
  else:
    args = [evaluate(arg) for arg in args]
    operator_func = operator_func_for_packet_type(packet_type)
    result = int(reduce(operator_func, args))
  return result


hexes = file_to_hexstream("input.txt")
bits = hexstream_to_bitstream(hexes)
ast = parse_bitstream(bits)
result = evaluate(ast)

print(result)
