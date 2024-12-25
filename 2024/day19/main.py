
def get_possbile_stripes(design, stripes):
    for stripe in stripes:
        if len(design) >= len(stripe) and stripe == design[0:len(stripe)]:
            yield stripe


def is_design_posible(design, stripes):
    if design == "":
        return True
    if any(is_design_posible(design[len(stripe):], stripes) for stripe in get_possbile_stripes(design, stripes)):
        return True
    return False


def first_part():
    stripes = []
    designs = []
    with open("input.txt") as file:
        lines = [l.strip() for l in file if l != "\n"]
        stripes = lines[0].replace(",", "").split()
        designs = [l for l in lines[1:]]

    possible = 0
    for design in designs:
        if is_design_posible(design, stripes):
            possible += 1
    print(f"Possible designs {possible}")


first_part()
