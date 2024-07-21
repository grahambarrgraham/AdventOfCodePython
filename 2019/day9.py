from pathlib import Path

import day5

TEST_MODE = False


def phase1(code):
    outputs, _, _ = day5.calc(code, [] if TEST_MODE else [1])
    return outputs[-1]


def phase2(code):
    outputs, _, _ = day5.calc(code, [] if TEST_MODE else [2])
    return outputs[-1]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day9_sample" if TEST_MODE else "input/day9").open() as f:
        values = [int(x) for x in [i.split(',') for i in f][0]]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
