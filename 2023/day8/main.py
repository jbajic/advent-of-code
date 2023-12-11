from functools import reduce


def get_map():
    with open("input.txt") as file:
        lines = file.readlines()

        map = dict()
        for line in lines[2:]:
            source, choices = line.split("=")
            left, right = choices.strip()[1:-1].split(", ")
            map[source.strip()] = (left, right)
        return map


def get_directions():
    with open("input.txt") as file:
        lines = file.readlines()
        return lines[0].strip()


def first():
    map = get_map()
    direction = get_directions()
    current = "AAA"
    current_direction = 0
    steps = 0

    while current != "ZZZ":
        steps += 1

        if direction[current_direction] == "L":
            current = map[current][0]
        else:
            current = map[current][1]
        if current_direction == len(direction) - 1:
            current_direction = 0
        else:
            current_direction += 1
    print(f"Number of steps to reach end {steps}")


def get_lcm(nums):
    from math import lcm
    return lcm(*list(nums))


def second():
    map = get_map()
    direction = get_directions()
    current_direction = 0
    start_nodes = [node for node in map.keys() if node[-1] == "A"]
    ending_nodes = {node: [] for node in map.keys() if node[-1] == "Z"}
    
    for start_node in start_nodes:
        current_node = start_node
        step = 0
 
        while True:
            step += 1
            if direction[current_direction] == "L":
                current_node = map[current_node][0]
            else:
                current_node = map[current_node][1]
            if current_direction == len(direction) - 1:
                current_direction = 0
            else:
                current_direction += 1
            
            if current_node[-1] == "Z":
                if any(start_node_steps["start_node"] == start_node for start_node_steps in ending_nodes[current_node]):
                    break
                else:
                    ending_nodes[current_node].append({"start_node": start_node, "steps": step})

    start_nodes_min = {start_node: 0 for start_node in start_nodes}
    for start_node in start_nodes:
        min_steps = None
        for _, pairs in ending_nodes.items():
            steps = next((checkpoint for checkpoint in pairs if checkpoint["start_node"] == start_node), None) 
            if steps:
                steps = steps["steps"]
                if min_steps is None:
                    min_steps = steps
                else:
                    min_steps = min(min_steps, steps)
        start_nodes_min[start_node] = min_steps

    lcm = get_lcm(start_nodes_min.values())

    print(f"LCM {lcm}")


first()
second()
