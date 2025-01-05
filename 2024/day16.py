
from dataclasses import dataclass
from pathlib import Path
from time import time
from typing import Iterator, Union

from lib import astar

TEST_MODE = False


class Graph:

    def __init__(self, map_):
        self.map_ = map_
        self.start, self.end = Graph.scan(map_)

    @staticmethod
    def scan(map_):
        start, end = None, None
        for y, l in enumerate(map_):
            for x, c in enumerate(l):
                if map_[y][x] == 'S':
                    start = (x, y)
                elif map_[y][x] == 'E':
                    end = (x, y)
        return start, end

    def val_at(self, x, y):
        return self.map_[y][x]


@dataclass(frozen=True)
class SearchNode:
    loc: tuple
    dir: str


move_map = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}
move_nb = {'>': ['^', 'v'], '<': ['^', 'v'], '^': ['<', '>'], 'v': ['<', '>']}


def next_move(graph, node: SearchNode):
    x, y = node.loc
    m_x, m_y = move_map[node.dir]
    return None if graph.val_at(x + m_x, y + m_y) == '#' else SearchNode((x + m_x, y + m_y), node.dir)


def cost(a: SearchNode, b: SearchNode):
    result = 0
    if a.loc != b.loc:
        result += 1
    if a.dir != b.dir:
        result += 1000
    return result


def search_graph(map_) -> Union[Iterator[Iterator[SearchNode]], None]:
    graph = Graph(map_)

    def neighbours(node: SearchNode):
        result = []
        x, y = node.loc
        nxt = next_move(graph, node)
        if nxt is not None:
            result.append(nxt)
        turns = [SearchNode((x, y), new_dir) for new_dir in move_nb[node.dir]]
        turns = [turn for turn in turns if next_move(graph, turn) is not None]
        result.extend(turns)
        return result

    return astar.find_path(SearchNode(graph.start, '>'),
                           is_goal_reached_fun=lambda current: current.loc == graph.end,
                           neighbors_fun=neighbours,
                           edge_cost_fun=cost,
                           heuristic_cost_estimate_fun=lambda a: 0)


def phase1(v):
    _, path_cost = next(next(search_graph(v)))
    return path_cost


def phase2(v):
    paths = next(search_graph(v))
    result = set()
    for path, _ in paths:
        result |= {node.loc for node in path}
    return len(result)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day16_sample" if TEST_MODE else "input/day16").open() as f:
        values = [i.strip() for i in f]
        now = time()
        print(f'Phase 1: {phase1(values)} {round(time() - now, 3)}s')
        print(f'Phase 2: {phase2(values)} {round(time() - now, 3)}s')
