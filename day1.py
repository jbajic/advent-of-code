# Puzzle 1
with open("input.txt", "r") as input:
    counter = 0
    previous_value = None
    for line in input:
        if previous_value is None:
            previous_value = int(line)
            continue
        if int(line) > previous_value:
            counter += 1
        previous_value = int(line)
    print(counter)


# Puzzle 2
with open("input.txt", "r") as input:
    counter = 0
    previous_value = None
    lines = input.readlines()
    for index in range(len(lines) - 3):
        sliding_win_1 = [int(line) for line in lines[index : index + 3]]
        sliding_win_2 = [int(line) for line in lines[index +1 : index + 4]]
        if sum(sliding_win_2) > sum(sliding_win_1):
            counter += 1
    print(counter)

