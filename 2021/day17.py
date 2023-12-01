from pathlib import Path
import sys
import re

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    return max(throws(v))


def phase2(v):
    return len(throws(v))


def throws(v):
    tar_min_x, tar_max_x = v['x']
    tar_min_y, tar_max_y = v['y']
    hits = []
    for x_vel in range(0, tar_max_x + 1):
        possible = True
        y_vel = tar_min_y
        while possible:
            hit, y = throw(x_vel, y_vel, v)
            if hit:
                hits.append(y)
            else:
                if y_vel >= 0:
                    margin = 20
                    possible = (tar_min_y - margin) < y < (tar_max_y + margin)
            y_vel += 1

    return hits


def throw(x_vel, y_vel, v):
    x, y = (0, 0)
    tar_min_x, tar_max_x = v['x']
    tar_min_y, tar_max_y = v['y']

    max_y = 0

    while x <= tar_max_x and y >= tar_min_y:
        x += x_vel
        y += y_vel
        max_y = max(max_y, y)
        if tar_max_x >= x >= tar_min_x and tar_max_y >= y >= tar_min_y:
            return True, max_y
        x_vel = drag(x_vel)
        y_vel -= 1

    return False, y


def drag(x):
    if x < 0:
        x += 1
    elif x > 0:
        x -= 1
    return x


def load(s):
    matches = re.match(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", s)
    return {"x": (int(matches.group(1)), int(matches.group(2))), "y": (int(matches.group(3)), int(matches.group(4)))}


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day17_sample" if TEST_MODE else "input/day17").open() as f:
        values = load([i.strip() for i in f][0])
        print(values)
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
