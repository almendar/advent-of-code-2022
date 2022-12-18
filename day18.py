from util import run_day
from dataclasses import dataclass
from typing import FrozenSet, Tuple


@dataclass
class Droplet:
    cubes: FrozenSet
    min_pos: int
    max_pos: int


def parse_line(line):
    return tuple(int(x) for x in line.split(","))


def load_droplet(input):
    with open(input) as f:
        cubes = frozenset(map(lambda x: parse_line(x), f.readlines()))
        min_pos = min(min(point) for point in cubes) - 1
        max_pos = max(max(point) for point in cubes) + 1
        return Droplet(cubes, min_pos, max_pos)


def neighbours(point, droplet):
    x, y, z = point
    candidates = set()
    if x > droplet.min_pos:
        candidates.add((x - 1, y, z))
    if x < droplet.max_pos:
        candidates.add((x + 1, y, z))
    if y > droplet.min_pos:
        candidates.add((x, y - 1, z))
    if y < droplet.max_pos:
        candidates.add((x, y + 1, z))
    if z > droplet.min_pos:
        candidates.add((x, y, z - 1))
    if z < droplet.max_pos:
        candidates.add((x, y, z + 1))
    return frozenset(candidates)


def part1(input):
    droplet = load_droplet(input)
    acc = 0
    for c in droplet.cubes:
        for j in neighbours(c, droplet):
            if j not in droplet.cubes:
                acc += 1
    return acc


def part2(input):
    droplet = load_droplet(input)
    total = 0
    frontier = [(droplet.min_pos, droplet.min_pos, droplet.min_pos)]
    steam = {frontier[0]}
    while frontier:
        point = frontier.pop()
        for other in neighbours(point, droplet) - steam:
            if other in droplet.cubes:
                total += 1
            else:
                steam.add(other)
                frontier.append(other)
    return total


run_day(18, part1, part2)
