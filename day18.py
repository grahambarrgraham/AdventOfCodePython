from pathlib import Path
import collections

TEST_MODE = False

Cube = collections.namedtuple("Cube", "x y z")


def planar_dict(tup, di):
    for a, b in tup:
        di.setdefault(a, []).append(b)
    return di


def planar_indexes(v):
    xy = planar_dict(([((c.x, c.y), c.z) for c in v]), {})
    xz = planar_dict(([((c.x, c.z), c.y) for c in v]), {})
    yz = planar_dict(([((c.y, c.z), c.x) for c in v]), {})
    return xy, xz, yz


def phase1(v):
    xy, xz, yz = planar_indexes(v)

    def faces_showing(c: Cube) -> int:
        xy_count = len([n for n in xy[(c.x, c.y)] if n == c.z + 1 or n == c.z - 1])
        xz_count = len([n for n in xz[(c.x, c.z)] if n == c.y + 1 or n == c.y - 1])
        yz_count = len([n for n in yz[(c.y, c.z)] if n == c.x + 1 or n == c.x - 1])
        return 6 - xy_count - xz_count - yz_count

    return sum([faces_showing(c) for c in v])


def phase2(v):
    xy, xz, yz = planar_indexes(v)
    fully_enclosed = set()

    def find_neighbours(c: Cube, visited):
        six = [Cube(c.x + 1, c.y, c.z), Cube(c.x - 1, c.y, c.z),
               Cube(c.x, c.y + 1, c.z), Cube(c.x, c.y - 1, c.z),
               Cube(c.x, c.y, c.z + 1), Cube(c.x, c.y, c.z - 1)]
        return [n for n in six if n not in visited and n not in v]

    def is_enclosed(c: Cube):
        if c in fully_enclosed:
            return True
        q = collections.deque()
        visited = set()
        neighbours = find_neighbours(c, visited)
        q.extend(neighbours)
        while len(q) > 0:
            n = q.popleft()
            if n in fully_enclosed:
                return True
            if n in visited:
                continue
            visited.add(n)
            if (n.x, n.y) not in xy or (n.y, n.z) not in yz or (n.x, n.z) not in xz:
                return False
            q.extend(find_neighbours(n, visited))
        fully_enclosed.update(visited)
        return True

    def faces_showing(c: Cube) -> int:
        xy_count = len([n for n in xy[(c.x, c.y)] if n == c.z + 1 or n == c.z - 1])
        xz_count = len([n for n in xz[(c.x, c.z)] if n == c.y + 1 or n == c.y - 1])
        yz_count = len([n for n in yz[(c.y, c.z)] if n == c.x + 1 or n == c.x - 1])
        enclosed_faces = len([n for n in find_neighbours(c, {}) if is_enclosed(n)])
        return 6 - xy_count - xz_count - yz_count - enclosed_faces

    return sum([faces_showing(c) for c in v])


def parse(line):
    v = line.split(",")

    def int_val(i):
        return int(v[i].strip())

    return Cube(int_val(0), int_val(1), int_val(2))


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day18_sample" if TEST_MODE else "input/day18").open() as f:
        values = [parse(i) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
