import re
from pathlib import Path

LEN_XMAS = len("XMAS")

TEST_MODE = False


def diagonals(v, len_=LEN_XMAS):
    results = []
    for y in range(len(v) - len_, 0, -1):
        diagonal = ''
        for i, y1 in enumerate(range(y, len(v))):
            diagonal += v[y1][i]
        results.append(diagonal)
    for x in range(len(v[0]) - len_ + 1):
        diagonal = ''
        for i, x1 in enumerate(range(x, len(v[0]))):
            diagonal += v[i][x1]
        results.append(diagonal)
    return results


def transpose(v):
    return [''.join([row[i] for row in v]) for i in range(len(v[0]))]


def backwards(v):
    return [s[::-1] for s in v]


def blocks(v):
    for x in range(0, len(v[0]) - 2):
        for y in range(0, len(v) - 2):
            yield [v[y + i][x:x + 3] for i in range(3)]


def phase1(v):
    all_strings = v + diagonals(v) + transpose(v) + diagonals(backwards(v))
    all_strings += backwards(all_strings)
    return sum(len(re.findall("XMAS", string)) for string in all_strings)


def phase2(v):
    crosses = [(diagonals(block, 3)[0], diagonals(backwards(block), 3)[0]) for block in blocks(v)]
    xmas_crosses = [(a, b) for a, b in crosses if a in ['MAS', 'SAM'] and b in ['MAS', 'SAM']]
    return len(xmas_crosses)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day4_sample" if TEST_MODE else "input/day4").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
