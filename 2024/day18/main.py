from collections import namedtuple
import heapq


Position = namedtuple("Position", ["x", "y"])

def manhattan_dist(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def first_part():
    incoming_bytes = []
    with open("input.txt") as file:
        incoming_bytes = [Position(*tuple(map(int, line.strip().split(",")))) for line in file]

    print(incoming_bytes)
    WIDTH = 71
    HEIGHT = 71
    CORRUPTED_BYTES = 1024
    grid = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for i in range(CORRUPTED_BYTES):
        grid[incoming_bytes[i].y][incoming_bytes[i].x] = "#"

    for r in grid: print(r)

    end_position = Position(WIDTH - 1, HEIGHT - 1)
    heap = []
    heapq.heappush(heap, (0, Position(0, 0), 0))
    min_steps = None
    visited = set()
    while len(heap) > 0:
        _, current, steps = heapq.heappop(heap)
        visited.add(current)
        if current == end_position: 
            print(f"{current} at {steps} and")
            print(f"Found it!")
            min_steps = steps
            break
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_position = Position(current.x + dx, current.y + dy)
            if new_position.x < 0 or new_position.x >= WIDTH:
                continue
            if new_position.y < 0 or new_position.y >= HEIGHT:
                continue
            if grid[new_position.y][new_position.x] == "#":
                continue
            if new_position in visited:
                continue

            score = manhattan_dist(new_position, end_position) + steps + 1
            visited.add(new_position)
            heapq.heappush(heap, (score, new_position, steps + 1))

    print(f"Min amount if steps {min_steps}")

first_part()
