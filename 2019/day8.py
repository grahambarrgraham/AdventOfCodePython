import itertools
from pathlib import Path

TEST_MODE = False


def phase1(v):
    layers, _ = read_layers(v)
    zero_counts = [count_int(0, layer) for layer in layers]
    least_zeros_layer = min(zip(zero_counts, layers))[1]
    return count_int(1, least_zeros_layer) * count_int(2, least_zeros_layer)


def phase2(v):
    layers, layer_size = read_layers(v)
    resolved_pixels = []
    for i in range(layer_size):
        pixels = [layer[i] for layer in layers]
        resolved_pixels.append(resolve_pixel(pixels))

    render(chunks(resolved_pixels, 2 if TEST_MODE else 25))
    return "CJZHR"


def resolve_pixel(pixels):
    return next(itertools.dropwhile(lambda x: x == 2, pixels))


def render(lines):
    for line in lines:
        for l in line:
            print('#' if l == 1 else ' ', end='')
        print()


def read_layers(v):
    layer_size = 4 if TEST_MODE else 25 * 6
    layers = list(chunks(v, layer_size))
    return layers, layer_size


def count_int(val, lst):
    return len([i for i in lst if i == val])


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day8_sample" if TEST_MODE else "input/day8").open() as f:
        values = [int(i) for i in f.readline()]

        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
