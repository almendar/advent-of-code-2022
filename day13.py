from util import run_day
from enum import IntEnum
from functools import cmp_to_key


def read(input):
    with open(input) as f:
        w = f.read()
        items = w.split("\n\n")
        return [k.split("\n") for k in items]


class Decision(IntEnum):
    Wrong = -1
    Undecided = 0
    Right = 1

    @staticmethod
    def from_int(a: int) -> "Decision":
        if a < 0:
            return Decision.Right
        elif a > 0:
            return Decision.Wrong
        else:
            return Decision.Undecided


def process(ll: list, rl: list) -> Decision:
    to = min(len(ll), len(rl))
    for i in range(to):
        decision = Decision.Undecided

        match ll[i], rl[i]:
            case int(l_nr), int(r_nr):
                decision = Decision.from_int(l_nr - r_nr)
            case list(li), list(ri):
                decision = process(li, ri)
            case int(l_nr), list(ri):
                decision = process([l_nr], ri)
            case list(li), int(l_nr):
                decision = process(li, [l_nr])

        if decision != Decision.Undecided:
            return decision

    return Decision.from_int(len(ll) - len(rl))


def part1(input):
    inputs = read(input)
    indices = []
    for ix, (lStr, rStr) in enumerate(inputs, 1):
        l = eval(lStr)
        r = eval(rStr)
        res = process(l, r)
        if res == Decision.Right:
            indices.append(ix)
    return sum(indices)


def part2(input):
    inputs = read(input)
    acc = [
        eval("[[2]]"),
        eval("[[6]]"),
    ]

    for lStr, rStr in inputs:
        l = eval(lStr)
        r = eval(rStr)
        acc.append(l)
        acc.append(r)

    def cmp(l, r):
        return process(l, r).value

    acc.sort(key=cmp_to_key(cmp))

    i1 = acc.index([[2]]) + 1
    i2 = acc.index([[6]]) + 1
    return i1 * i2


run_day(13, part1, part2)

# day13-part1-sample: 13
# day13-part1-input: 5196
# day13-part2-sample: 140
# day13-part1-input: 22134
