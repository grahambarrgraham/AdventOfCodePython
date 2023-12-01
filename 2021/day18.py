import copy
import functools
import itertools
import math
from pathlib import Path
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    current = functools.reduce(lambda a, b: reduce(plus_nodes(a, b)), v)
    return current.magnitude()


def phase2(v):
    permutations = list(itertools.permutations(v, 2))
    return max([reduce(copy.deepcopy(plus_nodes(a, b))).magnitude() for a, b in permutations])


def plus_nodes(a, b):
    resp = Node(None)
    resp.left = a
    resp.right = b
    resp.left.parent = resp
    resp.right.parent = resp
    return resp


def reduce(root):
    while True:
        n = explode(root)
        if n is not None:
            continue
        if split(root) is not None:
            continue
        break
    return root


def parse(s):
    def parse_inner(s, parent):
        n = Node(parent)
        left = True

        while True:
            c = next(s)
            if c == '[':
                if left:
                    n.left = parse_inner(s, n)
                else:
                    n.right = parse_inner(s, n)
            elif c == ',':
                left = False
            elif c == ']':
                return n
            else:
                if left:
                    n.left = int(c)
                else:
                    n.right = int(c)

    i = iter(s)
    next(i)
    return parse_inner(i, None)


class Node:
    def __init__(self, parent):
        self.left = None
        self.right = None
        self.parent = parent

    def magnitude(self):
        mag_left = 3 * (self.left if type(self.left) is int else self.left.magnitude())
        mag_right = 2 * (self.right if type(self.right) is int else self.right.magnitude())
        return mag_left + mag_right

    def level(self):
        return 0 if self.parent is None else 1 + self.parent.level()

    def find_leftmost(self, matches):
        exploder = None
        if type(self.left) is Node:
            exploder = self.left.find_leftmost(matches)
        if exploder is None and matches(self):
            return self
        if exploder is None and type(self.right) is Node:
            exploder = self.right.find_leftmost(matches)
        return exploder

    def find_exploder(self):
        def func(node):
            return node.level() == 4
        return self.find_leftmost(func)

    def find_splitter(self):
        def func(node):
            return (Node.is_splittable(node.left)) or (Node.is_splittable(node.right))

        return self.find_leftmost(func)

    def split(self):
        if self.is_splittable(self.left):
            split_value = self.left
            self.left = Node(self)
            self.left = Node(self)
            self.left.left = math.floor(split_value / 2)
            self.left.right = math.ceil(split_value / 2)
            return self
        if self.is_splittable(self.right):
            split_value = self.right
            self.right = Node(self)
            self.right.left = math.floor(split_value / 2)
            self.right.right = math.ceil(split_value / 2)
            return self
        return None

    @staticmethod
    def is_splittable(node_item):
        item_ = type(node_item) is int and node_item > 9
        return item_

    def find_nearest(self, is_left):

        if self.parent is None:
            return None

        a, b = self.parent.traverse_order(is_left)

        if self == a and type(b) is int:
            return self.parent
        if self == a and type(b) is Node:
            down = b.find_nearest_down(is_left)
            return down
        else:
            nearest = self.parent.find_nearest(is_left)
            return nearest

    def traverse_order(self, is_left):
        return (self.right, self.left) if is_left else (self.left, self.right)

    def find_nearest_down(self, is_left):
        a, b = self.traverse_order(is_left)
        if type(a) is int:
            return self
        resp = a.find_nearest_down(is_left)
        if resp is None:
            if type(b) is int:
                return self
            else:
                return b.find_nearest_down(is_left)
        else:
            return resp


def split(root):
    node = root.find_splitter()
    if node is not None:
        return node.split()


def explode(root):
    node = root.find_exploder()
    if node is None:
        return None
    left_node = node.find_nearest(True)
    right_node = node.find_nearest(False)
    if left_node is not None:
        if type(left_node.right) is int:
            left_node.right += node.left
        else:
            left_node.left += node.left
    if right_node is not None:
        if type(right_node.left) is int:
            right_node.left += node.right
        else:
            right_node.right += node.right
    if node.parent.left == node:
        node.parent.left = 0
    else:
        node.parent.right = 0
    return root, node, left_node, right_node


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day18_sample" if TEST_MODE else "input/day18").open() as f:
        values = [parse(i.strip()) for i in f]
        print(f'Phase 1: {phase1(copy.deepcopy(values))}')
        print(f'Phase 2: {phase2(copy.deepcopy(values))}')
