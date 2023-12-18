import collections
from pathlib import Path

from lib.polygon import polygon_area

TEST_MODE = False

# TAGS Polygon Area, Picks Formula, Shoelace

Coord = collections.namedtuple("Coord", "x y")
Instruction = collections.namedtuple("Instruction", "dir num, colour")
move_map = {'D': (0, 1), 'U': (0, -1), 'L': (-1, 0), 'R': (1, 0)}
decode_map = {0: 'R', 3: 'U', 2: 'L', 1: 'D'}


def phase1(instructions):
    return dig(instructions)


def phase2(instructions):
    return dig([decode(i) for i in instructions])


def decode(instruction):
    num = int(instruction.colour[1:-1], 16)
    dir_ = decode_map[int(instruction.colour[-1])]
    return Instruction(dir_, num, None)


def dig(instructions):
    vertices = [Coord(0, 0)]
    loc = vertices[0]
    for i in instructions:
        loc = apply(i, loc)
        vertices.append(loc)

    boundary_points = sum(n.num for n in instructions)
    area = polygon_area(vertices)
    # picks formula
    internal_points = area - boundary_points / 2 + 1
    return boundary_points + internal_points


def apply(instruction, loc):
    x_move, y_move = move_map[instruction.dir]
    x_move *= instruction.num
    y_move *= instruction.num
    return Coord(loc.x + x_move, loc.y + y_move)


def parse_instruction(line):
    a, b, c = line.split()
    return Instruction(a, int(b), c[1:-1])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day18_sample" if TEST_MODE else "input/day18").open() as f:
        values = [parse_instruction(i.strip()) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
