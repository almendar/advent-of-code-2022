from util import run_day, read_lines


def from_snafu(n: str) -> int:
    acc = 0
    for p, ch in enumerate(n[::-1]):
        k = pow(5, p)
        if ch == "-":
            acc += k * -1
        elif ch == "=":
            acc += k * -2
        else:
            acc += k * int(ch)

    return acc


def to_snafu(n: int) -> str:
    chars = "012=-"
    acc = ""
    while n > 0:
        rem = n % 5
        if rem > 2:
            n += 5
        n //= 5
        acc += chars[rem]
    return acc[::-1]


def part1(input):
    summed = sum(map(from_snafu, read_lines(input)))
    return to_snafu(summed)


def part2(inpit):
    return 0

# answer = 2=-0=1-0012-=-2=0=01

run_day(25, part1, part2)
