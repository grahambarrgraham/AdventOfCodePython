import itertools
from copy import deepcopy
from pathlib import Path
from computer import Computer

TEST_MODE = False


def phase1(amp_code):
    return find_max_signal(amp_code, [0, 1, 2, 3, 4])


def phase2(amp_code):
    return find_max_signal(amp_code, [5, 6, 7, 8, 9])


def find_max_signal(code, phase_settings):
    max_signal = 0
    combos = itertools.permutations(phase_settings, 5)
    for phase_settings in combos:
        val = find_thruster_signal(code, phase_settings)
        max_signal = max(val, max_signal)
    return max_signal


def find_thruster_signal(amp_code, phase_settings):
    input_signals = [0]
    num_amps = len(phase_settings)
    amps = []
    for i in range(num_amps):
        amp = Computer(deepcopy(amp_code))
        amps.append(amp)
        amp.compute([phase_settings[i]])

    while True:
        for amp in amps:
            input_signals = amp.compute(input_signals)

        if amps[-1].halted:
            return input_signals[-1]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day7_sample" if TEST_MODE else "input/day7").open() as f:
        values = [int(x) for x in [i.split(',') for i in f][0]]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
