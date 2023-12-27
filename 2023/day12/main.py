from more_itertools import distinct_permutations

def get_spring_islands(spring_line):
    islands = []
    island = []
    for elem in spring_line:
        if elem == "." and island:
            islands.append(island)
            island = []
        elif elem != ".":
            island.append(elem)

    if island:
        islands.append(island)

    return islands


def get_unknown_positions(spring_line):
    positions = []
    for i, e in enumerate(spring_line):
        if e == "?":
            positions.append(i)
    return positions


def is_variation_correct(variation, record):
    islands = get_spring_islands(variation)
    return len(record) == len(islands) and \
        all(group == sum(1 for elem in island if elem == "#") for group, island in zip(record, islands))
    

def get_number_of_variations(spring_line, unknonws_positions, record, number_of_missing_broken_springs):
    variation = ["." for _ in range(len(unknonws_positions))]
    for i in range(number_of_missing_broken_springs):
        variation[i] = "#"
    number_of_correct_variations = 0
    for var in distinct_permutations(variation):
        # replace with new in spring line
        for i in range(len(unknonws_positions)):
            spring_line[unknonws_positions[i]] = var[i]
        if is_variation_correct(spring_line, record):
            number_of_correct_variations += 1

    return number_of_correct_variations
    

def get_number_of_broken_springs(line):
    return sum(1 for e in line if e == "#")


def first():
    springs = []
    records = []
    with open("input.txt") as file:
        for line in file:
            splitted = line.strip().split()
            springs.append(list(splitted[0]))
            records.append([int(i) for i in splitted[1].strip().split(",")])

    num_of_variations = 0
    for spring_line, record in zip(springs, records):
        number_of_broken_springs = get_number_of_broken_springs(spring_line)
        number_of_missing_broken_springs = sum(record) - number_of_broken_springs
        unknonws_positions = get_unknown_positions(spring_line)

        num_of_variations += get_number_of_variations(spring_line, unknonws_positions, record, number_of_missing_broken_springs)

        # break
    print(f"Number of variations: {num_of_variations}")


first()
