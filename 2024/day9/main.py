def first_part():
    disk_map = None
    with open("input.txt") as file:
        disk_map = list(map(int, file.readline().strip()))
    print(disk_map)
    expand = []
    file_index = 0
    for i, space in enumerate(disk_map):
        if i % 2 == 0:
            expand.extend([file_index for _ in range(space)])
            file_index += 1
        else:
            expand.extend(["." for _ in range(space)])
    print(expand)

    left = 0
    right = len(expand) - 1
    while right > left:
        if expand[left] == "." and expand[right] != ".":
            expand[left], expand[right] = expand[right], expand[left]
        if expand[left] != ".":
            left += 1
        if expand[right] == ".":
            right -= 1
    print(expand)
    checksum = 0
    for i, file_index in enumerate(expand):
        if file_index != ".":
            checksum += i * file_index
    print(f"File checksum is {checksum}")

first_part()

