from pathlib import Path
import sys

TEST_MODE = False

shape = {'X': 1, 'Y': 2, 'Z': 3}

win = {('A', 'X'): 3, ('A', 'Y'): 6, ('A', 'Z'): 0,
       ('B', 'X'): 0, ('B', 'Y'): 3, ('B', 'Z'): 6,
       ('C', 'X'): 6, ('C', 'Y'): 0, ('C', 'Z'): 3}

strategy = {('A', 'X'): ('A', 'Z'), ('A', 'Y'): ('A', 'X'), ('A', 'Z'): ('A', 'Y'),
            ('B', 'X'): ('B', 'X'), ('B', 'Y'): ('B', 'Y'), ('B', 'Z'): ('B', 'Z'),
            ('C', 'X'): ('C', 'Y'), ('C', 'Y'): ('C', 'Z'), ('C', 'Z'): ('C', 'X')}


def phase1(v):
    return calc(v)


def phase2(v):
    return calc(map(lambda x: strategy[x], v))


def calc(v):
    return sum([win[i] + shape[i[1]] for i in v])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day2_sample" if TEST_MODE else "input/day2").open() as f:
        values = [tuple(i.strip().split(' ')) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
