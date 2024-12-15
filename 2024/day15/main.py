from dataclasses import dataclass

def get_direction(move):
    match move:
        case "^":
            return (-1, 0)
        case "v":
            return (1, 0)
        case ">":
            return (0, 1)
        case "<":
            return (0, -1)
        case _:
            raise Exception("Nooo")


@dataclass
class Robot:
    x: int
    y: int

    def move_group(self, area, current_position, move):
        match move:
            case "^":
                print("Replacing up")
                for i in range(current_position[0], self.x + 1):
                    assert area[i][current_position[1]] in ["O", "@"], f"Replacing {area[i][current_position[1]]}"
                    area[i - 1][current_position[1]] = area[i][current_position[1]]
                area[self.x][self.y] = "."
            case "v":
                print("Replacing down")
                for i in reversed(range(self.x, current_position[0] + 1)):
                    assert area[i][current_position[1]] in ["O", "@"], f"Replacing {area[i][current_position[1]]}"
                    area[i + 1][current_position[1]] = area[i][current_position[1]]
                area[self.x][self.y] = "."
            case ">":
                print("Replacing right")
                for j in reversed(range(self.y, current_position[1] + 1)):
                    assert area[current_position[0]][j] in ["O", "@"], f"Replacing {area[current_position[0]][j]} not working"
                    print(f"LADIDA ({current_position[0]}, {j + 1}) into {current_position[0]}, {j}")
                    area[current_position[0]][j + 1] = area[current_position[0]][j]
                area[self.x][self.y] = "."
            case "<":
                print("Replacing left")
                for j in range(current_position[1], self.y + 1):
                    assert area[current_position[0]][j] in ["O", "@"], f"Replacing {area[current_position[0]][j]} not working"
                    print(f"LADIDA ({current_position[0]}, {j + 1}) into {current_position[0]}, {j}")
                    area[current_position[0]][j - 1] = area[current_position[0]][j]
                area[self.x][self.y] = "."
            case _:
                raise Exception("Nooo")


# Can never escape bounds
    def move(self, area, move):
        change = get_direction(move)
        print(f"Movin robot in {change}")
        new_robot_position = (self.x + change[0], self.y + change[1])
        match area[new_robot_position[0]][new_robot_position[1]]:
            case ".":
                print("New robot position is .")
                area[new_robot_position[0]][new_robot_position[1]] = "@"
                area[self.x][self.y] = "."
                self.x = new_robot_position[0]
                self.y = new_robot_position[1]
            case "#":
                print("New robot position is #")
                pass
            case "O":
                print("New robot position is O")
                # check can it move at all
                change = get_direction(move)
                is_moveable = False
                current_position = new_robot_position 
                while True:
                    new_pos = (current_position[0] + change[0], current_position[1] + change[1])
                    print(f"Moving from {current_position} to {new_pos}")
                    match area[new_pos[0]][new_pos[1]]:
                        case ".":
                            is_moveable = True
                            break
                        case "#":
                            is_moveable = False
                            break
                        case "O":
                            pass
                        case _:
                            raise Exception("Nooo wtf is this")
                    current_position = new_pos
                print(f"We are {is_moveable} movable")
                if is_moveable:
                    print(f"We are moveable")
                    self.move_group(area, current_position, move)
                    # Map updated in move_group
                    self.x = new_robot_position[0]
                    self.y = new_robot_position[1]
            case _:
                raise Exception(f"Noooo cannot be we have found {area[new_robot_position[0]][new_robot_position[1]]}")
                    


def first_part():
    area = []
    movements = []
    with open("input.txt") as file:
        for line in file:
            if line == "\n":
                break
            area.append(list(line.strip()))

        for line in file:
            for elem in line.strip():
                movements.append(elem)
    for a in area: print(a)
    print()
    i, j = [(i, j) for i in range(len(area)) for j in range(len(area[i])) if area[i][j] == "@"][0]
    rob = Robot(i, j)
    for i, move in enumerate(movements):
        print(f"Movement {i} is {move}")
        print(f"Before move {rob}")
        rob.move(area, move)
        print(f"After move {rob}")
        print()

    boxes_sum = sum(100 * i + j for i in range(len(area)) for j in range(len(area[i])) if area[i][j] == "O")
    print(f"Sum of boxes {boxes_sum}")

first_part()

