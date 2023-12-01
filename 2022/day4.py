from pathlib import Path

TEST_MODE = True


def is_in(r1, r2):
    return r2[1] >= r1[0] >= r2[0] and r2[1] >= r1[1] >= r2[0]


def overlaps(r1, r2):
    return r2[1] >= r1[0] >= r2[0] or r2[1] >= r1[1] >= r2[0]


def either_overlaps(elf1, elf2):
    return overlaps(elf1, elf2) or overlaps(elf2, elf1)


def is_fully_contained(elf1, elf2):
    return is_in(elf1, elf2) or is_in(elf2, elf1)


def phase1(v):
    return len(list(filter(lambda i: is_fully_contained(*i), v)))


def phase2(v):
    return list(filter(lambda i: either_overlaps(*i), v))


def parse_assignment(s):
    return [tuple(int(i) for i in p.split('-')) for p in s.split(',')]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day4_sample" if TEST_MODE else "input/day4").open() as f:
        values = [parse_assignment(i) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


