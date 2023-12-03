import collections
from pathlib import Path

import lib.astar

TEST_MODE = False

Coord = collections.namedtuple("Coord", "x y")


def phase1(starting_map):
    start_node = SearchNode(Coord(1, 0), 0)
    target_location = Coord(len(starting_map[0]) - 2, len(starting_map) - 1)
    maps = pre_build_maps(starting_map)
    return search(maps, start_node, target_location).move_count


def phase2(starting_map):
    start_location = Coord(1, 0)
    target_location = Coord(len(starting_map[0]) - 2, len(starting_map) - 1)
    maps = pre_build_maps(starting_map)
    outbound_1 = search(maps, SearchNode(start_location, 0), target_location)
    return_for_snacks = search(maps, outbound_1, start_location)
    outbound_2 = search(maps, return_for_snacks, target_location)
    return outbound_2.move_count


class SearchNode:
    def __init__(self, location: Coord, move_count: int):
        self.location = location
        self.move_count = move_count

    def __repr__(self):
        return f"SearchNode: {self.location}, {self.move_count}"

    def __hash__(self):
        return hash(tuple([self.move_count, self.location]))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.move_count == other.move_count and self.location == other.location


class Node:
    def __init__(self, left_blizzard=False, right_blizzard=False, up_blizzard=False, down_blizzard=False):
        self.left_blizzard = left_blizzard
        self.right_blizzard = right_blizzard
        self.up_blizzard = up_blizzard
        self.down_blizzard = down_blizzard
        self.blizzards = self.list_blizzards()
        self.vacant = len(self.blizzards) == 0
        self.edge = False
        self.elves = False

    def list_blizzards(self):
        return [b for b in [self.left_blizzard, self.right_blizzard, self.down_blizzard, self.up_blizzard] if b is True]

    def __repr__(self):
        _l = len(self.blizzards)
        c = _l \
            if _l > 1 \
            else 'E' if self.elves \
            else '.' if self.vacant \
            else '<' if self.left_blizzard \
            else '>' if self.right_blizzard \
            else '^' if self.up_blizzard \
            else 'v' if self.down_blizzard \
            else '#'
        return f"{c}"

    def __hash__(self):
        return hash(tuple([self.left_blizzard, self.right_blizzard, self.up_blizzard, self.down_blizzard, self.edge]))

    def __eq__(self, other):
        return self.__class__ == other.__class__ \
            and self.right_blizzard == other.right_blizzard \
            and self.left_blizzard == other.left_blizzard \
            and self.up_blizzard == other.up_blizzard \
            and self.down_blizzard == other.down_blizzard \
            and self.edge == other.edge


def pre_build_maps(starting_map):
    maps = dict()
    maps[0] = starting_map
    n = starting_map
    for i in range(1, 2000):
        n = transform_map(n)
        maps[i] = n
    return maps


def search_neighbours(location: Coord, _map):
    right_extent = len(_map[0]) - 1
    down_extent = len(_map) - 1

    left = None if location.x - 1 < 0 or not _map[location.y][location.x - 1].vacant \
        else Coord(location.x - 1, location.y)

    right = None if location.x + 1 > right_extent or not _map[location.y][location.x + 1].vacant \
        else Coord(location.x + 1, location.y)

    up = None if location.y - 1 < 0 or not _map[location.y - 1][location.x].vacant \
        else Coord(location.x, location.y - 1)

    down = None if location.y + 1 > down_extent or not _map[location.y + 1][location.x].vacant \
        else Coord(location.x, location.y + 1)

    wait = None if not _map[location.y][location.x].vacant else Coord(location.x, location.y)

    return [(coord, desc) for coord, desc in
            [(left, 'left'), (right, 'right'), (up, 'up'), (down, 'down'), (wait, 'wait')] if coord is not None]


def search(_maps, start_node, target_location):
    def stop_func(search_node: SearchNode):
        return search_node.location == target_location

    def find_neighbours_func(search_node: SearchNode, _maps):
        new_map = _maps[search_node.move_count + 1]
        neighbours = search_neighbours(search_node.location, new_map)
        return [SearchNode(coord, search_node.move_count + 1) for coord, _ in neighbours]

    def cost_func(search_node: SearchNode, _unused):
        distance = abs(target_location.y - search_node.location.y) + abs(target_location.x - search_node.location.x)
        return search_node.move_count + distance

    return lib.astar.a_star_algorithm(_maps, start_node, stop_func, find_neighbours_func, cost_func)


def transform_map(_map):
    neighbour_map = dict()
    for y in range(len(_map)):
        for x in range(len(_map[0])):
            location = Coord(x, y)
            _neighbours = blizzard_neighbours(location, _map)
            neighbour_map[location] = _neighbours
    result = []
    for y in range(len(_map)):
        row = []
        for x in range(len(_map[0])):
            _neighbours = neighbour_map[Coord(x, y)]
            row.append(transform_node(*_neighbours) if _neighbours is not None else parse_node('#'))
        result.append(tuple(row))
    return tuple(result)


def parse_node(_char):
    node = Node()
    node.left_blizzard = True if _char == '<' else False
    node.right_blizzard = True if _char == '>' else False
    node.up_blizzard = True if _char == '^' else False
    node.down_blizzard = True if _char == 'v' else False
    node.edge = True if _char == '#' else False
    node.vacant = True if _char == '.' else False
    node.blizzards = node.list_blizzards()
    return node


def transform_node(left: Node, right: Node, up: Node, down: Node):
    return Node(right.left_blizzard, left.right_blizzard, down.up_blizzard, up.down_blizzard)


def print_map(_map):
    for row in _map:
        for node in row:
            print(node, end='')
        print()


def blizzard_neighbours(location, _map):
    if _map[location.y][location.x].edge:
        return None
    right_extent = len(_map[0]) - 1
    down_extent = len(_map) - 1

    if location.x - 1 < 0 or _map[location.y][location.x - 1].edge:
        left = _map[location.y][right_extent] if not _map[location.y][right_extent].edge else _map[location.y][
            right_extent - 1]
    else:
        left = _map[location.y][location.x - 1]

    if location.x + 1 > right_extent or _map[location.y][location.x + 1].edge:
        right = _map[location.y][0] if not _map[location.y][0].edge else _map[location.y][1]
    else:
        right = _map[location.y][location.x + 1]

    if location.y - 1 < 0 or _map[location.y - 1][location.x].edge:
        up = _map[down_extent][location.x] if not _map[down_extent][location.x].edge else _map[down_extent - 1][
            location.x]
    else:
        up = _map[location.y - 1][location.x]

    if location.y + 1 > down_extent or _map[location.y + 1][location.x].edge:
        down = _map[0][location.x] if not _map[0][location.x].edge else _map[1][location.x]
    else:
        down = _map[location.y + 1][location.x]

    return left, right, up, down


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day24_sample" if TEST_MODE else "input/day24").open() as f:
        values = tuple([tuple([parse_node(c) for c in line.strip()]) for line in f])
        # print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
