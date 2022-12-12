sampl_input = "input/day12-sample.txt"

from util import run_day

from dataclasses import dataclass
from typing import NamedTuple
from queue import PriorityQueue
from math import inf


def parse_input(input):
    acc = []
    start = Point(-1, -1)
    end = Point(-1, 1)
    with open(input) as f:
        for yi, line in enumerate(f):
            line_acc = []
            for xi, nr in enumerate(line.strip()):
                match nr:
                    case "S":
                        start = Point(xi, yi)
                        line_acc.append("a")
                    case "E":
                        end = Point(xi, yi)
                        line_acc.append("z")
                    case _:
                        line_acc.append(nr)
            acc.append(line_acc)
    return Maze(acc), start, end


class Point(NamedTuple):
    x: int
    y: int


def manhattan(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


@dataclass(frozen=True)
class Maze:
    fields: list[str]

    @property
    def y_len(self) -> int:
        return len(self.fields)

    @property
    def x_len(self) -> int:
        return len(self.fields[0])

    def neighbour(self, p: Point) -> list[Point]:
        def legal(p: Point):
            (x, y) = p
            y_valid = y in range(0, self.y_len)
            x_valid = x in range(0, self.x_len)
            return y_valid and x_valid

        (x, y) = p
        ch = self.fields[y][x]

        neighbours = []
        for move in (Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)):
            maybe = Point(x + move.x, y + move.y)
            if legal(maybe):
                maybeCh = self.fields[maybe.y][maybe.x]
                if ord(maybeCh) - ord(ch) <= 1:
                    neighbours.append(maybe)

        return neighbours

    def min_moves(self, start, end) -> int:
        frontier = PriorityQueue[tuple[int, Point]]()
        frontier.put((0, start))
        cost_so_far: dict[Point, int] = {}
        cost_so_far[start] = 0

        while not frontier.empty():
            (_, current) = frontier.get()

            if current == end:
                break

            for next in self.neighbour(current):
                cost = 1
                new_cost = cost_so_far[current] + cost
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + manhattan(next, end)
                    frontier.put((priority, next))

        infinity_like = 1 << 64
        return cost_so_far.get(end, infinity_like)


def find_a(maze: Maze) -> list[Point]:
    return [
        Point(xi, yi)
        for yi in range(0, maze.y_len)
        for xi in range(0, maze.x_len)
        if maze.fields[yi][xi] == "a"
    ]


def part1(input):
    maz, start, end = parse_input(input)
    return maz.min_moves(start, end)


def part2(input):
    maz, _, end = parse_input(input)
    all_a = find_a(maz)
    return min(map(lambda x: maz.min_moves(x, end), all_a))


run_day(12, part1, part2)
