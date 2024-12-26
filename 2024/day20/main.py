from collections import namedtuple,defaultdict

Position = namedtuple("Position", ["x", "y"])

def shortest_path(start, end, grid):
    queue = [(start, 0)]
    visited = set()
    while len(queue) > 0:
        current, seconds = queue.pop(0)
        visited.add(current)

        if current == end:
            return seconds
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0 ,-1)]:
            position = Position(current.x + dx, current.y + dy)
            if position.x < 0 or position.x >= len(grid):
                continue
            if position.y < 0 or position.y >= len(grid[0]):
                continue
            if grid[position.x][position.y] == "#":
                continue
            if position in visited:
                continue
            queue.append((position, seconds + 1))
    return None

def can_cheat_in_vertical(x, y, grid):
    if x - 1 < 0 or x + 1 >= len(grid):
        return False

    if grid[x-1][y] == "#" or grid[x+1][y] == "#":
        return False

    return True


def can_cheat_in_hozitontal(x, y, grid):
    if y - 1 < 0 or y + 1 >= len(grid[0]):
        return False

    if grid[x][y-1] == "#" or grid[x][y+1] == "#":
        return False

    return True


def get_walls_to_cheat(grid):
    walls = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "#" and (can_cheat_in_vertical(i,j,grid) or can_cheat_in_hozitontal(i,j,grid)):
                walls.append(Position(i, j))
    return walls


def first_part():
    grid = []
    with open("input.txt") as file:
        grid = [list(l.strip()) for l in file]
    for r in grid: print(r)

    start = [Position(i, j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == "S"][0]
    end = [Position(i, j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == "E"][0]

    max_ps = shortest_path(start, end, grid)
    walls_to_cheat = get_walls_to_cheat(grid)
    obstacles = sum(1 for r in grid for e in r if e == "#")
    print(f"I need to check {len(walls_to_cheat)}/{obstacles}")
    times = defaultdict(int)
    for i, wall in enumerate(walls_to_cheat):
        grid[wall.x][wall.y] = "."
        picoseconds = shortest_path(start, end, grid)
        if picoseconds is not None and (max_ps - picoseconds) >= 100:
            times[max_ps - picoseconds] += 1
        grid[wall.x][wall.y] = "#"
        print(f"Checkd {i}/{len(walls_to_cheat)}")
    print(f"There are {sum(v for v in times.values())} cheats that save 100ps or more")
    


first_part()

