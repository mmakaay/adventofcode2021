#!/bin/env python3

import unittest
from snail_tree import *


class TestSnailNodes(unittest.TestCase):
    def test_can_create_number(self):
        number = SnailNumber(1)
        self.assertEqual(1, number.value)

    def test_can_set_value_for_number(self):
        number = SnailNumber(42)
        number.set_value(73)
        self.assertEqual(73, number.value)

    def test_can_create_pair_without_arguments(self):
        pair = SnailPair()
        self.assertEqual(0, pair.left.value)
        self.assertEqual(0, pair.right.value)

    def test_can_create_pair_with_numbers(self):
        n1 = SnailNumber(4)
        n2 = SnailNumber(2)
        pair = SnailPair(n1, n2)
        self.assertEqual(4, pair.left.value)
        self.assertEqual(2, pair.right.value)

    def test_can_create_root_node_without_arguments(self):
        self.assertEqual("[0,0]", str(SnailRoot()))

    def test_can_create_root_node(self):
        number1 = SnailNumber(1)
        number2 = SnailNumber(2)
        self.assertEqual("[1,2]", str(SnailRoot(number1, number2)))

    def test_cannot_replace_root_node_with_numbers(self):
        root = SnailRoot()
        with self.assertRaises(SnailException):
            root.replace_with(SnailNumber(5))

    def test_can_replace_node_with_number(self):
        root = SnailRoot()
        root.left.replace_with(SnailNumber(9))
        self.assertEqual("[9,0]", str(root))

    def test_can_replace_node_twice(self):
        root = SnailRoot()
        root.left.replace_with(SnailNumber(9))
        root.left.replace_with(SnailNumber(7))
        self.assertEqual("[7,0]", str(root))

    def test_can_replace_node_number_with_pair(self):
        root = SnailRoot()
        pair1 = SnailPair(SnailNumber(1), SnailNumber(2))
        pair2 = SnailPair(SnailNumber(2), SnailNumber(3))
        root.left.replace_with(pair1)
        root.right.replace_with(pair2)
        self.assertEqual("[[1,2],[2,3]]", str(root))

    def test_can_replace_node_pair_with_number(self):
        root = SnailRoot()
        pair = SnailPair(SnailNumber(1), SnailNumber(2))
        number = SnailNumber(7)
        root.left.replace_with(pair)
        pair.replace_with(number)
        self.assertEqual("[7,0]", str(root))

    def test_can_create_complex(self):
        root = SnailRoot(
            SnailPair(
                SnailPair(SnailNumber(1), SnailNumber(2)),
                SnailPair(SnailNumber(3), SnailPair(SnailNumber(4), SnailNumber(5))),
            ),
            SnailPair(SnailNumber(6), SnailNumber(7)),
        )
        self.assertEqual("[[[1,2],[3,[4,5]]],[6,7]]", str(root))


class TestSnailVisitor(unittest.TestCase):
    def test_can_create_visitor(self):
        root = SnailRoot()
        visitor = SnailStringFormatter(root)

    def test_can_visit_number_node(self):
        number = SnailNumber(1)
        visitor = SnailStringFormatter(number)
        result = visitor.run()
        self.assertEqual("1", result)

    def test_can_visit_pair_node(self):
        pair = SnailPair(SnailNumber(1), SnailNumber(2))
        visitor = SnailStringFormatter(pair)
        result = visitor.run()
        self.assertEqual("[1,2]", result)

    def test_can_visit_nested_nodes(self):
        pair1 = SnailPair(SnailNumber(1), SnailNumber(2))
        pair2 = SnailPair(SnailNumber(3), SnailNumber(4))
        root = SnailRoot(pair1, pair2)
        visitor = SnailStringFormatter(root)
        result = visitor.run()
        self.assertEqual("[[1,2],[3,4]]", result)


class TestSnailParser(unittest.TestCase):
    def test_can_create_parser(self):
        parser = SnailParser()

    def test_parser_cases(self):
        parser = SnailParser()
        for code in [
            "[0,0]",
            "[1,2]",
            "[[1,2],3]",
            "[[1,2],[3,4]]",
            "[[[1,2],3],[4,5]]",
            "[[[1,[3,4]],5],[6,[7,[8,9]]]]",
        ]:
            with self.subTest():
                root = parser.parse(code)
                self.assertEqual(code, str(root))

    def test_parser_error_cases(self):
        parser = SnailParser()
        for code,error_pos, expected_in_msg in [
            ("", 0, "Unexpected end"),
            ("[", 1, "Unexpected end"),
            ("[1", 2, "Unexpected end"),
            ("[1,", 3, "Unexpected end"),
            ("[1,2", 4, "Unexpected end"),
            ("[1,2][", 5, "Extraneous"),
            ("]", 0, "Expected opening"),
            ("[]", 1, "Expected node"),
            ("[,", 1, "Expected node"),
            ("[,2]", 1, "Expected node"),
            ("[a,b]", 1, "Expected node"),
            ("[1]", 3, "Expected separator"),
            ("[1,]", 3, "Expected node"),
            ("[1,2[", 5, "Expected closing"),
        ]:
            with self.subTest():
                with self.assertRaises(SnailParserException) as context:
                    parser.parse(code)
                self.assertEqual(error_pos, context.exception.pos)
                self.assertIn(expected_in_msg, str(context.exception))

unittest.main()
