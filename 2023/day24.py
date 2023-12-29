import itertools
from collections import defaultdict
from functools import reduce
from pathlib import Path

TEST_MODE = False


# vectors, dot product, intersect


def phase1(v):
    pairs = itertools.combinations(v, 2)
    min_d, max_d = [7, 27] if TEST_MODE else [200000000000000, 400000000000000]

    def in_area(n):
        x, y, z = n
        return min_d <= x <= max_d and min_d <= y <= max_d

    acc = [crosses(a, b, lambda p: in_area(p)) for a, b in pairs]

    return len([b for b in acc if b is True])


def phase2(hail):
    def vel_pos_map(axis_index):
        acc = defaultdict(list)
        for p, vv in hail:
            acc[vv[axis_index]].append(p[axis_index])
        return acc

    # Inspiration from Reddit
    # Many snowballs have the same speed in any given direction. Since we have to be able to hit both of the
    # snowballs in any such pair, the coordinates of both must be equal modulo the speed of the rock. Once I took the
    # intersection of all the possible speeds of pairwise equally fast snowballs I got a single possible speed value
    # for each axis.

    vx, vy, vz = velocity_for_axis(vel_pos_map(0)), velocity_for_axis(vel_pos_map(1)), velocity_for_axis(vel_pos_map(2))

    # Inspiration from Reddit
    # Any hailstone with velocity exactly vx, vy or vz will only intersect the rock if it shares the same coordinate as
    # the rock in that dimension.  Otherwise, the rock would never catch it in that dimension.  It happens that
    # there is at least one hailstone in the input with each of vx, vy and vz, and where there is more than one
    # in that dimension they share the same coordinate.  So position of the rock is literally present in the input!

    px, py, pz = vel_pos_map(0)[vx][0], vel_pos_map(1)[vy][0], vel_pos_map(2)[vz][0]

    return px + py + pz


def velocity_for_axis(vel_pos_map):
    hail_with_same_velocity = {vel: pos for vel, pos in vel_pos_map.items() if len(pos) > 2}
    candidates = defaultdict(set)

    for hail_velocity, hail_positions in hail_with_same_velocity.items():
        for i in range(-1000, 1000):
            mods = {position % i for position in hail_positions if i != 0}
            if len(mods) == 1:
                candidates[hail_velocity].add(i + hail_velocity)

    common_val = reduce(lambda a, b: a & b, candidates.values())
    return common_val.pop()


def crosses(a, b, in_area):
    a_p, a_v = a
    b_p, b_v = b
    perp_dot_a_b = perp_dot(a_v, b_v)
    parallel = perp_dot_a_b == 0
    u = minus(a_p, b_p)
    perp_dot_a_u = perp_dot(a_v, u)
    coincident = parallel and perp_dot_a_u == 0
    if not parallel and not coincident:
        t = perp_dot_a_u / perp_dot_a_b
        p = plus(b_p, times(b_v, t))
        if is_m_ahead_of_p_v(p, b) and is_m_ahead_of_p_v(p, a) and in_area(p):
            return True
    elif coincident:
        if is_m_ahead_of_p_v(b_p, a) or is_m_ahead_of_p_v(a_p, b):
            return True
    return False


def is_m_ahead_of_p_v(m, p_v):
    p, v = p_v
    n_2 = plus(p, v)
    return is_between(n_2, p, m) or is_between(m, p, n_2)


def is_between(p, a, b):
    x_a, y_a, z_a = a
    x_b, y_b, z_b = b
    x_p, y_p, z_p = p

    d_x = x_b - x_a
    d_y = y_b - y_a

    if abs(d_x) >= abs(d_y):
        return x_a <= x_p <= x_b if d_x > 0 else x_b <= x_p <= x_a
    else:
        return y_a <= y_p <= y_b if d_y > 0 else y_b <= y_p <= y_a


def plus(a, b):
    x_a, y_a, z_a = a
    x_b, y_b, z_b = b
    return x_a + x_b, y_a + y_b, z_a + z_b


def times(v, m):
    x, y, z = v
    return x * m, y * m, z * m


def minus(a, b):
    x_a, y_a, z_a = a
    x_b, y_b, z_b = b
    return x_a - x_b, y_a - y_b, z_a - z_b


def dot(v1, v2):
    return sum([c1 * c2 for c1, c2 in zip(v1, v2)])


def perp_dot(a, b):
    x_a, y_a, z_a = a
    x_b, y_b, z_b = b
    return (x_a * y_b) - (y_a * x_b)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day24_sample" if TEST_MODE else "input/day24").open() as f:
        def vector(s):
            return tuple([int(i) for i in s.split(', ')])


        values = [tuple(vector(a) for a in i.strip().split(' @ ')) for i in f]

        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
