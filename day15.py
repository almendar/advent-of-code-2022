from typing import NamedTuple
from dataclasses import dataclass, field


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
    sensors: list[Sensor] = []
    for ft in input_data:
        s, b = ft
        sensors.append(Sensor(s, b))

    x_min = min(map(lambda it: it.loc.x - it.max_reach, sensors))
    x_max = max(map(lambda it: it.loc.x + it.max_reach, sensors))
    count = 0
    for xi in range(x_min, x_max + 1):
        for s in sensors:
            if s.covers(Coord(xi, y_pos)) and not Coord(xi, y_pos) == s.beacon:
                count += 1
                break

    return count


def part2(input, max):
    input_data = read_input(input)
    sensors: list[Sensor] = []
    for ft in input_data:
        s, b = ft
        sensors.append(Sensor(s, b))

    def look():
        for x in range(0, max + 1):
            y = 0
            while y <= max:
                anySensorCovering = [s for s in sensors if s.covers(Coord(x, y))]
                if not anySensorCovering:
                    return Coord(x, y)
                sensor = anySensorCovering[0]
                y = sensor.loc.y + sensor.max_reach - abs(x - sensor.loc.x) + 1
        raise ValueError()

    p = look()
    return p.x * 4000000 + p.y


sample_txt = "input/day15-sample.txt"
input_txtx = "input/day15-input.txt"

# 26
# 5240818
print(part1(sample_txt, 10))
print(part1(input_txtx, 2000000))

# 56000011
# 13213086906101
print(part2(sample_txt, 20))
print(part2(input_txtx, 4000000))
