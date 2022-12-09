from collections import namedtuple
from util import run_day

Move = tuple[int, int]

UP: Move = (0, 1)
DOWN: Move = (0, -1)
LEFT: Move = (-1, 0)
RIGHT = (1, 0)
NORM_MOVES: Move = (UP, DOWN, LEFT, RIGHT)

DIAG_R_UP: Move = (1, 1)
DIAG_L_UP: Move = (-1, 1)
DIAG_R_DOWN: Move = (1, -1)
DIAG_L_DOWN: Move = (-1, -1)
DIAG_MOVES: Move = (DIAG_L_DOWN, DIAG_L_UP, DIAG_R_DOWN, DIAG_R_UP)
NO_MOVE: Move = (0, 0)

Point = namedtuple("Point", ["x", "y", "c"])


def same_position(p1, p2):
    return p1.x == p2.x and p1.y == p2.y


def same_row_or_column(p1, p2):
    return p1.x == p2.x or p1.y == p2.y


def reachable_on_diag_move(start, end):
    for m in DIAG_MOVES:
        moved_to = move_point(start, m)
        if same_position(moved_to, end):
            return True
    return False


def reachable_by_one_move(start, end):
    for m in (UP, DOWN, RIGHT, LEFT):
        moved_to = move_point(start, m)
        if same_position(moved_to, end):
            return True
    return False


def move_point(point, move):
    (x, y, r) = point
    (dx, dy) = move
    return Point(x + dx, y + dy, r)


def move_rope(move, rope):
    acc = []
    next_move = move
    last_tail = rope[0]
    for i in range(1, len(rope)):
        head = rope[i - 1]
        tail = rope[i]
        (newhead, new_tail, new_move) = next_pos(head, tail, next_move)
        acc.append(newhead)
        next_move = new_move
        last_tail = new_tail
    acc.append(last_tail)
    return (*acc,)


# Return tail position and its move
def next_pos(head, tail, move) -> (Point, Point, Move):
    moved_head = move_point(head, move)
    moved_tail = move_point(tail, move)
    if same_row_or_column(moved_head, tail):
        if same_position(head, tail):
            return (moved_head, tail, NO_MOVE)
        elif same_position(moved_head, tail):
            return (moved_head, tail, NO_MOVE)
        elif reachable_by_one_move(moved_head, tail):
            return (moved_head, tail, NO_MOVE)
        else:
            for nor_move in NORM_MOVES:
                maybe_tail = move_point(tail, nor_move)
                if reachable_by_one_move(moved_head, maybe_tail):
                    return (moved_head, maybe_tail, nor_move)
            return (moved_head, moved_tail, move)
    # diagonal
    else:
        if reachable_on_diag_move(moved_head, tail):
            return (moved_head, tail, NO_MOVE)
        else:
            for diag_m in DIAG_MOVES:
                maybe_tail = move_point(tail, diag_m)
                if reachable_by_one_move(moved_head, maybe_tail):
                    return (moved_head, maybe_tail, diag_m)
                elif reachable_on_diag_move(moved_head, maybe_tail):
                    return (moved_head, maybe_tail, diag_m)


def print_nicely(*points):
    x_list = tuple(map(lambda p: p[0], points))
    y_list = tuple(map(lambda p: p[1], points))

    min_x = min(x_list)
    max_x = max(x_list)
    min_y = min(y_list)
    max_y = max(y_list)

    p_lookup = {}
    for p in points:
        if len(p) >= 3:
            (x, y, c) = p
            p_lookup[(x, y)] = c
        elif len(p) == 2:
            (x, y) = p
            p_lookup[(x, y)] = "#"

    for yi in range(15, -15, -1):
        print()
        for xi in range(-15, 15):
            if (xi, yi) in p_lookup:
                print(p_lookup[(xi, yi)], end="")
            elif (xi, yi) == (0, 0):
                print("s", end="")
            else:
                print(".", end="")
    print()


moves = (RIGHT, LEFT, LEFT, RIGHT, DOWN, UP, UP, LEFT, LEFT)
moves_mapping = {"R": RIGHT, "L": LEFT, "D": DOWN, "U": UP}


def part1(input):

    tail = Point(0, 0, "T")
    head = Point(0, 0, "H")
    tail_pos_acc = []
    with open(input) as f:
        for line in f:
            (move, cnt) = line.strip().split(" ")
            for i in range(0, int(cnt)):
                head, tail, next_move = next_pos(head, tail, moves_mapping[move])
                tail_pos_acc.append(tail)
    return len(set(tail_pos_acc))


def part2(input):
    rope = (Point(0, 0, "H"),) + tuple((Point(0, 0, f"{i}") for i in range(1, 10)))
    tail_pos_acc = [Point(0, 0, 9)]
    with open(input) as f:
        for line in f:
            (move, cnt) = line.strip().split(" ")
            for i in range(0, int(cnt)):
                new_rope = move_rope(moves_mapping[move], rope)
                *head, last = rope
                tail_pos_acc.append(last)
                rope = new_rope
            # print(cnt, moves_mapping[move])
            # print_nicely(*rope)
    return len(set(tail_pos_acc))


run_day(9, part1, part2)
