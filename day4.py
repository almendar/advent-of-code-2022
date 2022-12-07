from util import run_day


def part1(input):
    with open(input) as lines:
        acc = 0
        for line in lines:
            [l, r] = line.strip().split(",")
            [l_s, l_e] = map(int, l.split("-"))
            [r_s, r_e] = map(int, r.split("-"))
            if (l_s >= r_s and l_e <= r_e) or (r_s >= l_s and r_e <= l_e):
                acc += 1
        return acc


def contains(line: tuple[int, int], p: int) -> bool:
    (l, r) = line
    return l <= p and r >= p


def part2(input):
    with open(input) as lines:
        acc = 0
        for line in lines:
            [l, r] = line.strip().split(",")
            [l_s, l_e] = map(int, l.split("-"))
            [r_s, r_e] = map(int, r.split("-"))
            if (
                contains((l_s, l_e), r_s)
                or contains((l_s, l_e), r_e)
                or contains((r_s, r_e), l_s)
                or contains((r_s, r_e), l_e)
            ):
                acc += 1
        return acc


if __name__ == "__main__":
    run_day(4, part1, part2)
