from functools import cache

def first_part():
    stones = []
    with open("input.txt") as file:
        stones = list(map(int, file.readline().strip().split()))

    blinks = 25
    for _ in range(blinks):
        new_stones = []
        for stone in stones:
            stingified_stone = str(stone)
            if stone == 0:
                new_stones.append(1)
            elif len(stingified_stone) % 2 == 0 and stone != 1:
                left = int(stingified_stone[0:len(stingified_stone) // 2])
                right = int(stingified_stone[len(stingified_stone) // 2:])
                new_stones.append(left)
                new_stones.append(right)
            else:
                new_stones.append(stone * 2024)
        
        stones = new_stones
    print(f"Number of stones is {len(stones)}")


@cache
def get_number_of_stone_per_blink(stone, blink):
    stingified_stone = str(stone)
    new_stones = []
    if blink == 0:
        return 1
    stingified_stone = str(stone)
    if stone == 0:
        new_stones.append(1)
    elif len(stingified_stone) % 2 == 0 and stone != 1:
        left = int(stingified_stone[0:len(stingified_stone) // 2])
        right = int(stingified_stone[len(stingified_stone) // 2:])
        new_stones.append(left)
        new_stones.append(right)
    else:
        new_stones.append(stone * 2024)

    return sum(get_number_of_stone_per_blink(new_stone, blink-1) for new_stone in new_stones)

def second_part():
    stones = []
    with open("input.txt") as file:
        stones = list(map(int, file.readline().strip().split()))

    blinks = 75
    num_of_stones = 0
    print(stones)
    for stone in stones:
        new = get_number_of_stone_per_blink(stone, blinks)
        num_of_stones += new
    print(f"Number of stones is {num_of_stones}")


first_part()
second_part()
