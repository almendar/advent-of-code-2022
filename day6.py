import os
import timeit


def marker(msg: str, n: int) -> int:
    for i in range(n, len(msg)):
        uniq = len(set(msg[i - n : i]))
        if uniq == n:
            return i
    return -1

ord_a = ord("a")
ord_z = ord("z")
def marker_fast(msg: str, n: int) -> int:
    pos = lambda x: ord(x) - ord_a
    global_duplicate_count = 0
    counts = [0 for _ in range(ord_a, ord_z + 1)]
    for c in msg[: n - 1]:
        ch_pos = pos(c)
        counts[ch_pos] += 1
        if counts[ch_pos] == 2:
            global_duplicate_count += 1

    for i in range(n - 1, len(msg)):
        pop_candidate = pos(msg[i - n + 1])
        current_incoming = pos(msg[i])
        counts[current_incoming] += 1

        k = counts[current_incoming]
        if k == 2:
            global_duplicate_count += 1

        if k == 1 and global_duplicate_count == 0:
            return i + 1

        counts[pop_candidate] -= 1
        if counts[pop_candidate] == 1:
            global_duplicate_count -= 1
    return -1


if __name__ == "__main__":
    print(8 * "=" + " PART1 " + 8 * "=")
    with open("input/day6-sample.txt") as f:
        lines = list(filter(None, map(lambda x: x.strip(), f.readlines())))
        for l in lines:
            print(f"Packet start: {l} - {marker(l, 4)} {marker_fast(l, 4)}")
        for l in lines:
            print(f"Message start: {l} - {marker(l, 14)} {marker_fast(l, 14)}")
    print(8 * "=" + " PART2 " + 8 * "=")
    with open("input/day6-input.txt") as f:
        lines = list(filter(None, map(lambda x: x.strip(), f.readlines())))
        for l in lines:
            print(f"Packet start: {marker(l, 4)} {marker_fast(l, 4)}")  

        import cProfile
        import re
        for l in lines:
            print(timeit.timeit("marker(l, 14)", globals=locals(), number=10000))
            print(timeit.timeit("marker_fast(l, 14)", globals=locals(), number=10000))
            # cProfile.run('marker(l, 14)')
            # cProfile.run('marker_fast(l, 14)')
