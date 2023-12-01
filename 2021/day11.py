from pathlib import Path
import sys
import copy
# import curses
# import time

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    return sum([len(generation_step(v, gen + 1)) for gen in range(100)])


def phase2(v):
    gen = 1
    all_octopuses = len(all_coords(v))
    while True:
        flashed = generation_step(v, gen)
        if len(flashed) == all_octopuses:
            break
        gen = gen + 1

    return gen


def generation_step(v, gen):
    candidates = all_coords(v)
    flashed = set()
    while True:
        generate(candidates, v)
        flashes = {(x, y) for (x, y) in candidates if v[y][x] > 9 and (x, y) not in flashed}
        reset_flashed(flashes, v)
        # print_grid(v, candidates, flashes, flashed, gen)
        if len(flashes) > 0:
            flashed = flashed.union(flashes)
            candidates = [(x, y) for (x, y) in flatten([neighbours(flash, v) for flash in flashes]) if
                          (x, y) not in flashed]
        else:
            break
    return flashed


# def print_grid(v, neighbours, flashes, flashed, gen):
#     def grid():
#         stdscr.addstr(0, 0, "\nGeneration" + str(gen) + "\n")
#         def format(coord, val):
#             if coord in flashes:
#                 stdscr.addstr(str(val), curses.color_pair(1))
#             elif coord in neighbours:
#                 stdscr.addstr(str(val), curses.color_pair(2))
#             elif coord in flashed:
#                 stdscr.addstr(str(val), curses.color_pair(3))
#             else:
#                 stdscr.addstr(str(val))
#         for y, line in enumerate(v):
#             for x, val in enumerate(v[y]):
#                 format((x, y), val)
#             stdscr.addstr("\n")
#     grid()
#     stdscr.refresh()
#     time.sleep(0.05)


def flatten(t):
    return [item for sublist in t for item in sublist]


def all_coords(v):
    return [(x, y) for y in range(len(v)) for x in range(len(v[0]))]


def neighbours(coord, v):
    (x, y) = coord
    return [(x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (1, -1), (-1, -1), (-1, 1)] if
            len(v[0]) > x + a >= 0 and len(v) > y + b >= 0]


def reset_flashed(coords, v):
    for (x, y) in coords:
        if v[y][x] > 9:
            v[y][x] = 0


def generate(coords, v):
    for (x, y) in coords:
        v[y][x] = v[y][x] + 1


if __name__ == "__main__":
    # global stdscr
    # stdscr = curses.initscr()
    # curses.start_color()
    # curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    # curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    # curses.noecho()
    # curses.cbreak()

    with Path(__file__).parent.joinpath("input/day11_sample" if TEST_MODE else "input/day11").open() as f:
        values = [[int(j) for j in i.strip()] for i in f]
        phase1 = phase1(copy.deepcopy(values))
        phase2 = phase2(copy.deepcopy(values))

        # curses.echo()
        # curses.nocbreak()
        # curses.endwin()

        print(f'Phase 1: {phase1}')
        print(f'Phase 2: {phase2}')
