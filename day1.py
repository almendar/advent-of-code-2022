from util import run_day


def part1(input):
    running_max = 0
    with open(input) as input:
        acc = 0
        for line in input:
            if line.strip() == "":
                if acc > running_max:
                    running_max = acc
                acc = 0
            else:
                acc += int(line)
    return running_max


def part2(input):
    all_elements = []
    with open(input) as input:
        acc = 0
        for line in input:
            if line.strip() == "":
                all_elements.append(acc)
                acc = 0
            else:
                acc += int(line, base=10)
    all_elements.sort(reverse=True)
    return sum(all_elements[0:3])


if __name__ == "__main__":
    run_day(1, part1, part2)
