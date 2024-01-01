def get_patterns():
    patterns = []
    pattern = []
    with open("input.txt") as file:
        for line in file:
            if line == "\n":
                patterns.append(pattern)
                pattern = []
            else:
                pattern.append(list(line.strip()))

    if pattern:
        patterns.append(pattern)

    return patterns


def first():
    patterns = get_patterns()

    line_summed_up = 0
    for pattern in patterns:
        max_i = len(pattern)
        max_j = len(pattern[0])

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
            iter_max = min(i, max_i - i)
            if all(pattern[i + j][k] == pattern[i - j - 1][k] for j in range(iter_max) for k in range(max_j)):
                line_summed_up += i * 100
                found = True
                break
        assert(found), "Mirror had to be found"

    print(f"Sum of all lines {line_summed_up}")


def levenstein_dist(a, b):
    assert(len(a) == len(b))
    return sum(1 for x, y in zip(a,b) if x != y)

                
def second():
    patterns = get_patterns()

    line_summed_up = 0
    for pattern in patterns:
        max_i = len(pattern)
        max_j = len(pattern[0])

        found = False
        # This is a vertical mirror
        for j in range(1, max_j):
            smudges = 0
            
            iter_max = min(j, max_j - j)
            for i in range(iter_max):
                left_column = [pattern[k][j-i-1] for k in range(max_i)]
                right_column = [pattern[k][j+i] for k in range(max_i)]
                smudges += levenstein_dist(left_column, right_column)
                if smudges > 1:
                    break

            if smudges == 1:
                line_summed_up += j
                found = True
                break

        # This is a horizontal mirror
        if found:
            continue
        for i in range(1, max_i):
            smudges = 0

            iter_max = min(i, max_i - i)
            for j in range(iter_max):
                left_row = pattern[i-j-1]
                right_row = pattern[i+j]
                smudges += levenstein_dist(left_row, right_row)
                if smudges > 1:
                    break

            if smudges == 1:
                line_summed_up += 100 * i
                found = True
                break

        assert(found), "Mirror had to be found"

    print(f"Sum of all lines with smudeges {line_summed_up}")



first()
second()
