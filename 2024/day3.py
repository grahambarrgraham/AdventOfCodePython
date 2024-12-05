import re
from pathlib import Path

TEST_MODE = False


def operands(instr):
    return [int(operand) for operand in re.findall("\d+", instr)]


def multiply(a, b):
    return a * b


def phase1(v):
    m = re.findall("mul\\(\d+,\d+\\)", v)
    return sum(multiply(*operands(instr)) for instr in m)


def find_all_matches(pattern, string):
    pat = re.compile(pattern)
    pos, result = 0, []
    while match := pat.search(string, pos):
        pos = match.start() + 1
        result.append((pos, match[0]))
    return result


def phase2(v):
    instr = find_all_matches("do\\(\\)", v)
    instr.extend(find_all_matches("don't\\(\\)", v))
    instr.extend(find_all_matches("mul\\(\d+,\d+\\)", v))
    instr.sort(key=lambda x: x[0])
    b = True
    result = 0
    for _, inst in instr:
        if b and inst.startswith('mul'):
            result += multiply(*operands(inst))
        elif inst.startswith("do("):
            b = True
        elif inst.startswith("don"):
            b = False
    return result


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day3_sample" if TEST_MODE else "input/day3").open() as f:
        values = f.read().strip()
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


