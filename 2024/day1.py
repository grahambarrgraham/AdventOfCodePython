from collections import defaultdict
from pathlib import Path

TEST_MODE = False


def phase1(left, right):
    return sum((abs(a - b) for a, b in zip(sorted(left), sorted(right))))


def phase2(left, right):
    d = defaultdict(int)
    for i in right:
        d[i] += 1
    return sum(i * d[i] for i in left)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day1_sample" if TEST_MODE else "input/day1").open() as f:
        values = [i.split() for i in f]
        l_ = [int(a) for a, _ in values]
        r_ = [int(b) for _, b in values]
        print(f'Phase 1: {phase1(l_, r_)}')
        print(f'Phase 2: {phase2(l_, r_)}')


