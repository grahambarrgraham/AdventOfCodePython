import itertools
from pathlib import Path
import sys
import re

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    extent = Cube((-50, 50), (-50, 50), (-50, 50), False)
    phase1_cubes = [c for c in v if extent.fully_contains(c)]
    return calc(phase1_cubes)


def phase2(v):
    return calc(v)


def calc(v):
    on_count = 0
    cubes = set()
    for cube in v:
        new_volume = cube.volume() if cube.is_on else 0
        for overlapping_cube, intercept in [v for v in [cube.intersect(c) for c in cubes] if v is not None]:
            new_volume -= intercept.volume()
            cubes.remove(overlapping_cube)
            blockify = overlapping_cube.blockify(intercept)
            cubes = cubes.union(blockify)
        if cube.is_on:
            cubes.add(cube)
        on_count += new_volume
    return on_count


class Cube:

    def __init__(self, x_range, y_range, z_range, on_flag):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.is_on = on_flag

    def calc_on(self, cubes):
        v = self.volume() if self.is_on else 0
        i = [self.intersect(c) for c in cubes]
        i2 = [pair[0].intersect(pair[2]) for pair in itertools.combinations(l, 2)]
        return v - sum([c.volume for c in i]) + sum([c.volume for c in ii])

    def volume(self):
        def dist(v_range):
            return abs(v_range[0] - v_range[1]) + 1

        return dist(self.x_range) * dist(self.y_range) * dist(self.z_range)

    def intersect(self, cube):
        def intersect_range(range1, range2):
            if max(range1) < min(range2) or max(range2) < min(range1):
                return None
            s = sorted([range1[0], range1[1], range2[0], range2[1]])
            return s[1], s[2]

        x = intersect_range(self.x_range, cube.x_range)
        if x is not None:
            y = intersect_range(self.y_range, cube.y_range)
            if y is not None:
                z = intersect_range(self.z_range, cube.z_range)
                if z is not None:
                    return cube, Cube(x, y, z, self.is_on and cube.is_on)
        return None

    def __repr__(self):
        return f"on={self.is_on} <x={self.x_range} y={self.y_range} z={self.z_range} vol={self.volume()}>"

    def fully_contains(self, c):
        def contains_range(range1, range2):
            return max(range1) >= max(range2) and min(range1) <= min(range2)

        return contains_range(self.x_range, c.x_range) and contains_range(self.y_range, c.y_range) and contains_range(
            self.z_range, c.z_range)

    def blockify(self, intercept):
        left = None if min(intercept.x_range) <= min(self.x_range) else \
            Cube((min(self.x_range), min(intercept.x_range) - 1), self.y_range, self.z_range, True)
        right = None if max(intercept.x_range) >= max(self.x_range) else \
            Cube((max(intercept.x_range) + 1, max(self.x_range)), self.y_range, self.z_range, True)
        bottom = None if min(intercept.y_range) <= min(self.y_range) else \
            Cube(intercept.x_range, (min(self.y_range), min(intercept.y_range) - 1), self.z_range, True)
        top = None if max(intercept.y_range) >= max(self.y_range) else \
            Cube(intercept.x_range, (max(intercept.y_range) + 1, max(self.y_range)), self.z_range, True)
        front = None if min(intercept.z_range) <= min(self.z_range) else \
            Cube(intercept.x_range, intercept.y_range, (min(self.z_range), min(intercept.z_range) - 1), True)
        back = None if max(intercept.z_range) >= max(self.z_range) else \
            Cube(intercept.x_range, intercept.y_range, (max(intercept.z_range) + 1, max(self.z_range)), True)
        resp = [c for c in [left, right, top, bottom, back, front] if c is not None]
        resp_ = [c.volume() for c in resp]
        return resp


def parse(v) -> Cube:
    def load_instr(instruction):
        m = re.match(r"(.)=(-*\d+)\.\.(-*\d+)", instruction)
        return min(int(m.group(2)), int(m.group(3))), max(int(m.group(2)), int(m.group(3)))

    a = v.split(' ')
    ranges = [load_instr(l.strip()) for l in a[1].split(',')]
    return Cube(ranges[0], ranges[1], ranges[2], a[0] == 'on')


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day22_sample" if TEST_MODE else "input/day22").open() as f:
        values = [parse(i.strip()) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
