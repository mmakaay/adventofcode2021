#!/bin/env python3.10

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

    def test_sum_two_numbers(self):
        root1 = parse_snail_code("[1,1]")
        root2 = parse_snail_code("[2,2]")
        root3 = root1 + root2
        self.assertEqual("[[1,1],[2,2]]", str(root3))


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
        for code, error_pos, expected_in_msg in [
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
                    parse_snail_code(code)
                self.assertEqual(error_pos, context.exception.pos)
                self.assertIn(expected_in_msg, str(context.exception))

    def test_parse_snail_code_function(self):
        root = parse_snail_code("[1,[2,[3,[4,[5,6]]]]]")
        self.assertEqual("[1,[2,[3,[4,[5,6]]]]]", str(root))


class TestSnailExploder(unittest.TestCase):
    def test_explode_not(self):
        root = parse_snail_code("[9,9]")
        exploded = SnailExploder(root).run()
        self.assertFalse(exploded)
        self.assertEqual("[9,9]", str(root))

    def test_explode_one_to_the_left(self):
        root = parse_snail_code("[1,[2,[3,[4,[5,6]]]]]")
        exploded = SnailExploder(root).run()
        self.assertTrue(exploded)
        self.assertEqual("[1,[2,[3,[9,0]]]]", str(root))

    def test_explode_one_to_the_right(self):
        root = parse_snail_code("[[[[[1,2],3],4],5],6]")
        SnailExploder(root).run()
        self.assertEqual("[[[[0,5],4],5],6]", str(root))

    def test_explode_one_two_sides(self):
        root = parse_snail_code("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")
        SnailExploder(root).run()
        self.assertEqual("[[[[0,7],4],[15,[0,13]]],[1,1]]", str(root))

    def test_explode_cases_from_assignment(self):
        for code, exploded in [
            (
                "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]",
                "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]",
            ),
            ("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[15,[0,13]]],[1,1]]"),
            (
                "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]",
                "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
            ),
            ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
            ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
            ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
            (
                "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
                "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
            ),
            ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
            (
                "[[[[4,0],[5,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]",
                "[[[[4,0],[5,4]],[[0,[7,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]",
            ),
        ]:
            with self.subTest():
                root = parse_snail_code(code)
                SnailExploder(root).run()
                self.assertEqual(exploded, str(root))


class TestSnailSplitter(unittest.TestCase):
    def test_split_not(self):
        root = parse_snail_code("[9,9]")
        splitted = SnailSplitter(root).run()
        self.assertFalse(splitted)
        self.assertEqual("[9,9]", str(root))

    def test_split_simple_even_left(self):
        root = parse_snail_code("[10,9]")
        splitted = SnailSplitter(root).run()
        self.assertTrue(splitted)
        self.assertEqual("[[5,5],9]", str(root))

    def test_split_simple_uneven_left(self):
        root = parse_snail_code("[11,9]")
        SnailSplitter(root).run()
        self.assertEqual("[[5,6],9]", str(root))

    def test_split_simple_only_once(self):
        root = parse_snail_code("[[9,21],[22,23]]")
        SnailSplitter(root).run()
        self.assertEqual("[[9,[10,11]],[22,23]]", str(root))

    def test_split_cases_from_assignment(self):
        for code, splitted in [
            ("[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"),
            (
                "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]",
                "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]",
            ),
        ]:
            with self.subTest():
                root = parse_snail_code(code)
                SnailSplitter(root).run()
                self.assertEqual(splitted, str(root))


class TestSnailReduce(unittest.TestCase):
    def test_reduce_not(self):
        root = parse_snail_code("[9,9]")
        reduced = root.reduce()
        self.assertFalse(reduced)
        self.assertEqual("[9,9]", str(root))

    def test_reduce_one_explode(self):
        root = parse_snail_code("[[[[[1,2],3],4],5],6]")
        reduced = root.reduce()
        self.assertTrue(reduced)
        self.assertEqual("[[[[0,5],4],5],6]", str(root))

    def test_reduce_two_explodes(self):
        root = parse_snail_code("[[[[[1,2],[3,4]],5],6],7]")
        reduced = root.reduce()
        self.assertTrue(reduced)
        self.assertEqual("[[[[5,0],9],6],7]", str(root))

    def test_reduce_one_split(self):
        root = parse_snail_code("[10,1]")
        reduced = root.reduce()
        self.assertTrue(reduced)
        self.assertEqual("[[5,5],1]", str(root))

    def test_reduce_two_splits(self):
        root = parse_snail_code("[10,10]")
        reduced = root.reduce()
        self.assertTrue(reduced)
        self.assertEqual("[[5,5],[5,5]]", str(root))

    def test_reduce_buttload(self):
        root = parse_snail_code("[[[[[1,6],[6,7]],8],[9,10]],11]")
        reduced = root.reduce()
        self.assertTrue(reduced)
        self.assertEqual("[[[[0,6],[7,8]],[9,[5,5]]],[5,6]]", str(root))

    def test_reduce_with_examples_from_assignment(self):
        for code, expected_reduced in [
            (
                "[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]",
                "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
            ),
            (
                "[[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]]",
                "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]",
            ),
            (
                "[[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]]",
                "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]",
            ),
        ]:
            with self.subTest():
                root = parse_snail_code(code)
                root.reduce()
                self.assertEqual(expected_reduced, str(root))


class TestSnailMagnitude(unittest.TestCase):
    def test_magnitude_simple(self):
        root = parse_snail_code("[1,2]")
        magnitude = SnailMagnitudeComputer(root).run()
        self.assertEqual((3 * 1 + 2 * 2), magnitude)

    def test_magnitude_with_pair(self):
        root = parse_snail_code("[[1,2],3]")
        magnitude = SnailMagnitudeComputer(root).run()
        self.assertEqual((3 * (3 * 1 + 2 * 2) + 2 * 3), magnitude)

    def test_magnitude_with_two_pairs(self):
        root = parse_snail_code("[[1,2],[3,4]]")
        magnitude = SnailMagnitudeComputer(root).run()
        self.assertEqual((3 * (3 * 1 + 2 * 2) + 2 * (3 * 3 + 2 * 4)), magnitude)

    def test_magnitude_with_examples_from_assignment(self):
        for code, expected_magnitude in [
            ("[[1,2],[[3,4],5]]", 143),
            ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
            ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
            ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
            ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
            ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
        ]:
            with self.subTest():
                root = parse_snail_code(code)
                magnitude = SnailMagnitudeComputer(root).run()
                self.assertEqual(expected_magnitude, magnitude)

    def test_magnitude_method(self):
        root = parse_snail_code("[[1,2],[3,4]]")
        magnitude = root.magnitude()
        self.assertEqual(55, magnitude)


unittest.main()
