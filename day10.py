from pathlib import Path
import collections

TEST_MODE = False

Instruction = collections.namedtuple('Instruction', ('type', 'count'))


def phase1(v):
    signals = collect_signals(v, 0)
    res = [(cycle, signals[cycle]) for cycle in range(20, 221, 40)]
    return sum([a[0] * a[1] for a in res])


def phase2(v):
    signals = collect_signals(v, 1)
    lines = [''] * 6
    for line in range(6):
        for cycle in range(40):
            pos = signals[cycle + (line * 40)]
            lines[line] += '#' if cycle in range(pos-1, pos+2) else '.'

    for line in lines:
        print(line)

    return -1


def collect_signals(instructions, start):
    cycle = 0
    x = 1
    signals = {}
    for instruction in instructions:
        if instruction.type == "noop":
            cycle += 1
        else:
            cycle += 2
            signals[cycle] = x
            x += instruction.count

    all_signals = []
    for a in range(start, 240 + start):
        all_signals.append(pixel_pos(signals, a))

    return all_signals


def pixel_pos(signals, current):
    keys = list(signals.keys())
    for index, cycle in enumerate(keys):
        if cycle >= current:
            return signals[keys[index]]
    return signals[keys[-1]]


def parse(line):
    if line == "noop":
        return Instruction("noop", 0)
    else:
        return Instruction("add", int(line.split(" ")[1]))


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day10_sample" if TEST_MODE else "input/day10").open() as f:
        values = [parse(i.strip()) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


