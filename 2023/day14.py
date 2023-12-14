import collections
import time
from copy import deepcopy
from pathlib import Path

TEST_MODE = False

Coord = collections.namedtuple("Coord", "x y")


def phase1(v):
    blocks = {c for c in coords(v) if v[c.y][c.x] == 'O'}
    blocks, m = apply_tilt(v, blocks, 'n')
    return score(m)


def phase2(v):
    blocks = {c for c in coords(v) if v[c.y][c.x] == 'O'}
    b = tuple(blocks)

    block_cache = dict()
    m = deepcopy(v)

    # settles to a repeat ever 7 cycles after, so can extrapolate to 1000000000
    for i in range(1000):

        if b not in block_cache:

            for tilt in ['n', 'w', 's', 'e']:
                apply_tilt(m, blocks, tilt)

            block_cache[b] = (frozenset(blocks), deepcopy(m))
            b = frozenset(blocks)

        else:
            b, m = block_cache[b]
            blocks = set(b)

    return score(m)


def print_map(m):
    print()
    for a in m:
        print(a)


def score(m):
    val = len(m)
    acc = 0
    for row in m:
        n = len([c for c in row if c == 'O'])
        acc += n * val
        val -= 1
    return acc


def apply_tilt(m, blocks, tilt):
    n_s = tilt in ['n', 's']
    s_e = tilt in ['s', 'e']
    it = sorted(blocks, key=lambda n: n.y if n_s else n.x, reverse=s_e)
    for c in it:
        lowest = find_lowest(c, m, tilt)
        if lowest != c:
            m = move_to_lowest(c, lowest, m)
            blocks.remove(c)
            blocks.add(lowest)
    return blocks, m


def find_lowest(c: Coord, m: list, tilt):
    n_s = tilt in ['n', 's']
    n_w = tilt in ['n', 'w']
    axis = c.y if n_s else c.x
    extent = 0 if n_w else len(m) - 1
    y_step = -1 if tilt == 'n' else 1 if tilt == 's' else 0
    x_step = -1 if tilt == 'w' else 1 if tilt == 'e' else 0
    step = y_step if x_step == 0 else x_step

    def next_coord(x, y):
        return m[y + y_step][x + x_step]

    if axis == extent or next_coord(c.x, c.y) != '.':
        return c

    furthest = axis

    for i in range(axis, extent, step):
        nc = next_coord(c.x, i) if n_s else next_coord(i, c.y)
        if nc != '.':
            break
        furthest = i + step

    return Coord(c.x, furthest) if n_s else Coord(furthest, c.y)


def move_to_lowest(c, lowest, m):
    m[lowest.y][lowest.x] = 'O'
    m[c.y][c.x] = '.'
    return m


def coords(m: list):
    for y in range(len(m)):
        for x in range(len(m[0])):
            yield Coord(x, y)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day14_sample" if TEST_MODE else "input/day14").open() as f:
        values = [list(i.strip()) for i in f]
        p2values = deepcopy(values)
        st = time.time()
        phase1 = phase1(values)
        p1_time = time.time()
        print(f'Phase 1: {phase1} {round(p1_time - st, 3)}s')
        phase2 = phase2(p2values)
        p2_time = time.time()
        print(f'Phase 2: {phase2} {round(p2_time - p1_time, 3)}s')
