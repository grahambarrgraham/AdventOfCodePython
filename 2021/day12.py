from pathlib import Path
import sys
from collections import defaultdict

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):

    def visited(node, path):
        return node == 'start' or (node.islower() and node in path)

    return search(v, visited)


def phase2(v):

    def visited(node, path):
        return node == 'start' or (node.islower() and node in path and max({i: path.count(i) for i in path if i.islower()}.values()) > 1)

    return search(v, visited)


def search(cave_dict, visited_func):

    def find_paths(path):
        last_node = path[-1]

        children = [child for child in cave_dict[last_node] if not visited_func(child, path)]

        for child in children:
            next_path = path + [child]
            if child == 'end':
                all_paths.append(next_path)
            else:
                find_paths(next_path)

    all_paths = list()
    find_paths(['start'])
    return len(all_paths)


def load(v):
    res = defaultdict(list)
    for i, j in v:
        res[i].append(j)
        res[j].append(i)
    return dict(res)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day12_sample" if TEST_MODE else "input/day12").open() as f:
        cave_dict = load(([i.strip().split('-') for i in f]))
        print(f'Phase 1: {phase1(cave_dict)}')
        print(f'Phase 2: {phase2(cave_dict)}')
