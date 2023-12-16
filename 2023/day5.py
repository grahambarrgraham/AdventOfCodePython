import collections
import dataclasses
import re
from pathlib import Path

TEST_MODE = False

Range = collections.namedtuple("Range", "start stop")


def phase1(seeds: list[int], maps: dict):
    ranges = [Range(s, s + 1) for s in seeds]
    return min(r.start for r in process(maps, ranges))


def phase2(seeds: list[int], maps: dict):
    ranges = to_ranges(seeds)
    return min(r.start for r in process(maps, ranges))


def process(maps, ranges):
    name = 'seed'
    while name != 'location':
        current_map = maps[name]
        ranges = flatten([current_map.apply_range(range_) for range_ in ranges])
        name = current_map.next_map
    return sorted(ranges, key=lambda r: r.start)


@dataclasses.dataclass
class Map:
    name: str
    next_map: str
    mappings: list

    def apply_range(self, range_):
        acc = set()
        queue = [(range_, 0)]
        while len(queue) > 0:
            r, mapping_index = queue.pop(0)

            if mapping_index >= len(self.mappings):
                continue

            mapping = self.mappings[mapping_index]
            before, matching, after = mapping.match(r)
            if before is not None:
                queue.append((before, mapping_index + 1))
                acc.add(before)
            if after is not None:
                queue.append((after, mapping_index + 1))
                acc.add(after)
            if matching is not None:
                if r in acc:
                    acc.remove(r)
                mapped_range = mapping.map_range(matching)
                acc.add(mapped_range)

        return acc


@dataclasses.dataclass
class Mapping:
    destination_start: int
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
        diff = self.destination_start - self.source_start
        return Range(r.start + diff, r.stop + diff)


def to_ranges(seeds):
    return [Range(seeds[i], seeds[i + 1] + seeds[i]) for i in (range(0, len(seeds), 2))]


def flatten(l_):
    return [item for sublist in l_ for item in sublist]


def read_map(block) -> Map:
    lines = block.split("\n")
    match = re.match("(.+)-to-(.+) map:", lines[0])

    def read_range(_l: list[str]):
        return Mapping(int(_l[0]), int(_l[1]), int(_l[2]))

    ranges = [read_range(line.split(' ')) for line in lines[1:]]
    return Map(match.group(1), match.group(2), ranges)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day5_sample" if TEST_MODE else "input/day5").open() as f:
        blocks = [block.strip() for block in f.read().split("\n\n")]
        _seeds: list[int] = [int(seed_num) for seed_num in blocks[0].split(': ')[1].split(' ')]
        _maps: list[Map] = [read_map(block) for block in blocks[1:]]
        maps_dict: dict[str, Map] = {_map.name: _map for _map in _maps}
        print(f'Phase 1: {phase1(_seeds, maps_dict)}')
        print(f'Phase 2: {phase2(_seeds, maps_dict)}')
