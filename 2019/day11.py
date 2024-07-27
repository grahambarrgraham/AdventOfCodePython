import dataclasses
from collections import defaultdict
from pathlib import Path

from computer import Computer

TEST_MODE = True


@dataclasses.dataclass(frozen=True)
class Coord:
    x: int
    y: int


directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def phase1(code):
    map_ = defaultdict(int)
    paint(code, map_)
    return len(map_.keys())


def phase2(code):
    map_ = defaultdict(int)
    map_[Coord(0, 0)] = 1
    paint(code, map_)
    max_x = max([c.x for c in map_.keys()])
    max_y = max([c.y for c in map_.keys()])
    min_x = min([c.x for c in map_.keys()])
    min_y = min([c.y for c in map_.keys()])

    for y in range(min_y, max_y + 1, 1):
        for x in range(min_x, max_x + 1, 1):
            color = int(map_[Coord(x, y)])
            # print(x, y, color)
            print(' ' if color == 0 else '#', end='')
        print('')

    return "ABCLFUHJ"


def paint(code, map_):
    coord = Coord(0, 0)
    direction = 0
    computer = Computer(code)
    while not computer.halted:
        input_ = map_[coord]
        outputs = computer.compute([input_])
        map_[coord] = outputs[0]
        direction = ((direction + 1) if outputs[1] == 1 else (direction - 1 + len(directions))) % len(directions)
        coord = Coord(coord.x + directions[direction][0], coord.y + directions[direction][1])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day11_sample" if TEST_MODE else "input/day11").open() as f:
        values = [int(x) for x in [i.split(',') for i in f][0]]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
