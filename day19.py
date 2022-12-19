from util import day_data, read_lines
from dataclasses import dataclass
from typing import List
import re

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


print(Blueprint.from_file(sample_txt))
print(Blueprint.from_file(input_txt))
