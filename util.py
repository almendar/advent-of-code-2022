import functools

import operator


def run_day(day, part1, part2):
    (sample, input) = day_data(day)
    p1_sample = part1(sample)
    p1_input = part1(input)

    p2_sample = part2(sample)
    p2_input = part2(input)

    print(f"day{day}-part1-sample: {p1_sample}")
    print(f"day{day}-part1-input: {p1_input}")
    print(f"day{day}-part2-sample: {p2_sample}")
    print(f"day{day}-part1-input: {p2_input}")


def compose(*fs):
    return lambda arg: functools.reduce(lambda r, f: f(r), fs, arg)


def pipe(arg, *fs):
    return compose(*fs)(arg)


def read_lines(input: str):
    with open(input) as f:
        for i in f:
            yield i.strip()


def day_data(day):
    return (f"input/day{day}-sample.txt", f"input/day{day}-input.txt")
