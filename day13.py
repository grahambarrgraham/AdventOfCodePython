from pathlib import Path
import collections
from functools import cmp_to_key

TEST_MODE = False

Lists = collections.namedtuple("Lists", "left, right")


def phase1(pairs):
    in_right_order_indexes = []
    for index, pair in enumerate(pairs):
        if in_right_order(pair):
            in_right_order_indexes.append(index + 1)
    return sum(in_right_order_indexes)


def phase2(pairs):
    all_packets = [[[2]], [[6]]]
    for pair in pairs:
        all_packets.append(pair.left)
        all_packets.append(pair.right)

    def compare(item1, item2):
        return 1 if in_right_order(Lists(item1, item2)) else -1

    all_packets.sort(key=cmp_to_key(compare), reverse=True)

    marker_1 = all_packets.index([[2]]) + 1
    marker_2 = all_packets.index([[6]]) + 1

    return marker_1 * marker_2


def in_right_order(pair):
    for index, left in enumerate(pair.left):
        if index >= len(pair.right):
            return False
        right = pair.right[index]
        both_are_int = isinstance(left, int) and isinstance(right, int)
        if both_are_int:
            if left < right:
                return True
            elif left > right:
                return False
            else:
                continue
        if isinstance(left, int):
            left = [left]
        if isinstance(right, int):
            right = [right]
        child_in_right_order = in_right_order(Lists(left, right))
        if child_in_right_order is None:
            continue
        return child_in_right_order

    if len(pair.left) < len(pair.right):
        return True

    return None


def parse(s):
    def parse_inner(s):
        n = []
        digits = ''
        while True:
            c = next(s)
            if c == '[':
                n.append(parse_inner(s))
            elif c == ',':
                if digits != '':
                    n.append(int(digits))
                    digits = ''
                continue
            elif c == ' ':
                continue
            elif c == ']':
                if digits != '':
                    n.append(int(digits))
                    digits = ''
                return n
            else:
                digits += c

    i = iter(s)
    next(i)
    return parse_inner(i)


def to_lists(param):
    return Lists(parse(param[0]), parse(param[1]))


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day13_sample" if TEST_MODE else "input/day13").open() as f:
        values = [to_lists(tuple(map(lambda x: x, line.split("\n")))) for line in f.read().split("\n\n")]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


