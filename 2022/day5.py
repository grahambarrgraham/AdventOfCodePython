import copy
from pathlib import Path
import re

TEST_MODE = False


def phase1(stacks, instructions):
    for instruction in instructions:
        for i in range(instruction.to_move):
            container = stacks[instruction.from_stack].pop(0)
            stacks[instruction.to_stack].insert(0, container)
    return get_first_crate_in_stacks(stacks)


def phase2(stacks, instructions):
    for i in instructions:
        to_move = stacks[i.from_stack][:i.to_move]
        stacks[i.from_stack] = stacks[i.from_stack][i.to_move:]
        stacks[i.to_stack] = to_move + stacks[i.to_stack]
    return get_first_crate_in_stacks(stacks)


class Instruction:
    def __init__(self, instruction_data):
        self.to_move = int(instruction_data[0])
        self.from_stack = int(instruction_data[1]) - 1
        self.to_stack = int(instruction_data[2]) - 1

    def __repr__(self):
        return f"move={self.to_move} from={self.from_stack} to={self.to_stack}"


def get_first_crate_in_stacks(stacks):
    return ''.join([stack[0] if len(stack) > 0 else '' for stack in stacks])


def read_stack_line(line: str, stacks):
    count = 0
    for stack in range(len(stacks)):
        stack_index = 1 + (4 * count)
        if len(line) > stack_index and line[stack_index].strip() != '':
            stacks[stack].append(line[stack_index].strip())
        count = count + 1


def parse_stacks(v):
    result = [[], [], [], [], [], [], [], [], []]
    for line in v.split('\n')[:-1]:
        read_stack_line(line, result)
    return result


def parse_instruction(lines):
    instruction_data = [re.search(r"move (\d+) from (\d+) to (\d+)", line).groups() for line in lines.split('\n')]
    return [Instruction(i) for i in instruction_data]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day5_sample" if TEST_MODE else "input/day5").open() as f:
        blocks = [block for block in f.read().split("\n\n")]
        v_stacks = parse_stacks(blocks[0])
        v_instructions = parse_instruction(blocks[1])
        print(f'Phase 1: {phase1(copy.deepcopy(v_stacks), v_instructions)}')
        print(f'Phase 2: {phase2(copy.deepcopy(v_stacks), v_instructions)}')
