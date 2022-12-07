from util import run_day

encoding = {"A": 0, "B": 1, "C": 2, "X": 0, "Y": 1, "Z": 2}


def game_score(moves: tuple[int, int]) -> int:
    result = 0
    match moves:
        case (l, r) if l == r:
            # tie
            result = 3 + r + 1
        case (l, r) if (r + 1) % 3 == l:
            # lost
            result = 0 + r + 1
        case (_, r):
            # win
            result = 6 + r + 1
        case _:
            raise ValueError
    return result


def part1(input):
    acc = 0
    with open(input) as input:
        for line in input:
            moves = tuple(map(lambda x: encoding[x], line.strip().split(" ")))
            acc += game_score(moves)
    return acc


def part2(input):
    acc = 0
    with open(input) as input:
        for line in input:
            (l, r) = tuple(map(lambda x: encoding[x], line.strip().split(" ")))
            match r:
                case 0:  # X lose
                    acc += game_score((l, (l - 1) % 3))
                case 1:  # Y draw
                    acc += game_score((l, l))
                case 2:  # Z win
                    acc += game_score((l, (l + 1) % 3))
    return acc


if __name__ == "__main__":
    run_day(2, part1, part2)
