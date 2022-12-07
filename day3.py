from util import run_day
import string


def part1(input):
    with open(input) as lines:
        acc = 0
        for line in lines:
            line = line.strip()
            chars_number = int(len(line) / 2)
            (left, right) = (set(line[:chars_number]), set(line[chars_number:]))
            common = left & right
            acc += sum(map(lambda x: string.ascii_letters.index(x) + 1, common))
        return acc


def part2(input):
    acc = 0
    with open(input) as lines:
        while True:
            try:

                el1 = next(lines).strip()
                el2 = next(lines).strip()
                el3 = next(lines).strip()
                common = set(el1) & set(el2) & set(el3)
                acc += sum(map(lambda x: string.ascii_letters.index(x) + 1, common))
            except StopIteration:
                return acc


if __name__ == "__main__":
    run_day(3, part1, part2)
