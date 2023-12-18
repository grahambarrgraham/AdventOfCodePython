import collections
from pathlib import Path

import astar

# TAGS: search astar

TEST_MODE = False

Coord = collections.namedtuple("Coord", "x y")
SearchNode = collections.namedtuple("SearchNode", "location, move_count")


def phase1(_maps):
    _starting_map = _maps[0]
    start_location = Coord(1, 0)
    target_location = Coord(len(_starting_map[0]) - 2, len(_starting_map) - 1)
    return search(_maps, SearchNode(start_location, 0), target_location).move_count


def phase2(_maps):
    _starting_map = _maps[0]
    start_location = Coord(1, 0)
    target_location = Coord(len(_starting_map[0]) - 2, len(_starting_map) - 1)
    outbound_1 = search(_maps, SearchNode(start_location, 0), target_location)
    return_for_snacks = search(_maps, outbound_1, start_location)
    outbound_2 = search(_maps, return_for_snacks, target_location)
    return outbound_2.move_count


class Node:
    def __init__(self, left_blizzard, right_blizzard, up_blizzard, down_blizzard, edge=False):
        self.left_blizzard = left_blizzard
        self.right_blizzard = right_blizzard
        self.up_blizzard = up_blizzard
        self.down_blizzard = down_blizzard
        self.blizzards = self.list_blizzards()
        self.edge = edge
        self.vacant = len(self.blizzards) == 0 and edge is False

    @staticmethod
    def build(_char):
        return Node(
            left_blizzard=True if _char == '<' else False,
            right_blizzard=True if _char == '>' else False,
            up_blizzard=True if _char == '^' else False,
            down_blizzard=True if _char == 'v' else False,
            edge=True if _char == '#' else False)

    def list_blizzards(self):
        return [b for b in [self.left_blizzard, self.right_blizzard, self.down_blizzard, self.up_blizzard] if b is True]


def pre_build_maps(_starting_map):
    _maps = dict()
    _maps[0] = _starting_map
    n = _starting_map
    map_count = 900
    for i in range(1, map_count):
        n = transform_map(n)
        _maps[i] = n
    print(f"pre built {map_count} _maps")
    return _maps


def find_moves(location: Coord, _map):
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


def search(_maps, start_node: SearchNode, target_location: Coord):

    expansions = 0

    def stop_func(search_node: SearchNode, *_):
        return search_node.location == target_location

    def find_neighbours_func(search_node: SearchNode):
        next_map = _maps[search_node.move_count + 1]
        valid_moves = find_moves(search_node.location, next_map)
        nonlocal expansions
        expansions += 1
        return [SearchNode(coord, search_node.move_count + 1) for coord, _ in valid_moves]

    def cost_func(*_):
        return 1.0

    def heuristic_func(search_node: SearchNode, *_):
        return abs(target_location.y - search_node.location.y) + abs(target_location.x - search_node.location.x)

    result = astar.find_path(start_node, None, find_neighbours_func,
                             reversePath=False,
                             distance_between_fnct=cost_func,
                             heuristic_cost_estimate_fnct=heuristic_func,
                             is_goal_reached_fnct=stop_func)

    print(f"search stats, neighbour expansions: {expansions}")

    return list(result)[-1]


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
            row.append(transform_node(*_neighbours) if _neighbours is not None else Node.build('#'))
        result.append(tuple(row))
    return tuple(result)


def transform_node(left: Node, right: Node, up: Node, down: Node):
    return Node(right.left_blizzard, left.right_blizzard, down.up_blizzard, up.down_blizzard)


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
        starting_map = tuple([tuple([Node.build(c) for c in line.strip()]) for line in f])
        maps = pre_build_maps(starting_map)
        print(f'Phase 1: {phase1(maps)}')
        print(f'Phase 2: {phase2(maps)}')
