from pathlib import Path

TEST_MODE = False


def matches(towels, design):
    return matches_(towels, design, {})


def matches_(towels, design, resolved):

    if design in resolved:
        return resolved[design]

    if len(design) == 1 and design in towels:
        return 1

    if len(design) == 1 and design not in towels:
        return 0

    count = 0

    if design in towels:
        count = 1
        towels = [t for t in towels if t != design]

    for towel in towels:
        if design.startswith(towel):
            b = design[len(towel):]
            count_b = matches_(towels, b, resolved)
            resolved[b] = count_b
            count += count_b

    return count


def phase1(towels, designs):
    return sum([1 for design in designs if matches(towels, design) > 0])


def phase2(towels, designs):
    return sum(matches(towels, d) for d in designs)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day19_sample" if TEST_MODE else "input/day19").open() as f:
        towels_, designs_ = f.read().split('\n\n')
        towels_ = towels_.strip().split(', ')
        designs_ = designs_.strip().splitlines()

        print(f'Phase 1: {phase1(towels_, designs_)}')
        print(f'Phase 2: {phase2(towels_, designs_)}')
