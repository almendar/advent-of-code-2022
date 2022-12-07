from util import run_day
from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    count: int
    begin: int
    end: int


Stacks = list[list[str]]


def parse_move(m: str) -> Move:
    splited = m.split(" ")
    return Move(int(splited[1]), int(splited[3]), int(splited[5]))


def make_move9000(move: Move, stacks: Stacks):
    for _ in range(0, move.count):
        to_move = stacks[move.begin - 1].pop()
        stacks[move.end - 1].append(to_move)


def make_move9001(move: Move, stacks: Stacks):
    to_move = stacks[move.begin - 1][-move.count :]
    stacks[move.begin - 1] = stacks[move.begin - 1][: -move.count]
    stacks[move.end - 1] += to_move


def read_tops(stacks: Stacks) -> str:
    acc = ""
    for s in stacks:
        acc += s.pop()
    return acc





def parse(input):
    with open(input) as content:
        lines = content.readlines()
        split = lines.index("\n")
        cargo = lines[:split]
        moves = lines[split + 1 :]


        number_of_stacks = max(map(int, filter(None, cargo[-1].strip().split(" ") ))  )
        cargo.pop()
        cargo.reverse()
        stacks: Stacks = [[] for i in range(0, number_of_stacks)]
        for c in cargo:
            for i in range(0, number_of_stacks):
                ch = c[1 + 4 * i]
                if ch != " ":
                    stacks[i].append(ch)
        return stacks, moves


def part1(input):
    stacks, moves = parse(input)
    for m in moves:
        move = parse_move(m)
        make_move9000(move, stacks)
    return read_tops(stacks)


def part2(input):
    stacks, moves = parse(input)
    for m in moves:
        move = parse_move(m)
        make_move9001(move, stacks)
    return read_tops(stacks)


if __name__ == "__main__":
    run_day(5, part1, part2)
