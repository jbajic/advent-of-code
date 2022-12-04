from functools import reduce

braces = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}
scores1 = {")": 3, "]": 57, "}": 1197, ">": 25137}
scores2 = {"(": 1, "[": 2, "{": 3, "<": 4}


def puzzle1():
    score = 0
    with open("input.txt") as input:
        stack = []
        for line in input.readlines():
            for char in line:
                if char in ["\n"]:
                    continue
                if char in braces.values():
                    stack.append(char)
                else:
                    popped = stack.pop()
                    if popped != braces[char]:
                        score += scores1[char]
                        break
    print(score)


def is_correct(line):
    stack = []
    for char in line:
        if char in ["\n"]:
            continue
        if char in braces.values():
            stack.append(char)
        elif stack:
            popped = stack.pop()
            if popped != braces[char]:
                return False
    return True


def puzzle2():
    scores = []
    with open("input.txt") as input:
        for line in [l for l in input.readlines() if is_correct(l)]:
            stack = []
            for char in line:
                if char in ["\n"]:
                    continue
                if char in braces.values():
                    stack.append(char)
                elif stack:
                    stack.pop()
            if stack:
                print(f"Line needs to be finished for {stack} of {len(stack)}")
                s = 0
                for elem in stack[::-1]:
                    s = s * 5 + scores2[elem]
                scores.append(s)
                print(f"Sum is {s}")
    print(f"Middle score is: {sorted(scores)[len(scores) // 2]}")


def main():
    # puzzle1()
    puzzle2()


if __name__ == "__main__":
    main()
