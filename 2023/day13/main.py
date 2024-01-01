def get_patterns():
    patterns = []
    pattern = []
    with open("input.txt") as file:
        for line in file:
            if line == "\n":
                patterns.append(pattern)
                pattern = []
            else:
                pattern.append(line.strip())

    if pattern:
        patterns.append(pattern)

    return patterns


def first():
    patterns = get_patterns()

    line_summed_up = 0
    for pattern in patterns:
        max_i = len(pattern)
        max_j = len(pattern[0])

        print(f"Max i: {max_i} max j : {max_j}")
        found = False
        # This is a vertical mirror
        for j in range(1, max_j):
            iter_max = min(j, max_j - j)
            if all(pattern[k][j + i] == pattern[k][j - i - 1] for i in range(iter_max) for k in range(max_i)):
                line_summed_up += j
                found = True
                break

        if found:
            continue
        # This is a horizontal mirror
        for i in range(1, max_i):
            print(f"Current {i}")
            iter_max = min(i, max_i - i)
            for a in range(iter_max):
                for b in range(max_j):
                    # print(f"Comparing ({i+a+1}, {b}) ==  ({i-a}, {b})")
                    x = pattern[i + a][b]
                    y = pattern[i - a-1][b]
                    # print(f"Comparing {x}) == {y}")
            print(f"Horizontal Iter max {iter_max}")
            if all(pattern[i + j][k] == pattern[i - j - 1][k] for j in range(iter_max) for k in range(max_j)):
                print(f"Found horizontal line {i}")
                line_summed_up += i * 100
                found = True
                break
        assert(found), "Mirror had to be found"

    print(f"Sum of all lines {line_summed_up}")

                

first()
