from collections import defaultdict
from copy import deepcopy
from pathlib import Path

TEST_MODE = False


def phase1(code):
    outputs, _, _ = calc(deepcopy(code), [1])
    return outputs[-1]


def phase2(code):
    outputs, _, _ = calc(deepcopy(code), [5])
    return outputs[-1]


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


def calc(code, inputs, index=0):
    input_index = 0
    outputs = []
    halted = False
    relative_index = 0
    memory = defaultdict(int, dict(enumerate(code)))

    def read(_index, mode):
        if mode == 'Immediate':
            return memory[_index]
        elif mode == 'Position':
            return memory[memory[_index]]
        else:
            return memory[memory[_index] + relative_index]

    def write(val, _index, mode='Position'):
        if mode == 'Position':
            memory[memory[_index]] = val
        elif mode == 'Relative':
            memory[memory[_index] + relative_index] = val
        else:
            exit(999)

    while index < len(memory):
        op_str = str(memory[index])
        op, modes = read_op(op_str)
        if op == 1:
            write(read(index + 1, modes[0]) + read(index + 2, modes[1]), index + 3, modes[2])
            index += 4
        elif op == 2:
            write(read(index + 1, modes[0]) * read(index + 2, modes[1]), index + 3, modes[2])
            index += 4
        elif op == 3:
            if input_index < len(inputs):
                input_ = inputs[input_index]
                write(input_, index + 1, modes[0])
                index += 2
                input_index += 1
            else:
                break
        elif op == 4:
            outputs.append(read(index + 1, modes[0]))
            index += 2
        elif op == 5:
            index = read(index + 2, modes[1]) if read(index + 1, modes[0]) != 0 else index + 3
        elif op == 6:
            index = read(index + 2, modes[1]) if read(index + 1, modes[0]) == 0 else index + 3
        elif op == 7:
            write(1 if read(index + 1, modes[0]) < read(index + 2, modes[1]) else 0, index + 3, modes[2])
            index += 4
        elif op == 8:
            write(1 if read(index + 1, modes[0]) == read(index + 2, modes[1]) else 0, index + 3, modes[2])
            index += 4
        elif op == 9:
            relative_index += read(index + 1, modes[0])
            index += 2
        elif op == 99:
            halted = True
            break
    return outputs, halted, index


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day5_sample" if TEST_MODE else "input/day5").open() as f:
        values = [int(x) for x in [i.split(',') for i in f][0]]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
