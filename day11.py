from pathlib import Path
import collections
import copy

TEST_MODE = False

Monkey = collections.namedtuple("Monkey", "items operation test inspections")
Operation = collections.namedtuple("Operation", "op op1 op2")
Test = collections.namedtuple("Test", "div monkey_true monkey_false")


def phase1(monkeys):
    return calc(monkeys, True, 20)


def phase2(monkeys):
    return calc(monkeys, False, 10000)


divisible = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23


def worry_op(operation, item):
    op1 = item if operation.op1 == 'old' else operation.op1
    op2 = item if operation.op2 == 'old' else operation.op2
    if operation.op == "*":
        return op1 * op2 % divisible
    else:
        return op1 + op2


def calc(monkeys, reduce_worry, rounds):
    inspections = {monkey_id: 0 for monkey_id in range(len(monkeys))}
    for round in range(rounds):
        monkey_round(monkeys, inspections, reduce_worry)
    active = list(reversed(sorted(inspections.values())))
    return active[0] * active[1]


def monkey_round(monkeys, inspections, reduce_worry):
    for id, monkey in enumerate(monkeys):
        for item in monkey.items:
            worry = worry_op(monkey.operation, item)
            worry = int(worry / 3) if reduce_worry else worry
            next_monkey = monkey.test.monkey_true if worry % monkey.test.div == 0 else monkey.test.monkey_false
            monkeys[next_monkey].items.append(worry)
            inspections[id] += 1
        monkey.items.clear()


def parse(monkey_block):
    lines = monkey_block.split('\n')
    items = [int(i) for i in extract(lines[1], ":").split(', ')]
    tmp = [i for i in extract(lines[2], "=").split(' ')]
    operation = Operation(tmp[1], tmp[0], int(tmp[2]) if tmp[2].isdigit() else 'old')
    divide_by = int(extract(lines[3], 'by '))
    true_monkey = int(extract(lines[4], 'monkey '))
    false_monkey = int(extract(lines[5], 'monkey '))
    test = Test(divide_by, true_monkey, false_monkey)
    return Monkey(items, operation, test, 0)


def extract(line, monkey_):
    return line.split(monkey_)[1].strip()


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day11_sample" if TEST_MODE else "input/day11").open() as f:
        values = [parse(block.strip()) for block in f.read().split("\n\n")]
        print(f'Phase 1: {phase1(copy.deepcopy(values))}')
        print(f'Phase 2: {phase2(copy.deepcopy(values))}')
