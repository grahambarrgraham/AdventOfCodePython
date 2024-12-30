from copy import deepcopy
from pathlib import Path

TEST_MODE = False

move_map = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}


def phase1(map_, moves):
    run_sim(map_, moves)
    return score(map_, 'O')


def phase2(map_, moves):
    wide_map = widen_map(map_)
    run_sim(wide_map, moves)
    return score(wide_map, '[')


def run_sim(map_, moves):
    x, y = find_start(map_)
    count = 0
    for move in moves:
        actions = collect(map_, x, y, *move_map[move])
        play(map_, actions)
        x, y = (x, y) if len(actions) == 0 else actions[-1][1]
        count += 1


def play(map_, actions):
    for (x, y), (x1, y1) in actions:
        current = map_[y][x]
        map_[y][x] = '.'
        map_[y1][x1] = current


def collect(map_, x, y, m_x, m_y):
    nxt = map_[y + m_y][x + m_x]
    result = []
    if nxt == '.':
        result.extend([((x, y), (x + m_x, y + m_y))])
    elif nxt == 'O' or (nxt in ['[', ']'] and m_x != 0):
        nxt = collect(map_, x + m_x, y + m_y, m_x, m_y)
        if len(nxt) > 0:
            result.extend(nxt)
            result.extend([((x, y), (x + m_x, y + m_y))])
    elif nxt in ['[', ']']:
        d_x = 1 if nxt == '[' else -1
        nxt_a = collect(map_, x + m_x, y + m_y, m_x, m_y)
        nxt_b = collect(map_, x + d_x + m_x, y + m_y, m_x, m_y)
        if len(nxt_a) > 0 and len(nxt_b) > 0:
            result.extend(nxt_a)
            result.extend(nxt_b)
            if map_[y][x] == '@':
                result.extend([((x, y), (x + m_x, y + m_y))])
            else:
                d_x = 1 if map_[y][x] == '[' else -1
                result.extend([((x, y), (x + m_x, y + m_y))])
                result.extend([((x + d_x, y), (x + d_x + m_x, y + m_y))])
            result = sorted(set(result), key=lambda a: a[1][1], reverse=True if m_y > 0 else False)

    return result


def pretty_print(wide_map):
    for l in wide_map:
        print(''.join(l))


def find_start(map_):
    for y, l in enumerate(map_):
        for x, c in enumerate(l):
            if map_[y][x] == '@':
                return x, y


def score(map_, marker):
    result = 0
    for y, l in enumerate(map_):
        for x, c in enumerate(l):
            if map_[y][x] == marker:
                result += x + (y * 100)
    return result


def widen_map(map_):
    wide_map = []
    for line in map_:
        wide_line = []
        for c in line:
            if c == 'O':
                wide_line.extend(['[', ']'])
            elif c == '@':
                wide_line.extend(['@', '.'])
            else:
                wide_line.extend([c, c])
        wide_map.append(wide_line)
    return wide_map


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day15_sample" if TEST_MODE else "input/day15").open() as f:
        values = f.read().split('\n\n')
        _map = [list(s) for s in values[0].split('\n')]
        _moves = ''.join(s for s in values[1].split('\n'))
        print(f'Phase 1: {phase1(deepcopy(_map), _moves)}')
        print(f'Phase 2: {phase2(deepcopy(_map), _moves)}')
