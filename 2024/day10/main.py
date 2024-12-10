def first_part():
    hike_map = []
    with open("input.txt") as file:
        hike_map = [list(map(lambda x: int(x) if x.isdigit() else x, line.strip())) for line in file]
    print(hike_map)

    trailheads = [(i, j) for i in range(len(hike_map)) for j in range(len(hike_map[i])) if hike_map[i][j] == 0]
    score = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for trailhead in trailheads:
        local_score = 0
        positions = [trailhead]
        visited_tops = set()
        while len(positions) > 0:
            current = positions.pop()
            current_value = hike_map[current[0]][current[1]] 
            if current_value == 9:
                if current not in visited_tops:
                    local_score += 1
                visited_tops.add(current)
                continue

            for d1, d2 in directions:
                new_current = (current[0] + d1, current[1] + d2)
                if new_current[0] < 0 or new_current[0] >= len(hike_map):
                    continue
                if new_current[1] < 0 or new_current[1] >= len(hike_map[0]):
                    continue
                new_current_value = hike_map[new_current[0]][new_current[1]]
                if isinstance(new_current_value, int) and new_current_value - current_value == 1:
                    positions.append(new_current)

        score += local_score
    
    print(f"Position found that reach top: {score}")



def second_part():
    hike_map = []
    with open("input.txt") as file:
        hike_map = [list(map(lambda x: int(x) if x.isdigit() else x, line.strip())) for line in file]
    print(hike_map)

    trailheads = [(i, j) for i in range(len(hike_map)) for j in range(len(hike_map[i])) if hike_map[i][j] == 0]
    score = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for trailhead in trailheads:
        local_score = 0
        positions = [trailhead]
        while len(positions) > 0:
            current = positions.pop()
            current_value = hike_map[current[0]][current[1]] 
            if current_value == 9:
                local_score += 1
                continue

            for d1, d2 in directions:
                new_current = (current[0] + d1, current[1] + d2)
                if new_current[0] < 0 or new_current[0] >= len(hike_map):
                    continue
                if new_current[1] < 0 or new_current[1] >= len(hike_map[0]):
                    continue
                new_current_value = hike_map[new_current[0]][new_current[1]]
                if isinstance(new_current_value, int) and new_current_value - current_value == 1:
                    positions.append(new_current)

        score += local_score
    
    print(f"Position found that reach top: {score}")



first_part()
second_part()
