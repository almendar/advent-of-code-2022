from dataclasses import dataclass, field

from util import run_day
@dataclass
class Tree:
    height: int
    left_visible: bool = field(default=True)
    right_visible: bool = field(default=True)
    up_visible: bool = field(default=True)
    down_visible: bool = field(default=True)

    def is_visible(self) -> bool:
        return (
            self.right_visible
            or self.left_visible
            or self.down_visible
            or self.up_visible
        )

    def __repr__(self) -> str:
        return f"{self.height}:{self.is_visible()}"

@dataclass
class Plane:
    forest: list[list[Tree]]

    def __getitem__(self, key:int):
        return self.forest[key]
    
    @property
    def x_len(self) ->int:
        return len(self.forest[0])

    @property
    def y_len(self) ->int:
        return len(self.forest)


    def scenicScore(self, x :int, y :int)->int:
        height = self[y][x].height
        
        # right
        right_sum = 0
        for xi in range(x+1, self.x_len):
            if height > self[y][xi].height:
                right_sum += 1
            else:
                right_sum += 1
                break
        
        left_sum = 0
        #left
        for xi in range(x-1, -1,-1):
            if height > self[y][xi].height:

                left_sum+=1
            else:
                left_sum+=1
                break
        
        bottom_sum = 0
        #bottom
        for yi in range(y+1, self.y_len):
            if height > self[yi][x].height:

                bottom_sum +=1
            else:
                bottom_sum +=1
                break

        #up
        up_sum = 0
        for yi in range(y-1,-1,-1):
            if height > self[yi][x].height:

                up_sum += 1
            else:
                up_sum +=1
                break
        return left_sum * right_sum * up_sum * bottom_sum

    def count_visible(self) -> int:
        y_len = self.y_len
        x_len = self.x_len
        
        # left to right
        for y in range(1, y_len - 1):
            curr_max = self[y][0].height
            for x in range(1, x_len-1):
                curr = self[y][x]
                if curr_max >= curr.height:
                    curr.left_visible = False
                if curr.height > curr_max:
                    curr_max = curr.height

        # right to left
        for y in range(1, y_len - 1):
            curr_max = self[y][x_len-1].height
            for x in range(x_len - 2, 0, -1):
                curr = self[y][x]
                if curr_max >= curr.height:
                    curr.right_visible = False
                if curr.height > curr_max:
                    curr_max = curr.height
                

        # top to bottom
        for x in range(1, x_len-1):
            curr_max = self[0][x].height
            for y in range(1, y_len-1):
                curr = self[y][x]
                if curr_max >= curr.height:
                    curr.up_visible = False
            
                if curr.height > curr_max:
                    curr_max = curr.height
                

        # bottom to top
        for x in range(1, y_len-1):
            curr_max = self[y_len-1][x].height
            for y in range(y_len - 2, 0, -1):
                curr = self[y][x]
                if curr_max >= curr.height:
                    curr.down_visible = False
                if curr.height > curr_max:
                    curr_max = curr.height

        count = 0
        for y in range(0, y_len):
            for x in range(0, len(self[y])):
                if self[y][x].is_visible():
                    count += 1
        return count


def read_input(input: str) -> Plane:
    with open(input) as f:
        lines = [line.strip() for line in f]
        return Plane( [[Tree(int(nr)) for nr in line] for line in lines])

def part1(input):
    plane = read_input(input)
    return plane.count_visible()

def part2(input):
    plane = read_input(input)
    acc = []
    for y in range(0,plane.y_len):
        for x in range(0, plane.x_len):
           acc.append(plane.scenicScore(x,y))
    return max(acc)

run_day(8,part1, part2)
