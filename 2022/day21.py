
from pathlib import Path


TEST_MODE = False


class Operation:

    def __init__(self, val, a=None, b=None, op=None):
        self.a = a
        self.b = b
        self.op = op
        self.val = val
        self.op_a = None
        self.op_b = None

    def __repr__(self):
        return f"{self.val}" if self.val is not None else f"{self.a} {self.op} {self.b}"

    def calc(self, monkey_dict):
        if self.val is not None:
            return self.val
        else:
            self.op_a = monkey_dict[self.a].calc(monkey_dict)
            self.op_b = monkey_dict[self.b].calc(monkey_dict)
            if self.op == '*':
                return self.op_a * self.op_b
            elif self.op == '+':
                return self.op_a + self.op_b
            elif self.op == '-':
                return self.op_a - self.op_b
            elif self.op == '/':
                return self.op_a / self.op_b
            elif self.op == '=':
                return self.op_a == self.op_b


def phase1(v):
    return int(v['root'].calc(v))


def phase2(v):
    root = v['root']
    root.op = '='

    exponent = 16
    range_end = 10 ** exponent
    range_start = range_end * -1

    while True:
        step = 10 ** (exponent - 2)
        previous_diff = None

        for i in range(range_start, range_end, step):
            v['humn'].val = i
            root_result = root.calc(v)
            if root_result is True:
                return v['humn'].val

            current_diff = root.op_a - root.op_b

            if previous_diff is None:
                previous_diff = current_diff
                continue
            if have_different_sign(current_diff, previous_diff):
                range_start = i - step
                range_end = i
                exponent -= 2
                break
            previous_diff = current_diff


def have_different_sign(a, b):
    return b < 0 < a or b > 0 > a


def parse(line):
    name, instruction = line.split(':')
    parts = instruction.strip().split()
    if len(parts) == 1:
        return name, Operation(int(parts[0].strip()))
    else:
        return name, Operation(None, parts[0], parts[2], parts[1])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day21_sample" if TEST_MODE else "input/day21").open() as f:
        values = dict([parse(i) for i in f])
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


