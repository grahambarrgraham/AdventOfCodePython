import re
from pathlib import Path

TEST_MODE = False


def phase1(v):
    return sum(digits(v))


def phase2(v):
    subs = [('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'), ('five', '5'), ('six', '6'),
            ('seven', '7'), ('eight', '8'), ('nine', '9')]

    def _find_first_last(line):
        _first_index = 99999999
        _last_index = -1
        _first = None
        _last = None
        for sub in subs:
            i1 = line.find(sub[0])
            i2 = line.find(sub[1])
            if 0 <= i1 < _first_index:
                _first_index = i1
                _first = sub[1]
            if 0 <= i2 < _first_index:
                _first_index = i2
                _first = sub[1]
            i1 = line.rfind(sub[0])
            i2 = line.rfind(sub[1])
            if i1 > _last_index:
                _last_index = i1
                _last = sub[1]
            if i2 > _last_index:
                _last_index = i2
                _last = sub[1]
        return int(_first + _last)

    _digits = [_find_first_last(line) for line in v]
    return sum(_digits)


def digits(lines):
    for line in lines:
        line = line.lower()
        _digits = [a for a in line if a.isnumeric()]
        yield int(_digits[0] + _digits[-1])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day1_sample" if TEST_MODE else "input/day1").open() as f:
        values = [i for i in f]
        print(f'Phase 1: {phase1(values)}')
    with Path(__file__).parent.joinpath("input/day1_sample_phase2" if TEST_MODE else "input/day1").open() as f:
        values = [i for i in f]
        print(f'Phase 2: {phase2(values)}')

