from collections import namedtuple
from heapq import heappush, heappop


maze = []
with open("input.txt") as file:
    maze = [list(line.strip()) for line in file]

Position = namedtuple("Position", ["x", "y"])


def get_directions(dir):
    match dir:
        case "N":
            return [("N", 1), ("W", 1001), ("E", 1001)]
        case "E":
            return [("E", 1), ("N", 1001), ("S", 1001)]
        case "S":
            return [("S", 1), ("W", 1001), ("E", 1001)]
        case "W":
            return [("W", 1), ("N", 1001), ("S", 1001)]
        case _:
            raise Exception("Position not found")


def get_new_position(current, dir):
    match dir:
        case "N":
            return Position(current.x - 1, current.y)
        case "E":
            return Position(current.x, current.y + 1)
        case "S":
            return Position(current.x + 1, current.y)
        case "W":
            return Position(current.x, current.y - 1)
        case _:
            raise Exception("Position not found")


def first_part():
    min_score = get_min_score()
    print(f"Min score is {min_score}")

def get_min_score():
    start = [
        (i, j)
        for i in range(len(maze))
        for j in range(len(maze[i]))
        if maze[i][j] == "S"
    ][0]

    min_heap = []
    heappush(min_heap, (0, Position(start[0], start[1]), "E"))
    min_score = None
    visited = dict()
    while len(min_heap) > 0:
        current_score, current_pos, current_direction = heappop(min_heap)
        assert (
            maze[current_pos.x][current_pos.y] in [".", "E", "S"]
        ), f"Current position is ({current_pos.x}, {current_pos.y}) = {maze[current_pos.x][current_pos.y]}"
        visited[(current_pos, current_direction)] = current_score
        if maze[current_pos.x][current_pos.y] == "E":
            # print(f"Min score is {current_score} at position {current_pos}")
            if min_score is None:
                min_score = current_score
            else:
                min_score = min(min_score, current_score)

        for new_direction, new_score in get_directions(current_direction):
            new_position = get_new_position(current_pos, new_direction)
            added_score = new_score + current_score
            if (new_position, new_direction) in visited:
                if added_score > visited[(new_position, new_direction)]:
                    continue
                visited[(new_position, new_direction)] = added_score
            if maze[new_position.x][new_position.y] not in ["S", "#"]:
                heappush(min_heap, (added_score, new_position, new_direction))

    return min_score


def find_best_points(start_pos, end, backtrack_map, best_spots):
    current = end
    while current[0] != start_pos:
        best_spots.add(current[0])
        current = backtrack_map[current]


def second_part():
    start = [
        (i, j)
        for i in range(len(maze))
        for j in range(len(maze[i]))
        if maze[i][j] == "S"
    ][0]
    end = [
        (i, j)
        for i in range(len(maze))
        for j in range(len(maze[i]))
        if maze[i][j] == "E"
    ][0]

    min_score = get_min_score()

    start_pos = Position(start[0], start[1])
    end_pos = Position(end[0], end[1])
    visited = dict()
    stack = [(0, start_pos, "E")]
    best_spots = set()
    backtrack_map = dict()
    while len(stack) > 0:
        current_score, current_pos, current_direction = stack.pop()
        # current_score, current_pos, current_direction = heappop(min_heap)
        assert (
            maze[current_pos.x][current_pos.y] in [".", "E", "S"]
        ), f"Current position is ({current_pos.x}, {current_pos.y}) = {maze[current_pos.x][current_pos.y]}"
        visited[(current_pos, current_direction)] = current_score
        if maze[current_pos.x][current_pos.y] == "E":
            if current_score == min_score:
                assert (
                    current_pos,
                    current_direction,
                    current_score,
                ) in backtrack_map, f"End must be in backtrack map"
                find_best_points(
                    start_pos,
                    (end_pos, current_direction, current_score),
                    backtrack_map,
                    best_spots,
                )

        for new_direction, new_score in get_directions(current_direction):
            new_position = get_new_position(current_pos, new_direction)
            added_score = new_score + current_score

            if (new_position, new_direction) in visited:
                if added_score > visited[(new_position, new_direction)]:
                    continue
                visited[(new_position, new_direction)] = added_score
            if added_score > min_score:
                continue

            if maze[new_position.x][new_position.y] not in ["S", "#"]:
                # heappush(min_heap, (added_score, new_position, new_direction))
                stack.append((added_score, new_position, new_direction))
                backtrack_map[(new_position, new_direction, added_score)] = (
                    current_pos,
                    current_direction,
                    current_score,
                )
                assert any(
                    v[0] == start_pos for v in backtrack_map.values()
                ), "There must be a start in backtrack map"

    print(f"On best path of score {min_score} there are {len(best_spots) + 1} points")


first_part()
second_part()
