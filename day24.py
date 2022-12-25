from util import run_day, read_lines
from typing import List, NamedTuple
from queue import PriorityQueue
import heapq


class Coord(NamedTuple):
    x: int
    y: int


class BlizzardBasin:
    def __init__(self, bassing: List[str]):
        self.bassin = bassing
        self.Y_LEN = len(bassing)
        self.X_LEN = len(bassing[0])
        self.START = (bassing[0].find("."), 0)
        self.END = (bassing[-1].find("."), len(bassing) - 1)

    def free(self, x: int, y: int, time: int) -> bool:
        c = Coord(x, y)
        if c == self.START or c == self.END:
            return True

        if x <= 0 or x >= self.X_LEN - 1:
            return False

        if y <= 0 or y >= self.Y_LEN - 1:
            return False

        if self.bassin[y][(x + time - 1) % (self.X_LEN - 2) + 1] == "<":
            return False

        if self.bassin[y][(x - time - 1) % (self.X_LEN - 2) + 1] == ">":
            return False

        if self.bassin[(y + time - 1) % (self.Y_LEN - 2) + 1][x] == "^":
            return False

        if self.bassin[(y - time - 1) % (self.Y_LEN - 2) + 1][x] == "v":
            return False

        return True

    def search_path(self, start: Coord, end: Coord, startTime=0) -> int:
        endY, endX = end
        memoization = set()
        Q = []
        heapq.heappush(Q, (0, (startTime, start)))
        while len(Q) > 0:
            (priority, (time, (x, y))) = heapq.heappop(Q)

            if Coord(x, y) == end:
                return time

            for (nx, ny) in [(x + 1, y), (x - 1, y), (x, y), (x, y - 1), (x, y + 1)]:
                if self.free(nx, ny, time + 1):
                    state = (time + 1, Coord(nx, ny))
                    if state not in memoization:
                        memoization.add(state)
                        heapq.heappush(
                            Q, ((time + abs(endX - nx) + abs(endY - ny), state))
                        )


def part1(input):
    lines = list(map(lambda x: x.strip(), read_lines(input)))
    bb = BlizzardBasin(lines)
    return bb.search_path(bb.START, bb.END)


def part2(input):
    lines = list(map(lambda x: x.strip(), read_lines(input)))
    bb = BlizzardBasin(lines)
    path1 = bb.search_path(bb.START, bb.END)
    path2 = bb.search_path(bb.END, bb.START, path1)
    return bb.search_path(bb.START, bb.END, path2)


if __name__ == "__main__":
    run_day(24, part1, part2)
    pass
