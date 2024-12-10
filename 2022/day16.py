import collections
import re
from pathlib import Path

TEST_MODE = False

Valve = collections.namedtuple("Valve", "name, rate, tunnels")
State = collections.namedtuple("State", "location pressure_released move_count open_valves")
Graph = collections.namedtuple("Graph", "valves max_rate")


def max_rate(valves):
    return sum([v.rate for v in valves])


def phase1(valves):
    graph = {valve.name: valve for valve in valves}
    start = State("AA", 0, 0, frozenset())
    result = a_star_algorithm(Graph(graph, max_rate(graph.values())), start)
    return result


def phase2(v):
    return -1


def is_end_state(n):
    return n.move_count == 30


def release_rate(open_valves, graph):
    return sum([graph.valves[valve].rate for valve in open_valves])


def find_neighbours(state, graph):
    neighbours = []
    current_release_rate = release_rate(state.open_valves, graph)
    pressure_released = state.pressure_released + current_release_rate
    if state.robots not in state.open_valves:
        open_valves = state.open_valves.union({state.robots})
        next_state = State(state.robots, pressure_released, state.move_count + 1, open_valves)
        neighbours.append(next_state)

    for neighbour in graph.valves[state.robots].tunnels:
        next_state = State(neighbour, pressure_released, state.move_count + 1, state.open_valves)
        neighbours.append(next_state)

    return neighbours


def potential_remaining(open_valves, graph):
    all_valves = frozenset(graph.valves.keys())
    difference = all_valves.difference(open_valves)
    return sum([graph.valves[v].rate for v in difference])


def cost(state, graph):
    max_remaining = (30 - state.move_count) * graph.max_rate
    # max_remaining = (30 - state.move_count) * graph.max_rate
    score = state.pressure_released + max_remaining
    return -score


def a_star_algorithm(graph, start):
    open_set = {start}
    closed_set = set()
    node_scores = {start: 0}
    parents = {start: start}
    current_min = [start, 0]
    count = 0

    while len(open_set) > 0:

        n = None

        if current_min is None:
            for v in open_set:
                if n is None or node_scores[v] < node_scores[n]:
                    n = v
                    current_min = [v, node_scores[v]]
        else:
            n = current_min[0]

        if n is None:
            print('Path does not exist!')
            return None

        count += 1
        if count % 1000 == 0 or n.pressure_released > 1000:
            print(f"{node_scores[n]} {n} {len(open_set)} {len(closed_set)}")

        if is_end_state(n):
            print(n)
            return n.pressure_released

        for m in find_neighbours(n, graph):
            score = cost(m, graph)

            new_min = None
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                parents[m] = n
                node_scores[m] = score
                if score < current_min[1]:
                    new_min = [m, score]

            else:
                if node_scores[m] > score:
                    node_scores[m] = score
                    parents[m] = n

                    if score < current_min[1]:
                        new_min = [m, score]

                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)

        open_set.remove(n)
        closed_set.add(n)

        if new_min is None:
            current_min = None
        else:
            current_min = new_min

    return None


def parse(line):
    pattern = re.compile("Valve (.+) has flow rate=(.+); tunnels* leads* to valves* (.+)")
    m = pattern.match(line)
    tunnels = m.group(3).split(", ")
    return Valve(m.group(1), int(m.group(2)), tunnels)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day16_sample" if TEST_MODE else "input/day16").open() as f:
        values = [parse(i.strip()) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
