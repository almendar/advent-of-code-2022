from abc import ABC, abstractmethod
from dataclasses import dataclass
from operator import add, floordiv, mul, sub
from typing import Callable, Dict, cast

from util import run_day, read_lines


Op = Callable[[int, int], int]


op_map = {"+": add, "-": sub, "*": mul, "/": floordiv}
op_reversed = {"+": sub, "-": add, "*": floordiv, "/": mul}


class Monkey(ABC):
    @abstractmethod
    def shout(self) -> int:
        pass


@dataclass
class NumberMonkey(Monkey):
    name: str
    number: int

    def shout(self) -> int:
        return self.number


@dataclass
class OpMonkey(Monkey):
    name: str
    l: str
    r: str
    op: str
    ms: "MonkeyShow"

    def shout(self) -> int:
        l_m = self.ms.monkeys[self.l]
        r_m = self.ms.monkeys[self.r]
        op = op_map[self.op]
        return op(l_m.shout(), r_m.shout())


class MonkeyShow:

    HUMN = "humn"

    def __init__(self, input: str):
        self.monkeys: Dict[str, Monkey] = {}
        lines = read_lines(input)
        for l in lines:
            self.parse_line(l.strip())

    def parse_line(self, line: str):
        items = line.split(" ")
        monkey_name = items[0][:-1]
        if len(items) == 2:
            monkey_number = int(items[1])
            self.monkeys[monkey_name] = NumberMonkey(monkey_name, monkey_number)
        else:
            left_name = items[1]
            right_name = items[3]
            operator_name = items[2]
            self.monkeys[monkey_name] = OpMonkey(
                monkey_name, left_name, right_name, operator_name, self
            )

    def contains_monkey(self, searchedName: str, monkey: Monkey) -> bool:
        match monkey:
            case OpMonkey(name, l, r, _):
                if name == searchedName:
                    return True
                else:
                    return self.contains_monkey(
                        searchedName, self.monkeys[l]
                    ) or self.contains_monkey(searchedName, self.monkeys[r])
            case NumberMonkey(name, _):
                if name == searchedName:
                    return True
                else:
                    return False

        raise ValueError

    def solve(self, m: Monkey, expectedValue: int) -> int:
        match m:
            case OpMonkey(_, left, right, op):
                left_contains = self.contains_monkey(self.HUMN, self.monkeys[left])
                right_contains = self.contains_monkey(self.HUMN, self.monkeys[right])
                if right_contains and left_contains:
                    raise ValueError("Assumption does not hold")

                if left_contains:
                    right_value = self.monkeys[right].shout()
                    left_must_be = op_reversed[op](expectedValue, right_value)
                    return self.solve(self.monkeys[left], left_must_be)
                elif right_contains:
                    left_valie = self.monkeys[left].shout()
                    right_must_be = 0
                    match op:
                        case "+" | "*":
                            right_must_be = op_reversed[op](expectedValue, left_valie)

                        case "-" | "/":
                            right_must_be = op_map[op](left_valie, expectedValue)
                        case _:
                            raise ValueError("upps")
                    return self.solve(self.monkeys[right], right_must_be)
                else:
                    raise ValueError
            case NumberMonkey("humn", _):
                return expectedValue
            case _:
                raise ValueError


def part1(input):
    monkey_show = MonkeyShow(input)
    return monkey_show.monkeys["root"].shout()


def part2(input):
    monkey_show = MonkeyShow(input)
    root_monkey = cast(OpMonkey, monkey_show.monkeys["root"])
    me_monkey = cast(NumberMonkey, monkey_show.monkeys[MonkeyShow.HUMN])
    left = root_monkey.l
    right = root_monkey.r

    m_left = monkey_show.monkeys[left]
    m_right = monkey_show.monkeys[right]

    my_sub_tree, not_my_subtree = (
        (m_left, m_right)
        if monkey_show.contains_monkey(MonkeyShow.HUMN, m_left)
        else (m_right, m_left)
    )

    result = monkey_show.solve(my_sub_tree, not_my_subtree.shout())
    me_monkey.number = result
    assert m_right.shout() == m_left.shout()
    return result


if __name__ == "__main__":
    run_day(21, part1, part2)
