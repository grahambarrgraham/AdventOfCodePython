import copy
from pathlib import Path
import collections

TEST_MODE = False

Block = collections.namedtuple("Block", "x, y")
Cave = collections.namedtuple("Cave", "blocks y_index")


def phase1(cave):
    return calc(cave, None)


def phase2(cave):
    floor = max([b.y for b in cave.blocks]) + 2
    return calc(cave, floor)


def calc(cave, floor):
    sand = []
    while True:
        start = Block(500, -1)
        block = drop(start, cave, floor)
        if block is not None:
            sand.append(block)
            cave.blocks.add(block)
            update_index(cave.y_index, block)
        else:
            return len(sand)


def nearest_below(start, cave, floor):
    if start.x not in cave.y_index:
        return find_floor(floor, start)
    for y in cave.y_index[start.x]:
        if y > start.y:
            return Block(start.x, y - 1)
    return find_floor(floor, start)


def find_floor(floor, start):
    return None if floor is None else Block(start.x, floor - 1)


def drop(start, cave, floor):
    stop = nearest_below(start, cave, floor)

    if not stop:
        return None

    if stop.y - start.y < 1:
        return None

    if stop.y + 1 == floor:
        return stop

    if Block(stop.x - 1, stop.y + 1) not in cave.blocks:
        return drop(Block(stop.x - 1, stop.y), cave, floor)
    elif Block(stop.x + 1, stop.y + 1) not in cave.blocks:
        return drop(Block(stop.x + 1, stop.y), cave, floor)

    return stop


def to_blocks(x1, x2, y1, y2):
    x_step = 1 if x2 >= x1 else -1
    y_step = 1 if y2 >= y1 else -1
    for x in range(x1, x2 + x_step, x_step):
        for y in range(y1, y2 + y_step, y_step):
            yield Block(x, y)


def to_block(segment):
    split = segment.split(',')
    return Block(int(split[0]), int(split[1]))


def update_index(y_index, block):
    if block.x in y_index:
        y_index[block.x].append(block.y)
        y_index[block.x].sort()
    else:
        y_index[block.x] = [block.y]


def build_cave_map(lines):
    blocks = []
    for line in lines:
        segments = [to_block(segment) for segment in (line.split(" -> "))]
        segment_pairs = list(map(list, zip(segments, segments[1:])))
        for segment_pair in segment_pairs:
            blocks_add = list(to_blocks(segment_pair[0].x, segment_pair[1].x, segment_pair[0].y, segment_pair[1].y))
            blocks += blocks_add
    y_index = {}
    for block in blocks:
        update_index(y_index, block)
    return Cave(set(blocks), y_index)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day14_sample" if TEST_MODE else "input/day14").open() as f:
        values = build_cave_map([i.strip() for i in f])
        print(f'Phase 1: {phase1(copy.deepcopy(values))}')
        print(f'Phase 2: {phase2(copy.deepcopy(values))}')
