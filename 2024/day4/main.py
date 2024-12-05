
from re import L


def get_directions():
    return [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if i != 0 or j != 0] 


def first_part():
    lines = []
    with open("input.txt") as file:
        for line in file:
            lines.append(line.strip())
    WORD = "XMAS"
    words_found = 0
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "X":
                for (x, y) in get_directions():
                    word_pos = 0
                    current_i = i
                    current_j = j
                    while word_pos < len(WORD) - 1 and lines[current_i][current_j] == WORD[word_pos]:
                        if current_i + x < 0 or current_i + x >= len(lines):
                            break
                        if current_j + y < 0 or current_j + y >= len(lines[i]):
                            break
                        current_i += x
                        current_j += y
                        word_pos += 1
                    if word_pos == len(WORD) - 1 and lines[current_i][current_j] == WORD[word_pos]:
                        words_found += 1

    print(f"Number of XMAS words found {words_found}")


def second_part():
    lines = []
    with open("input.txt") as file:
        for line in file:
            lines.append(line.strip())
    reversed_lines = [line[::-1] for line in lines]

    words_found = 0
    for i in range(len(reversed_lines)):
        for j in range(len(reversed_lines[i])):
            if i + 2 >= len(reversed_lines) or j + 2 >= len(reversed_lines):
                continue
            if reversed_lines[i + 1][j+1] != "A":
                continue
            is_valid = True
            for coords in [[(0,0), (2, 2)], [(2, 0), (0, 2)]]:
                elems = {"M", "S"}
                for x, y in coords:
                    if reversed_lines[i + x][j + y] not in elems:
                        is_valid = False
                        break
                    elems.remove(reversed_lines[i + x][j + y])
                if not is_valid:
                    break
            if is_valid:
                words_found += 1

    print(f"Number of X-MAS words found {words_found}")

first_part()
second_part()
