import collections
import itertools
from pathlib import Path

TEST_MODE = False

Coord = collections.namedtuple("Coord", "x y")


def phase1(v):
    return process(v, 2)


def phase2(v):
    return process(v, 1000000)


def process(v, factor):
    warp_rows = find_warp_rows(v)
    warp_cols = find_warp_cols(v)
    stars = find_stars(v)
    pairs = itertools.combinations(stars, 2)
    paths = [shortest_path(warp_cols, warp_rows, *pair, factor=factor) for pair in pairs]
    return sum(paths)


def between(a, b, c):
    return max(a, b) > c > min(a, b)


def distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def shortest_path(warp_cols, warp_rows, a, b, factor):
    warp_col_count = len([c for c in warp_cols if between(a.x, b.x, c)])
    warp_row_count = len([c for c in warp_rows if between(a.y, b.y, c)])
    plus_cols = (warp_col_count * factor) - warp_col_count
    plus_rows = (warp_row_count * factor) - warp_row_count
    return distance(a, b) + plus_rows + plus_cols


def find_stars(v):
    for y in range(len(v)):
        for x in range(len(v[0])):
            if v[y][x] == '#':
                yield Coord(x, y)


def find_warp_cols(v):
    warp_col = set()
    a = transpose(v)
    for y, l in enumerate(a):
        if '#' not in l:
            warp_col.add(y)
    return warp_col


def find_warp_rows(v):
    warp_row = set()
    for y, l in enumerate(v):
        if '#' not in l:
            warp_row.add(y)
    return warp_row


def transpose(v):
    return [list(x) for x in zip(*v)]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day11_sample" if TEST_MODE else "input/day11").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
