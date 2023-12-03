import collections
from pathlib import Path
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")

Coord = collections.namedtuple("Coord", "x y")


def phase1(v):



    return -1


def phase2(v):
    return -1


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day3_sample" if TEST_MODE else "input/day3").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


