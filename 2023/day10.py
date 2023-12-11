import dataclasses
from pathlib import Path

TEST_MODE = False

all_neighbours_ = {(0, 1), (1, 0), (0, -1), (-1, 0)}

neighbour_map = {
    '.': {},
    'F': {(0, 1), (1, 0)},
    'L': {(0, -1), (1, 0)},
    '-': {(-1, 0), (1, 0)},
    '|': {(0, -1), (0, 1)},
    'J': {(0, -1), (-1, 0)},
    '7': {(0, 1), (-1, 0)},
    'S': all_neighbours_
}


@dataclasses.dataclass(frozen=True)
class Coord:
    x: int
    y: int


def phase1(m):
    found, parents = find_loop(m)
    return len(found) / 2


def phase2(m):
    _, parents = find_loop(m)
    start = find_start(m)
    loop = [c for c in loop_interator(start, parents)]
    b = len([x for x in loop])
    vertices = [(c.x, c.y) for c in loop if c not in ['-', '|']]
    vertices.append((start.x, start.y))
    area = polygon_area(vertices)
    # picks formula
    return area - b / 2 + 1


def polygon_area(vertices):  # shoelace formula
    num_vertices = len(vertices)
    sum1 = 0
    sum2 = 0

    for i in range(0, num_vertices - 1):
        sum1 = sum1 + vertices[i][0] * vertices[i + 1][1]
        sum2 = sum2 + vertices[i][1] * vertices[i + 1][0]

    # Add xn.y1
    sum1 = sum1 + vertices[num_vertices - 1][0] * vertices[0][1]
    # Add x1.yn
    sum2 = sum2 + vertices[0][0] * vertices[num_vertices - 1][1]

    area = abs(sum1 - sum2) / 2
    return area


def loop_interator(start, parents):
    p = start
    finished = False
    yield start
    while not finished:
        p = parents[p]
        if p != start:
            yield p
        else:
            finished = True


def pipe_neighbours(coord, map_) -> list[Coord]:
    ns = pipe_neighbours_(coord, map_)
    if map_[coord.y][coord.x] == 'S':
        ns = [n for n in ns if coord in pipe_neighbours_(n, map_)]
    return ns


def pipe_neighbours_(coord, map_) -> list[Coord]:
    max_ = Coord(len(map_[0]), len(map_))
    mapping = neighbour_map[symbol(coord, map_)]
    return neighbours(coord, mapping, max_)


def symbol(coord, map_):
    return map_[coord.y][coord.x]


def all_neighbours(coord, map_):
    max_ = Coord(len(map_[0]), len(map_))
    return neighbours(coord, all_neighbours_, max_)


def neighbours(coord, mapping, max_):
    all_ = [(n, Coord(coord.x + n[0], coord.y + n[1])) for n in mapping]
    all_in_map = [(n, c) for n, c in all_ if 0 <= c.x <= max_.x and 0 <= c.y <= max_.y]
    in_map_ = [c for n, c in all_in_map]
    return in_map_


def find_start(m) -> Coord:
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] == 'S':
                return Coord(x, y)
    return None


def find_loop(m):
    found = set()
    parents = {}
    start = find_start(m)
    queue = [start]
    last = None
    while len(queue) > 0:
        current = queue.pop()
        last = current
        found.add(current)
        ns = [n for n in pipe_neighbours(current, m) if n not in found]
        # queue.extend(ns)
        if len(ns) > 0:
            queue.append(ns[0])
        for n in ns:
            parents[n] = current
    parents[start] = last
    return found, parents


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day10_sample" if TEST_MODE else "input/day10").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
