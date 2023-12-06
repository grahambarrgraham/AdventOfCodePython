import dataclasses
import re
import unittest
from pathlib import Path

TEST_MODE = False


@dataclasses.dataclass
class Range:
    start: int
    stop: int


@dataclasses.dataclass
class Mapping:
    dest_start: int
    source_start: int
    length: int

    def source_range(self):
        return Range(self.source_start, self.source_start + self.length)

    def match(self, r: Range) -> (Range, Range, Range):

        s = self.source_range()

        if r.stop == r.start:
            return None, None, None

        if r.stop <= s.start:
            return r, None, None

        if r.start >= s.stop:
            return None, None, r

        before = None if r.start >= s.start else Range(r.start, s.start)
        after = None if r.stop <= s.stop else Range(s.stop, r.stop)
        match = Range(max(r.start, s.start), min(r.stop, s.stop))

        return before, match, after

    def map_range(self, r):
        diff = self.dest_start - self.source_start
        return Range(r.start + diff, r.stop + diff)


@dataclasses.dataclass
class Map:
    from_: str
    to_: str
    mappings: list[Mapping]

    def apply(self, input_: int):
        for mapping in self.mappings:
            if mapping.source_start <= input_ <= mapping.source_start + mapping.length:
                return mapping.dest_start + (input_ - mapping.source_start)
        return input_

    def apply_ranges(self, input_: Range):
        result = []
        queue = [input_]
        for mapping in self.mappings:
            if len(queue) == 0:
                break
            r = queue.pop()
            before, matching, after = mapping.match(r)
            # print(f"{r} split by {mapping.source_range()} to {before}, {matching}, {after}")
            if matching is not None:
                o = mapping.map_range(matching)
                print(f"{r} split by {mapping.source_range()} to {before}, {matching}, {after} - mapped to {o} by {mapping.source_start}->{mapping.dest_start}")
                result.append(o)
            if before is not None:
                queue.append(before)
            if after is not None:
                queue.append(after)
        result += queue
        return result


def phase1(seeds: list[int], maps: dict[str, Map]):
    print(v1(maps, seeds))
    ranges = [Range(s, s + 1) for s in seeds]
    return v2(maps, ranges)


def v1(maps, seeds):
    map_ = maps['seed']
    values = seeds
    # values = [79, 80, 81, 82, 83, 84]
    while True:
        values = [map_.apply(v) for v in values]
        if map_.to_ == 'location':
            break
        map_ = maps[map_.to_]
    print(values)
    return min(values)


def phase2(seeds: list[int], _maps: dict[str, Map]):
    ranges = [Range(seeds[0], seeds[0] + seeds[1]), Range(seeds[2], seeds[2] + seeds[3])]
    return v2(_maps, ranges)


def v2(_maps, ranges):
    map_ = _maps['seed']
    print(f"starting {ranges}")
    while True:
        print("---")
        print(map_)
        ranges = flatten([map_.apply_ranges(r) for r in ranges])
        print(ranges)
        if map_.to_ == 'location':
            break
        map_ = _maps[map_.to_]
    # print(ranges)
    return min([r.start for r in ranges])


def flatten(l_):
    return [item for sublist in l_ for item in sublist]


def read_map(block) -> Map:
    lines = block.split("\n")
    match = re.match("(.+)-to-(.+) map:", lines[0])

    def read_range(_l: list[str]):
        return Mapping(int(_l[0]), int(_l[1]), int(_l[2]))

    ranges = [read_range(line.split(' ')) for line in lines[1:]]
    return Map(match.group(1), match.group(2), ranges)


class MyTest(unittest.TestCase):

    def mappings(self):
        self.assertEqual(Mapping(10, 10, 10).match(Range(0, 10)), (Range(0, 10), None, None))
        self.assertEqual(Mapping(10, 10, 10).match(Range(0, 9)), (Range(0, 9), None, None))
        self.assertEqual(Mapping(10, 10, 10).match(Range(9, 21)), (Range(9, 10), Range(10, 20), Range(20, 21)))
        self.assertEqual(Mapping(10, 10, 10).match(Range(10, 10)), (None, None, None))
        self.assertEqual(Mapping(10, 10, 10).match(Range(10, 10)), (None, None, None))
        self.assertEqual(Mapping(10, 10, 10).match(Range(0, 21)), (Range(0, 10), Range(10, 20), Range(20, 21)))
        self.assertEqual(Mapping(10, 10, 10).match(Range(20, 21)), (None, None, Range(20, 21)))
        self.assertEqual(Mapping(10, 10, 10).match(Range(21, 22)), (None, None, Range(21, 22)))
        self.assertEqual(Mapping(10, 10, 10).match(Range(19, 22)), (None, Range(19, 20), Range(20, 22)))
        self.assertEqual(Mapping(-100, 10, 10).match(Range(19, 22)), (None, Range(19, 20), Range(20, 22)))
        self.assertEqual(Mapping(0, -10, 20).match(Range(-11, 12)), (Range(-11, -10), Range(-10, 10), Range(10, 12)))
        self.assertEqual(Mapping(0, -10, 10).match(Range(-10, 12)), (None, Range(-10, 0), Range(0, 12)))


def run_tests(tests: list[str]):
    suite = unittest.TestSuite()
    suite.addTests([MyTest(t) for t in tests])
    unittest.runner.TextTestRunner().run(suite)


if __name__ == "__main__":
    run_tests(['mappings'])
    with Path(__file__).parent.joinpath("input/day5_sample" if TEST_MODE else "input/day5").open() as f:
        blocks = [block.strip() for block in f.read().split("\n\n")]
        _seeds: list[int] = [int(seed_num) for seed_num in blocks[0].split(': ')[1].split(' ')]
        _maps: list[Map] = [read_map(block) for block in blocks[1:]]
        print(_maps)
        maps_dict: dict[str, Map] = {_map.from_: _map for _map in _maps}
        # print(f'Phase 1: {phase1(_seeds, maps_dict)}')
        print(f'Phase 2: {phase2(_seeds, maps_dict)}')
