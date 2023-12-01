from pathlib import Path
import sys
from collections import deque

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    return sum([parse(line)[0] for line in v])


def phase2(v):
    incompletes = [stack for (score, stack, line) in [parse(line) for line in v] if score == 0]
    stack_scores = sorted([score_stack(stack) for stack in incompletes])
    return stack_scores[int(len(stack_scores) / 2 - 0.5)]


def score_stack(stack):
    score = 0
    for bracket in reversed(stack):
        score = (5 * score) + completion_score_dict[bracket]
    return score


completion_score_dict = {'[': 2, '(': 1, '{': 3, '<': 4}
syntax_score_dict = {']': 57, ')': 3, '}': 1197, '>': 25137}
closes_dict = {']': '[', ')': '(', '}': '{', '>': '<'}


def parse(line):
    stack = deque()
    for bracket in line:
        match bracket:
            case '[' | '{' | '(' | '<':
                stack.append(bracket)
            case _:
                last = stack.pop()
                if not closes_dict[bracket] == last:
                    return syntax_score_dict[bracket], stack, line
    return 0, stack, line


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day10_sample" if TEST_MODE else "input/day10").open() as f:
        values = [list(i.strip()) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
