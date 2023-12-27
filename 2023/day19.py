import math
import re
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

TEST_MODE = False


def phase1(wfs, ratings):
    acc = 0
    for r in ratings:
        acc += workflows(wfs, *(int(i[2:]) for i in r))
    return acc


def phase2(wfs):
    acc = defaultdict(list)
    queue = [('in', {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)})]
    all_accepts = []

    while len(queue) > 0:
        wf, xmas = queue.pop(0)
        children, accepts = apply_workflow(wf, wfs, xmas)
        queue.extend(children)
        all_accepts.extend(accepts)

    return sum(combinations(a) for a in all_accepts)


def combinations(xmas):
    return math.prod([xmas[i][1] - xmas[i][0] + 1 for i in 'xmas'])


def apply_workflow(wf, wfs, xmas):
    children = []
    accepts = []
    for wf in wfs[wf]:
        if len(wf) > 1:
            constraint, destination = wf
            nxt_xmas = apply_inv_constraint(constraint, xmas)
            if destination == 'A':
                accepts.append(apply_constraint(constraint, xmas))
            elif destination != 'R':
                children.append((destination, apply_constraint(constraint, xmas)))
            xmas = nxt_xmas
        else:
            destination = wf[0]
            if destination == 'A':
                accepts.append(xmas)
            elif destination != 'R':
                destination = wf[0]
                children.append((destination, xmas))

    return children, accepts


def apply_inv_constraint(constraint, xmas):
    letter, op, operand = parse_constraint(constraint)
    xmas = deepcopy(xmas)
    mn, mx = xmas[letter]
    xmas[letter] = (mn, min(mx, operand)) if op == '>' else (max(mn, operand), mx)
    return xmas


def apply_constraint(constraint, xmas):
    letter, op, operand = parse_constraint(constraint)
    xmas = deepcopy(xmas)
    mn, mx = xmas[letter]
    xmas[letter] = (max(mn, operand + 1), mx) if op == '>' else (mn, min(mx, operand - 1))
    return xmas


def parse_constraint(constraint):
    letter = constraint[0]
    op = constraint[1]
    operand = int(constraint[2:])
    return letter, op, operand


def workflows(wfs, x, m, a, s):
    wf = wfs['in']
    while True:
        nxt = workflow(wf, x, m, a, s)
        if nxt not in 'AR':
            wf = wfs[nxt]
            continue
        break

    return sum([x, m, a, s]) if nxt == 'A' else 0


def workflow(wf, x, m, a, s):
    for rule in wf:
        nxt = rule[0] if len(rule) == 1 else rule[1] if eval(rule[0]) else None
        if nxt is not None:
            return nxt


def read_flows(block):
    flows = {}
    for r in block:
        m = re.match(r"(.+)\{(.+)\}", r)
        flows[m.group(1)] = [[j.split(':') for j in i.split(',')][0] for i in m.group(2).split(',')]
    return flows


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day19_sample" if TEST_MODE else "input/day19").open() as f:
        blocks = [[r for r in block.split()] for block in f.read().split("\n\n")]
        _flows = read_flows(blocks[0])
        _ratings = [r[1:-1].split(',') for r in blocks[1]]
        print(f'Phase 1: {phase1(_flows, _ratings)}')
        print(f'Phase 2: {phase2(_flows)}')
