from pathlib import Path

TEST_MODE = True

snafu_map = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
snafu_reverse_map = {4: '1-', 3: '1=', 2: '02', 1: '01', 0: '00', -1: "0-", -2: "0=", -3: "-2", -4: "-1"}


def to_base_10(snafu: str):
    power = acc = 0
    for c in reversed(snafu):
        acc += snafu_map[c] * (5 ** power)
        power += 1
    return acc


def to_snafu(base_10_value: int):
    pass


def plus(a_snafu, b_snafu):
    pass


def phase1(snafus: list[str]):
    total_base_10 = sum([to_base_10(snafu) for snafu in snafus])
    print(total_base_10)
    return to_snafu(total_base_10)


def phase2(v):
    return -1


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day25_sample" if TEST_MODE else "input/day25").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
