from typing import NamedTuple, FrozenSet, Dict, NewType, Tuple, Set
from itertools import groupby


sample_txt = "input/day15-sample.txt"
input_txtx = "input/day15-input.txt"


class Coor(NamedTuple):
    x: int
    y: int


class Sensor(Coor):
    pass


class Beacon(Coor):
    pass


ManhattanDistance = NewType("ManhattanDistance", int)


def parse_line(l):
    _, _, sx, sy, _, _, _, _, bx, by = l.split(" ")
    sx = int(sx[:-1].split("=")[1])
    sy = int(sy[:-1].split("=")[1])
    bx = int(bx[:-1].split("=")[1])
    by = int(by.split("=")[1])
    return (Sensor(sx, sy), Beacon(bx, by))


def read_input(path):
    with open(path) as f:
        return [parse_line(l) for l in f]


def manhattan(p1: Coor, p2: Coor) -> ManhattanDistance:
    return ManhattanDistance(abs(p1.x - p2.x) + abs(p1.y - p2.y))


def gen_coverage(p: Sensor, d: int):

    acc = set()
    for yi in range(p.y - d, p.y + d + 1):
        delta = abs(yi - p.y)
        for xi in range(p.x - d + delta, p.x + d + 1 - delta):
            if (xi, yi) != p:
                acc.add((xi, yi))
    return acc


def print_coverage(center, coverage):
    min_x = min(map(lambda x: x[0], coverage))
    max_x = max(map(lambda x: x[0], coverage))
    min_y = min(map(lambda x: x[1], coverage))
    max_y = max(map(lambda x: x[1], coverage))
    for yi in range(min_y, max_y + 1):
        for xi in range(min_x, max_x + 1):
            if (xi, yi) in coverage:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def coverage_at_y(s: Sensor, ray: ManhattanDistance, y: int):
    from_y = abs(y - s.y)
    if from_y > ray:
        return set()
    x_ray = ray - from_y
    return [(i, y) for i in range(s.x - x_ray, s.x + x_ray + 1)]


def part1(input, y_pos):
    input_data = read_input(input)
    trtrt = set()
    for ft in input_data:
        s, b = ft
        dis = manhattan(s, b)
        trtrt |= set(coverage_at_y(s, dis, y_pos))
        if b.y == y_pos:
            trtrt.remove(b)
    return len(trtrt)


part1(sample_txt, 10)
part1(input_txtx, 2000000)
