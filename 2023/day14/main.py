def get_input():
    with open("input.txt") as file:
        return [list(line.strip()) for line in file] 


def falling_rocks(platform, direction):
    max_i = len(platform) 
    max_j = len(platform[0]) 

    # Falling to the north
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
 

def sum_weight(platform, direction):
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

    sum = sum_weight(platform, "N")
    print(f"Rock weight sum is {sum}")


first()
second()
