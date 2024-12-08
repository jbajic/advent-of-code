def get_change(direction):
    match direction:
        case "^":
            return (-1, 0)
        case ">":
            return (0, 1)
        case "<":
            return (0, -1)
        case "v":
            return (1, 0)
        case _:
            raise Exception("Direction not found")

def get_new_direction(direction):
    match direction:
        case "^":
            return ">"
        case ">":
            return"v" 
        case "v":
            return"<" 
        case "<":
            return"^" 
        case _:
            raise Exception("Direction not found")


def first_part():
    visited = set()
    direction = start_direction
    current = start_position
    while True:
        visited.add(current)
        change = get_change(direction)
        ahead = (current[0] + change[0], current[1] + change[1])
        if ahead[0] < 0 or ahead[0] >= len(map) or ahead[1] < 0 or ahead[1] >= len(map[0]):
            break
        if map[ahead[0]][ahead[1]] == "#":
            direction = get_new_direction(direction)
        else:
            current = ahead
    print(f"Number of visited positions is {len(visited)}")


def is_there_loop(current, direction):
    visited = set()
    while True:
        change = get_change(direction)
        ahead = (current[0] + change[0], current[1] + change[1])
        if ahead[0] < 0 or ahead[0] >= len(map) or ahead[1] < 0 or ahead[1] >= len(map[0]):
            break
        if map[ahead[0]][ahead[1]] == "#":
            if (ahead[0], ahead[1], direction) in visited:
                return True
            visited.add((ahead[0], ahead[1], direction))
            direction = get_new_direction(direction)
        else:
            current = ahead
    return False


def second_part():
#     current = start_position
    # direction = start_direction
    loop_causing_obstacle_positions = set()
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == ".":
                old = map[i][j]
                map[i][j] = "#"
                if is_there_loop(start_position, start_direction):
                    loop_causing_obstacle_positions.add((i, j))
                map[i][j] = old

    print(f"Number of possible new obstacles is {len(loop_causing_obstacle_positions)}")

map = []
directions = ["^", ">", "<", "v"]
with open("input.txt") as file:
    for line in file:
        map.append(list(line.strip()))
start_position = [(i, j) for i in range(len(map)) for j in range(len(map[i])) if map[i][j] in directions][0]
start_direction = map[start_position[0]][start_position[1]]

first_part()
second_part()
