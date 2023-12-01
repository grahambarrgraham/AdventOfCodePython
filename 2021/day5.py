from pathlib import Path
import sys
import re

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    return calc([interpolate(points[0], points[1]) for points in v if is_not_diagonal(points)])


def phase2(v):
    return calc([interpolate(points[0], points[1]) for points in v])


def is_not_diagonal(points):
    return points[0][0] == points[1][0] or points[1][1] == points[0][1]


def calc(v):
    intersect_dict = {}
    for line in v:
        for point in line:
            intersect_dict[point] = intersect_dict.get(point, 0) + 1
    return len([k for (k, v) in intersect_dict.items() if v > 1])


def interpolate(point_a, point_b):
    x_range = [x for x in inclusive_range(point_a[0], point_b[0])]
    y_range = [y for y in inclusive_range(point_a[1], point_b[1])]
    if len(x_range) == 1 or len(y_range) == 1:
        return set([(x, y) for x in x_range for y in y_range])
    else:
        return set(zip(x_range, y_range))


def inclusive_range(a: int, b: int):
    return range(a, b + 1) if a < b else range(a, b - 1, -1)


def load(raw):
    points = []
    for line in raw:
        matches = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line)
        point_a = (int(matches.group(1)), int(matches.group(2)))
        point_b = (int(matches.group(3)), int(matches.group(4)))
        points.append((point_a, point_b))
    return points


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day5_sample" if TEST_MODE else "input/day5").open() as f:
        data = load([line.rstrip("\n") for line in f])
        print(f'Phase 1: {phase1(data)}')
        print(f'Phase 2: {phase2(data)}')
