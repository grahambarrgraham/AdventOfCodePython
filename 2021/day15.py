from pathlib import Path
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    return search(v)


def phase2(v):
    return search(big_graph(v))


def search(v):
    target_node = (len(v[0]) - 1), len(v) - 1
    return a_star_algorithm(v, (0, 0), target_node)


def big_graph(v):

    new_v = [None] * len(v) * 5

    for y, line in enumerate(v):
        for i in range(1, 5):
            v[y] = v[y] + [inc_val(x, i) for x in line]

    for y, line in enumerate(v):
        for i in range(5):
            new_v[y + (i * len(v))] = [inc_val(x, i) for x in v[y]]

    return new_v


def inc_val(val, inc):
    ret = val
    for i in range(inc):
        ret = 1 if ret == 9 else ret + 1
    return ret


def all_nodes(v):
    ret = []
    for y in range(len(v)):
        for x in range(len(v[0])):
            ret.append((x, y))
    return ret


neighbours_dict = {}


def find_neighbours(coord, v):
    if coord not in neighbours_dict:
        x, y = coord
        neighbours = [(x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1)] if
                len(v[0]) > x + a >= 0 and len(v) > y + b >= 0]

        neighbours_dict[coord] = neighbours

    return neighbours_dict[coord]


def cost(coord, v):
    x, y = coord
    return v[y][x]


def a_star_algorithm(graph, start, stop):
    open_set = {start}
    closed_set = set()
    node_scores = {start: 0}
    parents = {start: start}

    while len(open_set) > 0:
        n = None

        for v in open_set:
            if n is None or node_scores[v] < node_scores[n]:
                n = v

        if n is None:
            print('Path does not exist!')
            return None

        if n == stop:
            return node_scores[n]

        for m in find_neighbours(n, graph):
            weight = cost(m, graph)
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                parents[m] = n
                node_scores[m] = node_scores[n] + weight

            else:
                if node_scores[m] > node_scores[n] + weight:
                    node_scores[m] = node_scores[n] + weight
                    parents[m] = n

                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)

        open_set.remove(n)
        closed_set.add(n)

    return None


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day15_sample" if TEST_MODE else "input/day15").open() as f:
        values = [[int(j) for j in list(i.strip())] for i in f]
        print(f'Phase 1: {phase1(values)}')
        neighbours_dict = {}
        print(f'Phase 2: {phase2(values)}')



