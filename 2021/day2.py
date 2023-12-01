from pathlib import Path
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    depth = 0
    horizontal = 0

    for instr in v:
        match instr[0]:
            case 'down': depth = depth + instr[1]
            case 'up': depth = depth - instr[1]
            case 'forward': horizontal = horizontal + instr[1]
            case _: print("bad")

    return depth * horizontal


def phase2(v):
    depth = 0
    horizontal = 0
    aim = 0

    for instr in v:
        # print(instr, depth, horizontal, aim)
        match instr[0]:
            case 'down': aim = aim + instr[1]
            case 'up': aim = aim - instr[1]
            case 'forward':
                horizontal = horizontal + instr[1]
                depth = depth + (aim * instr[1])
            case _: print("bad")

    return depth * horizontal


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day2_sample" if TEST_MODE else "input/day2").open() as f:
        values = list(map(lambda x: [x[0], int(x[1])], [i.split(" ") for i in f]))
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')

