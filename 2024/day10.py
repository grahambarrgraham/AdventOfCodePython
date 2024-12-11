import collections
from pathlib import Path

TEST_MODE = False


class Graph:
    def __init__(self, map_):
        self.map_ = map_
        self.starts = []
        for y, l in enumerate(map_):
            for x, c in enumerate(l):
                if map_[y][x] == 0:
                    self.starts.append((x, y))

    def neighbours(self, x, y):
        result = []
        for n_x, n_y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nxt_x, nxt_y = x + n_x, y + n_y
            if 0 <= nxt_y < len(self.map_) and 0 <= nxt_x < len(self.map_[0]):
                if self.map_[nxt_y][nxt_x] - self.map_[y][x] == 1:
                    result.append((nxt_x, nxt_y))
        return result

    def destination(self, x, y):
        return self.map_[y][x] == 9

    def search(self, start):
        queue = collections.deque()
        queue.append((start, 0))
        results = list()
        while len(queue) > 0:
            node, distance = queue.popleft()

            if self.destination(*node):
                results.append(node)

            neighbours = self.neighbours(*node)
            for neighbour in neighbours:
                next_val = (neighbour, distance + 1)
                queue.append(next_val)
        return results


def phase1(v):
    graph = Graph(v)
    return sum([len(set(graph.search(start))) for start in graph.starts])


def phase2(v):
    graph = Graph(v)
    return sum([len(graph.search(start)) for start in graph.starts])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day10_sample" if TEST_MODE else "input/day10").open() as f:
        values = [[int(x) for x in i.strip()] for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
