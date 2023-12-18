from copy import deepcopy
from pathlib import Path

TEST_MODE = False

# TAGS: file-blocks, transpose


def phase1(maps):
    return sum([calc(r, c) for r, c in process_maps(maps)])


def phase2(maps):
    smudged = [processed_smudged(m) for m in maps]
    return sum([calc(r, c) for r, c in smudged])


def processed_smudged(map_):
    def new_reflections(new_):
        a = new_[0] if baseline[0] != new_[0] else None
        b = new_[1] if baseline[1] != new_[1] else None
        if a is not None and b is not None:
            a = None if baseline[0] is None else a
            b = None if baseline[1] is None else b
        return a, b

    baseline = process_map(map_)

    for i, smudged in enumerate(smudger(map_)):
        next_ = process_map(smudged, baseline)
        r, c = new_reflections(next_)
        if r is not None or c is not None:
            return r, c
    return None


def process_maps(maps):
    return [process_map(m) for m in maps]


def process_map(map_, baseline=None):
    rows = finding_matching(map_)
    cols = finding_matching(transpose(map_))
    return process(map_, rows, cols, baseline)


def smudger(map_):
    for y in range(len(map_)):
        for x in range(len(map_[y])):
            m = deepcopy(map_)
            m[y][x] = '#' if m[y][x] == '.' else '.'
            yield m


def calc(h, v):
    h_score = 0 if h is None else (h + 1) * 100
    v_score = 0 if v is None else v + 1
    return h_score + v_score


def process(m, rows, cols, baseline):
    y_max = len(m) - 1
    x_max = len(m[0]) - 1
    rows.sort(key=lambda c: abs(c[0] - c[1]), reverse=True)
    cols.sort(key=lambda c: abs(c[0] - c[1]), reverse=True)
    row_exclude = None if baseline is None else baseline[0]
    col_exclude = None if baseline is None else baseline[1]
    row = find_reflection_index(rows, y_max, row_exclude)
    col = find_reflection_index(cols, x_max, col_exclude)
    return row, col


def at_edge(l_, max_):
    return len([_v for _v in l_ if _v[0] == 0 or _v[1] == max_]) > 0


def find_reflection_index(pairs, max_index, exclude):
    def expand(pair):
        if at_edge([pair], max_index):
            return True
        n = [x for x in pairs if pair[0] - x[0] == 1 and pair[1] - x[1] == -1]
        if len(n) == 0:
            return False
        return expand(n[0])

    candidates = [a for a in pairs if a[1] - a[0] == 1 and a[0] != exclude]
    for c in candidates:
        if expand(c):
            return c[0]

    return None


def transpose(v):
    return [list(x) for x in zip(*v)]


def finding_matching(_map):
    acc = []
    for i, r in enumerate(_map):
        for j in range(i + 1, len(_map)):
            if _map[i] == _map[j]:
                acc.append((i, j))
    return acc


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day13_sample" if TEST_MODE else "input/day13").open() as f:
        blocks = [[list(r) for r in block.split()] for block in f.read().split("\n\n")]
        print(f'Phase 1: {phase1(blocks)}')
        print(f'Phase 2: {phase2(blocks)}')
