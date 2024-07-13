import itertools
from copy import deepcopy
from pathlib import Path

import day5

TEST_MODE = True


def phase1(code):
    return calc(code, find_thruster_signal_phase_1, [0, 1, 2, 3, 4])


def phase2(code):
    return calc(code, find_thruster_signal_phase_2, [5, 6, 7, 8, 9])


def calc(code, phase_func, phase_settings):
    max_signal = 0
    combos = itertools.permutations(phase_settings, 5)
    for phase_settings in combos:
        # print(phase_settings)
        val = phase_func(code, phase_settings)
        max_signal = max(val, max_signal)
    return max_signal


def find_thruster_signal_phase_1(code, phase_settings):
    input_signal = 0
    for i in range(0, 5):
        outputs, _ = day5.calc(code, [phase_settings[i], input_signal])
        input_signal = outputs[-1]
    return input_signal


def find_thruster_signal_phase_2(code, phase_settings):
    input_signals = [0]
    amps = []
    num_amps = len(phase_settings)
    for i in range(num_amps):
        amps.append(deepcopy(code))

    finished = False

    first_pass = True
    while not finished:
        for i in range(num_amps):
            if first_pass:
                input_signals = [phase_settings[i]] + input_signals
            outputs, finished = day5.calc(amps[i], input_signals)
            input_signals = outputs
        first_pass = False
    return input_signals[-1]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day7_sample" if TEST_MODE else "input/day7").open() as f:
        values = [int(x) for x in [i.split(',') for i in f][0]]
        # print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
