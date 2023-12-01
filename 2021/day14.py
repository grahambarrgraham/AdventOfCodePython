import re
import sys
from collections import defaultdict
from pathlib import Path

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    return calc(10, v)


def phase2(v):
    return calc(40, v)


def calc(stop, v):
    polymer, rules = v

    element_counts = defaultdict(int)
    for letter in polymer:
        element_counts[letter] += 1

    pairs = defaultdict(int)
    for element_pair in find_element_pairs(polymer):
        pairs[element_pair] += 1

    for i in range(stop):
        outcomes = [generate(a, b, pairs) for a, b in rules.items() if a in pairs]
        for original, new_left, new_right, new_element, count in outcomes:
            pairs[original] -= count
            pairs[new_left] += count
            pairs[new_right] += count
            element_counts[new_element] += count

    return max(element_counts.values()) - min(element_counts.values())


def generate(key, value, pairs_dict):
    return key, key[0] + value, value + key[1], value, (pairs_dict[key])


def find_element_pairs(polymer):
    return [a + b for a, b in zip(polymer, polymer[1:])]


def load(v):
    def load_rule(s):
        matches = re.match(r"(.+) -> (.)", s)
        return matches.group(1), matches.group(2)

    template = v[0]
    rules = dict([load_rule(x) for x in v[1:]])

    return template, rules


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day14_sample" if TEST_MODE else "input/day14").open() as f:
        values = load([i.strip() for i in f if len(i) > 1])
        # print(values)
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
