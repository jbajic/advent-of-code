def get_expanded_galaxy(galaxy, empty_rows, empty_cols, expansion):
    expanded_galaxy = []
    real_i, expanded_i = 0, 0
    i_max = len(galaxy) + (expansion - 1) * len(empty_rows)
    j_max = len(galaxy[0]) + (expansion - 1) * len(empty_cols)

    while expanded_i < i_max:
        if real_i in empty_rows:
            expanded_galaxy.append(["." for _ in range(j_max)])
            expanded_i += 1
            n = expansion - 1
            while n > 0:
                expanded_galaxy.append(["." for _ in range(j_max)])
                expanded_i += 1
                n -= 1
            real_i += 1
            continue

        expanded_galaxy.append(["0" for _ in range(j_max)])
        real_j, expanded_j = 0, 0
        while expanded_j < j_max:
            if real_j in empty_cols:
                n = expansion - 1
                while n > 0:
                    expanded_galaxy[expanded_i][expanded_j] = galaxy[real_i][real_j]
                    expanded_j += 1
                    n -= 1

            expanded_galaxy[expanded_i][expanded_j] = galaxy[real_i][real_j]
            expanded_j += 1
            real_j += 1

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
                galaxy_num += 1

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
    
    expanded_galaxy = get_expanded_galaxy(galaxy, empty_rows, empty_cols, 2)
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
    

def get_galaxy_coords_2(galaxy, empty_rows, empty_cols, expansion):
    coords = []
    galaxy_num = 0
    for i in range(len(galaxy)):
        for j in range(len(galaxy[i])):
            if galaxy[i][j] == "#":
                offset_i = sum(expansion - 1 for e in empty_rows if e < i)
                offset_j = sum(expansion - 1 for e in empty_cols if e < j)
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

    galaxies_coords = get_galaxy_coords_2(galaxy, empty_rows, empty_cols, 1000000)

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

    print(f"Sum of all min distance between far far away galaxies is {sum(d for d in pair_and_distances.values())}")



first()
second()
