import dataclasses
import itertools
import math
import re
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

TEST_MODE = False


@dataclasses.dataclass(unsafe_hash=True)
class Vector:
    x: int
    y: int
    z: int

    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def gravity_effect(self, other):

        def change(a, b):
            return 1 if a < b else -1 if a > b else 0

        return Vector(change(self.x, other.x), change(self.y, other.y), change(self.z, other.z))

    def copy(self):
        return Vector(self.x, self.y, self.z)

    def __lt__(self, other):
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)


@dataclasses.dataclass(unsafe_hash=True)
class Moon:
    pos: Vector

    def __init__(self, pos: Vector):
        self.pos = pos
        self.initial_pos = pos.copy()
        self.vel: Vector = Vector(0, 0, 0)

    def energy(self):
        return self.pos.energy() * self.vel.energy()

    def move(self):
        self.pos += self.vel

    def apply_gravity(self, moon):
        self.vel += self.pos.gravity_effect(moon.pos)

    def is_initial_state(self, dim):
        if dim == 'x':
            return self.pos.x == self.initial_pos.x and self.vel.x == 0
        elif dim == 'y':
            return self.pos.y == self.initial_pos.y and self.vel.y == 0
        elif dim == 'z':
            return self.pos.z == self.initial_pos.z and self.vel.z == 0


def phase1(moons: list[Moon]):

    for step in range(100 if TEST_MODE else 1000):

        moon_pairs = itertools.combinations(moons, 2)
        for moon_a, moon_b in moon_pairs:
            moon_a.apply_gravity(moon_b)
            moon_b.apply_gravity(moon_a)

        for moon in moons:
            moon.move()

    return sum([moon.energy() for moon in moons])


def phase2(moons):

    moon_dimension_repeat_steps = defaultdict(list)
    step = 1
    while step < 900000:

        moon_pairs = itertools.combinations(moons, 2)
        for moon_a, moon_b in moon_pairs:
            moon_a.apply_gravity(moon_b)
            moon_b.apply_gravity(moon_a)

        for moon in moons:
            moon.move()

            if moon.is_initial_state('x'):
                moon_dimension_repeat_steps[(moon.initial_pos, 'x')].append(step)

            if moon.is_initial_state('y'):
                moon_dimension_repeat_steps[(moon.initial_pos, 'y')].append(step)

            if moon.is_initial_state('z'):
                moon_dimension_repeat_steps[(moon.initial_pos, 'z')].append(step)

        step += 1

    moon_periods = set()
    for key in moon_dimension_repeat_steps.keys():
        pattern = find_repeated_pattern(list(pairwise_differences(moon_dimension_repeat_steps[key])))
        moon_periods.add(sum(pattern))

    return math.lcm(*moon_periods)


def find_repeated_pattern(intervals):
    size = 1
    while size <= len(intervals) - size:

        match = False

        template = intervals[0:size]
        for i in range(size, len(intervals) - size + 1, size):
            nxt = intervals[i:i + size]
            match = nxt == template
            if not match:
                break
        size += 1
        if match:
            return template
    return None


def pairwise_differences(list_):
    for i in range(1, len(list_)):
        yield list_[i] - list_[i - 1]


def load(raw) -> Moon:
    matches = re.match(r"<x=(-*\d+), y=(-*\d+), z=(-*\d+)>", raw)
    return Moon(Vector(int(matches.group(1)), int(matches.group(2)), int(matches.group(3))))


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day12_sample" if TEST_MODE else "input/day12").open() as f:
        data = [load(line.rstrip("\n")) for line in f]
        print(f'Phase 1: {phase1(deepcopy(data))}')
        print(f'Phase 2: {phase2(deepcopy(data))}')

