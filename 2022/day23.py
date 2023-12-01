import collections
from functools import partial
from pathlib import Path

TEST_MODE = False

Coord = collections.namedtuple("Coord", "x y")

all_neighbours = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
north_neighbours = [n for n in all_neighbours if n[1] < 0]
south_neighbours = [n for n in all_neighbours if n[1] > 0]
west_neighbours = [n for n in all_neighbours if n[0] < 0]
east_neighbours = [n for n in all_neighbours if n[0] > 0]


def phase1(v):
    elves = set(all_elves(v))
    rules = initial_rules()

    for i in range(10):
        elves, moving, moved = evolve(elves, rules)
        rules.append(rules.pop(0))

    max_x = max({coord.x for coord in elves})
    max_y = max({coord.y for coord in elves})
    min_x = min({coord.x for coord in elves})
    min_y = min({coord.y for coord in elves})
    area = ((max_y - min_y) + 1) * ((max_x - min_x) + 1)
    return area - len(elves)


def phase2(v):
    elves = set(all_elves(v))
    rules = initial_rules()
    _round = 0

    while True:
        elves, moving, moved = evolve(elves, rules)
        rules.append(rules.pop(0))
        _round += 1
        if len(moving) == 0:
            break

    return _round


def north(elf):
    return Coord(elf.x, elf.y - 1)


def south(elf):
    return Coord(elf.x, elf.y + 1)


def east(elf):
    return Coord(elf.x + 1, elf.y)


def west(elf):
    return Coord(elf.x - 1, elf.y)


def rule(_neighbours, _direction, elf, elves):
    return _direction(elf) if len(neighbours(elf, elves, _neighbours)) == 0 else None


def neighbours(elf, elves, _neighbours):
    def elf_at(offset):
        c = Coord(elf.x + offset[0], elf.y + offset[1])
        return c if c in elves else None

    return list(filter(None, [elf_at(offset) for offset in _neighbours]))


def candidate_move(elf, elves, rules):
    for _rule in rules:
        candidate = _rule(elf, elves)
        if candidate is None:
            continue
        else:
            return candidate

    return None


def evolve(elves, rules):
    eligible_elves = {elf for elf in elves if len(neighbours(elf, elves, all_neighbours)) > 0}

    move_map = collections.defaultdict(list)
    for elf in eligible_elves:
        c = candidate_move(elf, elves, rules)
        if c is not None:
            move_map[c].append(elf)

    moving_elves = {elf_list[0] for elf_list in move_map.values() if len(elf_list) == 1}
    moved_elves = {k for k, v in move_map.items() if len(v) == 1}
    elves -= moving_elves
    elves = elves.union(moved_elves)
    return elves, moving_elves, moved_elves


def all_elves(v):
    for y in range(len(v)):
        for x in range(len(v[0])):
            if v[y][x] == '#':
                yield Coord(x, y)


def initial_rules():
    rules = [partial(rule, north_neighbours, north),
             partial(rule, south_neighbours, south),
             partial(rule, west_neighbours, west),
             partial(rule, east_neighbours, east)]
    return rules


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day23_sample" if TEST_MODE else "input/day23").open() as f:
        values = [i.strip() for i in f]
        # print(values)
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
