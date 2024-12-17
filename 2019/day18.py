import collections
from dataclasses import dataclass
from pathlib import Path
from time import time

import astar

TEST_MODE = False


class Graph:

    def __init__(self, map_):
        self.map_ = map_
        self.doors, self.keys, self.robots = Graph.scan(map_)
        self.graph = self.compress_graph()

    @staticmethod
    def scan(map_):
        doors, keys, starts = {}, {}, set()
        for y, l in enumerate(map_):
            for x, c in enumerate(l):
                if map_[y][x] != '#':
                    if map_[y][x] == '@':
                        starts.add((x, y))
                    elif map_[y][x].isupper():
                        doors[map_[y][x]] = (x, y)
                    elif map_[y][x].islower():
                        keys[map_[y][x]] = (x, y)

        return doors, keys, starts

    def neighbours(self, x, y):
        width, height = len(self.map_[0]), len(self.map_)
        neighbours = [(x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1)]]
        return [(x, y) for x, y in neighbours if width > x >= 0 and height > y >= 0 and self.val_at(x, y) != '#']

    def compress_graph(self):
        queue = collections.deque()
        queue.extend(self.robots)
        results = {}
        while len(queue) > 0:
            nxt = queue.popleft()
            result = self.search(nxt)
            results[nxt] = result
            queue.extend([n for n, _ in result if n not in results.keys()])
        return results

    def search(self, start):
        queue = collections.deque()
        queue.append((start, 0))
        visited = {start}
        results = []
        while len(queue) > 0:
            nxt, distance = queue.popleft()
            if nxt not in visited and self.val_at(*nxt) != '.':
                results.append((nxt, distance))
                visited.add(nxt)
                continue
            visited.add(nxt)
            for neighbour in self.neighbours(*nxt):
                if neighbour not in visited:
                    next_val = (neighbour, distance + 1)
                    queue.append(next_val)
        return results

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

    result = list(astar.find_path(start, None,
                                  neighbours,
                                  heuristic_cost_estimate_fnct=lambda current, goal: len(current.keys),
                                  distance_between_fnct=cost,
                                  is_goal_reached_fnct=lambda current, goal: len(current.keys) == 0
                                  ))

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


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day18_sample" if TEST_MODE else "input/day18").open() as f:
        values = [i.strip() for i in f]
        now = time()
        print(f'Phase 1: {phase1(values)} {round(time() - now, 3)}s')
        print("Phase 2 takes about 230s")
        print(f'Phase 2: {phase2(values)} {round(time() - now, 3)}s')
