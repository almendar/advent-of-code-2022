from util import day_data, read_lines
from typing import List, NamedTuple, MutableSet
from itertools import chain, combinations
from util import run_day, day_data
import time

Label = str


class Node(NamedTuple):
    label: Label
    flow: int
    neighbours: List[Label]


class Graph(dict):
    pass


sample_txt, input_txt = day_data(16)


def read_graph(input) -> Graph:
    connections: Graph = Graph()
    for l in read_lines(input):
        parts = l.split(" ")
        (_, node, _, _, rate, _, _, _, _, *rest) = parts
        rate = int(rate.split("=")[1][:-1])
        n = Node(node, rate, list(map(lambda it: it.strip(","), rest)))
        connections[Label(node)] = n
    return connections


# Floyd–Warshall
def graph_travel_costs(g: Graph):
    d: dict[Label, dict[Label, int]] = {}
    former: dict[Label, dict[Label, Label]] = {}
    for v1 in g:
        for v2 in g:
            if v1 not in d:
                d[v1] = {}
            if v1 not in former:
                former[v1] = {}
            d[v1][v2] = 1 << 64
            d[v1][v1] = 0

    for (v1, node) in g.items():
        for v2 in node.neighbours:
            d[v1][v2] = 1
            former[v1][v2] = v1

    for u in g:
        for v1 in g:
            for v2 in g:
                if d[v1][v2] > d[v1][u] + d[u][v2]:
                    d[v1][v2] = d[v1][u] + d[u][v2]
                    former[v1][v2] = former[u][v2]
    return (d, former)


def DFS(
    G: Graph,
    distances,
    start: Label,
    already_open: MutableSet[Label],
    left_moves,
    per_minute,
    total,
    memoization,
) -> int:

    if (start, frozenset(already_open), total) in memoization:
        return memoization[(start, frozenset(already_open), left_moves, total)]

    if left_moves == 0:
        return total
    elif left_moves < 0:
        return -1

    node = G[start]
    left_unopen = frozenset(filter(lambda x: G[x].flow > 0, G)) - already_open

    if len(left_unopen) == 0 and left_moves >= 0:
        return total + left_moves * per_minute

    distances_set = set()
    for next_unopened in left_unopen:
        distance_there = distances[node.label][next_unopened]
        if distance_there > left_moves:
            distances_set.add(total + left_moves * per_minute)
            continue
        flow_on_this_move = per_minute * (distance_there + 1)
        opened_copy = set(already_open)
        opened_copy.add(next_unopened)

        d = DFS(
            G,
            distances,
            next_unopened,
            opened_copy,
            left_moves - distance_there - 1,
            per_minute + G[next_unopened].flow,
            total + flow_on_this_move,
            memoization,
        )
        distances_set.add(d)

    ret = max(distances_set)
    memoization[(start, frozenset(already_open), left_moves, total)] = ret
    return ret


def part1(input):
    G = read_graph(input)
    distances, _ = graph_travel_costs(G)
    a = DFS(G, distances, "AA", set([]), 30, 0, 0, {})
    return a


def powerset(iterable):
    s = set(iterable)
    return chain.from_iterable(set(combinations(s, r)) for r in range(len(s) + 1))


def current_milli_time():
    return round(time.time() * 1000)


def part2(input):
    max_flow = -1
    G = read_graph(input)
    all_with_flow = set(filter(lambda x: G[x].flow > 0, G))
    distances, _ = graph_travel_costs(G)
    subset = set(powerset(all_with_flow))
    memoization = {}
    start = current_milli_time()
    for i, sub in enumerate(subset):
        me = set(sub)
        elephant = all_with_flow - me
        if len(me) == 0 or len(elephant) == 0:
            continue

        if i % 100 == 0:
            now = current_milli_time()
            print((now - start) / 1000, i, me, elephant)

        meFlow = DFS(G, distances, "AA", me, 26, 0, 0, memoization)
        elephanFlow = DFS(G, distances, "AA", elephant, 26, 0, 0, memoization)
        max_flow = max(max_flow, meFlow + elephanFlow)
    return max_flow


run_day(16, part1, part2)
# sample, input = day_data(16)
# print(part2(sample))
# print(part2(input))
