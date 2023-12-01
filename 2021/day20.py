import copy
import sys
from pathlib import Path

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def to_number(s):
    return int(''.join(s), 2)


def phase1(v):
    algorithm, image = v
    return calc(algorithm, image, 2, flashes=algorithm[0] == '#' and algorithm[-1] == '.')


def phase2(v):
    algorithm, image = v
    return calc(algorithm, image, 50, flashes=algorithm[0] == '#' and algorithm[-1] == '.')


def calc(enhancement_dict, image, count, flashes):
    for it in range(count):
        surrounding_char = '#' if flashes and it % 2 == 1 else '.'
        image = enhance_image(enhancement_dict, image, surrounding_char)

    return sum(len([c for c in line if c == '#']) for line in image)


def frame(image, size, surrounding_char):
    resp = add_horizontal_frame(image, size, surrounding_char)
    for line in image:
        resp.append(list((surrounding_char * size) + ''.join(line) + (surrounding_char * size)))
    resp += add_horizontal_frame(image, size, surrounding_char)
    return resp


def add_horizontal_frame(image, size, surrounding_char):
    return [[surrounding_char for _ in range((len(image[0]) + 2 * size))] for _ in range(size)]


def enhance_image(enhancement_dict, image, surrounding_char):
    in_image = frame(image, 1, surrounding_char)
    out_image = copy.deepcopy(in_image)
    for y in range(len(in_image)):
        for x in range(len(in_image[0])):
            neighbours = find_neighbours((x, y), in_image, surrounding_char)
            n = to_number(neighbours)
            out_image[y][x] = enhancement_dict[n]
    return out_image


def print_image(image):
    for line in image:
        print(''.join(line))
    print()


def find_neighbours(coord, v, surrounding_char):
    (x, y) = coord

    def to_bin(c):
        return '0' if c == '.' else '1'

    def find_char(a, b):
        return v[b][a] if (len(v[0]) > a >= 0 and len(v) > b >= 0) else surrounding_char

    return [to_bin(find_char(x + a, y + b)) for a, b in
            [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]]


def load(param):
    algorithm = param[0]
    image = [list(line) for line in param[2:]]
    return algorithm, image


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day20_sample" if TEST_MODE else "input/day20").open() as f:
        values = load([i.strip() for i in f])
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
