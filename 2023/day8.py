import dataclasses
import math
import re
from functools import cached_property
from pathlib import Path

TEST_MODE = False


@dataclasses.dataclass(frozen=True)
class Rule:
    from_: str
    left: str
    right: str

    def apply(self, l_or_r):
        return self.left if l_or_r == 'L' else self.right


@dataclasses.dataclass
class Search:
    v2_matching: bool
    instructions: str
    rules: list[Rule]

    @cached_property
    def rules_dict(self):
        return {r.from_: r for r in self.rules}

    def at_destination(self, r: str) -> bool:
        return r[2] == 'Z' if self.v2_matching else r == 'ZZZ'

    def search(self, current) -> (int, str):
        finished = False
        steps = 0
        while not finished:
            steps_, current = self.apply(current)
            finished = self.at_destination(current)
            steps += steps_
        return steps, current

    def apply(self, current: str) -> (int, str):
        steps = 0
        for instruction in self.instructions:
            steps += 1
            rule = self.rules_dict[current]
            current = rule.apply(instruction)
            if self.at_destination(current):
                return steps, current

        return steps, current


def phase1(instructions: str, rules: list[Rule]):
    search = Search(False, instructions, rules)
    steps, node = search.search('AAA')
    return steps


def phase2(instructions: str, rules: list[Rule]):
    search = Search(True, instructions, rules)
    start_nodes = [r.from_ for r in rules if r.from_[2] == 'A']
    steps = [search.search(node)[0] for node in start_nodes]
    return math.lcm(*steps)


def parse(lines) -> (str, list[Rule]):
    def read_rule(rule_line: str):
        m = re.match("(...) = \\((...), (...)", rule_line)
        return Rule(m.group(1), m.group(2), m.group(3))

    instructions = lines[0].strip()
    return instructions, [read_rule(l_.strip()) for l_ in lines[2:]]


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day8_sample" if TEST_MODE else "input/day8").open() as f:
        values = parse([line for line in f])
        print(f'Phase 1: {phase1(*values)}')
        print(f'Phase 2: {phase2(*values)}')
