import collections
import re
from functools import cache
from pathlib import Path

TEST_MODE = False

Match = collections.namedtuple("Match", "springs groups")


def phase1(v: list[Match]):
    return sum(process(v))


def phase2(v):
    # v = v[2:3]
    # v = v[14:15]
    # firsts = process(v)
    # print(firsts)
    # seconds = process([unfold(m, 2) for m in v])
    # print(seconds)
    # # d = process([unfold(m, 3) for m in v])
    # # print(d)
    # # d = process([unfold(m, 5) for m in v])
    # # print(d)
    # multipliers = [pow(second / first, 4) for first, second in zip(firsts, seconds)]
    # print(multipliers)
    # vals = [first * multiplier for first, multiplier in zip(firsts, multipliers)]
    # print(vals)
    # return sum(vals)
    return -1


def unfold(m, num):
    s = (m.springs + '?') * num
    s = s[:-1]
    g = m.groups * num
    return Match(s, g)


def process(v):
    return [len(fits) for fits in [match(m) for m in v]]


def match(m):
    last_g = 0
    fits = [[]]
    for i, g in enumerate(m.groups):
        fits = find_fits(m.springs, fits, g, last_g)
        last_g = g
        # print(f"group: {i}={g} fits={len(fits)}")
    fits = [f for f in fits if count_groups(f, m) == len(m.groups)]

    # print(f"{m.springs} {m.groups}")
    # for fit, pretty in zip(fits, stringify_fits(fits, m)):
    #     # if count_groups(fit, m) != len(m.groups):
    #     #     print()
    #     #     print(f"{m.springs} {m.groups} {len(fits)}");
    #         print(f"{pretty} {fit} {count_groups(fit, m)}")
    # print(f"{m.springs} {m.groups} {len(fits)}")
    # print(f"{m.springs} {m.groups} {len(fits)} {list(zip(fits, pretty_print(fits, m)))}")
    # print(len(fits))
    return fits


@cache
def find_fits_(springs, num, start_index) -> list[int]:
    acc = []
    for i in range(start_index, len(springs) - num + 1):
        next_index = i + num
        no_dots = '.' not in springs[i: next_index]
        next_is_not_hash = (next_index < len(springs) and springs[next_index] != '#')
        next_is_at_end = next_index == len(springs)
        previous_is_not_hash = i > 0 and springs[i-1] != '#'
        at_start = i == 0
        if no_dots and (next_is_not_hash or next_is_at_end) and (previous_is_not_hash or at_start):
            acc.append(i)
    return acc


def find_fits(springs: str, fits: list[list[int]], num: int, last_num: int):

    def placement(_fit):
        start = _fit[-1] + last_num + 1
        for i in range(start, len(springs)):
            if springs[i-1] != '#':
                break
            start += 1
        return start

    acc = []
    for fit in fits:
        next_fits = find_fits_(springs, num, 0 if len(fit) == 0 else placement(fit))
        # next_fits = [f for f in next_fits if springs[f[0]] != '#']
        new = [fit + [next_fit] for next_fit in next_fits]
        acc.extend(new)
    return acc


def stringify_fit(fit, m):
    res = list(m.springs)
    for f, num in zip(fit, m.groups):
        for p in range(f, f+num):
            if m.springs[p] == '?':
                res[p] = 'X'
    join = "".join(res)
    join = join.replace('?', '.')
    return join


def stringify_fits(fits, m):
    acc = []
    for fit in fits:
        res = stringify_fit(fit, m)
        acc.append(res)
    return acc


def count_groups(fit, m):
    s = stringify_fit(fit, m)
    split = re.split("\\.+", s)
    return len([s for s in split if len(s) > 0])


def phase1(v: list[Match]):
    # v = v[-1:]
    acc = []
    for m in v:
        index = 0
        last_g = 0
        fits = [[]]
        for g in m.groups:
            fits = find_fits(m.springs, fits, g, last_g)
            last_g = g

        fits = [f for f in fits if count_groups(f, m) == len(m.groups)]
        acc.append(fits)

        # for fit, pretty in zip(fits, stringify_fits(fits, m)):
        #     if count_groups(fit, m) != len(m.groups):
        #         print()
        #         print(f"{m.springs} {m.groups} {len(fits)}");
        #         print(f"{pretty} {fit} {count_groups(fit, m)}")
        # print(f"{m.springs} {m.groups} {len(fits)}")
        # print(f"{m.springs} {m.groups} {len(fits)} {list(zip(fits, pretty_print(fits, m)))}")

    return sum([len(fits) for fits in acc])


def parse_match(line):
    p, g = line.split()
    return Match(p, [int(x) for x in g.split(',')])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day12_sample" if TEST_MODE else "input/day12").open() as f:
        values = [parse_match(i.strip()) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
