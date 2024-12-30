import collections
import copy
from pathlib import Path

TEST_MODE = False

Coord = collections.namedtuple("Coord", "x y")
Puzzle = collections.namedtuple("Puzzle", "map directions")
Cube = collections.namedtuple("Cube", "direction, matches_edge, same_direction")
Vector = collections.namedtuple("Vector", "loc, direction")

dir_map = {('R', 'R'): 'D',
           ('R', 'L'): 'U',
           ('U', 'R'): 'R',
           ('U', 'L'): 'L',
           ('L', 'R'): 'U',
           ('L', 'L'): 'D',
           ('D', 'R'): 'L',
           ('D', 'L'): 'R',
           }

dir_score_map = {'R': 0, 'D': 1, 'L': 2, "U": 3}

dir_symbol_map = {'R': '>', 'D': 'V', 'L': '<', "U": '^'}

edge_dict_test = {(2, 0, 'U'): 1, (2, 0, 'L'): 2, (2, 0, 'R'): 3,
                  (2, 1, 'R'): 4, (1, 1, 'U'): 5, (0, 1, 'U'): 6,
                  (0, 1, 'L'): 7, (0, 1, 'D'): 8, (1, 1, 'D'): 9,
                  (2, 2, 'L'): 10, (2, 2, 'D'): 11, (3, 2, 'D'): 12,
                  (3, 2, 'R'): 13, (3, 2, 'U'): 14}

edge_dict_reverse_test = {1: (2, 0, 'U'), 2: (2, 0, 'L'), 3: (2, 0, 'R'),
                          4: (2, 1, 'R'), 5: (1, 1, 'U'), 6: (0, 1, 'U'),
                          7: (0, 1, 'L'), 8: (0, 1, 'D'), 9: (1, 1, 'D'),
                          10: (2, 2, 'L'), 11: (2, 2, 'D'), 12: (3, 2, 'D'),
                          13: (3, 2, 'R'), 14: (3, 2, 'U')}

edge_map_dict_test = {1: (6, False), 2: (5, True), 3: (13, False),
                      4: (14, False), 5: (2, True), 6: (1, False),
                      7: (12, False), 8: (11, False), 9: (10, False),
                      10: (9, False), 11: (8, False), 12: (7, False),
                      13: (3, False), 14: (4, False)}

edge_dict = {(1, 0, 'U'): 1, (2, 0, 'U'): 2, (2, 0, 'R'): 3,
             (2, 0, 'D'): 4, (1, 0, 'L'): 5, (1, 1, 'L'): 6,
             (1, 1, 'R'): 7, (1, 2, 'R'): 8, (1, 2, 'D'): 9,
             (0, 3, 'R'): 10, (0, 3, 'D'): 11, (0, 3, 'L'): 12,
             (0, 2, 'L'): 13, (0, 2, 'U'): 14}

edge_dict_reverse = {1: (1, 0, 'U'), 2: (2, 0, 'U'), 3: (2, 0, 'R'),
                     4: (2, 0, 'D'), 5: (1, 0, 'L'), 6: (1, 1, 'L'),
                     7: (1, 1, 'R'), 8: (1, 2, 'R'), 9: (1, 2, 'D'),
                     10: (0, 3, 'R'), 11: (0, 3, 'D'), 12: (0, 3, 'L'),
                     13: (0, 2, 'L'), 14: (0, 2, 'U')}

edge_map_dict = {1: (12, True), 2: (11, True), 3: (8, False),
                 4: (7, True), 5: (13, False), 6: (14, True),
                 7: (4, True), 8: (3, False), 9: (10, True),
                 10: (9, True), 11: (2, True), 12: (1, True),
                 13: (5, False), 14: (6, True)}

opposite_dir = {'D': 'U', 'U': 'D', 'L': 'R', 'R': 'L'}


def find_start(line):
    return min(idx for idx in ((line.find('.')), (line.find('#'))) if idx != -1)


