def get_input():
    with open("input.txt") as file:
        instructions = []
        for line in file:
            dir, amount, color = line.strip().split()
            instructions.append((dir, int(amount), color[1:-1]))
        return instructions


def first():
    instructions = get_input()
    
    max_i, min_i = 0, 0
    max_j, min_j = 0, 0
    current_stop = (0,0)
    points = []
    for instruction in instructions:
        new_i = current_stop[0]
        new_j = current_stop[1]

        match instruction[0]:
            case "U":
                new_i -= instruction[1]
                min_i = min(new_i, min_i)
            case "D":
                new_i += instruction[1]
                max_i = max(new_i, max_i)
            case "R":
                new_j += instruction[1]
                max_j = max(new_j, max_j)
            case "L":
                new_j -= instruction[1]
                min_j = min(new_j, min_j)
 
        if current_stop[0] != new_i:
            step = 1
            if current_stop[0] > new_i:
                step = -1
            for k in range(current_stop[0], new_i, step):
                points.append((k, current_stop[1]))
        elif current_stop[1] != new_j:
            step = 1
            if current_stop[1] > new_j:
                step = -1
            for k in range(current_stop[1], new_j, step):
                points.append((current_stop[0], k))

#         if current_stop not in points:
            # points.append(current_stop)
        current_stop = (new_i, new_j)

    if min_i < 0 or min_j < 0:
        new_points = []
        offset_i = abs(min_i) if min_i < 0 else 0
        offset_j = abs(min_j) if min_j < 0 else 0
        max_i = max_i + offset_i
        max_j = max_j + offset_j
        for point in points:
            new_points.append((point[0] + offset_i, point[1] + offset_j))

        assert(len(points) == len(new_points))
        points = new_points

    # Shoelace formula
    area = 0
    num_of_points = len(points)
    for i, point in enumerate(points):
        area += point[0] * (points[(i+1) % num_of_points][1] - points[i-1][1])
    area /= 2
    area = abs(area)

    # Picks theorem
    # A = i + b/2 - 1, (i is interior points, b boundary points)
    interior_points = int(area) + 1 - len(points) / 2

    cubis_metres = interior_points + len(points)
    print(f"Number of cubic metres is {cubis_metres}")


def get_direction(d):
    match d:
        case "0":
            return "R"
        case "1":
            return "D"
        case "2":
            return "L"
        case "3":
            return "U"
        case _: raise Exception(f"Direction {d} not found")


def second():
    instructions = get_input()
    
    max_i, min_i = 0, 0
    max_j, min_j = 0, 0
    current_stop = (0,0)
    points = []
    all_boundary_points = 0
    for instruction in instructions:
        new_i = current_stop[0]
        new_j = current_stop[1]

        dist = int(instruction[2][1:6], 16)
        direction = get_direction(instruction[2][6:])
        match direction:
            case "U":
                new_i -= dist
                min_i = min(new_i, min_i)
            case "D":
                new_i += dist
                max_i = max(new_i, max_i)
            case "R":
                new_j += dist
                max_j = max(new_j, max_j)
            case "L":
                new_j -= dist
                min_j = min(new_j, min_j)
        all_boundary_points += dist        
        points.append(current_stop)
        current_stop = (new_i, new_j)
    
    if min_i < 0 or min_j < 0:
        new_points = []
        offset_i = abs(min_i) if min_i < 0 else 0
        offset_j = abs(min_j) if min_j < 0 else 0
        max_i = max_i + offset_i
        max_j = max_j + offset_j
        for point in points:
            new_points.append((point[0] + offset_i, point[1] + offset_j))

        assert(len(points) == len(new_points))
        points = new_points

    # Shoelace formula
    area = 0
    num_of_points = len(points)
    for i, point in enumerate(points):
        area += point[0] * (points[(i+1) % num_of_points][1] - points[i-1][1])
    area /= 2
    area = abs(area)

    # Picks theorem
    # A = i + b/2 - 1, (i is interior points, b boundary points)
    interior_points = int(area) + 1 - all_boundary_points / 2

    cubis_metres = interior_points + all_boundary_points
    print(f"Number of cubic metres with hex coords is {cubis_metres}")
 

first()
second()
