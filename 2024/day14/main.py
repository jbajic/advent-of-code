from dataclasses import dataclass
from collections import namedtuple
from sklearn.cluster import KMeans
import numpy as np


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
            new_x = HEIGHT + new_x
        if new_y < 0:
            new_y = WIDTH + new_y

        if new_x >= HEIGHT:
            new_y = WIDTH + new_y
            new_x = new_x % HEIGHT
        if new_y >= WIDTH:
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
        if isinstance(area[r.pos.x][r.pos.y], int):
           area[r.pos.x][r.pos.y] += 1 
        else:
           area[r.pos.x][r.pos.y] = 1 

    return area

def print_area(area):
    for i in range(len(area)):
        for j in range(len(area[i])):
            if area[i][j] == ".":
                print("0")
            else:
                print("1")
        print()

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

    print(f"The qudrands muplited are: {mul_quadrants(get_area(robots))}")

def is_tree2(area):
    points = [(i, j) for i, row in enumerate(area) for j, val in enumerate(row) if val != '.']
    kmeans = KMeans(n_clusters=10, random_state=0, n_init="auto").fit(points)
    labels = kmeans.labels_  # Cluster labels for each point
    counts = np.bincount(labels)  # Count points in each cluster

    for cluster_id, count in enumerate(counts):
        print(f"Cluster {cluster_id}: {count} elements")
        if count > 90:
            return True
    return False

def is_tree(area, robots):
    seen_pos = set()
    l = [robots[0].pos]
    while len(l) > 0:
        # print(l)
        r = l.pop()
        # print(f"New pos {r}")
        for dx in [0, -1, 1]:
            for dy in [0, -1, 1]:
                if dx == 0 and dy == 0:
                    continue
                current_x = r.x + dx
                current_y = r.y + dy
                if current_x < 0 or current_x >= HEIGHT:
                    continue
                if current_y < 0 or current_y >= WIDTH:
                    continue
                if area[current_x][current_y] == ".":
                    continue
                pos = Position(current_y, current_y)
                if pos in seen_pos:
                    continue
                seen_pos.add(pos)
                l.append(pos)

    # print("Checking...")
    return len(seen_pos) == sum(sum(1 for element in row if element != '.') for row in area) 


def second_part():
    robots = []
    with open("input.txt") as file:
        for i, line in enumerate(file):
            pos_str, speed_str = line.strip().split()
            pos_y, pos_x = list(map(int, pos_str.strip().split("=")[1].split(",")))
            vel_y, vel_x = list(map(int, speed_str.strip().split("=")[1].split(",")))
            pos = Position(pos_x, pos_y)
            vel = Speed(vel_x, vel_y)
            robots.append(Robot(i, pos, vel))


    seconds = 0
    for a in get_area(robots): print(a)
    current_try = 0
    try_max = 50
    try_offset = 20
    while True:
        seconds += 1
        for r in robots:
            r.move()
        if is_tree2(get_area(robots)):
            if current_try >= try_offset:
                with open(f"ladida_{seconds}.txt", "w") as file:
                    for a in get_area(robots):
                        for elem in a:
                            if elem == ".":
                                file.write(".")
                            else:
                                file.write("#")
                        file.write("\n")
            current_try += 1
            if current_try == try_max:
                break
            print(f"Tree found at {seconds} seconds")
        
        print(f"Current second {seconds}")


first_part()
# I don't know what a tree looks like you have to check files manually :)
second_part()
