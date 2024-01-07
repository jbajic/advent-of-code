import heapq as h


def get_input():
    with open("input.txt") as file:
        return [list(map(int, line.strip())) for line in file]


def is_opposite(lhs, rhs):
    match lhs:
        case "N":
            return rhs == "S"
        case "S":
            return rhs == "N"
        case "E":
            return rhs == "W"
        case "W":
            return rhs == "E"


def first():
    input = get_input()
    DIRECTIONS = [(-1, 0, "N"), (1, 0, "S"), (0, -1, "W"), (0, 1, "E")]

    max_i = len(input)
    max_j = len(input[0])
    end = (len(input) - 1, len(input[0]) - 1)
    queue = [(0, (0, 0), 1, "S")]
    queue = [(0, (0, 0), 1, "E")]

    visited = set()
    while queue:
        cost, pos, progress, dir = h.heappop(queue)

        if pos[0] == end[0] and pos[1] == end[1]:
            print(f"Min heat cost is {cost}")
            break

        if (pos, progress, dir) in visited:
            continue

        visited.add((pos, progress, dir))

        for i, j, d in DIRECTIONS:

            if is_opposite(d, dir):
                continue

            new_i = pos[0] + i
            new_j = pos[1] + j

            if new_i < 0 or new_i >= max_i or new_j < 0 or new_j >= max_j:
                continue

            if d == dir and progress + 1 > 3:
                continue

            # new_progress = 1 if dir != d else progress + 1
            new_progress = progress + 1 if dir == d else 1
            new_cost = cost + input[new_i][new_j]
            new_node = (new_cost, (new_i, new_j), new_progress, d)
            h.heappush(queue, new_node)



first()
