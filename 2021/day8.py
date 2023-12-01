from pathlib import Path
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    return len([val for val in (flatten([line[1] for line in v])) if len(val) in [2, 3, 4, 7]])


def phase2(v):
    return sum([decode_line(line[0], line[1]) for line in v])


def decode_line(patterns, output):
    one_code = [pattern for pattern in patterns if len(pattern) == 2][0]
    four_code = [pattern for pattern in patterns if len(pattern) == 4][0]
    digits = [decode_digit(digit, one_code, four_code) for digit in output]
    return to_number(digits)


def to_number(digits):
    s = ''.join(map(str, digits))
    return int(s)


def flatten(t):
    return [item for sublist in t for item in sublist]


def decode_digit(n, one_code, four_code):
    match len(n):
        case 2:
            return 1
        case 3:
            return 7
        case 4:
            return 4
        case 5:
            four_icount = intersect_count(four_code, n)
            one_icount = intersect_count(one_code, n)
            return 2 if four_icount == 2 else 5 if one_icount == 1 else 3
        case 6:
            four_icount = intersect_count(four_code, n)
            one_icount = intersect_count(one_code, n)
            return 9 if four_icount == 4 else 0 if one_icount == 2 else 6
        case 7:
            return 8


def intersect_count(a, b):
    return len(set(a).intersection(set(b)))


if __name__ == "__main__":

    def parse(v):
        return v[0].strip().split(" "), v[1].strip().split(" ")

    with Path(__file__).parent.joinpath("input/day8_sample" if TEST_MODE else "input/day8").open() as f:
        values = [parse(i.split('|')) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
