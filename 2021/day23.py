import copy
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1():
    start = Map(('A', 'B'), ('D', 'C'), ('C', 'B'), ('A', 'D'), {}, 2)
    stop = Map(('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), {}, 2)
    return a_star_algorithm(start, stop, True)


def phase2():
    start = Map(('C', 'D', 'D', 'D'), ('C', 'B', 'C', 'D'), ('B', 'A', 'B', 'A'), ('B', 'C', 'A', 'A'), {}, 4)
    start1 = Map(('C', 'D', 'D', 'D'), ('C', 'B', 'C', 'D'), ('B', 'A', 'B', 'A'), ('B', 'C'), {0: 'A', 1: 'A'}, 4)
    stop = Map(('A', 'A', 'A', 'A'), ('B', 'B', 'B', 'B'), ('C', 'C', 'C', 'C'), ('D', 'D', 'D', 'D'), {}, 4)
    return a_star_algorithm(start, start1, True) + a_star_algorithm(start1, stop, True)


class Map:
    amphipod_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    room_index = {'A': 2, 'B': 4, 'C': 6, 'D': 8}

    def __init__(self, a_room, b_room, c_room, d_room, hall, size):
        self.hall = hall
        self.rooms = {'A': a_room, 'B': b_room, 'C': c_room, 'D': d_room}
        self.room_size = size
        self.hash_val = -1
        self.heuristic_val = -1

    def room_can_be_entered(self, amphipod):
        return len([a for a in self.rooms[amphipod] if a != amphipod]) == 0

    def room_is_reachable(self, index, amphipod):
        target = self.room_index[amphipod]
        return len([i for i in self.hall.keys() if index < i < target or index > i > target]) == 0

    def hall_is_reachable(self, index, amphipod):
        target = self.room_index[amphipod]
        return len([i for i in self.hall.keys() if index <= i <= target or index >= i >= target]) == 0

    def move_to_room(self, index, amphipod):
        cost = self.amphipod_cost[amphipod] * (
                self.hall_moves(amphipod, index) + self.room_size - len(self.rooms[amphipod]))
        self.hall.pop(index)
        self.rooms[amphipod] += (amphipod,)
        self.hash_val = -1
        self.heuristic_val = -1
        return cost

    def create_hash(self):
        return hash((tuple(self.hall.items()), tuple(self.rooms.items())))

    def move_from_room(self, index, amphipod):
        amphipod_to_move = self.rooms[amphipod][-1]
        cost = self.amphipod_cost[amphipod_to_move] * (
                self.hall_moves(amphipod, index) + 1 + self.room_size - len(self.rooms[amphipod]))
        self.hall[index] = amphipod_to_move
        room = self.rooms[amphipod]
        self.rooms[amphipod] = room[:-1]
        self.hash_val = -1
        return cost

    def hall_moves(self, amphipod, index):
        return abs(self.room_index[amphipod] - index)

    def __repr__(self):
        return f"<{self.rooms}, {self.hall}>"

    def __eq__(self, other):
        return self.hall == other.hall and self.rooms == other.rooms

    def __hash__(self):
        if self.hash_val == -1:
            self.hash_val = self.create_hash()
        return self.hash_val

    def copy(self):
        return Map(self.rooms['A'], self.rooms['B'], self.rooms['C'], self.rooms['D'], copy.deepcopy(self.hall), self.room_size)

    def count_blocked(self):
        blocked_amount = 0
        blocked_count = 0
        for room in ['A', 'B', 'C', 'D']:
            if len(self.rooms[room]) > 0:
                amphipod_to_move = self.rooms[room][-1]
                dest_room_can_be_entered = self.room_can_be_entered(amphipod_to_move)
                dest_room_is_reachable = self.room_is_reachable(self.room_index[room], amphipod_to_move)
                if amphipod_to_move == room:
                    if not dest_room_can_be_entered:
                        blocked_amount += self.amphipod_cost[amphipod_to_move]
                        blocked_count += 1
                    continue
                if not dest_room_is_reachable:
                    blocked_amount += self.amphipod_cost[amphipod_to_move]
                    blocked_count += 1
                if not dest_room_can_be_entered:
                    blocked_amount += self.amphipod_cost[amphipod_to_move]
                    blocked_count += 1

        for hall_index, amphipod in self.hall.items():
            dest_room_can_be_entered = self.room_can_be_entered(amphipod)
            if not dest_room_can_be_entered:
                blocked_amount += self.amphipod_cost[amphipod_to_move]
                blocked_count += 1

        return blocked_amount, blocked_count

    def heuristic(self):

        def distance_to_room(hall_index_1, hall_index_2):
            return abs(hall_index_1 - hall_index_2)

        def calc_heuristic():
            resp = 0
            for hall_index, amphipod in self.hall.items():
                to_room = distance_to_room(self.room_index[amphipod], hall_index)
                resp += (to_room + 1) * self.amphipod_cost[amphipod]

            for room in ['A', 'B', 'C', 'D']:
                for index, amphipod in enumerate(self.rooms[room]):
                    if amphipod != room:
                        slots = self.room_size - index
                        to_room = distance_to_room(self.room_index[amphipod], self.room_index[room])
                        resp += (to_room + slots + 1) * self.amphipod_cost[amphipod]
            return resp

        if self.heuristic_val < 0:
            self.heuristic_val = calc_heuristic()
        return self.heuristic_val


def rule_room_to_room(map: Map, moves):
    for amphipod in map.rooms.keys():
        the_room = map.rooms[amphipod]
        if len(the_room) == 0:
            continue
        amphipod_to_move = the_room[-1]
        if amphipod_to_move == amphipod:
            continue
        if map.room_can_be_entered(amphipod_to_move) and map.room_is_reachable(map.room_index[amphipod],
                                                                               amphipod_to_move):
            new_map = map.copy()
            cost = new_map.move_from_room(new_map.room_index[amphipod_to_move], amphipod) + \
                   new_map.move_to_room(new_map.room_index[amphipod_to_move], amphipod_to_move)
            moves.append((new_map, cost))


def rule_hall_to_room(map, moves):
    for index, amphipod in map.hall.items():
        if map.room_can_be_entered(amphipod) and map.room_is_reachable(index, amphipod):
            new_map = map.copy()
            cost = new_map.move_to_room(index, amphipod)
            moves.append((new_map, cost))


def rule_room_to_hall(map, moves):
    for amphipod in map.rooms.keys():
        the_room = map.rooms[amphipod]
        if len(the_room) > 0 and not all(p == amphipod for p in the_room):
            for i in [0, 1, 3, 5, 7, 9, 10]:
                blocked_amount, blocked_count = map.count_blocked()
                if map.hall_is_reachable(i, amphipod):
                    new_map = map.copy()
                    cost = new_map.move_from_room(i, amphipod)
                    new_map_amount_blocked, new_map_count_blocked = new_map.count_blocked()
                    if new_map_count_blocked <= blocked_count or new_map_amount_blocked <= blocked_amount + 300:
                        moves.append((new_map, cost))


def find_neighbours(map: Map) -> [(Map, int)]:
    moves = []
    rule_room_to_room(map, moves)
    if len(moves) == 0:
        rule_hall_to_room(map, moves)
    if len(moves) == 0:
        rule_room_to_hall(map, moves)
    return moves


def a_star_algorithm(start, stop, use_heuristic):
    open_set = {start}
    closed_set = set()
    min_node = start
    node_scores = {start: 0}
    parents = {start: (start, 0)}
    while len(open_set) > 0:
        n = min_node

        if n is None:
            return None

        if n == stop:
            return node_scores[n]

        for m, weight in find_neighbours(n):
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                parents[m] = n
                node_scores[m] = node_scores[n] + weight
                if node_scores[m] < node_scores[min_node]:
                    min_node = m

            else:
                if node_scores[m] > node_scores[n] + weight:
                    node_scores[m] = node_scores[n] + weight
                    if node_scores[m] < node_scores[min_node]:
                        min_node = m
                    parents[m] = n

                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)

        open_set.remove(n)
        closed_set.add(n)

        if len(open_set) > 0:
            min_node = min(open_set, key=lambda v: (v.heuristic() if use_heuristic else 0) + node_scores[v])
        else:
            min_node = None
    return None


if __name__ == "__main__":
    print("phase 1:", phase1())
    print("phase 2:", phase2())
