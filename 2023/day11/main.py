def get_expanded_galaxy(galaxy, empty_rows, empty_cols):
    expanded_galaxy = []
    real_i, expanded_i = 0, 0
    while expanded_i < len(galaxy) + len(empty_rows):
        if real_i in empty_rows:
            expanded_galaxy.append(["." for _ in range(len(galaxy) + len(empty_cols))])
            expanded_galaxy.append(["." for _ in range(len(galaxy) + len(empty_cols))])
            expanded_i += 2
            real_i += 1
            continue

        expanded_galaxy.append(["0" for _ in range(len(galaxy) + len(empty_cols))])
        real_j, expanded_j = 0, 0
        while expanded_j < len(galaxy) + len(empty_cols):
            expanded_galaxy[expanded_i][expanded_j] = galaxy[real_i][real_j]

            if real_j in empty_cols:
                expanded_j += 1
                expanded_galaxy[expanded_i][expanded_j] = galaxy[real_i][real_j]

            real_j += 1
            expanded_j += 1

        expanded_i += 1
        real_i += 1

    return expanded_galaxy


def get_galaxy_coords(expanded_galaxy):
    coords = []
    galaxy_num = 0
    for i in range(len(expanded_galaxy)):
        for j in range(len(expanded_galaxy[i])):
            if expanded_galaxy[i][j] == "#":
                coords.append({
                    "name": galaxy_num,
                    "coord": (i, j)
                })
                galaxy_num += 2

    return coords


def first():
    galaxy = []
    with open("input.txt") as f:
        for l in f:
            galaxy.append(list(l.strip()))
    assert(len(galaxy) == len(galaxy[0]))

    # For every one of these add one in row iter
    empty_rows = []
    for i, row in enumerate(galaxy):
        if all(e == "." for e in row):
            empty_rows.append(i)
                        
    empty_cols = []
    for i in range(len(galaxy)):
        if all(galaxy[j][i] == "." for j in range(len(galaxy))):
            empty_cols.append(i)
    
    expanded_galaxy = get_expanded_galaxy(galaxy, empty_rows, empty_cols)
    galaxies_coords = get_galaxy_coords(expanded_galaxy)

    pair_and_distances = dict()
    for i, galaxy in enumerate(galaxies_coords):
        g_name = galaxy["name"]
        g_coords = galaxy["coord"]

        for other_galaxy in galaxies_coords:
            og_name = other_galaxy["name"]
            og_coords = other_galaxy["coord"]

            if g_name == og_name:
                continue
            min_manhattan_dist = abs(g_coords[0] - og_coords[0]) + abs(g_coords[1] - og_coords[1])
            if (g_name, og_name) not in pair_and_distances and \
                (og_name, g_name) not in pair_and_distances:
                pair_and_distances[(g_name, og_name)] = min_manhattan_dist

    print(f"Sum of all min distance between galaxies is {sum(d for d in pair_and_distances.values())}")
    

def get_galaxy_coords_2(galaxy, empty_rows, empty_cols):
    coords = []
    print(empty_rows)
    print(empty_cols)
    galaxy_num = 0
    for i in range(len(galaxy)):
        for j in range(len(galaxy[i])):
            if galaxy[i][j] == "#":
                offset_i = sum(10 for e in empty_rows if e < i)
                offset_j = sum(10 for e in empty_cols if e < j)
                print(f"Converting {i}, {j} into {i+offset_i}, {j + offset_j}")
                coords.append({
                    "name": galaxy_num,
                    "coord": (i + offset_i, j + offset_j)
                })
                galaxy_num += 1

    return coords
 

def second():
    galaxy = []
    with open("input.txt") as f:
        for l in f:
            galaxy.append(list(l.strip()))
    assert(len(galaxy) == len(galaxy[0]))

    empty_rows = []
    for i, row in enumerate(galaxy):
        if all(e == "." for e in row):
            empty_rows.append(i)
                        
    empty_cols = []
    for i in range(len(galaxy)):
        if all(galaxy[j][i] == "." for j in range(len(galaxy[i]))):
            empty_cols.append(i)

    galaxies_coords = get_galaxy_coords_2(galaxy, empty_rows, empty_cols)
    print(galaxies_coords)

    pair_and_distances = dict()
    for i, galaxy in enumerate(galaxies_coords):
        g_name = galaxy["name"]
        g_coords = galaxy["coord"]

        for other_galaxy in galaxies_coords:
            og_name = other_galaxy["name"]
            og_coords = other_galaxy["coord"]

            if g_name == og_name:
                continue
            min_manhattan_dist = abs(g_coords[0] - og_coords[0]) + abs(g_coords[1] - og_coords[1])
            if (g_name, og_name) not in pair_and_distances and \
                (og_name, g_name) not in pair_and_distances:
                pair_and_distances[(g_name, og_name)] = min_manhattan_dist

    print(pair_and_distances)
    print(f"Sum of all min distance between far far away galaxies is {sum(d for d in pair_and_distances.values())}")



first()
second()
