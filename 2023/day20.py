from collections import namedtuple, defaultdict
from math import lcm
from pathlib import Path

TEST_MODE = False

Module = namedtuple("Mod", "type, destinations")


def phase1(broadcaster, modules):
    acc, _ = propagate_pulses(broadcaster, modules, 1000)
    return acc[False] * acc[True]


def phase2(broadcaster, modules):
    _, all_highs = propagate_pulses(broadcaster, modules, 5000)
    cycles = [v[0] for k, v in all_highs.items() if k in ['rs', 'bd', 'pm', 'cc']]
    return lcm(*cycles)


def propagate_pulses(broadcaster, modules, presses):
    flip_flop = defaultdict(bool)
    conj = defaultdict(defaultdict)
    acc = defaultdict(int)
    queue = []
    all_highs = defaultdict(list)

    def pulse(press_num, m_name, h_l, _from):
        acc[h_l] += 1

        if m_name not in modules:
            return m_name == 'rx' and not h_l

        mod = modules[m_name]

        if mod.type == '&':
            conj[m_name][_from] = h_l
            all_high = len([high for high in conj[m_name].values() if high]) == len(conj[m_name])
            h_l = not all_high
            if all_high:
                all_highs[m_name].append(press_num)
        elif mod.type == '%':
            if h_l:
                return
            flip_flop[m_name] = not flip_flop[m_name]
            h_l = flip_flop[m_name]

        for nxt in mod.destinations:
            queue.append((nxt, h_l, m_name))

    conj_mods = {name for name, mod in modules.items() if mod.type == '&'}
    for n, mod in modules.items():
        for d in mod.destinations:
            if d in conj_mods:
                conj[d][n] = False

    for press in range(presses):
        acc[False] += 1

        for name in broadcaster:
            queue.append((name, False, 'broadcaster'))

        while len(queue) > 0:
            nxt = queue.pop(0)
            pulse(press + 1, *nxt)

    return acc, all_highs


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day20_sample" if TEST_MODE else "input/day20").open() as f:
        _modules = [i.strip().split(' -> ') for i in f]
        _broadcaster = [i for i in _modules if i[0] == 'broadcaster'][0][1].split(', ')
        _modules = {i[0][1:]: Module(i[0][0], i[1].split(', ')) for i in _modules if i[0] != 'broadcaster'}
        print(f'Phase 1: {phase1(_broadcaster, _modules)}')
        print(f'Phase 2: {phase2(_broadcaster, _modules)}')
