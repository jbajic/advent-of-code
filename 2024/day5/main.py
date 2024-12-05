from collections import defaultdict


def is_order_correct(order, rules):
    for i, page in enumerate(order):
        if page in rules:
            if any(i > order.index(after) for after in rules[page] if after in order):
                return False

    return True

def first_part():
    rules = defaultdict(list)
    orders = []
    with open("input.txt") as file:
        for line in file:
            if line == "\n":
                break
            before, after = map(int, line.strip().split("|"))
            rules[before].append(after)
        for line in file:
            orders.append(list(map(int, line.strip().split(","))))
    middle_sum = 0
    for order in orders:
        if is_order_correct(order, rules):
            print(order)
            middle_sum += order[len(order) // 2]
    print(f"Sum of middle pages is {middle_sum}")


def get_corrected(order, rules):
    corrected = [n for n in order]
    changed = True
    while changed:
        changed = False
        for i, page in enumerate(corrected):
            if page in rules:
                for after in rules[page]:
                    if after not in corrected:
                        continue
                    after_index = corrected.index(after)
                    if i > after_index:
                        changed = True
                        corrected[i], corrected[after_index] = corrected[after_index], corrected[i]
                        # break

    return corrected


def second_part():
    rules = defaultdict(list)
    orders = []
    with open("input.txt") as file:
        for line in file:
            if line == "\n":
                break
            before, after = map(int, line.strip().split("|"))
            rules[before].append(after)
        for line in file:
            orders.append(list(map(int, line.strip().split(","))))
    print(rules)
    print(orders)
    middle_sum = 0
    for order in orders:
        if not is_order_correct(order, rules):
            corrected_order = get_corrected(order, rules)
            print(f"from: {order} -> {corrected_order}")
            middle_sum += corrected_order[len(order) // 2]

    print(f"Sum of corrected middle pages is {middle_sum}")



# first_part()
second_part()
