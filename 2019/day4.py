from pathlib import Path

TEST_MODE = False


def phase1(v):
    def func(pwd):
        return len(set(pwd)) < len(pwd)
    return calc(v, func)


def phase2(v):
    def func(pwd):
        last_c = pwd[0]
        same_count = 1
        for c in pwd[1:]:
            if c == last_c:
                same_count += 1
            elif same_count == 2:
                break
            else:
                same_count = 1
            last_c = c
        return same_count == 2

    return calc(v, func)


def calc(v, pairs_func):
    start, end = v
    return sum([pairs_func(pwd) and sorted(pwd) == list(pwd) for pwd in [str(pwd) for pwd in range(start, end + 1)]])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day4_sample" if TEST_MODE else "input/day4").open() as f:
        values = [int(x) for x in [i.split('-') for i in f][0]]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
