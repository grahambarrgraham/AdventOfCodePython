from pathlib import Path

TEST_MODE = False

moves = {(0, 1), (0, -1), (1, 0), (-1, 0)}


def phase1(garden):
    start = [(find_start(garden))]

    for i in range(64):
        start = walk(garden, [(s, 0) for s in start])
        # print(f"{i + 1} {len(start)}")
    return len(start)


def phase2():
    # results taken from phase at 65, 65 + 131 and 65 + 131 + 131 steps
    # required help from reddit
    # can also be calculated using lagrange interpolation: https://www.dcode.fr/lagrange-interpolating-polynomial?__r=1.a9885fb68053dff943c8891f09fe61fb
    pre_cal = {65: 3701, 196: 33108, 327: 91853}
    first_increment = pre_cal[196] - pre_cal[65]
    second_increment = pre_cal[327] - pre_cal[196]
    first_order_inc = second_increment - first_increment
    second_order_inc = first_increment + first_order_inc + first_order_inc
    plots_visited = pre_cal[327] + second_order_inc
    steps = 327 + 131 + 131

    while steps <= 26501365:
        second_order_inc += first_order_inc
        plots_visited += second_order_inc
        steps += 131

    return plots_visited


def pretty_print(garden, locs):
    print()
    for y in range(len(garden)):
        line = ''
        for x in range(len(garden[0])):
            line += 'O' if (x, y) in locs else garden[y][x]
        print(line)


def walk(garden, start, max_steps=1):
    queue = []
    closed = set()
    queue.extend(start)
    while len(queue) > 0:
        current, steps = queue.pop(0)

        if steps >= max_steps:
            continue
        for n in find_neighbours(current, garden, closed):
            nxt = (n, steps + 1)
            queue.append(nxt)
            closed.add(n)

    return closed


def find_start(garden):
    for y in range(len(garden)):
        for x in range(len(garden[0])):
            if garden[y][x] == 'S':
                return x, y


def find_neighbours(coord, garden, closed):
    x, y = coord
    neighbours = [(x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1)]]
    return [(x, y) for x, y in neighbours if garden[y % len(garden)][x % len(garden[0])] != '#' and (x, y) not in closed]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day21_sample" if TEST_MODE else "input/day21").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2()}')
