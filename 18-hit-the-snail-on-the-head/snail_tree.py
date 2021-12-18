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
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def accept(self, visitor: SnailVisitor):
        visitor.visit_number(self)

    def set_value(self, value: int):
        self.value = value


class SnailPair(SnailNode):
    def __init__(self, left:SnailNode=SnailNumber(0), right:SnailNode=SnailNumber(0)):
        super().__init__()
        self.left = left
        self.left.parent = self
        self.right = right
        self.right.parent = self

    def replace_child(self, orig: SnailNode, replacement: SnailNode):
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

    def reduce(self):
        exploder = SnailExploder(self)
        splitter = SnailSplitter(self)
        reduced = False
        while exploder.run() or splitter.run():
            reduced = True
        return reduced


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


class SnailExploder(SnailVisitor):
    def __init__(self, node: SnailNode):
        super().__init__(node)
        self.exploded = False
        self.depth = 0

    def run(self):
        self.exploded = False
        super().run()
        return self.exploded

    def visit_pair_start(self, pair: SnailPair):
        self.depth += 1

    def visit_pair(self, pair: SnailPair):
        if self.depth != 5 or self.exploded:
            return

        # Find first number node to the left.
        prev_node = pair
        node = pair.parent
        while node and node.left == prev_node:
            prev_node = node
            node = node.parent
        if node:
            node = node.left
            while not isinstance(node, SnailNumber):
                if isinstance(node.right, SnailNumber):
                    node = node.right
                else:
                    node = node.left
            node.set_value(node.value + pair.left.value)

        # Find first number node to the right.
        prev_node = pair
        node = pair.parent
        while node and node.right == prev_node:
            prev_node = node
            node = node.parent
        if node:
            node = node.right
            while not isinstance(node, SnailNumber):
                if isinstance(node.left, SnailNumber):
                    node = node.left
                else:
                    node = node.right
            node.set_value(node.value + pair.right.value)

        pair.replace_with(SnailNumber(0))
        self.exploded = True

    def visit_pair_end(self, pair: SnailPair):
        self.depth -= 1


class SnailSplitter(SnailVisitor):
    def __init__(self, node: SnailNode):
        super().__init__(node)
        self.splitted = False

    def run(self):
        self.splitted = False
        super().run()
        return self.splitted

    def visit_number(self, number: SnailNumber):
        if number.value > 9 and not self.splitted:
            left = number.value // 2
            right = number.value - left
            number.replace_with(SnailPair(SnailNumber(left), SnailNumber(right)))
            self.splitted = True


class SnailMagnitudeComputer(SnailVisitor):
    def __init__(self, node: SnailNode):
        super().__init__(node, 0)
        self.splitted = False


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


def parse_snail_code(code):       
    parser = SnailParser()
    return parser.parse(code)

