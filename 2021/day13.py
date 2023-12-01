from pathlib import Path
import sys
import re

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    (dots, v_folds) = v
    return len(fold(dots, [v_folds[0]]))


def phase2(v):
    (dots, v_folds) = v
    return fold(dots, v_folds)


def pretty_print(dots):
    for y in range(8):
        line = ''
        for x in range(40):
            line += 'X' if (x, y) in dots else ' '
        print(line)


def fold(dots, folds):
    for fold in folds:
        (axis, line) = fold
        dots = fold_up(dots, line) if axis == 'y' else fold_left(dots, line)
    return dots


def fold_up(dots, y_fold):
    staying = [(x, y) for (x, y) in dots if y <= y_fold]
    moving = [(x, y - ((y - y_fold) * 2)) for (x, y) in dots if y > y_fold]
    return set(staying + moving)


def fold_left(dots, x_fold):
    staying = [(x, y) for (x, y) in dots if x <= x_fold]
    moving = [(x - ((x - x_fold) * 2), y) for (x, y) in dots if x > x_fold]
    return set(staying + moving)


def load(v):
    def load_fold(s):
        matches = re.match(r"fold along (.)=(\d+)", s)
        return matches.group(1), int(matches.group(2))

    def load_dot(s):
        return int(s[0]), int(s[1])

    dots, folds = [], []
    for x in v:
        folds.append(load_fold(x)) if x.startswith("fold") else dots.append(load_dot(x.split(",")))
    return dots, folds


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day13_sample" if TEST_MODE else "input/day13").open() as f:
        values = load([i.strip() for i in f if len(i) > 1])
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2:')
        pretty_print(phase2(values))
