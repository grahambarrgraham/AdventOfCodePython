# -*- coding: utf-8 -*-
""" generic A-Star path searching algorithm. Amended to return all paths of same cost, and yield all paths, in order of cost"""

from abc import ABC, abstractmethod
from typing import Callable, Dict, Iterable, Union, TypeVar, Generic
from math import inf as infinity

import sortedcontainers  # type: ignore

# introduce generic type
T = TypeVar("T")


################################################################################
class SearchNode(Generic[T]):
    """Representation of a search node"""

    __slots__ = ("data", "g_score", "f_score", "closed", "came_from", "in_openset")

    def __init__(
            self, data: T, g_score: float = infinity, f_score: float = infinity
    ) -> None:
        self.data = data
        self.g_score = g_score
        self.f_score = f_score
        self.closed = False
        self.in_openset = False
        self.came_from: list = []

    def __lt__(self, b: "SearchNode[T]") -> bool:
        """Natural order is based on the f_score value & is used by heapq operations"""
        return self.f_score < b.f_score


################################################################################
class SearchNodeDict(Dict[T, SearchNode[T]]):
    """A dict that returns a new SearchNode when a key is missing"""

    def __missing__(self, k) -> SearchNode[T]:
        v = SearchNode(k)
        self.__setitem__(k, v)
        return v


################################################################################
SNType = TypeVar("SNType", bound=SearchNode)


class OpenSet(Generic[SNType]):

    def __init__(self) -> None:
        self.sortedlist = sortedcontainers.SortedList(key=lambda x: x.f_score)

    def push(self, item: SNType) -> None:
        item.in_openset = True
        self.sortedlist.add(item)

    def pop(self) -> SNType:
        item = self.sortedlist.pop(0)
        item.in_openset = False
        return item

    def remove(self, item: SNType) -> None:
        self.sortedlist.remove(item)
        item.in_openset = False

    def __len__(self) -> int:
        return len(self.sortedlist)


class AStar(ABC, Generic[T]):
    __slots__ = ()

    @abstractmethod
    def heuristic_cost_estimate(self, current: T) -> float:
        """
        Computes the estimated (rough) distance between a node and the goal.
        This method must be implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def distance_between(self, n1: T, n2: T) -> float:
        """
        Gives the real distance between two adjacent nodes n1 and n2 (i.e n2
        belongs to the list of n1's neighbors).
        n2 is guaranteed to belong to the list returned by the call to neighbors(n1).
        This method must be implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def neighbors(self, node: T) -> Iterable[T]:
        """
        For a given node, returns (or yields) the list of its neighbors.
        This method must be implemented in a subclass.
        """
        raise NotImplementedError

    def is_goal_reached(self, current: T) -> bool:
        """
        Returns true when we can consider that 'current' is the goal.
        """
        raise NotImplementedError

    @staticmethod
    def reconstruct_paths(last: SearchNode) -> Union[Iterable[T], None]:
        """
        Returns all paths that have the same end score, along with the score
        """
        queue = [[last]]
        while len(queue) > 0:
            current = queue.pop()
            parents = current[0].came_from

            if len(parents) == 0:
                yield [i.data for i in reversed(current)], last.g_score
                continue

            for parent in parents:
                queue.append([parent] + current)

        return None

    def astar(self, start: T) -> Union[Iterable[T], None]:
        if self.is_goal_reached(start):
            return [start]

        open_set: OpenSet[SearchNode[T]] = OpenSet()
        search_nodes: SearchNodeDict = SearchNodeDict()
        start_node = search_nodes[start] = SearchNode(
            start, g_score=0.0, f_score=self.heuristic_cost_estimate(start)
        )
        open_set.push(start_node)

        while open_set:
            current = open_set.pop()

            if self.is_goal_reached(current.data):
                yield self.reconstruct_paths(current)

            current.closed = True

            for neighbor in map(lambda n: search_nodes[n], self.neighbors(current.data)):
                if neighbor.closed:
                    continue

                tentative_g_score = current.g_score + self.distance_between(
                    current.data, neighbor.data
                )

                if tentative_g_score > neighbor.g_score:
                    continue

                neighbor_from_openset = neighbor.in_openset

                if neighbor_from_openset:
                    # we have to remove the item from the heap, as its score has changed
                    open_set.remove(neighbor)

                # update the node
                neighbor.came_from.append(current)
                neighbor.g_score = tentative_g_score
                neighbor.f_score = tentative_g_score + self.heuristic_cost_estimate(neighbor.data)

                open_set.push(neighbor)

        return None


################################################################################
U = TypeVar("U")


def find_path(
        start: U,
        neighbors_fun: Callable[[U], Iterable[U]],
        is_goal_reached_fun: Callable[[U], bool],
        heuristic_cost_estimate_fun: Callable[[U], float] = lambda a: infinity,
        edge_cost_fun: Callable[[U, U], float] = lambda a, b: 1.0
) -> Union[Iterable[U], None]:
    """A non-class version of the path finding algorithm. Returns a generator of lists of paths, starting from the
    lowest cost paths, then increasing.  Set heuristic_cost_estimate_fun to return makes turns this algorithm to dykstra.
    Remember to ensure any heuristic_cost_estimate_fun that you do set is admissible to ensure the shortest path, although
    using an inadmissible function can sometimes produce fast results"""

    class FindPath(AStar):
        def heuristic_cost_estimate(self, current: U) -> float:
            return heuristic_cost_estimate_fun(current)  # type: ignore

        def distance_between(self, n1: U, n2: U) -> float:
            return edge_cost_fun(n1, n2)

        def neighbors(self, node) -> Iterable[U]:
            return neighbors_fun(node)  # type: ignore

        def is_goal_reached(self, current: U) -> bool:
            return is_goal_reached_fun(current)

    return FindPath().astar(start)


__all__ = ["AStar", "find_path"]
