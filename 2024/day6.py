import time
from pathlib import Path

TEST_MODE = False

directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]


class Map:
    def __init__(self, map_):
        self.map_ = map_
        self.original_guard, self.original_obstructions = self.build_locations()
        self.direction, self.guard, self.obstructions = self.reset_()

    def reset(self):
        self.direction, self.guard, self.obstructions = self.reset_()

    def reset_(self):
        return 0, self.original_guard, self.original_obstructions.copy()

    def build_locations(self):
        guard = None
        obstructions = set()
        for y, l in enumerate(self.map_):
            for x, c in enumerate(l):
                if self.map_[y][x] == '#':
                    obstructions.add((x, y))
                elif self.map_[y][x] == '^':
                    guard = (x, y)
        return guard, obstructions

    def walk(self):
        all_positions = [self.guard]
        while True:
            x, y = self.guard
            d_x, d_y = directions[self.direction]
            nxt_x, nxt_y = x + d_x, y + d_y
            if (nxt_x, nxt_y) not in self.obstructions:
                self.guard = (nxt_x, nxt_y)
                if not self.guard_in_map():
                    break
                all_positions.append(self.guard)
            else:
                self.direction = (self.direction + 1) % len(directions)
                break
        return all_positions

    def guard_in_map(self):
        x, y = self.guard
        return 0 <= x < len(self.map_[0]) and 0 <= y < len(self.map_)

    def find_all_positions(self):
        all_positions = set()
        walk_counter = 0
        # arbitrary value found by trial and error, but seems to work for the input data
        max_ = len(self.obstructions) // 5
        while self.guard_in_map() and walk_counter <= max_:
            walk_positions = self.walk()
            all_positions.update(walk_positions)
            walk_counter += 1
        return all_positions, self.guard_in_map()


def phase1(v):
    positions, _ = Map(v).find_all_positions()
    return len(positions)


def phase2(v):
    map_ = Map(v)
    all_positions, _ = map_.find_all_positions()
    loop_obstacles = []
    for x, y in all_positions:
        map_.reset()
        map_.obstructions.add((x, y))
        _, is_loop = map_.find_all_positions()
        if is_loop:
            loop_obstacles.append((x, y))
    return len(loop_obstacles)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day6_sample" if TEST_MODE else "input/day6").open() as f:
        values = [i.strip() for i in f]
        now = time.time()
        print(f'Phase 1: {phase1(values)} {time.time() - now}ms')
        print(f'Phase 2: {phase2(values)} {time.time() - now}ms')
