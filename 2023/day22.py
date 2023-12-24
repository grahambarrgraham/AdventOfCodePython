from copy import deepcopy
from pathlib import Path

TEST_MODE = False


def phase1(block_map):
    block_map, reverse_map, _ = settle(block_map)

    cant = set()
    for idx, blocks in block_map.items():
        map_ = list(get_supported_by(blocks, reverse_map))
        if len(map_) == 1:
            cant.add(map_[0])

    return len(block_map) - len(cant)


def phase2(block_map):
    block_map, _, _ = settle(block_map)
    acc = 0
    for idx in block_map:
        bm = deepcopy(block_map)
        bm.pop(idx)
        _, _, moves = settle(bm)
        print(idx, moves)
        acc += moves

    return acc


def settle(block_map):
    block_map = deepcopy(block_map)
    reverse_map = {}

    for idx, blocks in block_map.items():
        for block in blocks:
            reverse_map[block] = idx

    moved = set()
    while True:
        moves = [(idx, can_move_down(blocks, reverse_map.keys())) for idx, blocks in block_map.items()]
        moves = [(idx, m) for idx, m in moves if m > 0]
        if len(moves) == 0:
            break
        for idx, down in moves:
            moved.add(idx)
            blocks = block_map[idx]
            new_blocks = [(x, y, z - down) for x, y, z in blocks]
            for block in blocks:
                reverse_map.pop(block)
            for block in new_blocks:
                reverse_map[block] = idx
            block_map[idx] = new_blocks

    return block_map, reverse_map, len(moved)


def get_supported_by(blocks, revert_map):
    acc = set()

    for x, y, z in find_lowest(blocks):
        if z == 1:
            return []
        if (x, y, z - 1) in revert_map:
            acc.add(revert_map[(x, y, z - 1)])

    return acc


def can_move_down(blocks, all_blocks):
    if blocks[0][2] == 1:
        return False
    moves = 0
    lowest = find_lowest(blocks)
    while True:
        for x, y, z in lowest:
            if z - moves == 1 or (x, y, z - moves - 1) in all_blocks:
                return moves
        moves += 1


def find_lowest(blocks):
    lowest = None
    acc = []
    for x, y, z in blocks:
        if lowest is None:
            lowest = z
        if z == lowest:
            acc.append((x, y, z))
        else:
            break
    return acc


def parse(line):
    def block(t):
        return [int(i) for i in t.split(',')]

    a, b = line.split('~')
    b_a = block(a)
    b_b = block(b)
    blocks = []
    for x in range(b_a[0], b_b[0] + 1):
        for y in range(b_a[1], b_b[1] + 1):
            for z in range(b_a[2], b_b[2] + 1):
                blocks.append((x, y, z))
    return blocks


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day22_sample" if TEST_MODE else "input/day22").open() as f:
        values = {idx: parse(line.strip()) for idx, line in enumerate(f)}
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
