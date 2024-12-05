from pathlib import Path

TEST_MODE = False


def phase1(reports):
    return sum([safe(report) for report in reports])


def phase2(reports):
    return sum([any(safe(variation) for variation in variations(report)) for report in reports])


def safe(report):
    diffs = [report[i] - report[i + 1] for i in range(len(report) - 1)]
    return all(-3 <= x <= -1 for x in diffs) or all(1 <= x <= 3 for x in diffs)


def variations(report):
    for i in range(len(report)):
        yield report[0:i] + report[i+1:]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day2_sample" if TEST_MODE else "input/day2").open() as f:
        values = [[int(x) for x in i.split()] for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