class Map:
    def __init__(self, lines):
        self.lines = [[*l] for l in lines]
        self.x_starts = [find_start(line) for line in lines]
        self.x_ends = [len(line) - 1 for line in lines]
        self.y_starts = []
        self.y_ends = []
        self.loc = Coord(self.x_starts[0], 0)
        self.direction = 'R'
        self.build_y_ranges()

    def build_y_ranges(self):
        for x in range(max(self.x_ends) + 1):
            started = False
            ended = False
            for y in range(len(self.lines)):
                char = self.char_at(Coord(x, y))
                if char == " " and started:
                    self.y_ends.append(y - 1)
                    ended = True
                    break
                elif char != " " and not started:
                    started = True
                    self.y_starts.append(y)
            if not ended:
                self.y_ends.append(len(self.lines) - 1)

    def __repr__(self):
        result = ""
        for l in self.lines:
            result += "".join(l)
            result += '\n'
        return result

    def char_at(self, coord):
        if coord.y >= len(self.lines):
            return " "
        if coord.x >= len(self.lines[coord.y]):
            return " "
        if coord == self.loc:
            return self.direction
        return self.lines[coord.y][coord.x]

    def apply(self, instruction, func):
        if not isinstance(instruction, int):
            self.direction = dir_map[(self.direction, instruction)]
            self.lines[self.loc.y][self.loc.x] = dir_symbol_map[self.direction]
        else:
            for i in range(instruction):
                vector = func()
                if self.char_at(vector.loc) == '#':
                    return
                else:
                    self.direction = vector.direction
                    self.lines[vector.loc.y][vector.loc.x] = dir_symbol_map[self.direction]
                    self.loc = vector.loc

    def find_next_loc_part_1(self):
        if self.direction == 'R':
            return Vector(Coord(self.loc.x + 1 if self.loc.x < self.x_ends[self.loc.y] else self.x_starts[self.loc.y],
                         self.loc.y), self.direction)
        elif self.direction == 'L':
            return Vector(Coord(self.loc.x - 1 if self.loc.x > self.x_starts[self.loc.y] else self.x_ends[self.loc.y],
                         self.loc.y), self.direction)
        elif self.direction == 'U':
            return Vector(Coord(self.loc.x,
                         self.loc.y - 1 if self.loc.y > self.y_starts[self.loc.x] else self.y_ends[
                             self.loc.x]), self.direction)
        elif self.direction == 'D':
            return Vector(Coord(self.loc.x,
                         self.loc.y + 1 if self.loc.y < self.y_ends[self.loc.x] else self.y_starts[
                             self.loc.x]), self.direction)

    def find_next_loc_part_2(self):
        _edge_dict = edge_dict_test if TEST_MODE else edge_dict
        _edge_map_dict = edge_map_dict_test if TEST_MODE else edge_map_dict
        _edge_reverse_dict = edge_dict_reverse_test if TEST_MODE else edge_dict_reverse
        edge_length = 4 if TEST_MODE else 50

        def find_vector_on_joining_cube_face():
            edge = _edge_dict[(self.loc.x // edge_length, self.loc.y // edge_length, self.direction)]
            matching_edge, same_direction = _edge_map_dict[edge]
            edge_x, edge_y, edge_direction = _edge_reverse_dict[matching_edge]
            diff = self.loc.x % edge_length if self.direction == 'U' or self.direction == 'D' else self.loc.y % edge_length
            diff = diff if same_direction else edge_length - diff - 1
            new_direction = opposite_dir[edge_direction]
            vector = None
            if edge_direction == 'U':
                vector = Vector(Coord((edge_x * edge_length) + diff, edge_y * edge_length), new_direction)
            elif edge_direction == 'D':
                vector = Vector(Coord((edge_x * edge_length) + diff, ((edge_y + 1) * edge_length) - 1), new_direction)
            elif edge_direction == 'L':
                vector = Vector(Coord(edge_x * edge_length, (edge_y * edge_length) + diff), new_direction)
            elif edge_direction == 'R':
                vector = Vector(Coord((edge_x * edge_length) + diff, ((edge_y + 1) * edge_length) - 1), new_direction)
            print(f"{edge} {self.loc}, {self.direction} -> {matching_edge}, {same_direction}, {diff} {vector}")
            # print(self)
            return vector

        if self.direction == 'R':
            return Vector(Coord(self.loc.x + 1, self.loc.y), self.direction) if self.loc.x < self.x_ends[
                self.loc.y] else find_vector_on_joining_cube_face()
        elif self.direction == 'L':
            return Vector(Coord(self.loc.x - 1, self.loc.y), self.direction) if self.loc.x > self.x_starts[
                self.loc.y] else find_vector_on_joining_cube_face()
        elif self.direction == 'U':
            return Vector(Coord(self.loc.x, self.loc.y - 1), self.direction) if self.loc.y > self.y_starts[
                self.loc.x] else find_vector_on_joining_cube_face()
        elif self.direction == 'D':
            return Vector(Coord(self.loc.x, self.loc.y + 1), self.direction) if self.loc.y < self.y_ends[
                self.loc.x] else find_vector_on_joining_cube_face()


def phase1(v):
    return calc(v, v.map.find_next_loc_part_1)


def phase2(v):
    return calc(v, v.map.find_next_loc_part_2)


def calc(v, func):
    for i in v.directions:
        v.map.apply_phase_2(i, func)
        # print(f"{i} {v.map.loc}, {v.map.direction}")
    return (1000 * (v.map.loc.y + 1)) + (4 * (v.map.loc.x + 1)) + dir_score_map[v.map.direction]


def parse_instructions(s):
    previous = ""
    result = []
    for c in s:
        if c.isnumeric():
            previous += c
        else:
            result.append(int(previous))
            previous = ""
            result.append(c)
    if previous != "":
        result.append(int(previous))
    return result


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day22_sample" if TEST_MODE else "input/day22").open() as f:
        blocks = [block for block in f.read().split("\n\n")]
        values = Puzzle(Map(blocks[0].split("\n")), parse_instructions(blocks[1]))
        # print(f'Phase 1: {phase1(copy.deepcopy(values))}')
        print(f'Phase 2: {phase2(copy.deepcopy(values))}')
