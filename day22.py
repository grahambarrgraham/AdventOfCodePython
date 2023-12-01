import collections
from pathlib import Path

TEST_MODE = False

Coord = collections.namedtuple("Coord", "x y")
Puzzle = collections.namedtuple("Puzzle", "map directions")

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

    def apply(self, instruction):
        if not isinstance(instruction, int):
            self.direction = dir_map[(self.direction, instruction)]
            self.lines[self.loc.y][self.loc.x] = dir_symbol_map[self.direction]
        else:
            for i in range(instruction):
                next_loc = self.find_next_loc()
                if self.char_at(next_loc) == '#':
                    return
                else:
                    self.lines[next_loc.y][next_loc.x] = dir_symbol_map[self.direction]
                    self.loc = next_loc

    def find_next_loc(self):
        if self.direction == 'R':
            return Coord(self.loc.x + 1 if self.loc.x < self.x_ends[self.loc.y] else self.x_starts[self.loc.y],
                         self.loc.y)
        elif self.direction == 'L':
            return Coord(self.loc.x - 1 if self.loc.x > self.x_starts[self.loc.y] else self.x_ends[self.loc.y],
                         self.loc.y)
        elif self.direction == 'U':
            return Coord(self.loc.x,
                         self.loc.y - 1 if self.loc.y > self.y_starts[self.loc.x] else self.y_ends[self.loc.x])
        elif self.direction == 'D':
            return Coord(self.loc.x,
                         self.loc.y + 1 if self.loc.y < self.y_ends[self.loc.x] else self.y_starts[self.loc.x])


def phase1(v):
    for i in v.directions:
        v.map.apply(i)
        # print(f"{i} {v.map.loc}, {v.map.direction}")
        # print(v.map)

    score = (1000 * (v.map.loc.y + 1)) + (4 * (v.map.loc.x + 1)) + dir_score_map[v.map.direction]

    return score


def phase2(v):
    return -1


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
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
