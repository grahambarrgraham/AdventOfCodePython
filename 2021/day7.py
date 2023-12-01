from pathlib import Path
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    return calc(v, lambda a: a)


def phase2(v):

    cost_dict = {}

    def cost(a):
        if a not in cost_dict:
            cost_dict[a] = sum([i + 1 for i in range(a)])
        return cost_dict[a]

    return calc(v, cost)


def calc(v, cost_per_move):
    return min([sum([cost_per_move(abs(horiz_pos - sub_pos)) for sub_pos in v]) for horiz_pos in range(v[0], v[-1])])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day7_sample" if TEST_MODE else "input/day7").open() as f:
        values = sorted([[int(j) for j in i.split(",")] for i in f][0])
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
