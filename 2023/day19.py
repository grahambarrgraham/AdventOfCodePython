import re
from copy import deepcopy
from pathlib import Path

TEST_MODE = False


def phase1(wfs, ratings):
    acc = 0
    for r in ratings:
        acc += workflows(wfs, *(int(i[2:]) for i in r))
    return acc


def phase2(wfs, _):
    return -1


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
        # print(f'Phase 2: {phase2(values)}')
