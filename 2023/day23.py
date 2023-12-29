import sys
import time

from pathlib import Path

TEST_MODE = False

# TAGS: DFS, Longest Path, IDDFS, cyclic graph, simple path

slope_map = {(-1, 0): '<', (1, 0): '>', (0, -1): '^', (0, 1): 'v'}


def phase1(v):
    target = (len(v[0]) - 2, len(v) - 1)
    graph = build_graph(v, slopes=True)
    path = longest_simple_path(graph, (1, 0), target)
    _, length = path[-1]
    return length


def phase2(v):
    target = (len(v[0]) - 2, len(v) - 1)
    graph = build_graph(v, slopes=False)
    # hint from reddit, join consecutive vertices with only two edges to make graph smaller
    graph = compress_graph(graph)
    path = longest_simple_path(graph, (1, 0), target)
    _, length = path[-1]
    return length


def print_map(v, path):
    for y in range(len(v)):
        for x in range(len(v[0])):
            print(v[y][x] if (x, y) not in path else 'O', end='')
        print()


def build_graph(v, slopes):
    graph = {}
    for y in range(len(v)):
        for x in range(len(v[0])):
            if v[y][x] != '#':
                graph[(x, y)] = [(n, 1) for n in find_neighbours((x, y), v, slopes)]
    return graph


def compress_graph(graph):
    queue = [(1, 0)]
    visited = {(1, 0)}
    while queue:
        cur_vert = queue.pop()
        new_neighbours = []
        for nxt_vert, nxt_length in graph[cur_vert]:
            num_edges = len(graph[nxt_vert])
            if num_edges == 2:
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

    return graph


def longest_simple_path(graph, start, end):
    sys.setrecursionlimit(15000)
    visited = {node: False for node in graph}
    max_path = []
    dfs(graph, start, visited, [], max_path, end)
    return max_path


def dfs(graph, node, visited, path, max_path, end, length=0):
    visited[node] = True
    path.append((node, length))
    max_length = 0 if not max_path else max_path[-1][1]
    if node == end and length > max_length:
        max_path[:] = path
    for neighbor, nxt_length in graph[node]:
        if not visited[neighbor]:
            dfs(graph, neighbor, visited, path, max_path, end, length + nxt_length)
    path.pop()
    visited[node] = False


def find_neighbours(coord, v, slopes=False):
    x, y = coord
    neighbours = [(a, b, x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1)] if
                  len(v[0]) > x + a >= 0 and len(v) > y + b >= 0]

    def can_move(nxt, slope):
        curr = v[y][x]
        return curr in [slope, '.'] and nxt in (slope, '.')

    if slopes:
        return [(n_x, n_y) for a, b, n_x, n_y in neighbours if can_move(v[n_y][n_x], slope_map[(a, b)])]
    else:
        return [(n_x, n_y) for a, b, n_x, n_y in neighbours if v[n_y][n_x] != '#']


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day23_sample" if TEST_MODE else "input/day23").open() as f:
        values = [i.strip() for i in f]
        st = time.time()
        phase1 = phase1(values)
        p1_time = time.time()
        print(f'Phase 1: {phase1} {round(p1_time - st, 3)}s')
        phase2 = phase2(values)
        p2_time = time.time()
        print(f'Phase 2: {phase2} {round(p2_time - p1_time, 3)}s')
