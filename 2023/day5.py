import dataclasses
import re
import unittest
from pathlib import Path

TEST_MODE = False


@dataclasses.dataclass
class Range:
    start: int
    stop: int
    parent = None
    parent_action = None

    def explain(self):
        print(f"{self.parent_action}")
        print(f"{self.parent.explain()}")


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
        if before is not None:
            before.parent = r
            before.parent_action = "before"
        if after is not None:
            after.parent = r
            after.parent_action = "before"
        if match is not None:
            match.parent = r
            match.parent_action = "before"

        return before, match, after

    def map_range(self, r):
        diff = self.dest_start - self.source_start
        range1 = Range(r.start + diff, r.stop + diff)
        range1.parent = r
        range1.parent_action = f"{self.source_start}->{self.dest_start}"
        return range1


@dataclasses.dataclass
class Map:
    name: str
    next_map: str
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
                print(
                    f"{r} split by {mapping.source_range()} to {before}, {matching}, {after} - mapped to {o} by {mapping.source_start}->{mapping.dest_start}")
                result.append(o)
            if before is not None:
                queue.append(before)
            if after is not None:
                queue.append(after)
        result += queue
        return result


def phase1(seeds: list[int], maps: dict[str, Map]):
    return process(maps, [Range(s, s + 1) for s in seeds])


def phase2(seeds: list[int], _maps: dict[str, Map]):
    ranges = to_ranges(seeds)
    ranges = [r for r in ranges if r.start == 892394515]
    for range in ranges:
        s = process(_maps, [range])
        print(f"{range} {s}")
    return -1


def to_ranges(seeds):
    return [Range(seeds[i], seeds[i + 1] + seeds[i]) for i in (range(0, len(seeds), 2))]


def process(maps, ranges):
    current = maps['seed']
    print(f"starting {ranges}")
    while True:
        print("---")
        print(current)
        ranges = flatten([current.apply_ranges(range_) for range_ in ranges])
        print(ranges)
        if current.next_map == 'location':
            break
        current = maps[current.next_map]
    ranges.sort(key=lambda r: r.start)

    ranges[0].explain()

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


# class MyTest(unittest.TestCase):
#
#     def mappings(self):
#         self.assertEqual(Mapping(10, 10, 10).match(Range(0, 10)), (Range(0, 10), None, None))
#         self.assertEqual(Mapping(10, 10, 10).match(Range(0, 9)), (Range(0, 9), None, None))
#         self.assertEqual(Mapping(10, 10, 10).match(Range(9, 21)), (Range(9, 10), Range(10, 20), Range(20, 21)))
#         self.assertEqual(Mapping(10, 10, 10).match(Range(10, 10)), (None, None, None))
#         self.assertEqual(Mapping(10, 10, 10).match(Range(10, 10)), (None, None, None))
#         self.assertEqual(Mapping(10, 10, 10).match(Range(0, 21)), (Range(0, 10), Range(10, 20), Range(20, 21)))
#         self.assertEqual(Mapping(10, 10, 10).match(Range(20, 21)), (None, None, Range(20, 21)))
#         self.assertEqual(Mapping(10, 10, 10).match(Range(21, 22)), (None, None, Range(21, 22)))
#         self.assertEqual(Mapping(10, 10, 10).match(Range(19, 22)), (None, Range(19, 20), Range(20, 22)))
#         self.assertEqual(Mapping(-100, 10, 10).match(Range(19, 22)), (None, Range(19, 20), Range(20, 22)))
#         self.assertEqual(Mapping(0, -10, 20).match(Range(-11, 12)), (Range(-11, -10), Range(-10, 10), Range(10, 12)))
#         self.assertEqual(Mapping(0, -10, 10).match(Range(-10, 12)), (None, Range(-10, 0), Range(0, 12)))


# def run_tests(tests: list[str]):
#     suite = unittest.TestSuite()
#     suite.addTests([MyTest(t) for t in tests])
#     unittest.runner.TextTestRunner().run(suite)


if __name__ == "__main__":
    # run_tests(['mappings'])
    with Path(__file__).parent.joinpath("input/day5_sample" if TEST_MODE else "input/day5").open() as f:
        blocks = [block.strip() for block in f.read().split("\n\n")]
        _seeds: list[int] = [int(seed_num) for seed_num in blocks[0].split(': ')[1].split(' ')]
        _maps: list[Map] = [read_map(block) for block in blocks[1:]]
        maps_dict: dict[str, Map] = {_map.name: _map for _map in _maps}
        # print(f'Phase 1: {phase1(_seeds, maps_dict)}')
        # print(to_ranges([848725444, 8940450]))
        print(f'Phase 2: {phase2(_seeds, maps_dict)}')
