from collections import defaultdict
from pathlib import Path

TEST_MODE = False


def phase1(stones):
    return blink(25, stones)


def phase2(stones):
    return blink(75, stones)


def transform(stone):
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        stone_str = str(stone)
        half = len(stone_str) // 2
        return [int(stone_str[:half]), int(stone_str[half:])]
    else:
        return [stone * 2024]


def blink(num_blinks, v):
    stones = {s: 1 for s in v}
    for i in range(num_blinks):
        new_stones = defaultdict(int)
        for stone, count in stones.items():
            for transformed in transform(stone):
                new_stones[transformed] += count

        stones = new_stones
    return sum(stones.values())


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day11_sample" if TEST_MODE else "input/day11").open() as f:
        values = [int(i) for i in f.readline().strip().split()]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
