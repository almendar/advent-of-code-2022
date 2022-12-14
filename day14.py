from util import run_day


def readInput(input):
    cave = {}
    min_x = 1 << 64
    max_x = -1
    max_y = -1
    with open(input) as f:
        for line in f:
            coords = line.strip().split("->")
            l = len(coords)
            for i in range(1, l):
                fx, fy = tuple(map(lambda x: int(x), coords[i - 1].split(",")))
                tx, ty = tuple(map(lambda x: int(x), coords[i].split(",")))
                min_x = min(min_x, fx, tx)
                max_x = max(max_x, fx, tx)
                max_y = max(max_y, fy, ty)
                if fx == tx:
                    s = min(fy, ty)
                    e = max(fy, ty)
                    for k in range(s, e + 1):
                        cave[(fx, k)] = "#"
                elif fy == ty:
                    s = min(fx, tx)
                    e = max(fx, tx)
                    for k in range(s, e + 1):
                        cave[(k, fy)] = "#"
                    pass
                else:
                    raise ValueError
    return cave, min_x, max_x, max_y


def print_cave(cave, min_x, max_x, max_y):
    for yi in range(0, max_y + 1):
        print(f"{yi:03d} ", end="")
        for xi in range(min_x, max_x + 1):
            if (xi, yi) in cave:
                print(cave[(xi, yi)], end="")
            else:
                print(".", end="")
        print()


def pour_sand(cave, max_y, floor) -> bool:
    s = (500, 0)
    while True:
        sx, sy = s
        # overflow or floor
        if sy == max_y + 1:
            if floor:
                cave[s] = "o"
                return True
            else:
                return False
        # move down
        elif (sx, sy + 1) not in cave:
            s = (sx, sy + 1)
        # left
        elif (sx - 1, sy + 1) not in cave:
            s = (sx - 1, sy + 1)
        # right
        elif (sx + 1, sy + 1) not in cave:
            s = (sx + 1, sy + 1)
        # done
        else:
            cave[s] = "o"
            return True


def part1(input):
    cave, min_x, max_x, max_y = readInput(input)
    counter = 0
    while pour_sand(cave, max_y, False):
        counter += 1
    # print_cave(cave, min_x, max_x, max_y)
    return counter


def part2(input):
    cave, min_x, max_x, max_y = readInput(input)
    counter = 0
    while (500, 0) not in cave:
        pour_sand(cave, max_y, True)
        counter += 1
    return counter


# 979, 29044
run_day(14, part1, part2)
