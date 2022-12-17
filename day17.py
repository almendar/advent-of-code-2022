from dataclasses import dataclass, field
from typing import NamedTuple, Tuple, List
from itertools import cycle
from functools import reduce
from util import run_day

# fmt: off
pieces = [
    [
        [1, 1, 1, 1]
    ],
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 1]
    ],
    [
        [1],
        [1],
        [1],
        [1]
    ],
    [
        [1, 1],
        [1, 1]
    ]
]
# fmt: on


class Coord(NamedTuple):
    x: int
    y: int


@dataclass()
class Rock:
    shape: list[list[int]]
    left_top: Coord

    points: frozenset[Coord] = field(init=False)
    smashed_into_wall: bool = field(init=False)
    ground_level: bool = field(init=False)

    def __post_init__(self):
        acc = []
        self.smashed_into_wall = False
        self.ground_level = False
        for yi, row in enumerate(self.shape):
            for xi, cell_val in enumerate(row):
                new_x = self.left_top.x + xi
                new_y = self.left_top.y - yi
                if cell_val == 1:
                    acc.append(Coord(new_x, new_y))
                if new_x == 0 or new_x == 8:
                    self.smashed_into_wall = True
                if new_y == 0:
                    self.ground_level = True
        self.points = frozenset(acc)

    def move(self, dx: int, dy: int) -> "Rock":
        return Rock(self.shape, Coord(self.left_top.x + dx, self.left_top.y + dy))

    def collision(self, other: "Rock") -> bool:
        return len(self.points & other.points) != 0

    def gas_blow(self, cave: "Cave", wind: str):
        moved = None
        if wind == ">":
            moved = self.move(1, 0)
        elif wind == "<":
            moved = self.move(-1, 0)
        else:
            raise ValueError(f"wind broken {wind}")

        if moved.smashed_into_wall or cave.collides(moved):
            return self
        else:
            return moved


class Cave:
    def __init__(self, rocks: list[Rock]) -> None:
        if rocks == None:
            rocks = []
        self.rocks: list[Rock] = rocks
        self.current_top = 0

    def print_cave_with_rock(self, maybeRock):
        newRocks = self.rocks[:]
        maybeCave = Cave(rocks=newRocks)
        maybeCave.add(maybeRock)
        maybeCave.print()

    def collides(self, rock: Rock):
        return any(map(lambda x: x.collision(rock), self.rocks))

    def add(self, rock: Rock):
        self.rocks.append(rock)
        self.rocks.sort(key=lambda x: -x.left_top.y)
        self.current_top = self.rocks[0].left_top.y

    def print(self) -> str:
        all_points = reduce(
            lambda x, y: x | y, map(lambda x: x.points, self.rocks), set()
        )

        # max_x = max(map(lambda it: it.x, all_points))
        max_y = self.current_top
        print("\n")
        for yi in range(max_y, -1, -1):
            for xi in range(0, 9):
                if (xi, yi) in all_points:
                    print("#", end="")
                elif yi == 0:
                    print("-", end="")
                elif xi == 0 or xi == 8:
                    print("|", end="")
                else:
                    print(".", end="")
            print("")


@dataclass
class Wind:
    pattern: str
    wind: int = field(default=-1)

    def next_wind(self):
        self.wind = (self.wind + 1) % len(self.pattern)
        k = self.pattern[self.wind]
        # print("!!!:", k)
        return k

    def backtrace(self):
        self.wind -= 1


def part1(input):
    with open(input) as f:
        winds = next(f)
        cave = Cave([])
        wind = Wind(winds)
        for i, next_piece in enumerate(cycle(pieces)):
            if i == 2022:
                break
            rock = Rock(next_piece, Coord(3, cave.current_top + 3 + len(next_piece)))
            # print("new-start", cave.current_top)
            # cave.print_cave_with_rock(rock)

            rock = rock.gas_blow(cave, wind.next_wind())

            while True:
                rock = rock.move(0, -1)
                if rock.ground_level or cave.collides(rock):
                    # found our place, backtrace
                    cave.add(rock.move(0, 1))
                    break
                else:
                    rock = rock.gas_blow(cave, wind.next_wind())
        return cave.current_top


def part2(input):
    return -1


run_day(17, part1, part2)
