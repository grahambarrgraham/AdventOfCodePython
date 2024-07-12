from collections import defaultdict
from pathlib import Path

TEST_MODE = False


def phase1(orbits):
    counts, _ = count_orbits(orbits)
    return sum(counts.values())


def phase2(orbits):
    counts, reverse_index = count_orbits(orbits)
    you_path = get_path(reverse_index, 'YOU')
    san_path = get_path(reverse_index, 'SAN')

    common = 2 * counts[find_common_orbit(san_path, you_path)]

    return counts['YOU'] + counts['SAN'] - common - 2


def find_common_orbit(san_path, you_path):
    i = 0
    while you_path[i] == san_path[i]:
        i += 1
    common_orbit = you_path[i - 1]
    return common_orbit


def get_path(reverse_index, obj):
    result = []
    while obj != 'COM':
        obj = reverse_index[obj]
        result.append(obj)
    result.reverse()
    return result


def count_orbits(orbits):
    counts = defaultdict(int)
    reverse_index = {}
    stack = ['COM']
    while len(stack) > 0:
        parent = stack.pop()
        for orbit in orbits[parent]:
            counts[orbit] = counts[parent] + 1
            reverse_index[orbit] = parent
        stack.extend(orbits[parent])
    return counts, reverse_index


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day6_sample" if TEST_MODE else "input/day6").open() as f:
        values = defaultdict(list)
        for item in [i.strip().split(')') for i in f]:
            values[item[0]].append(item[1])

        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
