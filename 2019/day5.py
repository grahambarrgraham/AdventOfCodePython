from copy import deepcopy
from pathlib import Path

TEST_MODE = False


def phase1(v):
    outputs = calc(v, [1])
    return outputs[-1]


def phase2(v):
    outputs = calc(v, [5])
    return outputs[-1]


def read_op(param):
    def mode(val):
        return "Immediate" if val == '1' else "Position"

    param = param.zfill(4)
    op = int(param[3])
    modes = [mode(param[1]), mode(param[0])]
    return op, modes


def calc(v, inputs, reset=True):
    code = deepcopy(v) if reset else v

    def value_at(_index, mode):
        return code[_index] if mode == 'Immediate' else code[code[_index]]

    input_index = 0
    index = 0
    outputs = []
    halted = False
    while index < len(code):
        op, modes = read_op(str(code[index]))
        if op == 1:
            code[code[index + 3]] = value_at(index + 1, modes[0]) + value_at(index + 2, modes[1])
            index += 4
        elif op == 2:
            code[code[index + 3]] = value_at(index + 1, modes[0]) * value_at(index + 2, modes[1])
            index += 4
        elif op == 3:
            code[code[index + 1]] = inputs[input_index]
            index += 2
            input_index += 1
        elif op == 4:
            outputs.append(value_at(index + 1, modes[0]))
            index += 2
        elif op == 5:
            index = value_at(index + 2, modes[1]) if value_at(index + 1, modes[0]) != 0 else index + 3
        elif op == 6:
            index = value_at(index + 2, modes[1]) if value_at(index + 1, modes[0]) == 0 else index + 3
        elif op == 7:
            code[code[index + 3]] = 1 \
                if value_at(index + 1, modes[0]) < value_at(index + 2, modes[1]) else 0
            index += 4
        elif op == 8:
            code[code[index + 3]] = 1 \
                if value_at(index + 1, modes[0]) == value_at(index + 2, modes[1]) else 0
            index += 4
        elif op == 9:
            halted = True
            break
    return outputs, halted


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day5_sample" if TEST_MODE else "input/day5").open() as f:
        values = [int(x) for x in [i.split(',') for i in f][0]]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
