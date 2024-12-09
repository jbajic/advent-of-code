from collections import namedtuple


def first_part():
    disk_map = None
    with open("input.txt") as file:
        disk_map = list(map(int, file.readline().strip()))
    expand = []
    file_index = 0
    for i, space in enumerate(disk_map):
        if i % 2 == 0:
            expand.extend([file_index for _ in range(space)])
            file_index += 1
        else:
            expand.extend(["." for _ in range(space)])

    left = 0
    right = len(expand) - 1
    while right > left:
        if expand[left] == "." and expand[right] != ".":
            expand[left], expand[right] = expand[right], expand[left]
        if expand[left] != ".":
            left += 1
        if expand[right] == ".":
            right -= 1
    checksum = 0
    for i, file_index in enumerate(expand):
        if file_index != ".":
            checksum += i * file_index
    print(f"File checksum is {checksum}")

Entry = namedtuple("Entry", ["id", "count"])

def second_part():
    disk_map = None
    with open("input.txt") as file:
    # with open("input2.txt") as file:
        disk_map = list(map(int, file.readline().strip()))
    expand = []
    file_index = 0
    for i, space in enumerate(disk_map):
        if i % 2 == 0:
            expand.extend([file_index for _ in range(space)])
            file_index += 1
        else:
            expand.extend(["." for _ in range(space)])

    print(expand)
    expand_map = []
    current_elem = None
    current_count = 0
    old_expand_size = len(expand)
    for elem in expand:
        if current_elem is None:
            current_elem = elem
            current_count += 1
        elif elem == current_elem:
            current_count += 1
        else:
            expand_map.append(Entry(current_elem, current_count))
            current_elem = elem
            current_count = 1

    expand_map.append(Entry(current_elem, current_count))

    right = len(expand_map) - 1
    while True:
        left = 0
        current_right_id = None
        print(f"While true {right}")
        while right > left:
            if expand_map[left].id != ".":
                left += 1

            if expand_map[right].id == ".":
                right -= 1

            if expand_map[left].id == "." and expand_map[right].id != ".":
                assert(current_right_id is None or current_right_id == expand_map[right].id), "Can process single right in a loop"
                current_right_id = expand_map[right].id
                if expand_map[left].count >= expand_map[right].count:
                    # seen_ids.add(expand_map[right].id)
                    insert_id = expand_map[right].id
                    insert_count = expand_map[right].count 

                    expand_map[left] = Entry(".", expand_map[left].count - insert_count)
                    expand_map[right] = Entry(".", insert_count)
                    expand_map.insert(left, Entry(insert_id, insert_count))

                    right += 1
                    break
                left += 1

        right -= 1
        if right == 0:
            break

    expand = []
    for id, num in expand_map:
        expand.extend([id for _ in range(num)])
    assert(len(expand) == old_expand_size)

    checksum = 0
    for i, file_index in enumerate(expand):
        if file_index != ".":
            checksum += i * file_index

    print(f"File checksum is {checksum}")


first_part()
second_part()
