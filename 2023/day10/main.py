def get_maze():
    with open("input.txt") as file:
        return [l.strip() for l in file.readlines()]


def get_start(maze):
    for i, row in enumerate(maze):
        for j, elem in enumerate(row):
            if elem == "S":
                return i, j
    raise Exception("Start not found")


def is_available(elem, direction):
    match direction:
        case "N":
            return elem in ["|", "L", "J"]
        case "S":
            return elem in ["|", "7", "F"]
        case "E":
            return elem in ["-", "F", "L"]
        case "W":
            return elem in ["-", "7", "J"]
        case _:
            raise Exception("IsAvailable not found elem")


def get_directions(elem):
    match elem:
        case "|":
            return ["N", "S"]
        case "-":
            return ["W", "E"]
        case "7":
            return ["S", "W"]
        case "F":
            return ["S", "E"]
        case "L":
            return ["N", "E"]
        case "J":
            return ["N", "W"]
        case "S":
            return ["N", "S", "W", "E"]
        case ".":
            return []
        case _:
            raise Exception(f"Cannot be any other elem, but found {elem}")
 
def get_direction_coordinates(direction, start_x, start_y):
    match direction:
        case "N":
            return start_x - 1, start_y
        case "S":
            return start_x + 1, start_y
        case "E":
            return start_x, start_y + 1
        case "W":
            return start_x, start_y - 1
        case _:
            raise Exception("Direction not recognized")


def get_opposite_direction(direction):
    match direction:
        case "N":
            return "S"
        case "S":
            return "N"
        case "W":
            return "E"
        case "E":
            return "W"
        case _:
            raise Exception(f"Direction {direction} not recognized")

def get_second_maze(maze):
    maze2 = [[0 for _ in range(len(maze[0]))] for _ in range(len(maze))]
    start_x, start_y = get_start(maze)
    maze2[start_x][start_y] = 0
    
    visited = set()
    queue = [(start_x, start_y)]
    visited = set()
    while queue:
        current_x, current_y = queue.pop(0)
        visited.add((current_x, current_y))
        current_distance = maze2[current_x][current_y]

        # print(f"Current location {(current_x, current_y)} = {maze[current_x][current_y]}")
        for direction in get_directions(maze[current_x][current_y]):
            new_x, new_y = get_direction_coordinates(direction, current_x, current_y)
            # print(f"Current direction: {direction}")
            # print(f"Can go to {(new_x, new_y)} = {maze[new_x][new_y]} in direction {direction}: {res}")

            if new_x >= 0 and new_x < len(maze) and new_y >= 0 and new_y < len(maze[0]) \
            and is_available(maze[new_x][new_y], get_opposite_direction(direction)) and (new_x, new_y) not in visited:
                maze2[new_x][new_y] = current_distance + 1
                queue.append((new_x, new_y))

    return maze2


def first():
    maze = get_maze()
    maze2 = get_second_maze(maze)
    
    max_distance = max(dist for row in maze2 for dist in row)
    print(f"Max distance is {max_distance}")


def second():
    maze = get_maze()
    def sort_direction(d):
        match d:
            case "N": return 3
            case "S": return 1
            case "W": return 0
            case "E": return 2
            case _: raise Exception("Unknown direction")

    start_loop = get_start(maze)
    # start_loop = get_start(maze)
    # Find main loop path
    stack = [start_loop]
    visited = set()
    path = []
    while stack:
        current_x, current_y = stack.pop()
        visited.add((current_x, current_y))
        path.append((current_x, current_y))

        for direction in get_directions(maze[current_x][current_y]):
            new_x, new_y = get_direction_coordinates(direction, current_x, current_y)

            if new_x >= 0 and new_x < len(maze) and new_y >= 0 and new_y < len(maze[0]) \
            and is_available(maze[new_x][new_y], get_opposite_direction(direction)) and (new_x, new_y) not in visited:
                stack.append((new_x, new_y))

    path.pop()

    # Shoelace theorem
    area = 0
    for i, vertex in enumerate(path):
        area += vertex[0] * (path[(i + 1) % len(path)][1] - path[i - 1][1])
    print(f"Area is {area}")
    area = abs(area / 2)

    # Picks theorem
    i = area - (len(path) / 2) + 1
    print(f"Nubmer of dots in the loop: {i}")


first()
second()
