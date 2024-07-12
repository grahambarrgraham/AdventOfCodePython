from collections import defaultdict
from pathlib import Path

TEST_MODE = False


def phase1(v):
    wire_1, wire_2 = v
    intercepts = find_all_intercepts(wire_1, wire_2)
    manhattan = sorted(v for v in {abs(a) + abs(b) for a, b in intercepts} if v > 0)
    return manhattan[0]


def phase2(v):
    wire_1 = v[0]
    wire_2 = v[1]
    intercepts = [i for i in find_all_intercepts(wire_1, wire_2) if i != (0, 0)]
    print(intercepts)
    wire_1_steps = [steps(wire_1, intercept) for intercept in intercepts]
    wire_2_steps = [steps(wire_2, intercept) for intercept in intercepts]
    print(wire_1_steps, wire_2_steps)
    all_steps = sorted([a + b for a, b in zip(wire_1_steps, wire_2_steps)])
    return all_steps[0]


def steps(wire, intercept):
    i_x, i_y = intercept
    x = y = 0
    steps = 0
    for instr in wire:
        _dir = instr[0]
        count = int(instr[1:])
        if _dir == 'R':
            if y == i_y and x <= i_x <= x + count:
                return steps + i_x - x
            x = x + count
        elif _dir == 'L':
            if y == i_y and x - count <= i_x <= x:
                return steps + x - i_x
            x = x - count
        elif _dir == 'U':
            if x == i_x and y <= i_y <= y + count:
                return steps + i_y - y
            y = y + count
        elif _dir == 'D':
            if x == i_x and y - count <= i_y <= y:
                return steps + y - i_y
            y = y - count
        steps += count
    return steps


def find_all_intercepts(wire_1, wire_2):
    rows_1, cols_1 = find_segments(wire_1)
    rows_2, cols_2 = find_segments(wire_2)
    intercepts = []
    intercepts.extend(find_intercepts(rows_1, cols_2))
    intercepts.extend(find_intercepts(rows_2, cols_1))
    return intercepts


def in_seq(v, seqs):
    result = []
    for a, b in seqs:
        if a <= v <= b:
            result.append(v)
    return result


def find_intercepts(rows, cols):
    intercepts = []
    for y, x_seqs in rows.items():
        x_s = [x for x in cols.keys() if in_seq(x, x_seqs)]
        for x in x_s:
            y_s = in_seq(y, cols[x])
            intercepts.extend([(x, y) for y in y_s])
    return intercepts


def find_segments(wire) -> (dict, dict):
    rows = defaultdict(list)
    cols = defaultdict(list)
    x = y = 0
    for instr in wire:
        _dir = instr[0]
        count = int(instr[1:])
        if _dir == 'R':
            rows[y].append((x, x + count))
            x = x + count
        elif _dir == 'L':
            rows[y].append((x - count, x))
            x = x - count
        elif _dir == 'U':
            cols[x].append((y, y + count))
            y = y + count
        elif _dir == 'D':
            cols[x].append((y - count, y))
            y = y - count
    return rows, cols


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day3_sample" if TEST_MODE else "input/day3").open() as f:
        values = [i.split(',') for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
