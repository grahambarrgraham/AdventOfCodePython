from pathlib import Path

TEST_MODE = True


def phase1(v):
    return -1


def phase2(v):
    return -1


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/dayn_sample" if TEST_MODE else "input/dayn").open() as f:
        values = [int(i) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


