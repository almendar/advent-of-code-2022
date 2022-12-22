from typing import Dict, NamedTuple
from util import day_data
from dataclasses import dataclass, field
sample_txt, input_txt = day_data(22)

def get_lines(input):
    with open(input) as f:
        rr = f.readlines()
        instructions = rr[-1]
        maze = [p.rstrip("\n") for p in rr[:-2]]
 
        return (maze, instructions)


class Coord(NamedTuple):
    x: int
    y: int

    def dx(self, n:int)-> "Coord":
        return Coord(self.x + n, self.y)
    
    def dy(self, n:int)-> "Coord":
        return Coord(self.x , self.y + n)



@dataclass
class Maze:
    m:list[str]
    
    pos: Coord = field(init=False)
    # >, ^, <, v
    face: str = field(init=False)
    
    trail: Dict[Coord, str] = field(default_factory=lambda: dict())

    def __post_init__(self):
        y = 0
        x =  self.m[y].find(".")
        self.pos = Coord(x,y)
        
        self.face = ">"

        # self.trail[self.pos] = self.face

    def find_row_beginning(self,row:int)->int:
        return min(self.m[row].find("#"), self.m[row].find("."))
    
    def find_col_beg(self, col:int)->int:
        for i, row in enumerate(self.m):
            if col >= len(row):
                continue
            if row[col] != " ":
                return i
        raise ValueError("find_col_beg")

    def find_col_end(self, col:int)->int:
        for i in range(len(self.m)-1, -1,-1):
            if col >=len(self.m[i]):
                continue
            if self.m[i][col] != " ":
                return i
        raise ValueError("find_col_")

    def find_row_end(self,row:int)->int:
        return max(self.m[row].rfind("#"), self.m[row].rfind('.'))

    def print(self):
        for yi,row in enumerate(m):
            for xi,c in enumerate(row):
                if (coord :=Coord(xi, yi)) == self.pos:
                    print('@', end="")
                elif (coord :=Coord(xi, yi)) in self.trail:
                    print(self.trail[coord], end="")
                else:
                    print(c, end="")
            print()

    def move(self, steps:int):
        (x,y) = self.pos
        row_beg = self.find_row_beginning(y)
        row_end = self.find_row_end(y)
        col_beg = self.find_col_beg(x)
        col_end = self.find_col_end(x)
        match self.face:
            case ">":
                newX = x
                while steps > 0:
                    oldX = newX
                    newX = (newX + 1) 
                    if newX > row_end:
                        newX = (newX % (row_end+1)) + row_beg
                    if self.m[y][newX] == "#":
                        newX = oldX
                        break
                    else:
                        self.trail[Coord(oldX,y)] = self.face
                        steps-=1
                self.pos = Coord(newX, y)
            case "<":
                newX = x
                while steps > 0:
                    oldX = newX
                    newX = newX -1
                    if newX < row_beg:
                        newX = (newX - row_beg) % (row_end+1)
                    
                    if self.m[y][newX] == "#":
                        newX  = oldX
                        break
                    else:
                        self.trail[Coord(oldX,y)] = self.face
                        steps-=1
                self.pos = Coord(newX, y)
            
            case "v":
                newY = y
                while steps > 0:
                    oldY = newY
                    newY = newY + 1
                    if newY > col_end:
                        newY = newY%(col_end+1) + col_beg

                    if self.m[newY][x] == "#":
                        newY  = oldY
                        break
                    else:
                        self.trail[Coord(x,oldY)] = self.face
                        steps-=1
                self.pos = Coord(x, newY)
            
            case "^":
                newY = y
                while steps > 0:
                    oldY = newY
                    newY = newY - 1
                    if newY < col_beg:
                        newY = (newY - col_beg) % (col_end+1)
                    if self.m[newY][x] == "#":
                        newY  = oldY
                        break
                    else:
                        self.trail[Coord(x,oldY)] = self.face
                        steps-=1
                self.pos = Coord(x, newY)
    
    def simulate(self,args:str):
        reading_int = False
        int_str = ""
        for i in args:
            if i=='R' or i == 'L':
                if reading_int:
                    number  = int(int_str)
                    self.move(number)
                    self.face = turns[self.face][i]
                    int_str = ""
                    reading_int = False
                    # print(number)
                    # print(i)
            else:
                reading_int = True
                int_str += i
        if reading_int:
            number  = int(int_str)
            self.move(number)
            # print(number)



turns = {
    ">":{"R":"v", "L":"^"},
    "<":{"R":"^", "L":"v"},
    "v":{"R":"<", "L":">"},
    "^":{"R":">", "L":"<"},
}
    

m, i = get_lines(input_txt)
maze = Maze(m)
maze.simulate(i)


score = {
    ">": 0,
    "v": 1,
    "<":2,
    "^":3
}
password = 1000 * (maze.pos.y+1) + 4 *( maze.pos.x+1) + score[maze.face]
print(password)
