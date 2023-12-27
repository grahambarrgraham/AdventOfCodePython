import itertools
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

TEST_MODE = False


def phase1(graph, duplex_graph):
    # print(graph)
    reachable = bfs(duplex_graph, [], "cmg")
    # print(len(duplex_graph), len(reachable))
    # print(sorted(reachable))
    # print(sorted(duplex_graph.keys()))
    edges = list(all_edges(graph))
    edges.sort(key=lambda n: degree(n, duplex_graph), reverse=True)
    threes = itertools.combinations(edges, 3)
    group_count = 0
    num_vertices = len(duplex_graph.keys())
    i = 0
    for cuts in threes:
        print(i, [(c, degree(c, duplex_graph)) for c in cuts])
        # cut_graph = apply_cut(cuts, duplex_graph)
        reachable = bfs(duplex_graph, cuts, "cmg")
        if len(reachable) < num_vertices:
            group_count = len(reachable)
            break
        i += 1

    b = len(duplex_graph) - group_count
    # print(b)

    return b * group_count


def degree(edge, graph):
    v_a, v_b = edge
    return len(graph[v_a]) + len(graph[v_b])


def apply_cut(cuts, duplex_graph):
    result = deepcopy(duplex_graph)
    for a, b in cuts:
        result[a].remove(b)
        result[b].remove(a)
    return result


def phase2(graph, duplex_graph):
    return -1


def all_edges(graph):
    for k, v in graph.items():
        for i in v:
            yield k, i


def bfs(graph, cuts, start):
    visited = {start}
    queue = [start]

    while len(queue) > 0:
        node = queue.pop(0)

        neighbours = graph[node]
        for neighbour in neighbours:
            if neighbour not in visited \
                    and (node, neighbour) not in cuts \
                    and (neighbour, node) not in cuts:
                visited.add(neighbour)
                queue.append(neighbour)

    return visited


def to_graph(graph):
    r_graph = defaultdict(list)
    for k, v in graph.items():
        r_graph[k].extend(v)
        for i in v:
            r_graph[i].append(k)
    return r_graph


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day25_sample" if TEST_MODE else "input/day25").open() as f:
        values = [i.strip().split(": ") for i in f]
        _graph = {x[0]: x[1].split(' ') for x in values}
        _duplex_graph = to_graph(_graph)
        print(f'Phase 1: {phase1(_graph, _duplex_graph)}')
        print(f'Phase 2: {phase2(_graph, _duplex_graph)}')
