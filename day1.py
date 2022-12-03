import copy
from pathlib import Path


TEST_MODE = False


def phase1(v):
    return calc(v)[0]


def phase2(v):
    return sum(calc(v)[0:3])


def calc(v):
    return sorted([sum(s) for s in v], reverse=True)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day1_sample" if TEST_MODE else "input/day1").open() as f:
        values = [map(lambda x: int(x), line.split("\n")) for line in f.read().split("\n\n")]
        print(f'Phase 1: {phase1(copy.deepcopy(values))}')
        print(f'Phase 2: {phase2(copy.deepcopy(values))}')
