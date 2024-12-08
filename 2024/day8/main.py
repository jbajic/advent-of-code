from collections import defaultdict
from itertools import combinations


def first_part():
    with open("input.txt") as file:
        map = [list(line.strip()) for line in file]

    antennas_locations = defaultdict(list)
    for i, line in enumerate(map):
        for j, elem in enumerate(line):
            if elem != ".":
                antennas_locations[elem].append((i, j))

    antidote_locations = set()
    for _, locations in antennas_locations.items():
        for p1, p2 in combinations(locations, 2):
            if p1 == p2:continue
            assert(p1 != p2)
            # L2
            x_dist = abs(p2[0] - p1[0])
            # y = ax + b
            a = (p2[1] - p1[1])/(p2[0] - p1[0])
            b = p1[1] - a * p1[0]

            # New points
            points = []
            if p1[0] > p2[0]:
                points.append((p1[0] + x_dist, a * (p1[0] + x_dist) + b))
                points.append((p2[0] - x_dist, a * (p2[0] - x_dist) + b))
            else:
                points.append((p2[0] + x_dist, a * (p2[0] + x_dist) + b))
                points.append((p1[0] - x_dist, a * (p1[0] - x_dist) + b))

            for point in points:
                x = int(point[0])
                y = int(point[1])
                if x < 0 or y < 0 or x >= len(map) or y >= len(map[0]):
                    continue

                if (x,y) not in antidote_locations:
                    antidote_locations.add((x,y))

    print(f"There are {len(antidote_locations)}")
    

def second_part():
    with open("input.txt") as file:
        map = [list(line.strip()) for line in file]

    antennas_locations = defaultdict(list)
    for i, line in enumerate(map):
        for j, elem in enumerate(line):
            if elem != ".":
                antennas_locations[elem].append((i, j))

    antidote_locations = set()
    for antena, locations in antennas_locations.items():
        for p1, p2 in combinations(locations, 2):
            assert(p1 != p2)
            # L2
            x_dist = abs(p1[0] - p2[0])
            # y = ax + b
            a = (p2[1] - p1[1])/(p2[0] - p1[0])
            b = p1[1] - a * p1[0]

            # New points
            points = []
            max_x = len(map) // x_dist
            if p1[0] > p2[0]:
                points.extend([(p1[0] + x_dist * i, a * (p1[0] + x_dist * i) + b) for i in range(0, max_x)])
                points.extend([(p2[0] - x_dist * i, a * (p2[0] - x_dist * i) + b) for i in range(0, max_x)])
            else:
                points.extend([(p2[0] + x_dist * i, a * (p2[0] + x_dist * i) + b) for i in range(0, max_x)])
                points.extend([(p1[0] - x_dist * i, a * (p1[0] - x_dist * i) + b) for i in range(0, max_x)])

            for point in points:
                x = round(point[0], 5)
                y = round(point[1], 5)

                if isinstance(x, float) and not x.is_integer():
                    continue
                if isinstance(y, float) and not y.is_integer():
                    continue

                x = int(x)
                y = int(y)
                if x < 0 or y < 0 or x >= len(map) or y >= len(map[0]):
                    continue

                antidote_locations.add((x,y))
                if map[x][y] in ["T", "."]:
                    map[x][y] = "#"

    print(f"There are {len(antidote_locations)}")
    

first_part()
second_part()
