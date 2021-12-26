VAR_W = 0
VAR_X = 1
VAR_Y = 2
VAR_Z = 3

class ALUSyntaxError(Exception):
    pass

class ALURuntimError(Exception):
    pass

class ALUEmulator:
    def __init__(self):
        self._vars = [0, 0, 0, 0]
        self.debug = False

    def set_debug(self, on_off):
        self.debug = on_off

    def exec(self, src_line, func, *args):
        if (self.debug):
            a = self.vars
            func(*args)
            b = self.vars
            print(f"DEBUG: {src_line:10s} {a} -> {b}")
        else:
            func(*args)

    @property
    def vars(self):
        return tuple(self._vars)

    @property
    def w(self):
        return self._vars[VAR_W]

    @property
    def x(self):
        return self._vars[VAR_X]

    @property
    def y(self):
        return self._vars[VAR_Y]

    @property
    def z(self):
        return self._vars[VAR_Z]

    def inp(self, var, value):
        self._vars[var] = value

    def add(self, arg1, arg2, is_var):
        self._vars[arg1] += self._vars[arg2] if is_var else arg2

    def mul(self, arg1, arg2, is_var):
        self._vars[arg1] *= self._vars[arg2] if is_var else arg2

    def div(self, arg1, arg2, is_var):
        right = self._vars[arg2] if is_var else arg2
        self._vars[arg1] //= self._vars[arg2] if is_var else arg2

    def mod(self, arg1, arg2, is_var):
        left = self._vars[arg1]
        right = self._vars[arg2] if is_var else arg2
        self._vars[arg1] %= right

    def eql(self, arg1, arg2, is_var):
        compare_to = self._vars[arg2] if is_var else arg2
        self._vars[arg1] = int(self._vars[arg1] == compare_to)


class ALUProgram():
    def __init__(self):
        self.instructions = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def run(self, *args):
        alu = ALUEmulator()
        try:
            for instruction in self.instructions:
                args = instruction(alu, args)
        except IndexError:
            raise ALURuntimError("Not enough inputs provided for program")
        return alu.vars


class ALUCompiler:
    """The ALUCompiler can be used to translate ALU source code into
    a working ALU program."""

    def compile(self, src):
        """Compiles lines of source code into an ALU program."""
        program = ALUProgram()
        for line in src:
            src_line = line.strip()
            line = src_line
            if ";" in line:
                line = line[:line.index(";")]
            parts = line.lower().split()
            if not parts:
                continue

            instruction = None
            cmd = parts.pop(0)
            if cmd == "dbg":
                on_off = bool(parts.pop())
                instruction = self.make_dbg_instruction(src_line, on_off)
            elif cmd == "inp":
                var = self.get_var(line, parts)
                instruction = self.make_inp_instruction(src_line, var)
            elif cmd == "add":
                arg1 = self.get_var(line, parts)
                arg2, is_var = self.get_var_or_int(line, parts)
                instruction = self.make_add_instruction(src_line, arg1, arg2, is_var)
            elif cmd == "mul":
                arg1 = self.get_var(line, parts)
                arg2, is_var = self.get_var_or_int(line, parts)
                instruction = self.make_mul_instruction(src_line, arg1, arg2, is_var)
            elif cmd == "div":
                arg1 = self.get_var(line, parts)
                arg2, is_var = self.get_var_or_int(line, parts)
                instruction = self.make_div_instruction(src_line, arg1, arg2, is_var)
            elif cmd == "mod":
                arg1 = self.get_var(line, parts)
                arg2, is_var = self.get_var_or_int(line, parts)
                instruction = self.make_mod_instruction(src_line, arg1, arg2, is_var)
            elif cmd == "eql":
                arg1 = self.get_var(line, parts)
                arg2, is_var = self.get_var_or_int(line, parts)
                instruction = self.make_eql_instruction(src_line, arg1, arg2, is_var)
            else:
                raise ALUSyntaxError("Unknown operation:", line)
            if parts:
                raise ALUSyntaxError("Too many arguments:", line)

            program.add_instruction(instruction)

        return program

    def get_var_or_int(self, line, parts):
        try:
            value = int(parts[0])
            parts.pop(0)
            return value, False
        except (ValueError, IndexError):
            var = self.get_var(line, parts)
            return var, True

    def get_var(self, line, parts):
        if not parts:
            raise ALUSyntaxError("Missing argument(s):", line)
        name = parts.pop(0)
        if name == "w": return VAR_W
        if name == "x": return VAR_X
        if name == "y": return VAR_Y
        if name == "z": return VAR_Z
        raise ALUSyntaxError(f"Unknown variable name '{name}' used: {line}")

    def make_dbg_instruction(self, src_line, on_off):
        def instruction_(alu, args):
            alu.set_debug(on_off)
            return args
        return instruction_

    def make_inp_instruction(self, src_line, var):
        def instruction_(alu, args):
            value, args = args[0], args[1:]
            alu.exec(src_line, alu.inp, var, value)
            return args
        return instruction_

    def make_add_instruction(self, src_line, arg1, arg2, is_var):
        def instruction_(alu, args):
            alu.exec(src_line, alu.add, arg1, arg2, is_var)
            return args
        return instruction_

    def make_mul_instruction(self, src_line, arg1, arg2, is_var):
        def instruction_(alu, args):
            alu.exec(src_line, alu.mul, arg1, arg2, is_var)
            return args
        return instruction_

    def make_div_instruction(self, src_line, arg1, arg2, is_var):
        def instruction_(alu, args):
            alu.exec(src_line, alu.div, arg1, arg2, is_var)
            return args
        return instruction_

    def make_mod_instruction(self, src_line, arg1, arg2, is_var):
        def instruction_(alu, args):
            alu.exec(src_line, alu.mod, arg1, arg2, is_var)
            return args
        return instruction_

    def make_eql_instruction(self, src_line, arg1, arg2, is_var):
        def instruction_(alu, args):
            alu.exec(src_line, alu.eql, arg1, arg2, is_var)
            return args
        return instruction_
