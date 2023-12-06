import dataclasses
import math
from functools import reduce
from pathlib import Path

TEST_MODE = False


@dataclasses.dataclass
class Race:
    time: int
    distance: int

    def __add__(self, other):
        def str_add(a, b):
            return int(str(a) + str(b))
        return Race(str_add(self.time, other.time), str_add(self.distance, other.distance))


def phase1(races):
    return math.prod([run(race) for race in races])


def phase2(races: list[Race]):
    return run(reduce(lambda a, b: a + b, races, Race(0, 0)))


def run(race) -> int:
    winning = False
    lower = 0
    while not winning:
        lower += 1
        winning = is_winning(lower, race)
    upper = race.time
    winning = False
    while not winning:
        upper -= 1
        winning = is_winning(upper, race)
    return upper - lower + 1


def is_winning(press_time, race):
    return press_time + (race.distance // press_time) < race.time


def parse_input(lines):
    times = lines[0].split()[1:]
    distances = lines[1].split()[1:]
    return [Race(int(v[0]), int(v[1])) for v in zip(times, distances)]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day6_sample" if TEST_MODE else "input/day6").open() as f:
        values = parse_input([i.strip() for i in f])
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
