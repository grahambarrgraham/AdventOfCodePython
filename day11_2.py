from pathlib import Path
import collections
import copy

TEST_MODE = True

Monkey = collections.namedtuple("Monkey", "items operation test")
Operation = collections.namedtuple("Operation", "op op1 op2")
Test = collections.namedtuple("Test", "div monkey_true monkey_false")
Item = collections.namedtuple("Item", "worry factors check")


def phase1(monkeys):
    return calc(monkeys, True, 20)


def phase2(monkeys):
    return calc(monkeys, False, 20)


def ev(item):
    return item.worry + \
        (13 * item.factors[13]) \
        + (17 * item.factors[17]) \
        + (19 * item.factors[19]) \
        + (23 * item.factors[23])


def worry_op(operation, item) -> Item:
    if operation.op == '*' and operation.op1 == 'old' and operation.op2 == 19:
        deepcopy = copy.deepcopy(item.factors)
        deepcopy[19] += item.worry
        return Item(0, deepcopy, item.check * 19)
    elif operation.op == '+':
        return Item(item.worry + operation.op2, item.factors, item.check + operation.op2)
    else:
        v = ev(item)
        return Item(v * v, {13: 0, 17: 0, 19: 0, 23: 0}, item.check * item.check)


def calc(monkeys, reduce_worry, rounds):
    inspections = {monkey_id: 0 for monkey_id in range(len(monkeys))}
    print(f"start {[monkey.items for monkey in monkeys]}")
    for round in range(rounds):
        monkey_round(monkeys, inspections, reduce_worry)
        print(f"{round} {inspections}")
        # print(f"{round} {[monkey.items for monkey in monkeys]}")
    active = list(reversed(sorted(inspections.values())))
    return active[0] * active[1]


def factorise(worry, factors, check) -> Item:
    for v_factor in [13, 17, 19, 23]:
        worry = factor(worry, factors, v_factor)
    return Item(worry, factors, check)


def factor(worry, factors, v_factor):
    div, mod = divmod(worry, v_factor)
    if div >= 1 and mod == 0:
        factors[v_factor] += div
        return 0
    return worry


def is_factor(item, div):
    return item.check % div == 0
    # return item.factors[div] > 0


def monkey_round(monkeys, inspections, reduce_worry):
    for id, monkey in enumerate(monkeys):
        for item in monkey.items:
            new_item = worry_op(monkey.operation, item)
            if reduce_worry:
                new_item.worry //= 3
            # new_item = factorise(new_item.worry, copy.deepcopy(item.factors), item.check)
            next_monkey = monkey.test.monkey_true if is_factor(new_item, monkey.test.div) else monkey.test.monkey_false
            monkeys[next_monkey].items.append(new_item)
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
    return Monkey([Item(item, {13: 0, 17: 0, 19: 0, 23: 0}, item) for item in items], operation, test)


def extract(line, monkey_):
    return line.split(monkey_)[1].strip()


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day11_sample" if TEST_MODE else "input/day11").open() as f:
        values = [parse(block.strip()) for block in f.read().split("\n\n")]
        # print(f'Phase 1: {phase1(copy.deepcopy(values))}')
        print(f'Phase 2: {phase2(copy.deepcopy(values))}')
