def get_seeds(l):
    return [int(e) for e in l.strip().split(":")[1].split()]


def get_maps(lines):
    maps = []
    current_map = dict()
    for l in lines[2:]:
        l = l.strip()
        line_splitted = l.split()
        if l == "":
            maps.append(current_map)
            current_map = dict()
        elif "map:" in line_splitted:
            current_map["name"] = l
            current_map["ranges"] = []
        else:
            current_map["ranges"].append(tuple(int(e) for e in line_splitted))
    maps.append(current_map)
    return maps


def first():
    with open("input.txt") as file:
        lines = file.readlines();

    seeds = get_seeds(lines[0])
    maps = get_maps(lines)

    final_locations = []
    for seed in seeds:
        seed_current_location = seed
        for map in maps:
            for r in map["ranges"]:
                if seed_current_location >= r[1] and seed_current_location < (r[1] + r[2]):
                    seed_current_location = r[0] + (seed_current_location - r[1])
                    break
        final_locations.append(seed_current_location)
    print(f"Minimum location is {min(final_locations)}")


def second():
    with open("input.txt") as file:
        lines = file.readlines();

    seeds = get_seeds(lines[0])
    maps = get_maps(lines)

    all_seed_ranges = []
    for seed_range in zip(seeds[::2], seeds[1::2]):
        seed_current_ranges = [[seed_range[0], seed_range[0] + seed_range[1] - 1]]
        print(seed_current_ranges)
        for map in maps:
            print(f"Checking for map {map}")

            new_current_seeed_ranges = []
            for r in map["ranges"]:
                map_range_start = r[1]
                map_range_end = r[1] + r[2] - 1
                print(f"Check if {map_range_start} to {map_range_end} contains {seed_current_ranges}")

                for seed_current_range in seed_current_ranges:
                    if seed_current_range[0] <= map_range_end and seed_current_range[1] >= map_range_start:
                        # there is an intersection
                        offset = r[0] + 1
                        new_seed_start = offset + (max(map_range_start, seed_current_range[0]) - map_range_start)
                        new_seed_end = offset + (min(map_range_end, seed_current_range[1]) - map_range_start)
                        seed_current_rang = [new_seed_start, new_seed_end]
                        print(f"New seed range {seed_current_rang}")
                        new_current_seeed_ranges.append([new_seed_start, new_seed_end])
            seed_current_ranges = new_current_seeed_ranges if new_current_seeed_ranges else seed_current_ranges
            print()
        all_seed_ranges.extend(seed_current_ranges)
        break

    print(f"All seed ranges {all_seed_ranges}")
    # print(f"Minimum location is {min(r[0] for r in all_seed_ranges)}")


# first()
second()
