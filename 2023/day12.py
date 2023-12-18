from functools import cache
from pathlib import Path

TEST_MODE = False

# Memoization, Dynamic Programming, Pattern Matching

def phase1(v):
    acc = 0
    for lava, springs in v:
        acc += recurse(lava, springs)
    return acc


def phase2(v):
    acc = 0
    for lava, springs in v:
        springs = springs * 5
        lava = ('?'.join([lava] * 5))
        acc += recurse(lava, springs)
    return acc


# Couldn't solve part 2, solution below from Redit for easy reference
@cache
def recurse(lava, springs, result=0):
    if not springs:
        return '#' not in lava
    current, springs = springs[0], springs[1:]
    for i in range(len(lava) - sum(springs) - len(springs) - current + 1):
        if "#" in lava[:i]:
            break
        nxt = i + current
        if nxt <= len(lava) and '.' not in lava[i: nxt] and lava[nxt: nxt + 1] != "#":
            result += recurse(lava[nxt + 1:], springs)
    return result


def parse(line):
    lava, s = line.split()
    return lava, tuple(int(x) for x in s.split(','))


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day12_sample" if TEST_MODE else "input/day12").open() as f:
        values = [parse(i.strip()) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
        print('abcdef'[:3])
