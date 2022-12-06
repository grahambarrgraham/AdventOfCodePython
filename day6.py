from pathlib import Path

TEST_MODE = False


def phase1(v):
    return calc(4, v)


def phase2(v):
    return calc(14, v)


def calc(size, v):
    for count, code in enumerate(split(v, size)):
        if all_different(code, size):
            return count + size
    return -1


def all_different(code, size):
    return len({*code}) == size


def split(a_list: list, chunk_size: int) -> list:
    for i in range(0, len(a_list)):
        chunk = a_list[i:i + chunk_size]
        if len(chunk) == chunk_size:
            yield chunk


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day6_sample" if TEST_MODE else "input/day6").open() as f:
        values = [i for i in f][0]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


