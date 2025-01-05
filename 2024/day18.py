from pathlib import Path

from lib import astar

TEST_MODE = False

width = height = 6 if TEST_MODE else 70


def phase1(v):
    corruption = v[:12 if TEST_MODE else 1024]
    path, cost = search_graph(corruption)
    return cost


def phase2(v):
    start = 12 if TEST_MODE else 1024
    current = start
    step = 1000
    while step >= 1:
        for n in range(current, len(v), step):
            corruption = v[:n]
            result = search_graph(corruption)
            if result is None and step == 1:
                return corruption[-1]
            elif result is None:
                current = n - step
                step //= 10
                break

    return None


def search_graph(corruption: set):
    def neighbours(node: tuple):
        x, y = node
        candidates = [(x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1)] if
                      width >= x + a >= 0 and height >= y + b >= 0]
        return [(x, y) for x, y in candidates if (x, y) not in corruption]

    result = astar.find_path((0, 0),
                             is_goal_reached_fun=lambda current: current == (width, height),
                             neighbors_fun=neighbours)

    def unpack(r):
        r = next(r, None)
        return None if r is None else next(r, None)

    return None if result is None else unpack(result)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day18_sample" if TEST_MODE else "input/day18").open() as f:
        values = [i.split(',') for i in f]
        values = [(int(a), int(b)) for a, b in values]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
