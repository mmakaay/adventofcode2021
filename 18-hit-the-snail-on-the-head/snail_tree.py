#!/bin/env python3

from collections.abc import Iterable


class SnailException(Exception):
  pass


class SnailVisitor:
    def __init__(self, node, initial_result=None):
        self.node = node
        self.result = initial_result

    def run(self):
        self.node.accept(self)
        return self.result

    def visit_pair_start(self, pair):
        pass

    def visit_pair(self, pair):
        pass

    def visit_pair_end(self, pair):
        pass

    def visit_number(self, number):
        pass


class SnailNode:
    def __init__(self):
        self.parent = None

    def replace_with(self, node):
        self.parent.replace_child(self, node)

    def __str__(self):
        formatter = SnailStringFormatter(self)
        return formatter.run()


class SnailNumber(SnailNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def accept(self, visitor: SnailVisitor):
        visitor.visit_number(self)

    def set_value(self, value):
        self.value = value


class SnailPair(SnailNode):
    def __init__(self, left:SnailNode=SnailNumber(0), right:SnailNode=SnailNumber(0)):
        super().__init__()
        self.left = left
        self.left.parent = self
        self.right = right
        self.right.parent = self

    def replace_child(self, orig, replacement):
        if self.left == orig:
            self.left = replacement
            replacement.parent = self
        elif self.right == orig:
            self.right = replacement
            replacement.parent = self
        else:
            raise SnailException("Node to replace is not a child of this parent")

    def accept(self, visitor: SnailVisitor):
        visitor.visit_pair_start(self)
        self.left.accept(visitor)
        visitor.visit_pair(self)
        self.right.accept(visitor)
        visitor.visit_pair_end(self)


class SnailRoot(SnailPair):
    def __init__(self, left:SnailNode=SnailNumber(0), right:SnailNode=SnailNumber(0)):
        super().__init__(left, right)

    def replace_with(self, node):
        raise SnailException("The root node cannot be replaced")


class SnailStringFormatter(SnailVisitor):
    def __init__(self, node: SnailNode):
        super().__init__(node, "")

    def visit_number(self, node: SnailNode):
        self.result += str(node.value)

    def visit_pair_start(self, node: SnailNode):
        self.result += "["

    def visit_pair(self, node: SnailNode):
        self.result += ","

    def visit_pair_end(self, node: SnailNode):
        self.result += "]"


class SnailParserException(Exception):
    def __init__(self, msg, pos):
        super().__init__(msg)
        self.pos = pos


class SnailParser:
    def parse(self, code):
        self.code = code
        self.index = 0
        return self._parse()

    def _error(self, msg):
        raise SnailParserException(msg, self.index)

    def _peek(self):
        try:
            return self.code[self.index]
        except IndexError:
            self._error("Unexpected end of input")

    def _next(self):
        c = self._peek()
        self.index += 1 
        return c

    def _parse(self):
        c = self._peek()
        if c == "[":
            pair = self._parse_pair()
            if len(self.code) != self.index:
                self._error("Extraneous input after closing ']'")
            return SnailRoot(pair.left, pair.right)
        self._error(f"Expected opening '[', got '{c}'")

    def _parse_pair(self):
        c = self._next()
        if c != "[":
            self._error(f"Expected opening '[', got '{c}")
        left = self._parse_node()
        c = self._next()
        if c != ",":
            self._error(f"Expected separator ',', got '{c}")
        right = self._parse_node()
        c = self._next()
        if c != "]":
            self._error(f"Expected closing ']', got '{c}")
        return SnailPair(left, right)

    def _parse_node(self):
        c = self._peek()
        if c == "[":
            return self._parse_pair()
        if c.isdigit():
            number = self._next()
            while self._peek().isdigit():
                number += self._next()
            return SnailNumber(int(number))
        self._error(f"Expected node start (opening '[' or digit), got '{c}'")

        
        
