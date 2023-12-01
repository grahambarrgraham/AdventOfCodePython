from pathlib import Path
import collections

TEST_MODE = False

Coord = collections.namedtuple('Coord', ('x', 'y'))


def phase1(v):
    return len([coord for coord in generate_coords(v) if is_visible(v, coord.x, coord.y)])


def phase2(v):
    return max([scenic_score(v, coord.x, coord.y) for coord in generate_coords(v)])


def generate_coords(v):
    return [Coord(x, y) for x in range(len(v[0])) for y in range(len(v))]


def scenic_score(v, x, y):
    def score(fun):
        return len(list(scene(fun(v, x, y), v[y][x])))
    return 0 if on_edge(v, x, y) else score(above) * score(below) * score(left) * score(right)


def scene(view, height):
    for tree in view:
        yield tree
        if tree >= height:
            return


def is_visible(v, x, y):
    def visible(fun):
        return max(fun(v, x, y)) < v[y][x]
    return on_edge(v, x, y) or visible(above) or visible(below) or visible(left) or visible(right)


def on_edge(v, x, y):
    return x == 0 or x == len(v[0]) - 1 or y == 0 or y == len(v) - 1


def above(v, x, y):
    return reversed(col(v, x)[:y])


def below(v, x, y):
    return col(v, x)[y + 1:]


def left(v, x, y):
    return reversed(row(v, y)[:x])


def right(v, x, y):
    return row(v, y)[x + 1:]


def row(v, i):
    return v[i]


def col(v, i):
    return [x[i] for x in v]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day8_sample" if TEST_MODE else "input/day8").open() as f:
        values = [[int(i) for i in list(line.strip())] for line in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
