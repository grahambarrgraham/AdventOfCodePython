from collections import defaultdict


class Computer:
    memory: dict
    pc: int = 0
    halted: bool = False
    relative_index = 0
    inputs = []

    def __init__(self, code):
        self.memory = defaultdict(int, dict(enumerate(code)))

    def compute(self, new_inputs: list):
        outputs = []
        self.inputs = self.inputs + new_inputs
        while True:
            op_str = str(self.memory[self.pc])
            op, modes = Computer.read_op(op_str)
            if op == 1:
                self.write(self.read_arg1(modes) + self.read_arg2(modes), self.pc + 3, modes[2])
                self.pc += 4
            elif op == 2:
                self.write(self.read_arg1(modes) * self.read_arg2(modes), self.pc + 3, modes[2])
                self.pc += 4
            elif op == 3:
                if len(self.inputs) > 0:
                    input_ = self.inputs.pop(0)
                    self.write(input_, self.pc + 1, modes[0])
                    self.pc += 2
                else:
                    break
            elif op == 4:
                outputs.append(self.read_arg1(modes))
                self.pc += 2
            elif op == 5:
                self.pc = self.read_arg2(modes) if self.read_arg1(modes) != 0 else self.pc + 3
            elif op == 6:
                self.pc = self.read_arg2(modes) if self.read_arg1(modes) == 0 else self.pc + 3
            elif op == 7:
                self.write(1 if self.read_arg1(modes) < self.read_arg2(modes) else 0, self.pc + 3, modes[2])
                self.pc += 4
            elif op == 8:
                self.write(1 if self.read_arg1(modes) == self.read_arg2(modes) else 0, self.pc + 3, modes[2])
                self.pc += 4
            elif op == 9:
                self.relative_index += self.read_arg1(modes)
                self.pc += 2
            elif op == 99:
                self.halted = True
                break
        return outputs

    def read_arg2(self, modes):
        return self.read(self.pc + 2, modes[1])

    def read_arg1(self, modes):
        return self.read(self.pc + 1, modes[0])

    def read(self, _index, mode):
        if mode == 'Immediate':
            return self.memory[_index]
        elif mode == 'Position':
            return self.memory[self.memory[_index]]
        else:
            return self.memory[self.memory[_index] + self.relative_index]

    def write(self, val, _index, mode='Position'):
        if mode == 'Position':
            self.memory[self.memory[_index]] = val
        elif mode == 'Relative':
            self.memory[self.memory[_index] + self.relative_index] = val
        else:
            exit(999)

    @staticmethod
    def read_op(param):
        def mode(val):
            if val == '0':
                return "Position"
            elif val == '1':
                return "Immediate"
            elif val == '2':
                return "Relative"
            else:
                exit(123)

        param = param.zfill(5)
        op = int(param[3] + param[4])
        modes = [mode(param[2]), mode(param[1]), mode(param[0])]
        return op, modes
