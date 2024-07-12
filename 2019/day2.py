from copy import deepcopy
from pathlib import Path

TEST_MODE = False


def phase1(v):
    return calc(v, 12, 2)


def phase2(v):
    for noun in range(0, 100):
        for verb in range(0, 100):
            if calc(v, noun, verb) == 19690720:
                return (100 * noun) + verb
    return -1


def calc(v, noun, verb):
    code = deepcopy(v)
    index = 0
    if TEST_MODE is False:
        code[1] = noun
        code[2] = verb
    while index < len(code):
        op = code[index]
        if op == 99:
            break
        if op not in [1, 2]:
            exit(255)
        val = code[code[index + 1]] + code[code[index + 2]] if op == 1 else code[code[index + 1]] * code[code[index + 2]]
        code[code[index + 3]] = val
        index += 4
    return code[0]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day2_sample" if TEST_MODE else "input/day2").open() as f:
        values = [int(x) for x in [i.split(',') for i in f][0]]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


