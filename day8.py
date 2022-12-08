from dataclasses import dataclass, field

from util import run_day


@dataclass
class Tree:
    height: int
    left_visible: bool = field(default=True)
    right_visible: bool = field(default=True)
    up_visible: bool = field(default=True)
    down_visible: bool = field(default=True)

    def is_visible(self) -> bool:
        return (
            self.right_visible
            or self.left_visible
            or self.down_visible
            or self.up_visible
        )

    def __repr__(self) -> str:
        return f"{self.height}:{self.is_visible()}"


Plane = list[list[Tree]]

# @dataclass
# class Plane:
#     forest:

#     def __getitem__(self, key: int):
#         return self.forest[key]

#     @property
#     def x_len(self) -> int:
#         return len(self.forest[0])

#     @property
#     def y_len(self) -> int:
#         return len(self.forest)


def scenic_score(plane: Plane, x: int, y: int) -> int:
    height = plane[y][x].height
    x_len = len(plane[0])
    y_len = len(plane)

    # right
    right_sum = 0
    for xi in range(x + 1, x_len):
        right_sum += 1
        if height <= plane[y][xi].height:
            break

    # left
    left_sum = 0
    for xi in range(x - 1, -1, -1):
        left_sum += 1
        if height <= plane[y][xi].height:
            break

    # down
    down = 0
    for yi in range(y + 1, y_len):
        down += 1
        if height <= plane[yi][x].height:
            break

    # up
    up_sum = 0
    for yi in range(y - 1, -1, -1):
        up_sum += 1
        if height <= plane[yi][x].height:
            break

    return left_sum * right_sum * up_sum * down


def count_visible(plane: Plane) -> int:
    x_len = len(plane[0])
    y_len = len(plane)

    # left to right
    for y in range(1, y_len - 1):
        curr_max = plane[y][0].height
        for x in range(1, x_len - 1):
            curr = plane[y][x]
            if curr_max >= curr.height:
                curr.left_visible = False
            if curr.height > curr_max:
                curr_max = curr.height

    # right to left
    for y in range(1, y_len - 1):
        curr_max = plane[y][x_len - 1].height
        for x in range(x_len - 2, 0, -1):
            curr = plane[y][x]
            if curr_max >= curr.height:
                curr.right_visible = False
            if curr.height > curr_max:
                curr_max = curr.height

    # top to bottom
    for x in range(1, x_len - 1):
        curr_max = plane[0][x].height
        for y in range(1, y_len - 1):
            curr = plane[y][x]
            if curr_max >= curr.height:
                curr.up_visible = False

            if curr.height > curr_max:
                curr_max = curr.height

    # bottom to top
    for x in range(1, y_len - 1):
        curr_max = plane[y_len - 1][x].height
        for y in range(y_len - 2, 0, -1):
            curr = plane[y][x]
            if curr_max >= curr.height:
                curr.down_visible = False
            if curr.height > curr_max:
                curr_max = curr.height

    count = 0
    for y in range(0, y_len):
        for x in range(0, len(plane[y])):
            if plane[y][x].is_visible():
                count += 1
    return count


def read_input(input: str) -> Plane:
    with open(input) as f:
        lines = [line.strip() for line in f]
        return Plane([[Tree(int(nr)) for nr in line] for line in lines])


def part1(input):
    plane = read_input(input)
    return count_visible(plane)


def part2(input):
    plane = read_input(input)
    x_len = len(plane[0])
    y_len = len(plane)
    return max(
        [scenic_score(plane, x, y) for y in range(0, y_len) for x in range(0, x_len)]
    )


run_day(8, part1, part2)
