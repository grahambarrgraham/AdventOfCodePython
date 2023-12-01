from pathlib import Path
import collections
from operator import attrgetter
import re
import time

Coord = collections.namedtuple("Coord", "x y")
Sensor = collections.namedtuple("Sensor", "location beacon manhattan")
XRange = collections.namedtuple("XRange", "start end")

TEST_MODE = False


def phase1(y_index):
    line = 10 if TEST_MODE else 2000000
    return sum([r.end - r.start for r in y_index[line]])


def phase2(y_index):
    v_max = 25 if TEST_MODE else 4000000
    for y in range(1, v_max + 1):
        ranges = y_index[y]
        if len(ranges) > 1:
            return (ranges[0].end + 1) * 4000000 + y
    return -1


def build_index(v_sensors):
    y_index = {}
    for sensor in v_sensors:
        update_index(y_index, sensor.location, sensor.manhattan)
    return y_index


def get_x_range(location, y, manhattan):
    offset = manhattan - abs(location.y - y)
    return XRange(location.x - offset, location.x + offset)


def combine_ranges(ranges):
    ranges.sort(key=attrgetter('start'))
    result = []
    for r in ranges:
        if not result:
            result.append(r)
        else:
            result.extend(combine_range(result.pop(), r))
    return result


def combine_range(r1, r2):
    if r1.start <= r2.start <= r1.end:
        return [XRange(r1.start, max(r1.end, r2.end))]
    elif r1.start <= r2.end <= r1.end:
        return [XRange(min(r1.start, r2.start), r2.end)]
    else:
        return [r1, r2]


def update_index(y_index, location, manhattan):
    for y in range(location.y - manhattan, location.y + manhattan + 1):
        x_range = get_x_range(location, y, manhattan)
        if y in y_index:
            y_index[y].append(x_range)
            y_index[y] = combine_ranges(y_index[y])
        else:
            y_index[y] = [x_range]


def manhattan_distance(loc, beacon):
    return abs(loc.x - beacon.x) + abs(loc.y - beacon.y)


def parse_sensor(line):
    pattern = re.compile("Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)")
    m = pattern.match(line)
    loc = Coord(int(m.group(1)), int(m.group(2)))
    beacon = Coord(int(m.group(3)), int(m.group(4)))
    return Sensor(loc, beacon, manhattan_distance(loc, beacon))


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day15_sample" if TEST_MODE else "input/day15").open() as f:
        t0 = int(time.time() * 1000)
        sensors = [parse_sensor(i.strip()) for i in f]
        index = build_index(sensors)
        t1 = int(time.time() * 1000)
        print(f"index took:{t1 - t0}")
        print(f'Phase 1: {phase1(index)}')
        print(f'Phase 2: {phase2(index)}')

