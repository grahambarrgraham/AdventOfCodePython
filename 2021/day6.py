from pathlib import Path
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    return calc(v, 80)


def phase2(v):
    return calc(v, 256)


def calc(v, days):
    fish_dict = {}
    for fish in v:
        fish_dict[fish] = fish_dict.get(fish, 0) + 1

    for i in range(days):
        next_gen = {}
        for fish in sorted(fish_dict.keys(), reverse=True):
            if fish == 0:
                next_gen[6] = fish_dict.get(0, 0) + next_gen.get(6, 0)
                next_gen[8] = fish_dict.get(0, 0)
            else:
                next_gen[fish - 1] = fish_dict.get(fish, 0)

        fish_dict = next_gen

    return sum([v for v in fish_dict.values()])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day6_sample" if TEST_MODE else "input/day6").open() as f:
        values = [[int(j) for j in i.split(",")] for i in f][0]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


