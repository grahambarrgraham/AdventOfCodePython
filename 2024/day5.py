import functools
from pathlib import Path

TEST_MODE = False


def sort_by_rules(rules_, values):
    def comparator(v1, v2):
        return -1 if (v1, v2) in rules_ else 1 if (v2, v1) in rules else 0
    return sorted(values, key=functools.cmp_to_key(comparator))


def unsorted_sorted_pairs(rules_, updates_):
    return [(update, sort_by_rules(rules_, update)) for update in updates_]


def sum_of_middles(updates_):
    return sum([int(update[(len(update) // 2)]) for update in updates_])


def phase1(rules_, updates_):
    return sum_of_middles([a for a, b, in (unsorted_sorted_pairs(rules_, updates_)) if a == b])


def phase2(rules_, updates_):
    return sum_of_middles([b for a, b, in (unsorted_sorted_pairs(rules_, updates_)) if a != b])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day5_sample" if TEST_MODE else "input/day5").open() as f:
        r, u = f.read().split('\n\n')
        rules = {tuple(x.split('|')) for x in r.split()}
        updates = [[y for y in x.split(',')] for x in u.split()]
        print(f'Phase 1: {phase1(rules, updates)}')
        print(f'Phase 2: {phase2(rules, updates)}')


