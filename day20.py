from dataclasses import dataclass, field
from typing import Callable
from util import day_data


@dataclass
class Node:
    value: int
    prev: "Node" = field(init=False)
    next: "Node" = field(init=False)
    original_next: "Node" = field(init=False)
    sentinel: bool = field(default=False)

    def __post_init__(self):
        self.prev = self
        self.next = self
        self.original_next = self

    def create(self, val: int) -> "Node":
        n = Node(val)
        curr_next = self.next
        curr_next.prev = n
        self.next = n
        self.original_next = n
        n.prev = self
        n.next = curr_next
        n.original_next = curr_next
        return n

    def nth(self, n: int) -> "Node":
        iter = self
        while n > 0:
            iter = iter.next
            if iter.sentinel:
                iter = iter.next
            n -= 1
        return iter

    def attach_after(self, n: "Node") -> "Node":
        curr_next = self.next
        curr_next.prev = n
        self.next = n
        n.prev = self
        n.next = curr_next
        return n

    def attach_before(self, n: "Node") -> "Node":
        curr_prev = self.prev
        curr_prev.next = n
        self.prev = n
        n.next = self
        n.prev = curr_prev
        return n

    def deattach(self) -> "Node":
        if self.sentinel:
            raise ValueError("deattach of sentinel")
        prev, next = self.prev, self.next
        prev.next = next
        next.prev = prev
        return self

    def move(self, delta: int):
        # print("moving", self.value)
        deattach = self

        op = None
        if delta == 0:
            return self
        elif delta > 0:
            op = lambda x: x.next
        elif delta < 0:
            op = lambda x: x.prev

        cnt = abs(delta)
        wheere_to_attach = self
        while cnt > 0:
            wheere_to_attach = op(wheere_to_attach)
            if wheere_to_attach.sentinel:
                wheere_to_attach = op(wheere_to_attach)
            cnt -= 1

        if deattach == wheere_to_attach:
            return

        deattach.deattach()
        if delta > 0:
            wheere_to_attach.attach_after(deattach)
            if wheere_to_attach.next.sentinel:
                wheere_to_attach = wheere_to_attach.next
        elif delta < 0:
            if wheere_to_attach.prev.sentinel:
                wheere_to_attach = wheere_to_attach.prev
            wheere_to_attach.attach_before(deattach)

    def __repr__(self) -> str:
        if self.sentinel:
            return "#"
        else:
            return str(self.value)


@dataclass
class Chain:
    sentinel: Node

    def append(self, value: int) -> "Node":
        return self.sentinel.prev.create(value)

    def print(self):
        acc = []
        node = self.sentinel.next
        while not node.sentinel:
            acc.append(node.value)
            node = node.next
        print(acc)


numbers = range(1, 14)


def parse_input():
    pass


def part1(input):
    numbers = []
    with open(input) as f:
        numbers = [int(i.strip()) for i in f]

    # numbers = [1, 2, -3, 3, -2, 0, 4]
    sentinel = Node(0, True)
    chain = Chain(sentinel)

    for i in numbers:
        chain.append(i)

    iter = sentinel.original_next
    while not iter.sentinel:
        # chain.print()
        iter.move(iter.value)
        iter = iter.original_next

    # chain.print()
    iter = sentinel.next
    while not iter.sentinel and iter.value != 0:
        iter = iter.next

    n_1000 = iter.nth(1000).value
    n_2000 = iter.nth(2000).value
    n_3000 = iter.nth(3000).value
    return n_1000 + n_2000 + n_3000


sample_txt, input_txt = day_data(20)

print(part1(sample_txt))
print(part1(input_txt))
