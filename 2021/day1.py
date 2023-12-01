from pathlib import Path
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    previous = -1
    count = 0
    for i in range(len(v)):
        if -1 < previous < v[i]:
            count = count + 1
        previous = v[i]

    return count


def phase2(v):
    smoothed_list = [sum(item) for item in [values[i:i + 3] for i in range(0, len(values) - 2, 1)]]
    return phase1(smoothed_list)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day1_sample" if TEST_MODE else "input/day1").open() as f:
        values = [int(i) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


