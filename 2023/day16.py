import collections
from pathlib import Path

TEST_MODE = False

Coord = collections.namedtuple("Coord", "x y")
Beam = collections.namedtuple("Beam", "loc dir")


move_map = {'right': (1, 0), 'left': (-1, 0), 'down': (0, 1), 'up': (0, -1)}
dir_map = {
    ('right', '/'): 'up', ('left', '/'): 'down', ('up', '/'): 'right',
    ('down', '/'): 'left',  ('right', '\\'): 'down', ('left', '\\'): 'up',
    ('up', '\\'): 'left', ('down', '\\'): 'right'
}


def phase1(m):
    return process(m, Beam(Coord(-1, 0), 'right'))


def phase2(m):
    return max([process(m, start) for start in all_starts(m)])


def all_starts(m):
    for y in range(len(m)):
        yield Beam(Coord(-1, y), 'right')
        yield Beam(Coord(len(m[0]), y), 'left')

    for x in range(len(m[0])):
        yield Beam(Coord(x, -1), 'down')
        yield Beam(Coord(x, len(m)), 'up')


def process(m, start):
    closed_beams = set()
    open_beams = [start]
    while len(open_beams) > 0:
        beam = open_beams.pop(0)
        new_beams = move(beam, m)
        for nb in new_beams:
            if nb not in closed_beams:
                closed_beams.add(nb)
                open_beams.append(nb)
    energised = {b.loc for b in closed_beams}
    return len(energised)


def move(b: Beam, m) -> list[Beam]:
    move_inc = move_map[b.dir]
    next_coord = Coord(b.loc.x + move_inc[0], b.loc.y + move_inc[1])
    if is_off_map(m, next_coord):
        return []
    symbol = m[next_coord.y][next_coord.x]
    if symbol == '.' or (symbol == '-' and b.dir in ['left', 'right']) or (symbol == '|' and b.dir in ['up', 'down']):
        return [Beam(next_coord, b.dir)]
    if symbol == '|':
        return [Beam(next_coord, dir_) for dir_ in ['up', 'down']]
    if symbol == '-':
        return [Beam(next_coord, dir_) for dir_ in ['left', 'right']]
    if symbol in ['\\', '/']:
        return [Beam(next_coord, dir_map[(b.dir, symbol)])]


def is_off_map(m, next_coord):
    return next_coord.x < 0 or next_coord.x >= len(m[0]) or next_coord.y < 0 or next_coord.y >= len(m)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day16_sample" if TEST_MODE else "input/day16").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
