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
        case "<":
            return"^" 
        case "v":
            return"<" 
        case _:
            raise Exception("Direction not found")



def first_part():
    map = []
    directions = ["^", ">", "<", "v"]
    with open("input.txt") as file:
        for line in file:
            map.append(line.strip())
    start_position = [(i, j) for i in range(len(map)) for j in range(len(map[i])) if map[i][j] in directions][0]
    print(start_position)

    visited = set()
    direction = map[start_position[0]][start_position[1]]
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


first_part()
