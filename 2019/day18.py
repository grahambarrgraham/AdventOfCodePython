from dataclasses import dataclass
from pathlib import Path
from time import time

import astar

TEST_MODE = False


class Graph:

    def __init__(self, map_):
        self.map_ = map_
        self.graph, self.doors, self.keys, self.robots = Graph.build_graph(map_)
        self.graph = self.compress_graph()

    @staticmethod
    def build_graph(map_):
        graph, doors, keys, starts = {}, {}, {}, set()
        for y in range(len(map_)):
            for x in range(len(map_[0])):
                if map_[y][x] != '#':
                    graph[(x, y)] = [(n, 1) for n in Graph.find_neighbours((x, y), map_)]
                    if map_[y][x] == '@':
                        starts.add((x, y))
                    elif map_[y][x].isupper():
                        doors[map_[y][x]] = (x, y)
                    elif map_[y][x].islower():
                        keys[map_[y][x]] = (x, y)

        return graph, doors, keys, starts

    @staticmethod
    def find_neighbours(coord, v):
        x, y = coord

        neighbours = [(a, b, x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1)] if
                      len(v[0]) > x + a >= 0 and len(v) > y + b >= 0]

        return [(n_x, n_y) for a, b, n_x, n_y in neighbours if v[n_y][n_x] != '#']

    def compress_graph(self):
        queue = [(1, 1)]
        visited = {(1, 1)}
        map_, graph = self.map_, self.graph.copy()
        while queue:
            cur_vert = queue.pop()
            new_neighbours = []
            for nxt_vert, nxt_length in graph[cur_vert]:
                num_edges = len(graph[nxt_vert])
                n_x, n_y = nxt_vert
                if num_edges == 2 and map_[n_y][n_x] == '.':
                    nxt_2_vert, nxt_2_length = [(n, l) for n, l in graph[nxt_vert] if n != cur_vert][-1]
                    new_neighbours.append((nxt_2_vert, nxt_length + nxt_2_length))
                    graph[nxt_2_vert].remove((nxt_vert, nxt_2_length))
                    graph[nxt_2_vert].append((cur_vert, nxt_length + nxt_2_length))
                    del graph[nxt_vert]
                else:
                    new_neighbours.append((nxt_vert, nxt_length))
            graph[cur_vert] = new_neighbours
            visited.add(cur_vert)
            queue.extend([n for n, _ in new_neighbours if n not in visited])

        dead_ends = [(x, y) for (x, y), v in graph.items() if map_[y][x] == '.' and len(v) == 1]
        return {(x, y): [((x1, y1), l) for (x1, y1), l in v if (x1, y1) not in dead_ends] for (x, y), v in
                graph.items() if (x, y) not in dead_ends}

    def val_at(self, x, y):
        return self.map_[y][x]


@dataclass(frozen=True)
class SearchNode:
    robots: tuple
    doors: tuple
    keys: tuple


def find_keys_cost(map_) -> int:
    graph = Graph(map_)

    def cost(a: SearchNode, b: SearchNode):
        for i, a_robot in enumerate(a.robots):
            b_robot = b.robots[i]
            if a_robot != b_robot:
                cost = [w for l, w in graph.graph[a_robot] if l == b_robot][0]
                return cost
        raise Exception('no robot moved')

    def neighbours(node: SearchNode):
        result_ = []
        for i, robot in enumerate(node.robots):
            for nxt_robot_loc, nxt_doors, nxt_keys in robot_neighbours(robot, node.doors, node.keys):
                robots = list(node.robots)
                robots[i] = nxt_robot_loc
                result_.append(SearchNode(tuple(robots), nxt_doors, nxt_keys))
        return result_

    def robot_neighbours(robot, doors, keys):
        neighbours__ = [(x, y) for (x, y), _ in graph.graph[robot] if graph.val_at(x, y) not in doors]
        result_ = []
        for x, y in neighbours__:
            c = graph.map_[y][x]
            nxt_doors = doors
            nxt_keys = keys
            if c.islower():
                if c.upper() in graph.doors:
                    door_loc = graph.doors[c.upper()]
                    door = graph.val_at(*door_loc)
                    if door in doors:
                        tmp_doors = list(doors)
                        tmp_doors.remove(door)
                        nxt_doors = tuple(tmp_doors)
                key = graph.val_at(x, y)
                if key in keys:
                    tmp_keys = list(keys)
                    tmp_keys.remove(key)
                    nxt_keys = tuple(tmp_keys)
            result_.append(((x, y), nxt_doors, nxt_keys))
        return result_

    start = SearchNode(tuple(graph.robots), tuple(graph.doors.keys()), tuple(graph.keys.keys()))

    result = astar.find_path(start, None,
                             neighbours,
                             heuristic_cost_estimate_fnct=lambda current, goal: len(current.keys),
                             distance_between_fnct=cost,
                             is_goal_reached_fnct=lambda current, goal: len(current.keys) == 0
                             )
    result = list(result)
    # print([graph.val_at(*n.robots) for n in result if graph.val_at(*n.robots).islower()])
    costs = [cost(result[x], result[x + 1]) for x in range(len(result) - 1)]
    return sum(costs)


def phase1(v):
    return find_keys_cost(v)


def phase2(v):
    def find_start():
        for y, l in enumerate(v):
            for x, c in enumerate(l):
                if c == '@':
                    return x, y
        return None

    x, y = find_start()
    v[y - 1] = v[y - 1][:x - 1] + "@#@" + v[y - 1][x + 2:]
    v[y] = v[y][:x - 1] + "###" + v[y][x + 2:]
    v[y + 1] = v[y + 1][:x - 1] + "@*@" + v[y + 1][x + 2:]

    return find_keys_cost(v)
    # for y, l in enumerate(v):
    #     print(l)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day18_sample" if TEST_MODE else "input/day18").open() as f:
        values = [i.strip() for i in f]
        now = time()
        print(f'Phase 1: {phase1(values)} {round(time() - now, 3)}s')
        print(f'Phase 2: {phase2(values)} {round(time() - now, 3)}s')
