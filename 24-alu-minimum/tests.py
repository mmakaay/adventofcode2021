#!/bin/env python3
#
# This script contains unit tests for the alu module.

import unittest
from alu import *


class TestALUEmulator(unittest.TestCase):
    def test_can_create_ALUEmulator(self):
        alu = ALUEmulator()

    def test_initializes_vars_at_zero(self):
        alu = ALUEmulator()
        self.assertEqual(0, alu.w)
        self.assertEqual(0, alu.x)
        self.assertEqual(0, alu.y)
        self.assertEqual(0, alu.z)

    def test_inp_sets_variable(self):
        alu = ALUEmulator()
        alu.inp(VAR_W, 1)
        alu.inp(VAR_X, 2)
        alu.inp(VAR_Y, 3)
        alu.inp(VAR_Z, 4)
        self.assertEqual(1, alu.w)
        self.assertEqual(2, alu.x)
        self.assertEqual(3, alu.y)
        self.assertEqual(4, alu.z)

    def test_inp_variable_can_be_negative(self):
        alu = ALUEmulator()
        alu.inp(VAR_X, -10)
        self.assertEqual(-10, alu.x)

    def test_add_with_var(self):
        alu = ALUEmulator()
        alu.inp(VAR_W, 4)
        alu.inp(VAR_X, 5)
        alu.add(VAR_W, VAR_X, True)
        self.assertEqual(9, alu.w)

    def test_add_with_value(self):
        alu = ALUEmulator()
        alu.inp(VAR_X, 5)
        alu.add(VAR_X, 3, False)
        self.assertEqual(8, alu.x)

    def test_mul(self):
        alu = ALUEmulator()
        alu.inp(VAR_X, -2)
        alu.inp(VAR_Y, 5)
        alu.mul(VAR_X, VAR_Y, True)
        self.assertEqual(-10, alu.x)

    def test_div(self):
        alu = ALUEmulator()
        alu.inp(VAR_W, 8)
        alu.inp(VAR_X, 2)
        alu.div(VAR_W, VAR_X, True)
        alu.inp(VAR_Y, 7)
        alu.inp(VAR_Z, 3)
        alu.div(VAR_Y, VAR_Z, True)
        self.assertEqual(4, alu.w)
        self.assertEqual(2, alu.y)

    def test_mod(self):
        alu = ALUEmulator()
        alu.inp(VAR_W, 8)
        alu.inp(VAR_X, 2)
        alu.mod(VAR_W, VAR_X, True)
        alu.inp(VAR_Y, 7)
        alu.inp(VAR_Z, 3)
        alu.mod(VAR_Y, VAR_Z, True)
        self.assertEqual(0, alu.w)
        self.assertEqual(1, alu.y)

    def test_eql_true(self):
        alu = ALUEmulator()
        alu.inp(VAR_X, 4)
        alu.inp(VAR_Y, 4)
        alu.eql(VAR_X, VAR_Y, True)
        self.assertEqual(1, alu.x)

    def test_eql_false(self):
        alu = ALUEmulator()
        alu.inp(VAR_X, 4)
        alu.inp(VAR_Y, 5)
        alu.eql(VAR_X, VAR_Y, True)
        self.assertEqual(0, alu.x)


class TestALUCompiler(unittest.TestCase):
    def test_can_create_compiler(self):
        ALUCompiler()

    def test_can_compile_empty_program(self):
        program = ALUCompiler().compile([""])
        result = program.run()
        self.assertEqual((0, 0, 0, 0), result)

    def test_exception_when_using_unknown_operation(self):
        with self.assertRaises(ALUSyntaxError) as context:
            ALUCompiler().compile(["wut w"])
        self.assertIn("Unknown operation", str(context.exception))


    def test_can_compile_inp_w(self):
        for var_name, expected in [
            ("w", (1, 0, 0, 0)),
            ("x", (0, 1, 0, 0)),
            ("y", (0, 0, 1, 0)),
            ("z", (0, 0, 0, 1)),
        ]:
            with self.subTest():
                program = ALUCompiler().compile([f"inp {var_name}"])
                result = program.run(1)
                self.assertEqual(expected, result)

    def test_can_compile_multiple_instructions(self):
        program = ALUCompiler().compile([
            " inp w",
            "inp x ",
            "inp  y",
            "inp Z  "
        ])
        self.assertEqual((-2, -1, 0, 1), program.run(-2, -1, 0, 1))

    def test_can_compile_add(self):
        program = ALUCompiler().compile([
            "inp x",
            "inp y",
            "add x y"
        ])
        self.assertEqual((0, 42, 10, 0), program.run(32, 10))

    def test_can_use_number_for_second_argument(self):
        program = ALUCompiler().compile([
            "inp x",
            "add x 5"
        ])
        self.assertEqual((0, 5, 0, 0), program.run(0))
        self.assertEqual((0, 10, 0, 0), program.run(5))

    def test_can_compile_mul(self):
        program = ALUCompiler().compile([
            "inp x",
            "inp y",
            "mul x y"
        ])
        self.assertEqual((0, 42, 7, 0), program.run(6, 7))

    def test_can_compile_div_and_mod(self):
        program = ALUCompiler().compile([
            "inp w",
            "inp x",
            "inp y",
            "inp z",
            "div w x",
            "mod y z",
        ])
        self.assertEqual((3, 4, 1, 4), program.run(13, 4, 13, 4))
        self.assertEqual((2, 2, 0, 2), program.run(4, 2, 4, 2))

    def test_can_compile_eql(self):
        program = ALUCompiler().compile([
            "inp w",
            "inp x",
            "eql w x"
        ])

        self.assertEqual((0, 7, 0, 0), program.run(6, 7))
        self.assertEqual((1, 6, 0, 0), program.run(6, 6))

    def test_exception_when_using_not_enough_arguments(self):
        with self.assertRaises(ALUSyntaxError) as context:
            ALUCompiler().compile(["inp"])
        self.assertIn("Missing argument", str(context.exception))

    def test_exception_when_using_too_many_arguments(self):
        with self.assertRaises(ALUSyntaxError) as context:
            ALUCompiler().compile(["inp w z"])
        self.assertIn("Too many arguments", str(context.exception))

    def test_compile_to_binary_example(self):
        program = ALUCompiler().compile([
            "inp w",
            "add z w",
            "mod z 2",
            "div w 2",
            "add y w",
            "mod y 2",
            "div w 2",
            "add x w",
            "mod x 2",
            "div w 2",
            "mod w 2",
        ])
        self.assertEqual((0, 0, 0, 1), program.run(1))
        self.assertEqual((0, 0, 1, 0), program.run(2))
        self.assertEqual((0, 1, 0, 0), program.run(4))
        self.assertEqual((1, 0, 0, 0), program.run(8))
        self.assertEqual((1, 0, 1, 0), program.run(10))
        self.assertEqual((1, 1, 1, 0), program.run(14))
        self.assertEqual((1, 1, 1, 1), program.run(15))


unittest.main()
