from util import run_day
from dataclasses import dataclass
from typing import NamedTuple, Set, List, Dict, List
from enum import Enum
from collections import deque, defaultdict


def read_lines(input) -> List[str]:
    with open(input) as f:
        return [l.strip() for l in f.readlines()]


class Coord(NamedTuple):
    x: int
    y: int

    def move(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


def build_elf_positions(lines: List[str]) -> Set[Coord]:
    return set(
        [
            Coord(x, y)
            for y, row in enumerate(lines)
            for x, ch in enumerate(row)
            if ch == "#"
        ]
    )


E = Coord(1, 0)
W = Coord(-1, 0)
S = Coord(0, 1)
N = Coord(0, -1)
NE = Coord(1, -1)
NW = Coord(-1, -1)
SE = Coord(1, 1)
SW = Coord(-1, 1)

ALL_DIRECTIONS: List[Coord] = [E, W, S, N, NE, NW, SE, SW]


class Garden:
    def __init__(self, lines: List[str]):
        self.positions: Set[Coord] = build_elf_positions(lines)
        self.directions = deque([N, S, W, E])

    def _can_move(self, pos: Coord, dirs: Set[Coord]) -> bool:
        return not any([(pos.move(dir)) in self.positions for dir in dirs])

    def has_neighbour(self, elf):
        return any([(elf.move(dir)) in self.positions for dir in ALL_DIRECTIONS])

    def can_move_N(self, pos: Coord) -> bool:
        return self._can_move(pos, set([N, NE, NW]))

    def can_move_S(self, pos: Coord) -> bool:
        return self._can_move(pos, set([S, SE, SW]))

    def can_move_W(self, pos: Coord) -> bool:
        return self._can_move(pos, set([W, NW, SW]))

    def can_move_E(self, pos: Coord) -> bool:
        return self._can_move(pos, set([E, NE, SE]))

    def print(self):
        xs = [p.x for p in self.positions]
        ys = [p.x for p in self.positions]
        max_x, min_x = max(xs), min(xs)
        max_y, min_y = max(ys), min(ys)

        for y in range(min_y - 3, max_y + 3):
            for x in range(min_x - 3, max_x + 3):
                if (x, y) in self.positions:
                    print("#", end="")
                else:
                    print(".", end="")
            print()
        print()

    def round(self) -> bool:
        pos_before = len(self.positions)
        result = False
        all_proposals: Dict[Coord, List[Coord]] = defaultdict(list)
        for pos in self.positions:
            if self.has_neighbour(pos):
                found = False
                for dir in self.directions:
                    if dir == N and self.can_move_N(pos):
                        all_proposals[pos.move(N)].append(pos)
                        found = True
                        break

                    elif dir == S and self.can_move_S(pos):
                        all_proposals[pos.move(S)].append(pos)
                        found = True
                        break

                    elif dir == E and self.can_move_E(pos):
                        all_proposals[pos.move(E)].append(pos)
                        found = True
                        break

                    elif dir == W and self.can_move_W(pos):
                        all_proposals[pos.move(W)].append(pos)
                        found = True
                        break

                if not found:
                    all_proposals[pos].append(pos)
            else:
                all_proposals[pos].append(pos)

        new = set()
        for new_pos, elf_that_proposed_this in all_proposals.items():
            if len(elf_that_proposed_this) == 1:
                new.add(new_pos)
                if new_pos != elf_that_proposed_this[0]:
                    result = True
            else:
                new.update(elf_that_proposed_this)
                result = True

        self.positions = new
        self.directions.append(self.directions.popleft())
        assert pos_before == len(self.positions)
        return result


def part1(input: str):

    lines = read_lines(input)
    G = Garden(lines)

    for _ in range(10):
        G.round()

    xs = [p.x for p in G.positions]
    ys = [p.x for p in G.positions]
    dx = max(xs) - min(xs) + 1
    dy = max(ys) - min(ys)  # why no adding +1 here?!

    return dx * dy - len(set(G.positions))


def part2(input):
    acc = 0
    lines = read_lines(input)
    G = Garden(lines)
    while G.round():
        acc += 1
    # becuase first not moved, not last moved
    return acc + 1


if __name__ == "__main__":
    run_day(23, part1, part2)
