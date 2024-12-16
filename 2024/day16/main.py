from collections import namedtuple
from heapq import heappush, heappop, heapify


maze = []
with open("input.txt") as file:
    maze = [list(line.strip()) for line in file]

visited = set()

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
    for m in maze:
        print(m)
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
            print(f"Min score is {current_score} at position {current_pos}")
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

    print(f"Min score is {min_score}")


first_part()
