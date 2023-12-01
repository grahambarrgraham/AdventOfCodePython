from pathlib import Path
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    gamma = epsilon = ''

    for i in range(len(v[0])):
        column = [row[i] for row in v]
        count = len([item for item in column if item == '0'])
        gamma = gamma + ('0' if count > len(v) / 2 else '1')
        epsilon = epsilon + ('0' if count <= len(v) / 2 else '1')

    return int(gamma, 2) * int(epsilon, 2)


def phase2(v):

    def fewer_ones(one_count, total):
        return one_count < total / 2

    def equal_or_more_ones(one_count, total):
        return one_count >= total / 2

    oxygen = find_gas(v, equal_or_more_ones)
    co2 = find_gas(v, fewer_ones)
    return oxygen * co2


def find_gas(gas, func):
    for col in range(len(gas[0])):
        column = [row[col] for row in gas]
        one_count = len([item for item in column if item == '1'])
        if func(one_count, len(gas)):
            gas = [gas[n] for n in range(len(gas)) if column[n] == '1']
        else:
            gas = [gas[n] for n in range(len(gas)) if column[n] == '0']
        if len(gas) == 1:
            break
    return int(gas[0], 2)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day3_sample" if TEST_MODE else "input/day3").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
