from pathlib import Path
import sys
import math

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    minima = []
    for y, line in enumerate(v):
        for x, height in enumerate(line):
            coords = neighbours((x, y), v)
            if height < min([v[b][a] for a, b in coords]):
                minima.append(height + 1)
    return sum(minima)


def phase2(v):
    seen_list = set()
    basins = [basin((x, y), v, seen_list) for y in range(len(v)) for x in range(len(v[0]))]
    basins = sorted(basins, reverse=True, key=len)[0:3]
    return math.prod([len(b) for b in basins])


def neighbours(coord, v):
    (x, y) = coord
    return [(x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1)] if
            len(v[0]) > x + a >= 0 and len(v) > y + b >= 0]


def basin(coord, v, seen):
    (x, y) = coord

    if v[y][x] == 9 or coord in seen:
        return []

    seen.add(coord)
    collector = [coord]
    for neighbour in neighbours(coord, v):
        if neighbour not in seen:
            collector = collector + basin(neighbour, v, seen)

    return collector


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day9_sample" if TEST_MODE else "input/day9").open() as f:
        values = [[int(j) for j in list(i.strip())] for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
