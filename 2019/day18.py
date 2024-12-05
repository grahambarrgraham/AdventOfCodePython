from pathlib import Path

TEST_MODE = True


def phase1(v):
    g = build_graph(v)
    g = compress_graph(g)
    for k, v in g.items():
        print(k, v)
    return -1


def phase2(v):
    return -1


def print_map(v, path):
    for y in range(len(v)):
        for x in range(len(v[0])):
            print(v[y][x] if (x, y) not in path else 'O', end='')
        print()


def build_graph(v):
    graph = {}
    for y in range(len(v)):
        for x in range(len(v[0])):
            if v[y][x] != '#':
                graph[(x, y)] = [(n, 1, v[y][x]) for n in find_neighbours((x, y), v)]
    return graph


def compress_graph(graph):
    queue = [(1, 1)]
    visited = {(1, 1)}
    while queue:
        cur_vert = queue.pop()
        new_neighbours = []
        for nxt_vert, nxt_length, thing in graph[cur_vert]:
            num_edges = len(graph[nxt_vert])
            if num_edges == 2:
                nxt_2_vert, nxt_2_length = [(n, l) for n, l, _ in graph[nxt_vert] if n != cur_vert][-1]
                new_neighbours.append((nxt_2_vert, nxt_length + nxt_2_length))
                graph[nxt_2_vert].remove((nxt_vert, nxt_2_length))
                graph[nxt_2_vert].append((cur_vert, nxt_length + nxt_2_length, thing))
                del graph[nxt_vert]
            else:
                new_neighbours.append((nxt_vert, nxt_length))
        graph[cur_vert] = new_neighbours
        visited.add(cur_vert)
        queue.extend([n for n, _ in new_neighbours if n not in visited])

    return graph


def find_neighbours(coord, v):
    x, y = coord

    neighbours = [(a, b, x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1)] if
                  len(v[0]) > x + a >= 0 and len(v) > y + b >= 0]

    return [(n_x, n_y) for a, b, n_x, n_y in neighbours if v[n_y][n_x] != '#']


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day18_sample" if TEST_MODE else "input/day18").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
