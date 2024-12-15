from dataclasses import dataclass
from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])


@dataclass
class Region:
    plant_type: str
    points: set[Point]


def bound_check(point, area):
    if point.x < 0 or point.x >= len(area):
        return False
    if point.y < 0 or point.y >= len(area[0]):
        return False
    return True

def get_updownrightleft():
    return [(1, 0), (-1, 0), (0, 1), (0, -1)]

def first_part():
    area = []
    with open("input.txt") as file:
        area = [list(line.strip()) for line in file]
    
    explored = set()
    regions = []
    for i in range(len(area)):
        for j in range(len(area[i])):
            if (i,j) in explored:
                continue
            # eplore

            points = set()
            exploring_type = area[i][j]
            to_visit = [Point(i,j)]
            while len(to_visit) > 0:
                current = to_visit.pop()
                points.add(current)
                for d1,d2 in get_updownrightleft():
                    new_point = Point(current.x + d1, current.y + d2)
                    if not bound_check(new_point, area):
                        continue

                    if area[new_point.x][new_point.y] == exploring_type and new_point not in points:
                        to_visit.append(new_point)
            explored.update(points)
            regions.append(Region(exploring_type, points))

    total_cost = 0
    for reg in regions:

        perimeter = 0
        for p in reg.points:
            surrounding_same = 0
            for d1, d2 in get_updownrightleft():
                neibgour = Point(p.x + d1, p.y + d2)
                if not bound_check(neibgour, area):
                    continue
                if area[neibgour.x][neibgour.y] == reg.plant_type:
                     surrounding_same += 1       

            match surrounding_same:
                case 0:
                    perimeter += 4
                case 1:
                    perimeter += 3
                case 2:
                    perimeter += 2
                case 3:
                    perimeter += 1
                case 4:
                    pass
                case _:
                    raise Exception("Not possible")
        print(f"For reg {reg} the cost is {perimeter * len(reg.points)} with perimeter {perimeter}")
        total_cost += perimeter * len(reg.points)
        print()
    print(f"Total cost is {total_cost}")
                

first_part()
