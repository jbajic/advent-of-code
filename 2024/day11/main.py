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


first_part()
