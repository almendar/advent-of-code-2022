from dataclasses import dataclass, field
from typing import Optional, List, Dict, Callable
from util import run_day


@dataclass
class File:
    name: str
    _size: int
    pass

    def size(self) -> int:
        return self._size


@dataclass
class Directory:
    name: str
    parent: Optional["Directory"] = field(default=None)
    subdirs: Dict[str, "Directory"] = field(default_factory=dict)
    files: List[File] = field(default_factory=list)

    def size(self) -> int:
        file_sizes = sum([f.size() for f in self.files])
        subdir_sizes = sum([self.subdirs[name].size() for name in self.subdirs])
        return file_sizes + subdir_sizes

    def root(self) -> "Directory":
        if self.parent == None:
            return self
        else:
            return self.parent.root()


def visit_collect(
    d: Directory, predicate: Callable[[Directory], bool], acc:List[Directory] = 
) -> List[Directory]:

    if acc == None:
        acc = []

    if predicate(d):
        acc.append(d)
    for _, v in d.subdirs.items():
        visit_collect(v, predicate, acc)

    return acc


def parse(input) -> Directory:
    with open(input) as f:
        navigation : Directory = Directory("/")
        for line in f:
            line_el = line.strip().split(" ")
            match line_el:
                case ["$", "cd", "/"]:
                    pass
                case ["$", "cd", ".."]:
                    if navigation.parent:
                        navigation = navigation.parent
                    else:
                        raise ValueError
                case ["$", "cd", folder]:
                    navigation = navigation.subdirs[folder]
                case ["$", "ls"]:
                    pass
                case ["$", "cd", rest]:
                    navigation = navigation.subdirs[rest]
                case ["dir", name]:
                    newDir = Directory(name, navigation)
                    navigation.subdirs[name] = newDir
                case [file_size, file_name]:
                    newFile = File(file_name, int(file_size))
                    navigation.files.append(newFile)
                case _:
                    raise ValueError
        return navigation.root()


def bigger_than_100k(d: Directory) -> bool:
    return d.size() < 100000


        
    
    

def part1(input: str):
    root = parse(input)
    collected = visit_collect(root, bigger_than_100k)
    sum_size = sum([d.size() for d in collected])
    return sum_size


def part2(input: str):
    root = parse(input)
    TOTAL = 70000000
    NEED = 30000000
    used_space = root.size()
    def delete_candidates(d: Directory) -> bool:
        free_space_now = TOTAL - used_space
        free_after_delete = free_space_now + d.size()
        return free_after_delete >= NEED
    collected = visit_collect(root, delete_candidates)
    return min([d.size() for d in collected])
    


if __name__ == "__main__":
    run_day(7, part1, part2)
