from dataclasses import dataclass
from collections import namedtuple

Position = namedtuple("Position", ("x", "y"))
Speed = namedtuple("Speed", ("x", "y"))

WIDTH = 101
HEIGHT = 103

@dataclass
class Robot:
    id: int
    pos: Position
    speed: Speed

    def move(self):
        new_x = self.pos.x + self.speed.x
        new_y = self.pos.y + self.speed.y 
        if new_x < 0:
            print(f"new_x is {new_x} new val is {HEIGHT+new_x}")
            new_x = HEIGHT + new_x
        if new_y < 0:
            print(f"new_y is {new_y} new val is {WIDTH+new_y}")
            new_y = WIDTH + new_y

        if new_x >= HEIGHT:
            print(f"new_x is big and is {new_x} new val is {HEIGHT-new_x}")
            new_y = WIDTH + new_y
            new_x = new_x % HEIGHT
        if new_y >= WIDTH:
            print(f"new_y is big and is {new_y} new val is {WIDTH-new_y}")
            new_y = new_y % WIDTH

        assert new_x >= 0 and new_x < HEIGHT, f"new_x is {new_x}"
        assert new_y >= 0 and new_y < HEIGHT, f"new_y is {new_y}"
        self.pos = Position(
            new_x,
            new_y
        )

def get_area(robots):
    area = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for r in robots:
        print(f"robot {r}")
        if isinstance(area[r.pos.x][r.pos.y], int):
           area[r.pos.x][r.pos.y] += 1 
        else:
           area[r.pos.x][r.pos.y] = 1 

    return area

def mul_quadrants(area):
    q1 = sum(area[i][j] for i in range(HEIGHT) for j in range(WIDTH) if i < HEIGHT // 2 and j < WIDTH // 2 if area[i][j] != ".")
    q2 = sum(area[i][j] for i in range(HEIGHT) for j in range(WIDTH) if i < HEIGHT // 2 and j > WIDTH // 2 if area[i][j] != ".")
    q3 = sum(area[i][j] for i in range(HEIGHT) for j in range(WIDTH) if i > HEIGHT // 2 and j < WIDTH // 2 if area[i][j] != ".")
    q4 = sum(area[i][j] for i in range(HEIGHT) for j in range(WIDTH) if i > HEIGHT // 2 and j > WIDTH // 2 if area[i][j] != ".")

    return q1 * q2 * q3 * q4


def first_part():
    robots = []
    with open("input.txt") as file:
        for i, line in enumerate(file):
            pos_str, speed_str = line.strip().split()
            pos_y, pos_x = list(map(int, pos_str.strip().split("=")[1].split(",")))
            vel_y, vel_x = list(map(int, speed_str.strip().split("=")[1].split(",")))
            pos = Position(pos_x, pos_y)
            vel = Speed(vel_x, vel_y)
            robots.append(Robot(i, pos, vel))

    seconds = 100

    for a in get_area(robots): print(a)
    for r in robots:
        for _ in range(seconds):
            r.move()

    # for a in get_area(robots): print(a)
    print(f"The qudrands muplited are: {mul_quadrants(get_area(robots))}")


first_part()
