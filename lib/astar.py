def a_star_algorithm(graph, start, stop_func, find_neighbours, cost):
    open_set = {start}
    closed_set = set()
    node_scores = {start: 0}
    parents = {start: start}

    while len(open_set) > 0:
        n = None

        for v in open_set:
            if n is None or node_scores[v] < node_scores[n]:
                n = v

        if n is None:
            print('Path does not exist!')
            return None

        if stop_func(n):
            return n

        for m in find_neighbours(n, graph):
            weight = cost(m, graph)
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                parents[m] = n
                node_scores[m] = node_scores[n] + weight

            else:
                if node_scores[m] > node_scores[n] + weight:
                    node_scores[m] = node_scores[n] + weight
                    parents[m] = n

                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)

        open_set.remove(n)
        closed_set.add(n)

    return None