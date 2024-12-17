from pathlib import Path

TEST_MODE = False


def phase1(v):
    return sum([len(polygon) * len(fence(polygon)) for polygon in (find_polygons(v))])


def phase2(v):
    return sum([len(polygon) * len(sides(fence(polygon), polygon)) for polygon in (find_polygons(v))])


def sides(fences, polygon):
    result = []
    below_fences = {(x, y) for x, y in fences if (x, y + 1) in polygon}
    above_fences = {(x, y) for x, y in fences if (x, y - 1) in polygon}
    left_fences = {(x, y) for x, y in fences if (x + 1, y) in polygon}
    right_fences = {(x, y) for x, y in fences if (x - 1, y) in polygon}
    result.extend(group_left_right(below_fences))
    result.extend(group_left_right(above_fences))
    result.extend(group_up_down(right_fences))
    result.extend(group_up_down(left_fences))
    return result


def group_up_down(fences: set):
    return group(fences, lambda v: v, lambda a, b: a[0] == b[0] and abs(a[1] - b[1]) == 1)


def group_left_right(fences: set):
    return group(fences, lambda v: (v[1], v[0]), lambda a, b: a[1] == b[1] and abs(a[0] - b[0]) == 1)


def group(fences: set, sort_fun, adjacent):
    sorted_fences = sorted(fences, key=sort_fun)
    groups = []
    current_group = []

    for x, y in sorted_fences:
        if len(current_group) == 0:
            current_group.append((x, y))
        elif adjacent((x, y), current_group[-1]):
            current_group.append((x, y))
        else:
            groups.append(current_group)
            current_group = [(x, y)]

    groups.append(current_group)
    return groups


def find_polygons(v):
    visited = set()
    polygons = []
    for y, l in enumerate(v):
        for x, c in enumerate(l):
            if (x, y) not in visited:
                polygon = fill(v, (x, y), visited)
                polygons.append(polygon)
    return polygons


def fill(v, start, visited):
    polygon = {start}
    queue = [start]
    while len(queue) > 0:
        x, y = queue.pop()
        visited.add((x, y))
        for a, b in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + a, y + b
            if 0 <= ny < len(v) and 0 <= nx < len(v[0]) and (nx, ny) not in visited and v[y][x] == v[ny][nx]:
                polygon.add((nx, ny))
                queue.append((nx, ny))
    return polygon


def fence(polygon):
    result = []
    queue = list(polygon)
    while len(queue) > 0:
        x, y = queue.pop()
        for a, b in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + a, y + b
            if (nx, ny) not in polygon:
                result.append((nx, ny))
    return result


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day12_sample" if TEST_MODE else "input/day12").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
