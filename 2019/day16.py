import time
from pathlib import Path

TEST_MODE = False

base_pattern = [0, 1, 0, -1]


def phase1(input_signal_str: str):
    input_signal = tuple([int(c) for c in input_signal_str])
    for phase in range(100):
        nxt_signal = []
        signal_len = len(input_signal)
        for i in range(signal_len):
            tot = 0
            for first, last, sign in generate_pattern_phase_1(i, signal_len):
                tot += sum(input_signal[first:last]) * sign
            nxt_signal.append(abs(tot) % 10)
        input_signal = nxt_signal
    return ''.join([str(i) for i in input_signal[:8]])


# Needed hints for stage 2, the insight is that the offset is in the 2nd half of dataset
# and the pattern at the point is a sequence of zeros followed by ones
# 0 1 1 1 1
# 0 0 1 1 1
# 0 0 0 1 1
# 0 0 0 0 1

def phase2(input_signal_str: str):
    input_signal = tuple([int(c) for c in input_signal_str])
    offset = int(''.join(input_signal_str[:7]))
    input_signal *= 10000
    required_signal = input_signal[offset:]

    for phase in range(100):
        sums = []
        last_sum = 0
        for i in range(len(required_signal) - 1, -1, -1):
            nxt_sum = last_sum + required_signal[i]
            last_sum = nxt_sum
            sums.append(nxt_sum)
        sums.reverse()

        nxt_signal = []
        for i in range(len(required_signal)):
            nxt_signal.append(sums[i] % 10)
        required_signal = nxt_signal

    return ''.join([str(i) for i in required_signal[:8]])


def generate_pattern_phase_1(phase, max_):
    index = -1
    pattern_index = 0

    while index < max_:
        last = index + phase + 1
        val = base_pattern[pattern_index]
        last = min(max_, last)
        if val != 0:
            yield index, last, val
        index = last
        pattern_index = 0 if pattern_index == 3 else pattern_index + 1


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day16_sample" if TEST_MODE else "input/day16").open() as f:
        input_ = [i.strip() for i in f][0]
        t0 = time.time()
        print(f'Phase 1: {phase1(input_)} {time.time() - t0}s')
        result = phase2(input_)
        print(f"Phase 2: {result} {time.time() - t0}s")
