from functools import reduce


def get_game(l):
    game, rest = l.split(":")
    _, id = game.split()

    sets = rest.split(";")
    game = dict()
    for i, s in enumerate(sets):
        elems = s.split(",")
        game_set = dict()
        for e in elems:
            num, color = e.split()
            game_set[color.strip()] = int(num)
        game[i] = game_set

    return int(id), game

def first():
    with open("input.txt") as file:
        games = []
        bag = {"red": 12, "green": 13, "blue": 14}
        for l in file:
            id, game = get_game(l)
            if all(color in bag and bag[color] >= num for _, game_set in game.items() for color, num in game_set.items()):
                games.append(id)

        print(f"Sum is {sum(games)}")

def second():
    with open("input.txt") as file:
        games = []
        for l in file:
            _, game = get_game(l)
            game_min = {
                "red": None,
                "green": None,
                "blue": None,
            }
            for game_set in game.values():
                for color, num in game_set.items():
                    if game_min[color] is None or game_min[color] < num:
                        game_min[color] = num
            game_min = {k: v for k, v in game_min.items() if v is not None}
            games.append(reduce((lambda x, y: x * y), game_min.values()))

        print(f"Sum of triplets multipled is {sum(games)}")

first()
second()
