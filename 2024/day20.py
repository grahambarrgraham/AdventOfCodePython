from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from time import time
from typing import Iterator, Union

from lib import astar

TEST_MODE = False


def phase1(map_):
    return find_cheats(map_, 2)


def phase2(map_):
    return find_cheats(map_, 20)


def moves(max_moves=20):
    start = (0, 0)
    visited = set()

    def neighbours(x, y):
        return [(x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1)] if (x + a, y + b) not in visited]

    frontier = {start}
    for i in range(max_moves + 1):
        visited.update(frontier)
        nxt_frontier = set()
        for x, y in frontier:
            nxt_frontier.update(neighbours(x, y))
        frontier = nxt_frontier

    return visited


def find_cheats(map_, duration):
    start, end = scan(map_)
    main_path, main_cost = next(next(search_graph(map_, start, end)))
    distances_from_start = {node: i for i, node in enumerate(main_path)}
    distances_to_end = {node: len(main_path) - i - 1 for i, node in enumerate(main_path)}

    all_shortcuts = set()
    moves_ = moves(duration)
    for node in main_path:
        shortcuts = find_shortcuts(map_, node, moves_)
        all_shortcuts.update(shortcuts)

    savings = defaultdict(list)

    for entry, exit_ in all_shortcuts:
        start_to_entry_cost = distances_from_start[entry]
        entry_to_exit_cost = manhattan(entry, exit_)
        exit_to_end_cost = distances_to_end.get(exit_, None)

        if exit_to_end_cost is None:
            sub_map = deepcopy(map_)
            exit_to_end_path, exit_to_end_cost = next(next(search_graph(sub_map, start, end)))
            for i, (x, y) in enumerate(exit_to_end_path):
                distances_to_end[(x, y)] = len(exit_to_end_path) - i - 1

        total_cost_with_shortcut = start_to_entry_cost + entry_to_exit_cost + exit_to_end_cost

        saving = main_cost - total_cost_with_shortcut
        if saving > 0:
            savings[saving].append((entry, exit_))

    return sum(len(cheats) for saving, cheats in savings.items() if saving >= 100)


def find_shortcuts(map_, start, moves):
    x, y = start
    result = [(x + dx, y + dy) for dx, dy in moves]
    return [(start, (x, y)) for x, y in result if len(map_[0]) > x >= 0 and len(map_) > y >= 0 and map_[y][x] != '#']


def manhattan(entry, exit_):
    return abs(entry[0] - exit_[0]) + abs(entry[1] - exit_[1])


def scan(map_):
    start, end = None, None
    for y, l in enumerate(map_):
        for x, c in enumerate(l):
            if map_[y][x] == 'S':
                start = (x, y)
            elif map_[y][x] == 'E':
                end = (x, y)
    return start, end


def search_graph(map_, start, end) -> Union[Iterator[Iterator[tuple]], None]:

    def neighbours(node: tuple):
        x, y = node
        return [(x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1)] if
                map_[y + b][x + a] != '#']

    def heuristic(node: tuple):
        x, y = node
        e_x, e_y = end
        return abs(x - e_x) + abs(y - e_y)

    return astar.find_path(start,
                           is_goal_reached_fun=lambda current: current == end,
                           neighbors_fun=neighbours,
                           heuristic_cost_estimate_fun=heuristic)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day20_sample" if TEST_MODE else "input/day20").open() as f:
        values = [i.strip() for i in f]
        now = time()
        print(f'Phase 1: {phase1(values)} {round(time() - now, 3)}s')
        now = time()
        print(f'Phase 2: {phase2(values)} {round(time() - now, 3)}s')
