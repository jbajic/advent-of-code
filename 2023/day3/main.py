def get_engine_schematic():
    with open("input.txt") as file:
        rows = []
        for l in file:
            rows.append(list(l.strip()))
        return rows

def is_safe(MAX_X, MAX_Y, i, j):
    return i >= 0 and i < MAX_X and j >= 0 and j < MAX_Y

def first():
    rows = get_engine_schematic()
    nums = []
    MAX_X = len(rows[0])
    MAX_Y = len(rows)

    current_include = False
    current_num = None
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            if c.isdigit():
                if current_num is None:
                    current_num = c
                else:
                    current_num += c

                if not current_include and current_num is not None:
                    for a in [1, 0, -1]:
                        for b in [1, 0, -1]:
                            check_i = i + a
                            check_j = j + b
                            if is_safe(MAX_X, MAX_Y, check_i, check_j) and (rows[check_i][check_j] != "." and not rows[check_i][check_j].isdigit()):
                                current_include = True
                                break
                        if current_include:
                            break

            elif current_num is not None:
                if current_include:
                    nums.append(int(current_num))
                current_num = None
                current_include = False
    print(sum(nums))


def get_numbers(rows, i, j):
    MAX_X = len(rows[0])
    MAX_Y = len(rows)

    nums = []
    for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
            check_i = i + a
            check_j = j + b
            if is_safe(MAX_X, MAX_Y, check_i, check_j) and rows[check_i][check_j].isdigit(): 
                print(f"Checking {rows[check_i][check_j]}")
                num_start = check_j
                # Find start
                while num_start > 0 and rows[check_i][num_start - 1].isdigit():
                    num_start -= 1
                # If it is the same number cancel
                if any(num[0] == (check_i, num_start) for num in nums):
                    print(f"Same start at {num_start}")
                    break
                # Get num
                current_num = rows[check_i][num_start]
                num_current = num_start + 1
                while num_current < MAX_X and (c := rows[check_i][num_current]).isdigit():
                    current_num += c
                    num_current += 1
                nums.append(((check_i, num_start), int(current_num)))

    return [num[1] for num in nums]


def second():
    rows = get_engine_schematic()
    nums = []

    gear_rations = []
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            if c == "*":
                # Found gear look for numbers
                nums = get_numbers(rows, i, j)
                print(f"Nums are {nums}")
                if len(nums) == 2:
                    gear_rations.append(nums[0] * nums[1])
                else:
                    print(f"There are no two numbers in gear {nums}")
    return sum(gear_rations)



print(f"First: {first()}")
print(f"Second: {second()}")

