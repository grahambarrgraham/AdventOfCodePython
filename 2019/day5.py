from pathlib import Path

from computer import Computer

TEST_MODE = False


def phase1(code):
    outputs = Computer(code).compute([1])
    return outputs[-1]


def phase2(code):
    outputs = Computer(code).compute([5])
    return outputs[-1]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day5_sample" if TEST_MODE else "input/day5").open() as f:
        values = [int(x) for x in [i.split(',') for i in f][0]]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
