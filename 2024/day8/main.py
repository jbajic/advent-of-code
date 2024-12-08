from collections import defaultdict
from itertools import permutations, combinations


def first_part():
    with open("input.txt") as file:
        map = [list(line.strip()) for line in file]

    antennas_locations = defaultdict(list)
    for i, line in enumerate(map):
        for j, elem in enumerate(line):
            if elem != ".":
                antennas_locations[elem].append((i, j))

    for l in map:
        print(l)

    antidote_locations = set()
    for antena, locations in antennas_locations.items():
        print(f"Check  antena {antena}")
        for p1, p2 in combinations(locations, 2):
            print()
            print(f"Check {p1} {p2} permutation")
            assert(p1 != p2)
            # L2
            x_dist = abs(p1[0] - p2[0])
            print(f"Distance is {x_dist}")
            # y = ax + b
            a = (p2[1] - p1[1])/(p2[0] - p1[0])
            b = p1[1] - a * p1[0]
            print(f"Slope {a} and intercept {b}")

            # New points
            points = []
            if p1[0] > p2[0]:
                points.append((p1[0] + x_dist, a * (p1[0] + x_dist) + b))
                points.append((p2[0] - x_dist, a * (p2[0] - x_dist) + b))
            else:
                points.append((p2[0] + x_dist, a * (p2[0] + x_dist) + b))
                points.append((p1[0] - x_dist, a * (p1[0] - x_dist) + b))
            print(f"Possible antidotes {points}")

            for point in points:
                print(f"Check Point {point}")
                x = int(point[0])
                y = int(point[1])
                if x < 0 or y < 0 or x >= len(map) or y >= len(map[0]):
                    print("Goes out of bound")
                    continue

                if (x,y) not in antidote_locations:
                    # map[x][y] = "#"
                    print("Adding")
                    antidote_locations.add((x,y))
                else:
                    print(f"Cannot add, ther is {map[x][y]}")

            print(f"Slope {a} and intercept {b}")
    print(f"There are {len(antidote_locations)}")
    

first_part()
