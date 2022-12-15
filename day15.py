from typing import NamedTuple, FrozenSet, Dict, NewType, Tuple, Set
from dataclasses import dataclass, field

sample_txt = "input/day15-sample.txt"
input_txtx = "input/day15-input.txt"


class Coord(NamedTuple):
    x: int
    y: int


def manhattan(p1: Coord, p2: Coord) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


@dataclass
class Sensor:
    loc: Coord
    beacon: Coord
    max_reach: int = field(init=False)

    def __post_init__(self):
        self.max_reach = manhattan(self.loc, self.beacon)

    def covers(self, c: Coord) -> bool:
        return manhattan(self.loc, c) <= self.max_reach


def parse_line(l):
    _, _, sx, sy, _, _, _, _, bx, by = l.split(" ")
    sx = int(sx[:-1].split("=")[1])
    sy = int(sy[:-1].split("=")[1])
    bx = int(bx[:-1].split("=")[1])
    by = int(by.split("=")[1])
    return Coord(sx, sy), Coord(bx, by)


def read_input(path):
    with open(path) as f:
        return [parse_line(l) for l in f]


def coverage_at_y(s: Sensor, y: int):
    loc = s.loc
    from_y = abs(y - loc.y)
    if from_y > s.max_reach:
        return set()
    x_ray = s.max_reach - from_y
    return {(i, y) for i in range(loc.x - x_ray, loc.x + x_ray + 1)}


def part1(input, y_pos):
    input_data = read_input(input)
    trtrt = set()
    for ft in input_data:
        s, b = ft
        trtrt |= coverage_at_y(Sensor(s, b), y_pos)
        if b.y == y_pos:
            trtrt.remove(b)
    return len(trtrt)


def part2(input):
    pass
    # input_data = read_input(input)
    # trtrt = set()
    # for ft in input_data:
    #     s, b = ft
    #     trtrt |= coverage_at_y(Sensor(s, b), y_pos)
    #     if b.y == y_pos:
    #         trtrt.remove(b)


print(part1(sample_txt, 10))
print(part1(input_txtx, 2000000))
