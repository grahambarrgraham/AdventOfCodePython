import itertools
from copy import deepcopy
from itertools import combinations
from pathlib import Path

import day5

TEST_MODE = False


def phase1(code):
    max_signal = 0
    combos = itertools.permutations([0, 1, 2, 3, 4], 5)
    for phase_settings in combos:
        # print(phase_settings)
        val = find_thruster_signal_phase_1(code, phase_settings)
        max_signal = max(val, max_signal)
    return max_signal


def phase2(v):
    max_signal = 0
    combos = itertools.permutations([5, 6, 7, 8, 9], 5)

    return -1


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
        amps.append((phase_settings[i], deepcopy(code)))

    finished = False
    i = 0
    while not finished:
        phase, code = amps[i % num_amps]
        input_signals = 
        outputs, halted = day5.calc(code, input_signals)
        input_signals = outputs
        i += 1

    return input_signal


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day7_sample" if TEST_MODE else "input/day7").open() as f:
        values = [int(x) for x in [i.split(',') for i in f][0]]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
