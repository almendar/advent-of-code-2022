from util import day_data, read_lines
from typing import List, DefaultDict, NamedTuple, FrozenSet, MutableSet
from util import run_day

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
) -> int:
    if left_moves == 0:
        return total

    node = G[start]
    left_unopen = frozenset(filter(lambda x: G[x].flow > 0, G)) - already_open

    if len(left_unopen) == 0 and left_moves >= 0:
        return total + left_moves * per_minute

    distances_set = set([0])
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
            per_minute=per_minute + G[next_unopened].flow,
            total=total + flow_on_this_move,
        )
        distances_set.add(d)

    ret = max(distances_set)
    return ret


def part1(input):
    G = read_graph(input)
    distances, _ = graph_travel_costs(G)
    return DFS(G, distances, "AA", set(), 30, 0, 0)


def part2(input):
    return -1


run_day(16, part1, part2)
