from pathlib import Path

TEST_MODE = False


def predict_forward(s):
    pairs = [(s[i + 1], s[i]) for i in range(0, len(s) - 1)]
    for p in reversed(pairs):
        p[1].append(p[1][-1] + p[0][-1])
    return s


def predict_backward(s):
    pairs = [(s[i + 1], s[i]) for i in range(0, len(s) - 1)]
    for p in reversed(pairs):
        p[1].insert(0, (p[1][0] - p[0][0]))
    return s


def all_zeros(s):
    return len(s) > 0 and s[0] == 0 and len(set(s)) == 1


def diffs(s: list):
    acc = [s]
    zero_diff = False
    while not zero_diff:
        s = diff(s)
        if not all_zeros(s):
            acc.append(s)
        else:
            zero_diff = True
    return acc


def diff(s: list):
    return [(s[i + 1] - s[i]) for i in range(0, len(s) - 1)]


def phase1(v):
    all_diffs = [diffs(i) for i in v]
    # print(all_diffs)
    predicts = [predict_forward(d)[0][-1] for d in all_diffs]
    # print(predicts)
    return sum(predicts)


def phase2(v):
    all_diffs = [diffs(i) for i in v]
    # print(all_diffs)
    predicts = [predict_backward(d)[0][0] for d in all_diffs]
    # print(predicts)
    return sum(predicts)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day9_sample" if TEST_MODE else "input/day9").open() as f:
        values = [[int(x) for x in i.strip().split()] for i in f]
        # print(f'Phase 1: {phase1(values.copy())}')
        print(f'Phase 2: {phase2(values.copy())}')
