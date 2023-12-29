import math
from collections import defaultdict
from pathlib import Path

from igraph import Graph

TEST_MODE = False


def phase1(graph, duplex_graph):

    index = {}
    for i, v in enumerate(duplex_graph.keys()):
        index[v] = i

    edges = list(all_edges(graph))
    indexed_edges = [(index[v1], index[v2]) for v1, v2 in edges]

    cut = Graph(edges=indexed_edges).mincut()
    return math.prod(cut.sizes())


def phase2(graph, duplex_graph):
    return -1


def all_edges(graph):
    for k, v in graph.items():
        for i in v:
            yield k, i


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
