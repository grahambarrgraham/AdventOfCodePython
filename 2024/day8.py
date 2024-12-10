from collections import defaultdict
from itertools import combinations
from pathlib import Path

TEST_MODE = False


class Map:
    def __init__(self, map_):
        self.map_ = map_
        self.antennas = defaultdict(set)
        for y, l in enumerate(map_):
            for x, c in enumerate(map_[y]):
                if c != '.':
                    self.antennas[c].add((x, y))

    def find_all_antinodes(self, a, b):
        queue = [(a, b)]
        result = set()
        while len(queue) > 0:
            a, b = queue.pop()
            if self.is_on_map(*a) and self.is_on_map(*b):
                result.update([a, b])
                nxt_a, nxt_b = [n for n in self.find_antinodes(a, b)]
                if nxt_a not in result:
                    queue.append((a, nxt_a))
                if nxt_b not in result:
                    queue.append((b, nxt_b))
        return result

    def find_antinodes(self, a, b):
        x_a, y_a = a
        x_b, y_b = b
        x_diff = x_a - x_b
        y_diff = y_a - y_b
        x_an_1, y_an_1 = x_a + x_diff, y_a + y_diff
        x_an_2, y_an_2 = x_b - x_diff, y_b - y_diff
        result = (x_an_1, y_an_1), (x_an_2, y_an_2)
        return result

    def is_on_map(self, x, y):
        return len(self.map_[0]) > x >= 0 and len(self.map_) > y >= 0


def find_antinodes(map_, my_fun):
    all_antinodes = set()
    for frequency, antennas_ in map_.antennas.items():
        antenna_pairs = combinations(antennas_, 2)
        for antenna_a, antenna_b in antenna_pairs:
            all_antinodes.update(my_fun(antenna_a, antenna_b))
    return all_antinodes


def phase1(v):
    map_ = Map(v)
    result = [(x, y) for x, y in (find_antinodes(map_, map_.find_antinodes)) if map_.is_on_map(x, y)]
    return len(result)


def phase2(v):
    map_ = Map(v)
    return len(find_antinodes(map_, map_.find_all_antinodes))


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day8_sample" if TEST_MODE else "input/day8").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
