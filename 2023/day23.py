import collections
from copy import deepcopy
from pathlib import Path

import astar

TEST_MODE = False

slope_map = {(-1, 0): '<', (1, 0): '>', (0, -1): '^', (0, 1): 'v'}


def phase1(v):
    start = (1, 0)
    target = (len(v[0]) - 2, len(v) - 1)

    graph = {}
    for y in range(len(v)):
        for x in range(len(v[0])):
            if v[y][x] != '#':
                graph[(x, y)] = find_neighbours((x, y), v)

    routes = bfs(graph, start, target)
    longest = routes[-1]

    print([len(r) for r in routes])

    # result = astar.find_path((start, frozenset(start)), None,
    #                          lambda search_node: find_neighbours_s(search_node, v),
    #                          # heuristic_cost_estimate_fnct=lambda a, b: 99999999,
    #                          distance_between_fnct=lambda a, b: 1,
    #                          is_goal_reached_fnct=lambda n, _: n[0] == target)
    #
    # l = [x for x, y in result]
    # print(l)

    for y in range(len(v)):
        for x in range(len(v[0])):
            print(v[y][x] if (x, y) not in longest else 'O', end='')
        print()

    print(sorted(longest))
    return len(longest)
    # return len(l)


def phase2(v):
    return -1


def bfs(graph, start, destination):
    queue = [(start, set())]
    acc = []

    while len(queue) > 0:
        node, visited = queue.pop()

        if node == destination:
            print("found", len(visited), "queue", len(queue))
            acc.append(visited)

        neighbours = graph[node]
        for neighbour in neighbours:

            if neighbour not in visited:
                nxt = set(visited)
                nxt.add(node)
                queue.append((neighbour, nxt))

    return acc


def find_neighbours_s(n, v):
    c, visited = n
    res = find_neighbours(c, v)
    nxt = set(visited)
    nxt.add(c)
    return [(x, frozenset(nxt)) for x in res if x not in visited]


def find_neighbours(coord, v):
    x, y = coord

    neighbours = [(a, b, x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1)] if
                  len(v[0]) > x + a >= 0 and len(v) > y + b >= 0]

    def can_move(nxt, slope):
        curr = v[y][x]
        return curr in [slope, '.'] and nxt in (slope, '.')

    def can_move_v2(nxt):
        return nxt != '#'

    # neighbours = [(n_x, n_y) for a, b, n_x, n_y in neighbours if can_move(v[n_y][n_x], slope_map[(a, b)])]
    neighbours = [(n_x, n_y) for a, b, n_x, n_y in neighbours if can_move_v2(v[n_y][n_x])]

    # if coord in [(11, 3), (12, 3)]:
    #     print(coord, v[y][x], neighbours)

    return neighbours


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day23_sample" if TEST_MODE else "input/day23").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
