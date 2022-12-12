from dataclasses import dataclass, field
from typing import Callable
from collections import deque, Counter

Op = Callable[[int], int]


@dataclass
class Jungle:
    monkey_items: list[deque[int]]
    monkey_behaviour: list[Op]
    monkey_divs: list[int]
    passTo: list[tuple[int, int]]  # true, false
    reduce_level: Callable[[int], int]
    inspections: Counter[int] = field(default_factory=Counter)

    def monkey_business(self) -> int:
        moves = list(self.inspections.values())
        moves.sort(reverse=True)
        [first, second] = moves[0:2]
        return first * second

    def move_round(self):
        for m in range(0, len(self.monkey_items)):
            while len(self.monkey_items[m]) > 0:
                self.one_move(m)

    def one_move(self, monkey_number):
        self.inspections[monkey_number] += 1
        inspected_item = self.monkey_items[monkey_number].popleft()
        new_worry_leve = self.monkey_behaviour[monkey_number](inspected_item)
        worry_level_reduced = self.reduce_level(new_worry_leve)
        test = self.monkey_divs[monkey_number]
        test_outcome = 0 if worry_level_reduced % test == 0 else 1
        pass_to_monkey = self.passTo[monkey_number][test_outcome]
        self.monkey_items[pass_to_monkey].append(worry_level_reduced)


def build_sample_jungle(stress_relief):
    return Jungle(
        [deque([79, 98]), deque([54, 65, 75, 74]), deque([79, 60, 97]), deque([74])],
        [lambda x: x * 19, lambda x: x + 6, lambda x: x * x, lambda x: x + 3],
        [23, 19, 13, 17],
        [(2, 3), (2, 0), (1, 3), (0, 1)],
        stress_relief,
    )


def buikd_input_junge(stress_relief):
    return Jungle(
        [
            deque([57, 58]),
            deque([66, 52, 59, 79, 94, 73]),
            deque([80]),
            deque([82, 81, 68, 66, 71, 83, 75, 97]),
            deque([55, 52, 67, 70, 69, 94, 90]),
            deque([69, 85, 89, 91]),
            deque([75, 53, 73, 52, 75]),
            deque([94, 60, 79]),
        ],
        [
            lambda x: x * 19,
            lambda x: x + 1,
            lambda x: x + 6,
            lambda x: x + 5,
            lambda x: x * x,
            lambda x: x + 7,
            lambda x: x * 7,
            lambda x: x + 2,
        ],
        [7, 19, 5, 11, 17, 13, 2, 3],
        [(2, 3), (4, 6), (7, 5), (5, 2), (0, 3), (1, 7), (0, 4), (1, 6)],
        stress_relief,
    )


def part1():
    sample_jungle = build_sample_jungle(lambda x: x // 3)
    input_jungle = buikd_input_junge(lambda x: x // 3)
    for _ in range(0, 20):
        sample_jungle.move_round()
        input_jungle.move_round()

    print(sample_jungle.monkey_business())
    print(input_jungle.monkey_business())


def part2():
    from functools import reduce

    sample_jungle = build_sample_jungle(lambda x: x)
    input_jungle = buikd_input_junge(lambda x: x)

    sample_jungle.reduce_level = lambda x: x % reduce(
        lambda x, y: x * y, sample_jungle.monkey_divs, 1
    )
    input_jungle.reduce_level = lambda x: x % reduce(
        lambda x, y: x * y, input_jungle.monkey_divs, 1
    )
    for _ in range(0, 10000):
        sample_jungle.move_round()
        input_jungle.move_round()

    print(sample_jungle.monkey_business())
    print(input_jungle.monkey_business())


part1()
part2()
