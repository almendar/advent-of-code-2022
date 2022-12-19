from util import day_data, read_lines
from dataclasses import dataclass, field
import dataclasses
from typing import List, NamedTuple, Tuple
from collections import deque
import functools
import multiprocessing

sample_txt, input_txt = day_data(19)


@dataclass
class Blueprint:
    id: int
    ore_robot_cost_in_ore: int
    clay_roboty_cost_in_ore: int
    obsidian_robot_cost_in_ore: int
    obsidian_robot_cost_in_clay: int
    geode_robot_cost_in_ore: int
    geode_robot_cost_in_obsidian: int

    def build_ore_robot(self):
        return self.ore_robot_cost_in_ore, 0, 0, 0

    def build_clay_robot(self):
        return self.clay_roboty_cost_in_ore, 0, 0, 0

    def build_obsidian_robot(self):
        return self.obsidian_robot_cost_in_ore, self.obsidian_robot_cost_in_clay, 0, 0

    def build_geode(self):
        return (
            self.geode_robot_cost_in_ore,
            0,
            self.geode_robot_cost_in_obsidian,
            0,
        )

    @staticmethod
    def from_file(input: str) -> List["Blueprint"]:
        return list(map(Blueprint.from_string, (i.strip() for i in read_lines(input))))

    @staticmethod
    def from_string(s: str) -> "Blueprint":
        splited = s.split(" ")
        # blueprint  1, and cut off ':'
        # ore 6
        # clay 12
        # obsidian 18, 21
        # geode 27, 30
        return Blueprint(
            *tuple(
                map(
                    int,
                    (
                        splited[1][:-1],
                        splited[6],
                        splited[12],
                        splited[18],
                        splited[21],
                        splited[27],
                        splited[30],
                    ),
                )
            )
        )


@dataclass(unsafe_hash=True)
class Resource:
    ore: int = 0
    clay: int = 0
    obsidians: int = 0
    geode: int = 0

    def validate(self):
        if self.ore < 0 or self.clay < 0 or self.obsidians < 0 or self.geode < 0:
            raise ValueError(self)

    def __add__(self, other: "Resource") -> "Resource":
        return Resource(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidians + other.obsidians,
            self.geode + other.geode,
        )

    def __sub__(self, other: "Resource"):
        return Resource(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidians - other.obsidians,
            self.geode - other.geode,
        )


@dataclass(unsafe_hash=True)
class Robots:
    ore: int = 1
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def dig(self) -> Resource:
        return Resource(self.ore, self.clay, self.obsidian, self.geode)


class Build(NamedTuple):
    ore: bool = False
    clay: bool = False
    obsidian: bool = False
    geodot: bool = False


def robots_can_be_build(moneybag: Resource, blueprint: Blueprint) -> Build:
    can_build_ore: bool = moneybag.ore - blueprint.ore_robot_cost_in_ore >= 0
    can_build_clay: bool = moneybag.ore - blueprint.clay_roboty_cost_in_ore >= 0
    can_build_obsidian: bool = (
        moneybag.ore - blueprint.obsidian_robot_cost_in_ore >= 0
    ) and (moneybag.clay - blueprint.obsidian_robot_cost_in_clay >= 0)
    can_build_geode: bool = (
        moneybag.ore - blueprint.geode_robot_cost_in_ore >= 0
    ) and (moneybag.obsidians - blueprint.geode_robot_cost_in_obsidian >= 0)
    return Build(can_build_ore, can_build_clay, can_build_obsidian, can_build_geode)


@dataclass(unsafe_hash=True)
class State:
    moneybag: Resource
    robots: Robots
    time: int
    prevBuildOptions: Build


