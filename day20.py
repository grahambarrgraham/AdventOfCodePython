from pathlib import Path

TEST_MODE = False


def phase1(v):
    return calc(v, 1, 1)


def phase2(v):
    return calc(v, 10, 811589153)


def calc(v, iterations, multiplier):
    l = CircularLinkedList()
    nodes = [Node(n * multiplier) for n in v]
    zero = [n for n in nodes if n.data == 0][0]

    for n in nodes:
        l.insert_at_end(n)

    for i in range(iterations):
        for n in nodes:
            l.move(n, n.data)

    coordinates = [l.find(zero, i, 0).data for i in (1000, 2000, 3000)]
    return sum(coordinates)


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"{self.data} : [{self.prev.data}, {self.next.data}]"


class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert_empty(self, new_node):
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
            self.size += 1
        else:
            print("List is not empty.")

    def insert_at_end(self, new_node):
        if self.head is None:
            self.insert_empty(new_node)
        else:
            last_node = self.head.prev
            last_node.next = new_node
            new_node.prev = last_node
            new_node.next = self.head
            self.head.prev = new_node
            self.size += 1

    def find(self, node, places, adjust=-1):
        places_to_move = places % (self.size + adjust)
        if self.head is None or places_to_move == 0:
            return node
        result = node
        for i in range(places_to_move):
            result = result.next
        return result

    def move(self, node_to_move, places):
        insert_at = self.find(node_to_move, places)
        if insert_at == node_to_move:
            return

        node_to_move.prev.next = node_to_move.next
        node_to_move.next.prev = node_to_move.prev

        node_to_move.prev = insert_at
        node_to_move.next = insert_at.next

        insert_at.next.prev = node_to_move
        insert_at.next = node_to_move

    def traverse(self):
        if self.head is None:
            print("List is empty.")
        else:
            curr_node = self.head
            while curr_node.next != self.head:
                print(curr_node.data, end=' ')
                curr_node = curr_node.next
            print(curr_node.data)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day20_sample" if TEST_MODE else "input/day20").open() as f:
        values = [int(i) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
