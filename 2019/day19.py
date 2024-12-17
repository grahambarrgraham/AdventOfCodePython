from pathlib import Path
from computer import Computer

TEST_MODE = True


def phase1(intcode):
    computer = Computer(intcode)


    # //-10003-340100100
    # //10010100100100100100100101001001001001001001010010010010010010100100100100100

    s = 200
    a = [(x, y, Computer(intcode).compute([x, y])) for x in range(s) for y in range(s)]
    b = {(x, y) for x, y, c in a if c == [1]}

    m = {}
    for y in range(s):
        count = 0
        first_x = -1
        for x in range(s):
            print('.' if (x, y) not in b else '#', end='')
            if (x, y) in b:
                count += 1
                if first_x == -1:
                    first_x = x
        print()
        # print(first_x, y, count)
        m[y] = (first_x, count)

    for y in sorted(m.keys(), reverse=True):
        if y == 0:
            continue
        x1, l1 = m[y]
        x2, l2 = m[y-1]
        print(y, x1 - x2, l1 - l2)

    for y in sorted(m.keys()):
        if y == 0:
            continue
        x1, l1 = m[y]
        x2, l2 = m[y-1]
        print(x1 + l1 - (x2 + l2), end='')
    print()
    for y in sorted(m.keys()):
        if y == 0:
            continue
        x1, l1 = m[y]
        x2, l2 = m[y-1]
        print(x1 - x2, end='')
    print()

    # x - from 19, increase 0, 1, then 0, 0, 1 six times and repeats (at 19, value of x is 7)

    return len(b)


def phase2(v):
    return -1

def line(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    D = 2*dy - dx
    y = y0

    for x in range(x0, x1):
        print(x, y)
        if D > 0:
            y = y + 1
            D = D - 2*dx

        D = D + 2*dy

if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day19_sample" if TEST_MODE else "input/day19").open() as f:
        values = [int(i) for i in f.readline().split(',')]
        # print(f'Phase 1: {phase1(values)}')
        # print(f'Phase 2: {phase2(values)}')

    line(0, 0, 100000, 10)


