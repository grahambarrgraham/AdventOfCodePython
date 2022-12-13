from pathlib import Path
import collections

TEST_MODE = False

Coord = collections.namedtuple('Coord', ('x', 'y'))
Instruction = collections.namedtuple('Instruction', ('direction', 'count'))


def phase1(v):
    rope = [Coord(0, 0)] * 2
    return calc(rope, v)


def phase2(v):
    rope = [Coord(0, 0)] * 10
    return calc(rope, v)


def move_head(head_pos, instruction):
    match instruction.direction:
        case 'U':
            return Coord(head_pos.x, head_pos.y + instruction.count)
        case 'D':
            return Coord(head_pos.x, head_pos.y - instruction.count)
        case 'L':
            return Coord(head_pos.x - instruction.count, head_pos.y)
        case 'R':
            return Coord(head_pos.x + instruction.count, head_pos.y)
    return None


def move_tail(head_pos, tail_pos):
    if abs(head_pos.x - tail_pos.x) < 2 and abs(head_pos.y - tail_pos.y) < 2:
        return tail_pos

    if head_pos.x == tail_pos.x:
        return Coord(tail_pos.x,
                     tail_pos.y + (1 if head_pos.y > tail_pos.y else -1))

    if head_pos.y == tail_pos.y:
        return Coord(tail_pos.x + (1 if head_pos.x > tail_pos.x else -1),
                     tail_pos.y)

    return Coord(tail_pos.x + (1 if head_pos.x > tail_pos.x else -1),
                 tail_pos.y + (1 if head_pos.y > tail_pos.y else -1))


def calc(rope, instructions):
    tail_positions = [Coord(0, 0)]
    for instruction in instructions:
        for _ in range(instruction.count):
            rope[0] = move_head(rope[0], Instruction(instruction.direction, 1))
            for index, knot in enumerate(rope[1:]):
                rope[index + 1] = move_tail(rope[index], rope[index + 1])
            tail_positions.append(rope[-1])
    return len(set(tail_positions))


def parse(line):
    split = line.strip().split(' ')
    return Instruction(split[0], int(split[1]))


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day9_sample" if TEST_MODE else "input/day9").open() as f:
        values = [parse(i) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
