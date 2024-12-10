from pathlib import Path
from time import time

TEST_MODE = False


def phase1(v):
    files, space = build_file_system(v)

    while len(space) > 0:
        last_file = max(files.keys())
        file_id, num_file_blocks = files[last_file]
        del files[last_file]
        space_indexes = iter(sorted(space.keys()))
        while num_file_blocks > 0:
            space_index = next(space_indexes, None)
            if space_index is None:
                files[max(files.keys()) + 1] = (file_id, num_file_blocks)
                break
            _, spaces = space[space_index]
            if spaces <= num_file_blocks:
                del space[space_index]
                files[space_index] = (file_id, spaces)
                num_file_blocks -= spaces
            else:
                files[space_index] = (file_id, num_file_blocks)
                del space[space_index]
                space[space_index + num_file_blocks] = ('.', spaces - num_file_blocks)
                num_file_blocks = 0

    return checksum(files, space)


def phase2(v):
    files, space = build_file_system(v)

    for file_index, (file_id, num_blocks) in sorted(files.items(), reverse=True):
        for space_index, (_, spaces) in sorted(space.items()):
            if spaces >= num_blocks and space_index < file_index:
                del files[file_index]
                del space[space_index]
                space[file_index] = ('.', num_blocks)
                files[space_index] = (file_id, num_blocks)
                if spaces > num_blocks:
                    space[space_index + num_blocks] = ('.', spaces - num_blocks)
                break

    return checksum(files, space)


def pretty(files, space):
    for _, (id_, num_blocks) in sorted((files | space).items()):
        for i in range(num_blocks):
            print(id_, end='')
    print()


def checksum(files, space):
    result, index = 0, 0
    for _, (file_id, num_blocks) in sorted((files | space).items()):
        for i in range(num_blocks):
            if file_id != '.':
                result += (i + index) * file_id
        index += num_blocks
    return result


def build_file_system(v):
    space, files = {}, {}
    block_num, index = 0, 0
    for i, c in enumerate(v):
        val = int(c)
        is_block = i % 2 == 0
        if is_block:
            files[index] = (block_num, val)
            block_num += 1
        elif val > 0:
            space[index] = ('.', val)
        index += val
    return files, space


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day9_sample" if TEST_MODE else "input/day9").open() as f:
        value = f.readline().strip()
        now = time()
        print(f'Phase 1: {phase1(value)} {round(time() - now, 3)}s')
        print(f'Phase 2: {phase2(value)} {round(time() - now, 3)}s')
