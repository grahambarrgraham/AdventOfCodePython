from pathlib import Path

TEST_MODE = False


class Computer:
    def __init__(self, registers, program):
        self.program = program
        self.registers = registers

    def run(self):

        pointer = 0
        out = []
        while pointer < len(self.program):
            a, b, c = self.registers
            if self.program[pointer] == 0:
                self.registers[0] = int(a / (2 ** self.combo(pointer)))
                pointer += 2
            elif self.program[pointer] == 1:
                self.registers[1] = b ^ self.literal(pointer)
                pointer += 2
            elif self.program[pointer] == 2:
                self.registers[1] = self.combo(pointer) % 8
                pointer += 2
            elif self.program[pointer] == 3:
                if a != 0:
                    pointer = self.literal(pointer)
                else:
                    pointer += 2
            elif self.program[pointer] == 4:
                self.registers[1] = b ^ c
                pointer += 2
            elif self.program[pointer] == 5:
                out.append(self.combo(pointer) % 8)
                pointer += 2
            elif self.program[pointer] == 6:
                self.registers[1] = int(a / (2 ** self.combo(pointer)))
                pointer += 2
            elif self.program[pointer] == 7:
                self.registers[2] = int(a / (2 ** self.combo(pointer)))
                pointer += 2
            else:
                raise "Invalid op"
        return out

    def literal(self, pointer):
        return self.program[pointer + 1]

    def combo(self, pointer):
        a, b, c = self.registers
        operand = self.literal(pointer)
        if operand == 4:
            operand = a
        elif operand == 5:
            operand = b
        elif operand == 6:
            operand = c
        elif operand == 7:
            raise "Invalid operand 7"
        return operand


def phase1(registers, program):
    computer = Computer(registers, program)
    out = computer.run()
    return ','.join(str(i) for i in out)


def phase2(registers, program):
    computer = Computer(registers, program)
    reg_a, digits = 3, 2
    in_registers, output = None, None

    def reg_gen(n):
        for i in range(n // 2):
            yield [n + i, 0, 0]

    while output != program:
        # brute force found [24, 0, 0] produces output [3,0], generate series from there
        register_gen = reg_gen(reg_a * 8)
        while output != program[-1 * digits:]:
            in_registers = next(register_gen)
            computer.registers = in_registers.copy()
            output = computer.run()
        print(in_registers, output)
        reg_a = in_registers[0]
        digits += 1

    return reg_a


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day17_sample" if TEST_MODE else "input/day17").open() as f:
        registers_, program_ = f.read().strip().split("\n\n")
        registers_ = [int(r[11:]) for r in registers_.split('\n')]
        program_ = [int(i) for i in program_[8:].split(",")]
        print(f'Phase 1: {phase1(registers_, program_)}')
        print(f'Phase 2: {phase2(registers_, program_)}')
