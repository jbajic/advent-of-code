

def get_input():
    with open("input.txt") as file:
        return [list(line.strip()) for line in file] 


def falling_rocks(platform, direction):
    max_i = len(platform) 
    max_j = len(platform[0]) 

    match direction:
        case "N":
            for i in range(max_i):
                for j in range(max_j):
                    if platform[i][j] == "O":
                        falling_i = i
                        has_fallen = False
                        while falling_i > 0 and platform[falling_i -1][j] == ".":
                            falling_i -= 1
                            has_fallen = True

                        if has_fallen:
                            platform[i][j] = "."
                            platform[falling_i][j] = "O"
        case "S":
            for i in reversed(range(max_i)):
                for j in range(max_j):
                    if platform[i][j] == "O":
                        falling_i = i
                        has_fallen = False
                        while falling_i < max_i - 1 and platform[falling_i + 1][j] == ".":
                            falling_i += 1
                            has_fallen = True

                        if has_fallen:
                            platform[i][j] = "."
                            platform[falling_i][j] = "O"
        case "E":
            for i in range(max_i):
                for j in reversed(range(max_j)):
                    if platform[i][j] == "O":
                        falling_j = j
                        has_fallen = False
                        while falling_j < max_j - 1 and platform[i][falling_j + 1] == ".":
                            falling_j += 1
                            has_fallen = True

                        if has_fallen:
                            platform[i][j] = "."
                            platform[i][falling_j] = "O"
        case "W":
            for i in range(max_i):
                for j in range(max_j):
                    if platform[i][j] == "O":
                        falling_j = j
                        has_fallen = False
                        while falling_j > 0 and platform[i][falling_j - 1] == ".":
                            falling_j -= 1
                            has_fallen = True

                        if has_fallen:
                            platform[i][j] = "."
                            platform[i][falling_j] = "O"

        case _:
            raise Exception(f"Direction {direction} not found")

 

def sum_weight(platform):
    max_i = len(platform) 
    max_j = len(platform[0]) 

    sum = 0
    for i in range(max_i):
        for j in range(max_j):
            if platform[i][j] == "O":
                sum += max_i - i

    return sum


def first():
    platform = get_input()
    for i in platform:
        print(i)

    print()
    falling_rocks(platform, "N")

    sum = sum_weight(platform)
    print(f"Rock weight sum is {sum}")



def second():
    platform = get_input()
    NUMBER_OF_CYCLES = 1000000000

    weights = []
    cycle_group = None
    for _ in range(NUMBER_OF_CYCLES):
        falling_rocks(platform, "N")
        weight_n = sum_weight(platform)

        falling_rocks(platform, "W")
        weight_w = sum_weight(platform)

        falling_rocks(platform, "S")
        weight_s = sum_weight(platform)

        falling_rocks(platform, "E")
        weight_e = sum_weight(platform)

        weight_group = (weight_n, weight_w, weight_s, weight_e)
        if weight_group in weights:
            cycle_group = weight_group
            break
        weights.append(weight_group)

    cycles_after_begin = weights.index(cycle_group)
    loop_length = len(weights) - weights.index(cycle_group)

    index_at_cycles_end = (NUMBER_OF_CYCLES - cycles_after_begin) % loop_length
    loop_groups = weights[weights.index(cycle_group):]
    last_weight = loop_groups[index_at_cycles_end-1][3]

    print(f"Rock weight sum after {NUMBER_OF_CYCLES} cycles is {last_weight}")


first()
second()
