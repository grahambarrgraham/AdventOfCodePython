import collections
import math
import re
from pathlib import Path

TEST_MODE = False

# TAGS: regexp finditer

Coord = collections.namedtuple("Coord", "x y")


def phase1(v):
    symbol_indexes: set[Coord] = get_symbol_indexes(v, find_all_symbol_coords)
    candidate_part_nums: dict[Coord, str] = get_candidate_part_nums(v)

    part_nums = list()

    for coord, digits in candidate_part_nums.items():
        if is_touching_symbol(coord, digits, symbol_indexes):
            part_nums.append(int(digits))

    return sum(part_nums)


def phase2(v):
    symbol_indexes = set()
    for index, line in enumerate(v):
        symbol_indexes = symbol_indexes.union(find_asterix_coords(index, line))

    candidate_part_nums: dict[Coord, str] = get_candidate_part_nums(v)
    ratios = [calc_gear_ration(symbol, candidate_part_nums) for symbol in symbol_indexes]
    return sum(ratios)


def calc_gear_ration(symbol: Coord, candidates: dict[Coord, str]):
    part_nums = set()
    symbol_coords: set[Coord] = find_neighbours(symbol)
    symbol_coords.add(symbol)
    for start_coord, digits in candidates.items():
        for coord in digit_coords_list(start_coord, digits):
            if coord in symbol_coords:
                part_nums.add(int(digits))
    return 0 if len(part_nums) != 2 else math.prod(part_nums)


def is_touching_symbol(digits_first_coord: Coord, digits: str, symbols: set[Coord]):
    for coord in digit_coords_list(digits_first_coord, digits):
        if coord in symbols:
            return True
    return False


def get_candidate_part_nums(v) -> dict[Coord, str]:
    candidate_part_nums = dict[Coord, str]()
    for index, line in enumerate(v):
        line_dict = find_part_num_start_indexes(index, line)
        for k, v in line_dict.items():
            candidate_part_nums[k] = v
    return candidate_part_nums


def get_symbol_indexes(v, find_symbol_func) -> set[Coord]:
    symbol_indexes = set()
    for index, line in enumerate(v):
        symbol_indexes = symbol_indexes.union(find_symbol_func(index, line))
    for index in symbol_indexes:
        symbol_indexes = symbol_indexes.union(find_neighbours(index))
    return symbol_indexes


def find_all_symbol_coords(y, line) -> set[Coord]:
    x_indexes = {m.start(0) for m in re.finditer("([0-9)]|\.)", line)}
    remaining_x_indexes = set(range(len(line))).difference(x_indexes)
    return {Coord(x, y) for x in remaining_x_indexes}


def find_asterix_coords(y, line) -> set[Coord]:
    x_indexes = {m.start(0) for m in re.finditer("(\*)", line)}
    return {Coord(x, y) for x in x_indexes}


all_neighbours = [Coord(-1, -1), Coord(-1, 0), Coord(-1, 1), Coord(0, -1), Coord(0, 1), Coord(1, -1), Coord(1, 0),
                  Coord(1, 1)]


def find_neighbours(coord: Coord) -> set[Coord]:
    return {Coord(coord.x + offset.x, coord.y + offset.y) for offset in all_neighbours}


def find_part_num_start_indexes(y, line) -> dict[Coord, str]:
    matches = [m for m in re.finditer("[0-9]+", line)]
    return {Coord(m.start(0), y): m.group(0) for m in matches}


def digit_coords_list(coord: Coord, part_num: str) -> list[Coord]:
    return [Coord(coord.x + i, coord.y) for i in range(len(part_num))]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day3_sample" if TEST_MODE else "input/day3").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
