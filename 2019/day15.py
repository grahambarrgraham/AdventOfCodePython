import dataclasses
import astar

from collections import defaultdict
from pathlib import Path
from computer import Computer

TEST_MODE = False


@dataclasses.dataclass(frozen=True)
class Coord:
    x: int
    y: int


directions = {(1, 0): 3, (0, 1): 1, (-1, 0): 4, (0, -1): 2}


def phase1(code):
    map_ = defaultdict(int)
    target = discover_target(code, map_)
    path = search(map_, target)
    return len(path) - 1


def phase2(code):
    map_ = defaultdict(int)
    target = discover_target(code, map_)
    map_[target] = 3  # make the target appear visited multiple times, allows map to be fully explored.
    discover_target(code, map_)

    fill_count = 0
    visited = {target}
    fill_list = [target]

    while len(fill_list) > 0:
        neighbours = set()
        for c in fill_list:
            nxt = {n for n in find_neighbours(map_, c) if n not in visited}
            neighbours = neighbours.union(nxt)
        fill_list = list(neighbours)
        visited = visited.union(neighbours)
        if len(fill_list) > 0:
            fill_count += 1

    return fill_count


def discover_target(code, map_):
    computer = Computer(code)
    coord = Coord(0, 0)
    map_[coord] = 1
    while True:
        new_coord, direction = pick_direction(map_, coord)
        outputs = computer.compute([direction])
        if outputs[0] == 2:
            map_[new_coord] = -2
            return new_coord
        elif outputs[0] == 0:
            map_[new_coord] = -1
        else:
            coord = new_coord
            map_[coord] += 1


def pick_direction(map_, coord: Coord):
    coords = find_neighbours(map_, coord)
    coord = sorted(coords.keys(), key=lambda c: map_[c])[0]
    return coord, directions[coords[coord]]


def find_neighbours(map_, coord: Coord):
    coords = {Coord(coord.x + x, coord.y + y): (x, y) for x, y in directions.keys()}
    return {k: v for k, v in coords.items() if map_[k] >= 0}


def search(_map, target_location: Coord):
    def find_neighbours_func(coord: Coord):
        candidates = [Coord(coord.x + d[0], coord.y + d[1]) for d in directions]
        candidates = [c for c in candidates if _map[c] > 0 or _map[c] == -2]
        return candidates

    result = astar.find_path(Coord(0, 0), target_location, find_neighbours_func, reversePath=False)

    return list(result)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day15_sample" if TEST_MODE else "input/day15").open() as f:
        values = [int(x) for x in [i.split(',') for i in f][0]]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
