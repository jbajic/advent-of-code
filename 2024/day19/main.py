from functools import cache

STRIPES = []
with open("input.txt") as file:
    lines = [l.strip() for l in file if l != "\n"]
    STRIPES = lines[0].replace(",", "").split()


def get_possbile_stripes(design):
    for stripe in STRIPES:
        if len(design) >= len(stripe) and stripe == design[0 : len(stripe)]:
            yield stripe


def is_design_posible(design):
    if design == "":
        return True
    if any(
        is_design_posible(design[len(stripe) :])
        for stripe in get_possbile_stripes(design)
    ):
        return True
    return False


@cache
def how_many_ways(design):
    if design == "":
        return 1
    return sum(
        how_many_ways(design[len(stripe) :]) for stripe in get_possbile_stripes(design)
    )


def first_part():
    designs = []
    with open("input.txt") as file:
        lines = [l.strip() for l in file if l != "\n"]
        designs = [l for l in lines[1:]]

    possible = 0
    for design in designs:
        if is_design_posible(design):
            possible += 1

    print(f"Possible designs {possible}")


def second_part():
    designs = []
    with open("input.txt") as file:
        lines = [l.strip() for l in file if l != "\n"]
        designs = [l for l in lines[1:]]

    ways = 0
    for design in designs:
        # print(f"For {design} there are {way}")
        ways += how_many_ways(design)
    print(f"Possible ways {ways}")


first_part()
second_part()
