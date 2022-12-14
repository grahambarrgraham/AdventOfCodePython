from pathlib import Path
import sys
import collections

TEST_MODE = False

Coord = collections.namedtuple('Coord', ('x', 'y'))
Search = collections.namedtuple('Search', ('graph', 'start', 'end', 'lines'))
Node = collections.namedtuple("Node", "point, distance")


def phase1(search):
    return bfs(search.graph, search.start, search.end)


def phase2(v_search):
    starts = [coord for coord in v_search.graph.keys() if v_search.lines[coord.y][coord.x] == 'a']
    return min([bfs(v_search.graph, start, v_search.end) for start in starts])


def bfs(graph, start, destination):
    visited = {start}
    queue = collections.deque()
    queue.append(Node(start, 0))

    while len(queue) > 0:
        node = queue.popleft()

        if node.point == destination:
            return node.distance

        neighbours = graph[node.point]
        for neighbour in neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                next_val = Node(neighbour, node.distance + 1)
                queue.append(next_val)

    return sys.maxsize


def generate_coords(v):
    return [Coord(x, y) for x in range(len(v[0])) for y in range(len(v))]


def find_neighbours(coord, lines):
    neighbours = [Coord(coord.x + 1, coord.y),
                  Coord(coord.x - 1, coord.y),
                  Coord(coord.x, coord.y + 1),
                  Coord(coord.x, coord.y - 1)]
    return [n for n in neighbours if 0 <= n.x < len(lines[0]) and 0 <= n.y < len(lines)]


def can_transit(from_node, to_node):
    return ord('z' if to_node == 'E' else to_node) \
        - ord('a' if from_node == 'S' else from_node) <= 1


def parse_graph(lines):
    start = None
    end = None
    edges = {}
    for coord in generate_coords(lines):
        current = lines[coord.y][coord.x]
        neighbours = [n for n in find_neighbours(coord, lines) if can_transit(current, lines[n.y][n.x])]
        if current == 'S':
            start = coord
        elif current == 'E':
            end = coord
        edges[coord] = neighbours
    return Search(edges, start, end, lines)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day12_sample" if TEST_MODE else "input/day12").open() as f:
        values = parse_graph([i.strip() for i in f])
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
