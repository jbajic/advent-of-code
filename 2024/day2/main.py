
def check_level(level):
    isIncreasing = True if level[0] < level[1] else False
    prev = None
    safe = True
    for elem in level:
        if prev is None:
            prev = elem 
            continue
        
        if abs(elem - prev) > 3 or abs(elem - prev) < 1:
            safe = False
            break
        if isIncreasing and elem < prev:
            safe = False
            break
        if not isIncreasing and elem > prev:
            safe = False
            break
        prev = elem

    return safe


def first_part():
    report = []
    with open("input.txt") as file:
        for line in file:
            report.append(list(map(int, line.split())))
    
    safe_levels = 0
    for level in report:
        if check_level(level):
            safe_levels += 1

    print(f"Number of safe levels {safe_levels}")


def second_part():
    report = []
    with open("input.txt") as file:
        for line in file:
            report.append(list(map(int, line.split())))
    
    safe_levels = 0
    for level in report:
        if check_level(level):
            safe_levels += 1
            continue
        for i in range(len(level)):
            modified_level = [e for j, e in enumerate(level) if j != i]
            if check_level(modified_level):
               safe_levels += 1
               break
 
    print(f"Number of safe levels {safe_levels}")

first_part()
second_part()
