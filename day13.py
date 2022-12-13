from util import run_day
from enum import Enum


def read(input):
    with open(input) as f:
        w = f.read()
        items = w.split("\n\n")
        return [k.split("\n") for k in items]


class Decision(Enum):
    Right = 1
    Wrong = 2
    Undecided = 3


def process(ll: list, rl: list) -> Decision:
    # print(ll, rl, sep=" VS ")
    to = min(len(ll), len(rl))

    for i in range(to):
        match ll[i], rl[i]:
            case list(li), list(ri):
                d = process(li, ri)
                if d == Decision.Undecided:
                    continue
                else:
                    return d
            case int(l_nr), int(r_nr):
                # print(l_nr, r_nr, sep=" VS ")
                if l_nr < r_nr:
                    return Decision.Right
                elif l_nr > r_nr:
                    return Decision.Wrong
                else:
                    continue
            case int(l_nr), list(ri):
                # print(l_nr, ri, sep=" VS ")
                d = process([l_nr], ri)
                if d == Decision.Undecided:
                    continue
                else:
                    return d
            case list(li), int(l_nr):
                # print(li, l_nr, sep=" VS ")
                d = process(li, [l_nr])
                if d == Decision.Undecided:
                    continue
                else:
                    return d
            case wat:
                raise ValueError(wat)

    if len(ll) < len(rl):
        return Decision.Right
    elif len(ll) == len(rl):
        return Decision.Undecided
    else:
        return Decision.Wrong


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
    return -1


run_day(13, part1, part2)