import collections
from pathlib import Path

import match

TEST_MODE = False

# TAG: search, astar

Coord = collections.namedtuple("Coord", "x y")
SearchNode = collections.namedtuple("SearchNode", "loc, previous_move")
moves = {(0, 1), (0, -1), (1, 0), (-1, 0)}


def phase1(map_):
    start = Coord(0, 0)
    target = Coord(len(map_[0]) - 1, len(map_) - 1)
    return search(map_, start, lambda n, _: n.loc == target, max_moves=3, min_moves=0)


def phase2(map_):
    start = Coord(0, 0)
    target = Coord(len(map_[0]) - 1, len(map_) - 1)
    min_moves = 4

    def goal_reached(search_node, _) -> bool:
        prev_x, prev_y = search_node.previous_move
        return search_node.loc == target and (abs(prev_x) >= min_moves or abs(prev_y) >= min_moves)

    return search(map_, start, goal_reached, max_moves=10, min_moves=4)


def search(map_, start_loc: Coord, goal_func, max_moves, min_moves):
    start = SearchNode(start_loc, (0, 0))

    result = astar.find_path(start, None,
                             lambda search_node: valid_moves(map_, search_node, max_moves, min_moves),
                             heuristic_cost_estimate_fun=lambda a, b: 0,
                             edge_cost_fun=lambda a, b: cost(map_, a.loc, b.loc),
                             is_goal_reached_fun=goal_func
                             )
    result = list(result)
    costs = [cost(map_, result[x].loc, result[x + 1].loc) for x in range(len(result) - 1)]
    # pairs = [(result[x].loc, result[x + 1].loc) for x in range(len(result) - 1)]
    # for c, p in zip(costs, pairs):
    #     start, stop = p
    #     print(f"{c} {start}->{stop}")
    return sum(costs)


def valid_moves(map_, node: SearchNode, max_moves, min_moves) -> list[SearchNode]:
    candidate_moves = [(move, merge_moves(move, node.previous_move), node.previous_move) for move in moves]
    allowed_moves = [(move, merged_move) for move, merged_move, previous_move in candidate_moves if
                     allowed(merged_move, previous_move, max_moves, min_moves)]
    candidates_nodes = [SearchNode(destination(node.loc, move), merged_move) for move, merged_move in allowed_moves]
    result = [node for node in candidates_nodes if not is_off_map(map_, node.loc)]
    # print(f"valid moves for {node} -> {result}")
    return result


def allowed(merged_move, previous_move, max_moves, min_moves):
    x, y = merged_move
    prev_x, prev_y = previous_move
    in_max_moves = abs(x) <= max_moves and abs(y) <= max_moves
    turn_180 = (prev_x < 0 < x) or (prev_x > 0 > x) or (prev_y < 0 < y) or (prev_y > 0 > y)
    turn_90 = (prev_x != 0 and y != 0) or (prev_y != 0 and x != 0)
    if min_moves > 0 and turn_90:
        within_lower_limit = (abs(prev_x) >= min_moves or abs(prev_y) >= min_moves)
    else:
        within_lower_limit = True
    return in_max_moves and not turn_180 and within_lower_limit


def merge_moves(move, previous_move):
    prev_x, prev_y = previous_move
    x, y = move

    def _merge(a, b):
        if (a < 0 and b < 0) or (a > 0 and b > 0):
            return a + b
        return a

    x = _merge(x, prev_x)
    y = _merge(y, prev_y)
    return x, y


def cost(m, start, stop):
    move_y = stop.y - start.y
    move_x = stop.x - start.x
    y_step = 0 if move_y == 0 else 1 if move_y > 0 else -1
    x_step = 0 if move_x == 0 else 1 if move_x > 0 else -1
    acc = 0
    if y_step != 0:
        y_start = start.y + y_step
        for y in range(y_start, y_start + move_y, y_step):
            acc += m[y][start.x]
    if x_step != 0:
        x_start = start.x + x_step
        for x in range(x_start, x_start + move_x, x_step):
            acc += m[start.y][x]
    # print(f"cost for {start} to {stop} is {acc}")
    return acc


def is_off_map(m, next_coord):
    return next_coord.x < 0 or next_coord.x >= len(m[0]) or next_coord.y < 0 or next_coord.y >= len(m)


def destination(coord, move):
    return Coord(coord.x + move[0], coord.y + move[1])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day17_sample" if TEST_MODE else "input/day17").open() as f:
        values = [[int(n) for n in i.strip()] for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
