from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    data: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def parse_tree(string: str) -> Node:
    if string[0] != "[":
        return Node(int(string), None, None)

    level = 0
    for i, elem in enumerate(string):
        if elem == "[":
            level += 1
        if elem == "]":
            level -= 1

        if elem == "," and level == 1:
            return Node(-1, parse_tree(string[1:i]), parse_tree(string[i+1:-1]))
    assert False


def print_tree(node: Node, depth: int = 0) -> None:
    if depth == 0:
        print()
    print(f"{' ' * depth}{node.data if node.data >= 0 else '*'}")
    if node.left is not None:
        print_tree(node.left, depth + 1)
    if node.right is not None:
        print_tree(node.right, depth + 1)


index = 0


def find_explode(node: Node, depth: int = 0) -> int:
    global index
    if depth == 4 and node.data < 0:
        return index

    if node.data >= 0:
        index += 1
        return -1

    left = find_explode(node.left, depth + 1)
    if left >= 0:
        return left

    return find_explode(node.right, depth + 1)


def list_values(node):
    if node is None:
        return []
    if node.data >= 0:
        return [node.data]
    return list_values(node.left) + list_values(node.right)


exploded = False


def explode(node: Node, explode_index: int, explode_values):
    global index
    global exploded

    if node.data >= 0:
        if index == explode_index - 1:
            node.data += explode_values[0]
        elif index == explode_index + 2:
            node.data += explode_values[1]
        index += 1
        return
    explode(node.left, explode_index, explode_values)
    explode(node.right, explode_index, explode_values)

    if not exploded and index == explode_index + 2:
        node.data = 0
        node.left = node.right = None
        exploded = True


def do_split(node: Node):
    if node is None:
        return False
    if node.data >= 0:
        if node.data >= 10:
            node.left = Node(node.data // 2)
            node.right = Node((node.data + 1) // 2)
            node.data = -1
            return True
        return False
    if do_split(node.left):
        return True
    return do_split(node.right)


def clean(node):
    global index
    global exploded
    while True:
        index = 0
        explode_index = find_explode(node)
        if explode_index >= 0:
            values = list_values(node)
            index = 0
            exploded = False
            explode(node, explode_index, (values[explode_index], values[explode_index + 1]))
            continue
        index = 0
        if do_split(node):
            print_tree(node)
            continue
        break


def add(lhs: Node, rhs: Node):
    return Node(-1, lhs, rhs)


def magnitude(node: Node):
    if node is None:
        return 0
    if node.data >= 0:
        return node.data
    return 3 * magnitude(node.left) + 2 * magnitude(node.right)


def main() -> None:
    with open("input.txt") as input:
        lines = [l.strip() for l in input.readlines()]
        tree = parse_tree(lines[0])
        for line in lines[1:]:
            tree = add(tree, parse_tree(line))
            clean(tree)
        # print_tree(tree)
        print(magnitude(tree))
        max = 0
        for i in range(len(lines)):
            for j in range(len(lines)):
                if i == j:
                    continue
                tree = add(parse_tree(lines[i]), parse_tree(lines[j]))
                clean(tree)
                value = magnitude(tree)
                if value > max:
                    max = value
        print(f"Max: {max}")



if __name__ == "__main__":
    main()
