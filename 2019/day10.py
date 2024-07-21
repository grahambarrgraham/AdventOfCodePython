import dataclasses
import math
from collections import defaultdict
from pathlib import Path
from typing import Generator

TEST_MODE = False


@dataclasses.dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __gt__(self, other):
        return self

    def manhattan(self, c):
        return abs(self.x - c.x) + abs(self.y - c.y)


def phase1(map_):
    asteroids = find_asteroids(map_)
    num_visible, _ = find_max_visible(asteroids)
    return num_visible


def phase2(map_):
    asteroids = find_asteroids(map_)
    _, start = find_max_visible(asteroids)
    asteroids.remove(start)
    angle_asteroid_map = defaultdict(list)

    for asteroid in asteroids:
        angle_asteroid_map[find_clock_degrees(start, asteroid)].append(asteroid)

    for k in angle_asteroid_map.keys():
        angle_asteroid_map[k] = sorted(set(angle_asteroid_map[k]), key=lambda c: start.manhattan(c))

    destroyed = []
    while len(angle_asteroid_map.keys()) > 0 and len(destroyed) < 200:
        for key in sorted(angle_asteroid_map.keys(), reverse=True):
            if len(angle_asteroid_map[key]) > 0:
                destroyed.append(angle_asteroid_map[key][0])
                angle_asteroid_map[key] = angle_asteroid_map[key][1:]
            else:
                del angle_asteroid_map[key]

    return destroyed[199].x * 100 + destroyed[199].y


def find_max_visible(asteroids):
    visible_asteroids = {asteroid: find_visible(asteroid, asteroids) for asteroid in asteroids}
    num_visible, location = max([(len(v), k) for k, v in visible_asteroids.items()])
    return num_visible, location


def find_asteroids(map_):
    asteroids = set()
    for y, line in enumerate(map_):
        for x, c in enumerate(line):
            if c == '#':
                asteroids.add(Coord(x, y))
    return asteroids


def find_visible(asteroid, asteroids) -> set[int]:
    return {a for a in asteroids if a != asteroid and is_visible(asteroid, a, asteroids)}


def is_visible(from_, to_, asteroids) -> float:
    for coord in intermediates(from_, to_):
        if coord in asteroids:
            return False
    return True


def find_clock_degrees(a, b):
    run, rise = a.x - b.x, a.y - b.y

    if run == 0 and rise > 0:
        return 360
    elif run == 0 and rise < 0:
        return 180
    else:
        m = rise / run
        degrees = math.atan(m) * (180 / math.pi)
        return (90 if run > 0 else 270) - degrees


def intermediates(a: Coord, b: Coord) -> Generator[Coord, None, None]:
    run, rise = a.x - b.x, a.y - b.y

    if run == 0:
        for y in range(min(a.y, b.y) + 1, max(a.y, b.y)):
            yield Coord(a.x, y)
    else:
        m = rise / run
        c = a.y - m * a.x
        for x in range(min(a.x, b.x) + 1, max(a.x, b.x)):
            y = (m * x) + c
            if math.isclose(y, round(y)):
                yield Coord(x, round(y))


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day10_sample" if TEST_MODE else "input/day10").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
