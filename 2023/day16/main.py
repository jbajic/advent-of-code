def get_input():
    with open("input.txt") as file:
        return [line.strip() for line in file]


def get_mirror_new_direction(beam, direction, field):
    if field == '\\':
        match direction:
            case "N":
                return (beam[0], beam[1] - 1, "W")
            case "S":
               return (beam[0], beam[1] + 1, "E")
            case "E":
               return (beam[0] + 1, beam[1], "S")
            case "W":
               return (beam[0] - 1, beam[1], "N")
    elif field == "/":
        match direction:
            case "N":
               return (beam[0], beam[1] + 1, "E")
            case "S":
               return (beam[0], beam[1] - 1, "W")
            case "E":
               return (beam[0] - 1, beam[1], "N")
            case "W":
               return (beam[0] + 1, beam[1], "S")
    raise Exception("Field not found")


def first():
    input = get_input()
    print(input)

    beams = [(0, 0, "E")]
    energized_tiles = set()
    beams_directions = set()
    while beams:
        current_beam = beams.pop()

        if current_beam in beams_directions:
            continue
        
        if current_beam[0] < 0 or current_beam[0] >= len(input):
            continue

        if current_beam[1] < 0 or current_beam[1] >= len(input):
            continue

        beams_directions.add(current_beam)
        energized_tiles.add((current_beam[0], current_beam[1]))

        current_field = input[current_beam[0]][current_beam[1]]
        current_dir = current_beam[2]

        if current_field == "." or \
        (current_field == "|" and (current_dir == "N" or current_dir == "S")) or \
            (current_field == "-" and (current_dir == "E" or current_dir == "W")):
            print(f"Going straight for {current_beam} on {current_field}")
            match current_dir:
                case "N":
                    beams.append((current_beam[0] - 1, current_beam[1], "N"))
                case "S":
                    beams.append((current_beam[0] + 1, current_beam[1], "S"))
                case "E":
                    beams.append((current_beam[0], current_beam[1] + 1, "E"))
                case "W":
                    beams.append((current_beam[0], current_beam[1] - 1, "W"))
                case _:
                    raise Exception("Direction not found!")
        elif current_field == "|" and current_dir in ["E", "W"]:
            print(f"Splitting into N and S {current_beam} on {current_field}")
            beams.append((current_beam[0] - 1, current_beam[1], "N"))
            beams.append((current_beam[0] + 1, current_beam[1], "S"))
        elif current_field == "-" and current_dir in ["N", "S"]:
            print(f"Splitting into W and E {current_beam} on {current_field}")
            beams.append((current_beam[0], current_beam[1] + 1, "E"))
            beams.append((current_beam[0], current_beam[1] - 1, "W"))
        elif current_field in ["\\", "/"]:
            beams.append(get_mirror_new_direction(current_beam, current_dir, current_field))


    print(f"Energized tiles {len(energized_tiles)}")



first()
