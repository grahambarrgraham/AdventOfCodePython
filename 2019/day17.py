import dataclasses
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from nltk import flatten

from computer import Computer

TEST_MODE = False


@dataclasses.dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __iter__(self):
        return iter((self.x, self.y))


dirs = ['^', '<', 'v', '>']
l_r = {'<': 'L', '>': 'R'}
move_map = [('^', 0, -1), ('>', 1, 0), ('v', 0, 1), ('<', -1, 0)]
opp_dir = {'^': 'v', 'v': '^', '>': '<', '<': '>'}
turn_dir = {('>', '^'): '<', ('>', 'v'): '>',
            ('<', '^'): '>', ('<', 'v'): '<',
            ('v', '<'): '>', ('v', '>'): '<',
            ('^', '>'): '>', ('^', '<'): '<'}


class Map:

    def __init__(self, intcode):
        self.intcode = intcode
        self.computer = Computer(intcode)
        self.raw_map = ''.join([chr(i) for i in self.computer.compute([])])
        self.map_ = self.raw_map.split()
        self.intersections = set()
        self.segments = []
        self.map_scaffold()

    def __repr__(self):
        return self.raw_map

    def robot_location(self):
        for y, line in enumerate(self.map_):
            for x, d in enumerate(line):
                if d in dirs:
                    return Coord(x, y), d

    def next_scaffolds(self, loc: Coord, dir_: str) -> (Coord, chr, str):
        return [(d, l, c) for d, l, c, in self.neighbours(loc) if c == '#' and d != opp_dir[dir_]]

    def neighbours(self, loc: Coord) -> (Coord, chr, str):
        all_moves = [(dir_, Coord(loc.x + off_x, loc.y + off_y)) for dir_, off_x, off_y in move_map]
        return [(d, l, self.char_at(l)) for d, l in all_moves if self.is_on_map(l)]

    def char_at(self, c):
        return self.map_[c.y][c.x] if self.is_on_map(c) else None

    def is_on_map(self, coord):
        return 0 <= coord.x < len(self.map_[0]) and 0 <= coord.y < len(self.map_)

    def map_scaffold(self):
        previous_loc, previous_dir = self.robot_location()
        dir_, loc = [(d, l) for d, l, c in self.neighbours(previous_loc) if c == '#'][0]
        nxt = self.next_scaffolds(loc, dir_)
        move_count = 0
        last_turn = None
        while len(nxt) > 0:
            nxt = self.next_scaffolds(loc, dir_)
            if len(nxt) == 1:
                dir_, loc = [(d, l) for d, l, c in nxt][0]
            elif len(nxt) > 1:
                self.intersections.add(loc)
                dir_, loc = [(d, l) for d, l, c in nxt if d == dir_][0]
            if dir_ != previous_dir:
                if move_count == 0:
                    move_count += 1
                else:
                    self.segments.append(f"{last_turn}{move_count}")
                    move_count = 0
                last_turn = turn_dir[previous_dir, dir_]
                previous_dir = dir_
            move_count += 1
        self.segments.append(f"{last_turn}{move_count - 1}")

    def compute_dust(self, solution):
        sorted_indexes = sorted(flatten([i for _, i in solution]))
        main_routine = ['A' if i in solution[0][1] else 'B' if i in solution[1][1] else 'C' for i in sorted_indexes]
        functions = [segment for segment, _ in solution]
        self.intcode[0] = 2
        self.computer = Computer(self.intcode)
        robot_input = []
        for i, function in enumerate(main_routine):
            robot_input.append(ord(function))
            robot_input.append(44 if i < len(main_routine) - 1 else 10)
        self.computer.compute(robot_input)
        for function in functions:
            robot_input = []
            for i, step in enumerate(function):
                robot_input.append(ord((l_r[step[0]])))
                robot_input.append(44)
                robot_input.extend([ord(i) for i in step[1:]])
                robot_input.append(44 if i < len(function) - 1 else 10)
            self.computer.compute(robot_input)

        return self.computer.compute([ord('n'), 10])[-1]


def expand(a, b, c):
    def expand_single(segment, indexes):
        return [list(range(i, i + len(segment))) for i in indexes]

    return set(flatten([expand_single(*a), expand_single(*b), expand_single(*c)]))


def phase1(v):
    return sum([x * y for x, y in Map(v).intersections])


def phase2(v):
    map_ = Map(v)
    segments = map_.segments
    sub_lists = defaultdict(list)
    for i in range(len(segments)):
        for j in range(i + 1, len(segments) + 1):
            segment = tuple(segments[i:j])
            encode_seg_len = sum([len(s) for s in segment]) + len(segment) - 1
            if encode_seg_len <= 20:
                sub_lists[segment].append(i)

    def is_valid_solution(a, b, c):
        indexes = sorted(expand(a, b, c))
        return len(indexes) == len(segments) and indexes[0] == 0 and indexes[-1] == len(segments) - 1 and len(indexes) == len(set(indexes))

    solution = [(a, b, c) for a, b, c in combinations(sub_lists.items(), 3) if is_valid_solution(a, b, c)]
    return map_.compute_dust(solution[0])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day17_sample" if TEST_MODE else "input/day17").open() as f:
        values = [int(c) for c in f.readline().split(',')]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')