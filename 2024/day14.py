import re
from collections import defaultdict
from functools import reduce
from pathlib import Path

TEST_MODE = False

width, height = (11, 7) if TEST_MODE else (101, 103)


def phase1(pos_: dict[int, tuple], vel_: dict[int, tuple]):
    for s in range(100):
        move_robots(pos_, vel_)
    return reduce(lambda a, b: a * b, quadrants(group_by_position(pos_.values())).values(), 1)


def phase2(pos: dict[int, tuple], vel: dict[int, tuple]):
    seconds = 1
    while (not christmas_tree(pos)) and seconds < 200000:
        # print(seconds)
        move_robots(pos, vel)
        seconds += 1
    return seconds


def christmas_tree(pos):
    p = group_by_position(pos.values())

    x_buckets = defaultdict(int)
    for (x, y), count in p.items():
        x_buckets[x // (width // 3)] += count
    x_buckets = dict(sorted(x_buckets.items()))
    x_counts = list(x_buckets.values())[0:3]

    y_buckets = defaultdict(int)
    for (x, y), count in p.items():
        y_buckets[y // (height // 3)] += count
    y_buckets = dict(sorted(y_buckets.items()))
    y_counts = list(y_buckets.values())[0:3]

    middle_x = x_counts[2] * 1.4 < x_counts[1] > x_counts[0] * 1.4
    middle_y = y_counts[2] * 1.4 < y_counts[1] > y_counts[0] * 1.4

    return middle_x and middle_y


def quadrants(pos_count_map: dict[tuple, int]):
    result = defaultdict(int)
    for (x, y), count in pos_count_map.items():
        left, right = x < width // 2, x > width // 2
        bottom, top = y > height // 2, y < height // 2
        if top and left:
            result[0] += count
        elif top and right:
            result[1] += count
        elif bottom and right:
            result[2] += count
        elif bottom and left:
            result[3] += count
    return result


def group_by_position(pos: iter):
    p = defaultdict(int)
    for v in pos:
        p[v] += 1
    return p


def move_robots(pos, vel):
    for robot in range(len(pos)):
        x, y = pos[robot]
        v_x, v_y = vel[robot]
        nxt_x, nxt_y = (x + v_x) % width, (y + v_y) % height
        pos[robot] = (nxt_x, nxt_y)


def pretty_print(p):
    for y in range(height):
        for x in range(width):
            if (x, y) in p:
                print(p[(x, y)], end='')
            else:
                print('.', end='')
        print()


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day14_sample" if TEST_MODE else "input/day14").open() as f:
        values = [i.strip() for i in f]
        positions, velocities = {}, {}
        re_s = 'p=(-*\\d+),(-*\\d+) v=(-*\\d+),(-*\\d+)'
        for i, v in enumerate(values):
            m = re.match(re_s, v)
            positions[i] = (int(m.group(1)), int(m.group(2)))
            velocities[i] = (int(m.group(3)), int(m.group(4)))

        print(f'Phase 1: {phase1(positions.copy(), velocities)}')
        print(f'Phase 2: {phase2(positions.copy(), velocities)}')
