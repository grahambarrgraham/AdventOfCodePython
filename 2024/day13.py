import math
import re
from pathlib import Path

TEST_MODE = False

n = 10000000000000
tol = 1 / n


def phase1(slots):
    return sum(cost(*slot) for slot in slots)


def phase2(slots):
    slots = [(a, b, (x + n, y + n)) for a, b, (x, y) in slots]
    return sum(cost(*slot) for slot in slots)


def cost(a, b, p):
    (a_x, a_y), (b_x, b_y), (p_x, p_y) = a, b, p
    lcm = math.lcm(p_x, p_y)
    m_x, m_y = lcm // p_x, lcm // p_y
    (na_x, na_y) = (a_x * m_x, a_y * m_y)
    (nb_x, nb_y) = (b_x * m_x, b_y * m_y)
    ratio = abs((na_y - na_x) / (nb_y - nb_x))
    pull_a = p_y / (a_y + (ratio * b_y))
    pull_b = (p_y - (pull_a * a_y)) / b_y
    r_a, r_b = round(pull_a, 0), round(pull_b, 0)
    if math.isclose(pull_a, r_a, rel_tol=tol) and math.isclose(pull_b, r_b, rel_tol=tol):
        pull_a, pull_b = r_a, r_b
        return int((pull_a * 3) + pull_b)
    return 0


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day13_sample" if TEST_MODE else "input/day13").open() as f:
        values = f.read().split('\n\n')
        slot_machines = []
        for v in values:
            a, b, p = v.split('\n')
            re_button = '.*X\\+(\\d+), Y\\+(\\d+)'
            matches = re.match(re_button, a)
            a = (int(matches.group(1)), int(matches.group(2)))
            matches = re.match(re_button, b)
            b = (int(matches.group(1)), int(matches.group(2)))
            matches = re.match('.+X=(\\d+), Y=(\\d+)', p)
            p = (int(matches.group(1)), int(matches.group(2)))
            slot_machines.append((a, b, p))
        print(f'Phase 1: {phase1(slot_machines)}')
        print(f'Phase 2: {phase2(slot_machines)}')
