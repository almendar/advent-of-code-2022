from dataclasses import dataclass, field
from typing import Callable
from util import run_day


@dataclass
class Node:
    value: int
    prev: "Node" = field(init=False)
    next: "Node" = field(init=False)
    original_next: "Node" = field(init=False)

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
            n -= 1
        return iter

    def attach_after(self, n: "Node"):
        curr_next = self.next
        curr_next.prev = n
        self.next = n
        n.prev = self
        n.next = curr_next
        return n

    def attach_before(self, n: "Node"):
        curr_prev = self.prev
        curr_prev.next = n
        self.prev = n
        n.next = self
        n.prev = curr_prev
        return n

    def deattach(self):
        prev, next = self.prev, self.next
        prev.next = next
        next.prev = prev

    def move(self, delta: int):
        deattach = self
        op = None
        if delta == 0:
            return self
        elif delta > 0:
            op = lambda x: x.next
        elif delta < 0:
            op = lambda x: x.prev

        deattach.deattach()
        cnt = abs(delta)
        wheere_to_attach = self
        while cnt > 0:
            wheere_to_attach = op(wheere_to_attach)
            cnt -= 1

        if delta > 0:
            wheere_to_attach.attach_after(deattach)
        elif delta < 0:
            wheere_to_attach.attach_before(deattach)

    def print_chain(self):
        acc = []
        acc.append(self.value)
        node = self.next
        while not node == self:
            acc.append(node.value)
            node = node.next
        print(acc)

    def __repr__(self) -> str:
        return str(self.value)


def part1(input):
    numbers = []
    with open(input) as f:
        numbers = [int(i.strip()) for i in f]

    head = Node(numbers[0])
    last = head
    for i in numbers[1:]:
        last = last.create(i)

    head.move(head.value)
    iter = head.original_next
    while iter != head:
        iter.move(iter.value)
        iter = iter.original_next

    iter = head
    while iter.value != 0:
        iter = iter.next

    n_1000 = iter.nth(1000).value
    n_2000 = iter.nth(2000).value
    n_3000 = iter.nth(3000).value
    return n_1000 + n_2000 + n_3000


def reduce_delta(steps, list_length):
    if steps == 0:
        return steps
    if steps > (list_length - 1):
        steps = steps % (list_length - 1)

    if steps < 0:
        step_abs = abs(steps)
        if step_abs > (list_length - 1):
            step_abs = step_abs % (list_length - 1)
        steps = list_length - 1 - step_abs

    return steps


def part2(input):
    MULTIPLY = 811589153

    numbers = []
    with open(input) as f:
        numbers = [int(i.strip()) for i in f]

    head = Node(numbers[0] * MULTIPLY)
    last = head
    for i in numbers[1:]:
        last = last.create(i * MULTIPLY)

    list_length = len(numbers)

    for k in range(10):
        steps = reduce_delta(head.value, list_length)
        head.move(steps)
        iter = head.original_next
        while iter != head:
            steps = reduce_delta(iter.value, list_length)
            iter.move(steps)
            iter = iter.original_next

    iter = head
    while iter.value != 0:
        iter = iter.next
    n_1000 = iter.nth(1000).value
    n_2000 = iter.nth(2000).value
    n_3000 = iter.nth(3000).value
    return n_1000 + n_2000 + n_3000


# sample_txt, input_txt = day_data(20)

run_day(20, part1, part2)
# print(part1(sample_txt))  # 3
# print(part1(input_txt))  # 8721
# print(part2(sample_txt))  # 1623178306
# print(part2(input_txt))  # 831878881825
