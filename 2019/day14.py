import dataclasses
from collections import defaultdict
from pathlib import Path

TEST_MODE = False


@dataclasses.dataclass(frozen=True)
class Chemical:
    num: int
    name: str

    @staticmethod
    def parse(val):
        a, b = val.split(' ')
        return Chemical(int(a), b)


@dataclasses.dataclass(frozen=True)
class Rule:
    inputs: list[Chemical]
    out: Chemical

    @staticmethod
    def parse(line):
        in_, out_ = line.split(' => ')
        return Rule([Chemical.parse(s) for s in in_.split(', ')], Chemical.parse(out_))


def phase1(rules):
    return count_ore(rules_to_map(rules))


def phase2(rules: list[Rule]):
    step = 100000
    amount_of_fuel = step
    while True:
        num_ore = count_ore(rules_to_map(rules, amount_of_fuel))
        if num_ore > 1000000000000:
            amount_of_fuel -= step
            step = step // 10
            if step == 0:
                break
        else:
            amount_of_fuel += step

    return amount_of_fuel


def count_ore(chem_rule_map: dict[str, Rule]):
    spares = defaultdict(int)
    root = chem_rule_map['FUEL']
    while len(root.inputs) > 1:
        rewrite = defaultdict(int)
        for input_ in root.inputs:
            if input_.name == 'ORE':
                rewrite['ORE'] += input_.num
                continue
            substitutes, num_spares = substitute(input_, spares[input_.name], chem_rule_map[input_.name])
            spares[input_.name] = num_spares
            for sub in substitutes:
                rewrite[sub.name] += sub.num
        root = Rule([Chemical(v, k) for k, v in rewrite.items()], root.out)
    num_ore = root.inputs[0].num
    return num_ore


def substitute(chem: Chemical, num_spares: int, rule: Rule) -> (list[Chemical], int):
    multiplier, mod_ = chem.num // rule.out.num, chem.num % rule.out.num
    chem_remain = 0
    if mod_ > 0:
        multiplier += 1
        chem_remain = (multiplier * rule.out.num) - chem.num
    num_spares += chem_remain
    spare_reuse = min(num_spares // rule.out.num, multiplier)
    multiplier -= spare_reuse
    if spare_reuse > 0:
        num_spares -= spare_reuse * rule.out.num
    return [Chemical(c.num * multiplier, c.name) for c in rule.inputs], num_spares


def rules_to_map(rules: list[Rule], fuel_multiplier: int = 1):
    chem_rule_map = {r.out.name: r for r in rules}
    if fuel_multiplier > 1:
        root_rule = chem_rule_map['FUEL']
        inputs_ = [Chemical(c.num * fuel_multiplier, c.name) for c in root_rule.inputs]
        chem_rule_map['FUEL'] = Rule(inputs_, root_rule.out)
    return chem_rule_map


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day14_sample" if TEST_MODE else "input/day14").open() as f:
        values = [Rule.parse(i.strip()) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
