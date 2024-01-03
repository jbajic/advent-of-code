def get_input():
    with open("input.txt") as file:
        return file.readline().strip().split(",")


def calculate_hash_value(s):
    current_value = 0
    for e in s:
        current_value += ord(e)
        current_value = current_value * 17
        current_value = current_value % 256

    return current_value


def first():
    input = get_input()
    s = sum(calculate_hash_value(step) for step in input)
    print(f"Total sum is {s}")


def second():
    input = get_input() 

    boxes = [[] for _ in range(256)]
    for step in input:
        remove = False
        if "-" in step:
            remove = True
        label, num = step.split("-") if remove else step.split("=")
        box_num = calculate_hash_value(label)

        index_in_box = next(iter(i for i, lens in enumerate(boxes[box_num]) if lens[0] == label), None)
        if remove:
            if index_in_box is not None:
                print("Popping")
                boxes[box_num].pop(index_in_box)
        else:
            if index_in_box is not None:
                boxes[box_num][index_in_box] = (label, int(num))
            else:
                boxes[box_num].append((label, int(num)))

    for i, box in enumerate(boxes):
        if box:
            print(f"Box {i}: {box}")
    resulting_focus_power = 0
    for box_num, box in enumerate(boxes):
        for i in range(len(box)):
            resulting_focus_power += (box_num + 1) * box[i][1] * (i+1)
    print(f"Resulting power is {resulting_focus_power}")



# first()
second()