def nextState(state: State, blueprint: Blueprint, decision: Build) -> State:
    newMoney = state.robots.dig()
    currentOptins = robots_can_be_build(state.moneybag, blueprint)
    newCost = Resource()
    newRobots = state.robots
    if decision.ore:
        newCost = Resource(*blueprint.build_ore_robot())
        newRobots = dataclasses.replace(state.robots, ore=state.robots.ore + 1)
        currentOptins = Build()
    elif decision.clay:
        newCost = Resource(*blueprint.build_clay_robot())
        newRobots = dataclasses.replace(state.robots, clay=state.robots.clay + 1)
        currentOptins = Build()
    elif decision.obsidian:
        newCost = Resource(*blueprint.build_obsidian_robot())
        newRobots = dataclasses.replace(
            state.robots, obsidian=state.robots.obsidian + 1
        )
        currentOptins = Build()
    elif decision.geodot:
        newCost = Resource(*blueprint.build_geode())
        newRobots = dataclasses.replace(state.robots, geode=state.robots.geode + 1)
        currentOptins = Build()

    newMoneyBag = state.moneybag + newMoney - newCost
    newMoneyBag.validate()
    return State(newMoneyBag, newRobots, state.time + 1, currentOptins)


def simulate(blueprint: Blueprint, MAX_TIME):
    startState = State(Resource(), Robots(), 0, Build())
    prunnned_by_best = 0
    cache_prunned = 0
    prunned_by_skipping = 0
    Q = deque()
    Q.appendleft(startState)
    bestSoFar = -1

    cache = set()

    while len(Q) > 0:
        state: State = Q.pop()

        if state in cache:
            cache_prunned += 1
            continue
        else:
            cache.add(state)

        time_left = MAX_TIME - state.time

        canProduce = state.moneybag.geode + sum(
            [state.moneybag.geode + it for it in range(time_left)]
        )

        if canProduce < bestSoFar:
            prunnned_by_best += 1
            continue

        current_robots_can_build = robots_can_be_build(state.moneybag, blueprint)

        if state.time > MAX_TIME:
            continue

        bestSoFar = max(bestSoFar, state.moneybag.geode)

        qlen = len(Q)
        if qlen % 10_000_000 == 0:
            total_prunnedd = prunnned_by_best + prunned_by_skipping + cache_prunned
            print(
                f"candidates: {qlen} best:{prunnned_by_best} skippint:{prunned_by_skipping} cache:{cache_prunned} total: {total_prunnedd}",
            )

        # Do nothing
        Q.appendleft(nextState(state, blueprint, Build()))

        # Ore robot
        if current_robots_can_build.ore and not state.prevBuildOptions.ore:
            Q.appendleft(nextState(state, blueprint, Build(ore=True)))

        if current_robots_can_build.clay and not state.prevBuildOptions.clay:
            Q.appendleft(nextState(state, blueprint, Build(clay=True)))

        if current_robots_can_build.obsidian and not state.prevBuildOptions.obsidian:
            Q.appendleft(nextState(state, blueprint, Build(obsidian=True)))

        if current_robots_can_build.geodot and not state.prevBuildOptions.geodot:
            Q.appendleft(nextState(state, blueprint, Build(geodot=True)))

        # prunning cound
        if current_robots_can_build.ore and state.prevBuildOptions.ore:
            prunned_by_skipping += 1

        if current_robots_can_build.clay and state.prevBuildOptions.clay:
            prunned_by_skipping += 1

        if current_robots_can_build.obsidian and state.prevBuildOptions.obsidian:
            prunned_by_skipping += 1

        if current_robots_can_build.geodot and not state.prevBuildOptions.geodot:
            prunned_by_skipping += 1

    return (bestSoFar, blueprint.id)


def simulate_part1(blueprint):
    return simulate(blueprint, 24)


def simulate_part2(blueprint):
    return simulate(blueprint, 32)


def part1(input):
    with multiprocessing.Pool(4) as pool:
        blueprints = Blueprint.from_file(sample_txt)
        results = 0
        for result in pool.map(simulate_part1, blueprints):
            bestSoFar, id = result
            results += bestSoFar * id
        return results


def part2(input):
    with multiprocessing.Pool(4) as pool:
        blueprints = Blueprint.from_file(sample_txt)
        results = 1
        for result in pool.map(simulate_part2, blueprints):
            print(result)
        return results


print(part2(sample_txt))
