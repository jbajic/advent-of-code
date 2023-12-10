from functools import reduce, cmp_to_key

card_strength_without_joker = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
card_strength_with_joker = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

def get_card_strength(cards):
    unique_cards = set(cards)
    match len(unique_cards):
        case 1:
            # Five of a kind
            return 7
        case 2:
            # Four of a kind could be 4 + 1
            if any(cards.count(e) == 1 for e in unique_cards):
                return 6
            else:
                # Full house 3 + 2
                return 5
        case 3:
            # Three of a kinds this is 3 + 1 + 1
            if any(cards.count(e) == 3 for e in unique_cards):
                return 4
            else:
                # Two pairs 2 + 2 + 1
                return 3
        case 4:
            # One pair 2 + 1 + 1 + 1
            return 2
        case 5:
            # All unique
            return 1
        case _: raise Exception("Num of cards incorrect")


def upgrade_card_strength_with_joker(cards, card_strength, joker_count):
    match card_strength:
        case 1:
            card_strength = 2
        case 2:
            card_strength = 4
        case 3:
            if joker_count == 2:
                card_strength = 6
            else:
                card_strength = 5
        case 4:
            card_strength = 6
        case 5:
            card_strength = 7
        case 6:
            card_strength = 7

    return card_strength


def get_card_strength_with_jokers(cards):
    strength = get_card_strength(cards)
    if (joker_count := cards.count("J")) > 0:
        return upgrade_card_strength_with_joker(cards, strength, joker_count)
    return strength


def compare_cards_without_joker(x, y):
    if x["strength"] < y["strength"]:
        return -1
    elif y["strength"] < x["strength"]:
        return 1
    else:
        for (card_x, card_y) in zip(x["cards"], y["cards"]):
            if card_strength_without_joker.index(card_x) > card_strength_without_joker.index(card_y):
                return -1
            elif card_strength_without_joker.index(card_y) > card_strength_without_joker.index(card_x):
                return 1

        return 0


def compare_cards_with_joker(x, y):
    if x["strength"] < y["strength"]:
        return -1
    elif y["strength"] < x["strength"]:
        return 1
    else:
        for (card_x, card_y) in zip(x["cards"], y["cards"]):
            if card_strength_with_joker.index(card_x) > card_strength_with_joker.index(card_y):
                return -1
            elif card_strength_with_joker.index(card_y) > card_strength_with_joker.index(card_x):
                return 1

        return 0


def first():
    cards_sets = []

    with open("input.txt") as file:
        for line in file:
            splitted = line.split()
            cards_sets.append({
                "cards": splitted[0],
                "bid": int(splitted[1].strip()),
            })
            
    for card_set in cards_sets:
        card_set["strength"] = get_card_strength(card_set["cards"])
 
    ordered_sets = sorted(cards_sets, key=cmp_to_key(compare_cards_without_joker))
    for i in range(0, len(ordered_sets)):
        ordered_sets[i]["rank"] = i + 1

    total_winnings = reduce(lambda x, y: x + y["rank"] * y["bid"], ordered_sets, 0)
    print(f"First: Total winnings: {total_winnings}")


def second():
    cards_sets = []

    with open("input.txt") as file:
        for line in file:
            splitted = line.split()
            cards_sets.append({
                "cards": splitted[0],
                "bid": int(splitted[1].strip()),
            })

    for card_set in cards_sets:
        card_set["strength"] = get_card_strength_with_jokers(card_set["cards"])

    ordered_sets = sorted(cards_sets, key=cmp_to_key(compare_cards_with_joker))
    for i in range(0, len(ordered_sets)):
        ordered_sets[i]["rank"] = i + 1

    total_winnings = reduce(lambda x, y: x + y["rank"] * y["bid"], ordered_sets, 0)
    print(f"Second: Total winnings: {total_winnings}")


first()
second()
# 247092911
# 246764010
# 246387481
