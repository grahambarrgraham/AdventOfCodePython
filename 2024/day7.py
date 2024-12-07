import functools
import itertools
from pathlib import Path
from time import time

TEST_MODE = False


def times(a, b):
    return a * b


def plus(a, b):
    return a + b


def concat(a, b):
    return int(str(a) + str(b))


def calculate(vals, ops):
    # always one less op than val
    current = ops[0](vals[0], vals[1])
    for i, op in enumerate(ops[1:]):
        current = op(current, vals[i + 2])
    return current


@functools.cache
def permutations_with_duplicates(ops, num):
    # this is generated from scratch for every equation, could re-use existing smaller sequences
    return list(itertools.product(ops, repeat=num))


def calibrate(answer, vals: list[int], all_ops):
    for ops in permutations_with_duplicates(all_ops, len(vals) - 1):
        c = calculate(vals, ops)
        if c == answer:
            return answer
    return 0


def phase1(v):
    return sum(calibrate(*equation, (plus, times)) for equation in v)


def phase2(v):
    return sum(calibrate(*equation, (plus, times, concat)) for equation in v)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day7_sample" if TEST_MODE else "input/day7").open() as f:
        values = [i.strip().split(': ') for i in f]
        values = [(int(a), [int(x) for x in b.split(' ')]) for a, b in values]
        now = time()
        print(f'Phase 1: {phase1(values)} {round(time() - now, 3)}s')
        print(f'Phase 2: {phase2(values)} {round(time() - now, 3)}s')
